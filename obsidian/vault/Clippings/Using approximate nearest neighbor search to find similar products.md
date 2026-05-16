---
title: "Using approximate nearest neighbor search to find similar products"
source: "https://blog.vespa.ai/image-similarity-search/"
author:
  - "[[Jo Kristian Bergum]]"
published: 2021-02-16
created: 2026-05-16
description: "Approximate nearest neighbor search demonstration using Amazon Product dataset"
tags:
  - "clippings"
---
{ }

## Vespa Blog

We Make AI Work

![Jo Kristian Bergum](https://blog.vespa.ai/assets/avatars/jobergum.jpg)

In this blog we give an introduction to how to use the  
[Vespa’s approximate nearest neighbor search](https://docs.vespa.ai/en/approximate-nn-hnsw.html) query operator.

We demonstrate how nearest neighbor search in an image feature vector space can be used to find similar products. Given an image of a product, we want to find similar products, but also with the possibility to filter the returned products by inventory status, price or other real world constraints.

We’ll be using the [Amazon Products dataset](http://jmcauley.ucsd.edu/data/amazon/links.html) as our demo dataset. The subset we use has about 22K products.

- The dataset contains product information like title, description and price and we show how to map the data into the Vespa document model
- The dataset also contains binary feature vectors for images, features produced by a neural network model. We’ll use these image vectors and show you how to store and index vectors in Vespa.

We also demonstrate some of the [real world challenges with using nearest neighbor search](https://blog.vespa.ai/using-approximate-nearest-neighbor-search-in-real-world-applications/):

- Combining the nearest neighbor search with filters, for example on inventory status
- Real time indexing of vectors and update documents with vectors
- True partial updates to update inventory status at scale

Since we use the Amazon Products dataset, we also recommend these resources:

- [Vespa.ai Use case Shopping Search](https://docs.vespa.ai/en/use-case-shopping.html)
- [E-commerce search and recommendation with Vespa.ai](https://blog.vespa.ai/e-commerce-search-and-recommendation-with-vespaai/)
- [Approximate nearest neighbor search in Vespa](https://blog.vespa.ai/approximate-nearest-neighbor-search-in-vespa-part-1/)

## PyVespa

In this blog we’ll be using [pyvespa](https://vespa-engine.github.io/pyvespa/), which is a simple python api built on top of Vespa’s native HTTP apis.

The python api is not meant as a production ready api, but an api to explore features in Vespa. It is also for training ML models, which can be deployed to Vespa for serving.

## Exploring the Amazon Product dataset

Let us download the demo data from the Amazon Products dataset, we use the *Amazon\_Fashion* subset.

```
!wget -nc https://raw.githubusercontent.com/alexklibisz/elastiknn/master/examples/tutorial-notebooks/amazonutils.py
!wget -nc http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Amazon_Fashion.json.gz
!wget -nc http://snap.stanford.edu/data/amazon/productGraph/image_features/categoryFiles/image_features_Amazon_Fashion.b
```
```
from amazonutils import *
from pprint import pprint
```

Let us have a look at a selected slice of the dataset:

```
for p in islice(iter_products('meta_Amazon_Fashion.json.gz'), 221,223):
  pprint(p)
  display(Image(p['imUrl'], width=128, height=128))
```
```
{'asin': 'B0001KHRKU',
 'categories': [['Amazon Fashion']],
 'imUrl': 'http://ecx.images-amazon.com/images/I/31J78QMEKDL.jpg',
 'salesRank': {'Watches': 220635},
 'title': 'Midas Remote Control Watch'}
```

![jpeg](https://blog.vespa.ai/assets/2021-02-16-image-similarity-search/output_7_1.jpg)

```
{'asin': 'B0001LU08U',
 'categories': [['Amazon Fashion']],
 'imUrl': 'http://ecx.images-amazon.com/images/I/41q0XD866wL._SX342_.jpg',
 'salesRank': {'Clothing': 1296873},
 'title': 'Solid Genuine Leather Fanny Pack Waist Bag/purse with '
          'Cellphoneholder'}
```

## Build basic search functionality

A Vespa instance is described by a [Vespa application package](https://docs.vespa.ai/en/application-packages.html). Let us create an application called product and define our [document schema](https://docs.vespa.ai/en/schemas.html). We use pyvespa to define our application. This is not a requirement for creating a Vespa application, one can just use a text editor of choice.

```
from vespa.package import ApplicationPackage
app_package = ApplicationPackage(name = "product")
```
```
from vespa.package import Field
app_package.schema.add_fields(        
    Field(name = "asin", type = "string", indexing = ["attribute", "summary"]),
    Field(name = "title", type = "string", indexing = ["index", "summary"], index = "enable-bm25"),
    Field(name = "description", type = "string", indexing = ["index", "summary"], index = "enable-bm25"),
    Field(name = "price", type = "float", indexing = ["attribute", "summary"]),
    Field(name = "salesRank", type = "weightedset<string>", indexing = ["summary","attribute"]),
    Field(name = "imUrl", type = "string", indexing = ["summary"])
)
```

We define a fieldset which is a way to combine matching over multiple string fields. We will only do text queries over the *title* and *description* field.

```
from vespa.package import FieldSet
app_package.schema.add_field_set(
    FieldSet(name = "default", fields = ["title", "description"])
)
```

Then define a simple [ranking](https://docs.vespa.ai/en/ranking.html) function which uses a linear combination of the [bm25](https://docs.vespa.ai/en/reference/bm25.html) text ranking feature over our two free text string fields.

```
from vespa.package import RankProfile
app_package.schema.add_rank_profile(
    RankProfile(
        name = "bm25", 
        first_phase = "0.9*bm25(title) + 0.2*bm25(description)")
)
```

So let us deploy this application. We use docker in this example. See also [Vespa quick start](https://docs.vespa.ai/en/vespa-quick-start.html)

### Deploy the application and start Vespa

```
from vespa.package import VespaDocker
vespa_docker = VespaDocker(port=8080)

app = vespa_docker.deploy(
    application_package = app_package,
    disk_folder="/home/centos/product_search" # include the desired absolute path here
)
```
```
Waiting for configuration server.
Waiting for configuration server.
Waiting for configuration server.
Waiting for configuration server.
Waiting for configuration server.
Waiting for application status.
Waiting for application status.
Finished deployment.
```

### Index our product data

Pyvespa does expose a feed api, but in this notebook we use the raw [Vespa http /document/v1 feed api](https://docs.vespa.ai/en/document-v1-api-guide.html).

The HTTP document api is synchronous and the operation is visible in search when acked with a response code 200. In this case, the feed throughput is limited by the client as we are posting one document at a time. For high throughput use cases use the asynchronous feed api, or use more client threads with the synchronous api.

```
import requests 
session = requests.Session()

def index_document(product):
    asin = product['asin']
    doc = {
        "fields": {
            "asin": asin,
            "title": product.get("title",None),
            "description": product.get('description',None),
            "price": product.get("price",None),
            "imUrl": product.get("imUrl",None),
            "salesRank": product.get("salesRank",None)     
        }
    }
    resource = "http://localhost:8080/document/v1/demo/product/docid/{}".format(asin)
    request_response = session.post(resource,json=doc)
    request_response.raise_for_status()
```

With our routine defined we can iterate over the data and index the products, one doc at a time:

```
from tqdm import tqdm
for product in tqdm(iter_products("meta_Amazon_Fashion.json.gz")):
    index_document(product)
```
```
24145it [01:46, 226.40it/s]
```

So we have our index ready, no need to perform any additional index maintenance operations like merging segments. All the data is searchable. Let us define a simple routine to display search results. Parsing the [Vespa JSON search response](https://docs.vespa.ai/en/reference/default-result-format.html) format:

```
def display_hits(res, ranking):
    time = 1000*res['timing']['searchtime'] #convert to ms
    totalCount = res['root']['fields']['totalCount']
    print("Found {} hits in {:.2f} ms.".format(totalCount,time))
    print("Showing top {}, ranked by {}".format(len(res['root']['children']),ranking))
    print("")
    for hit in res['root']['children']:
        fields = hit['fields']
        print("{}".format(fields.get('title', None)))
        display(Image(fields.get("imUrl"), width=128, height=128))  
        print("documentid: {}".format(fields.get('documentid')))
        if 'inventory' in fields:
            print("Inventory: {}".format(fields.get('inventory')))
        print("asin: {}".format(fields.get('asin')))
        if 'price' in fields:
            print("price: {}".format(fields.get('price',None)))
        if 'priceRank' in fields:
            print("priceRank: {}".format(fields.get('priceRank',None)))  
        print("relevance score: {:.2f}".format(hit.get('relevance')))
        print("")
```

### Query our product data

We use the [Vespa HTTP Search API](https://docs.vespa.ai/en/query-api.html#http) to search our product index.

In this example we assume there is a user query ‘mens wrist watch’ which we use as input to the [YQL](https://docs.vespa.ai/en/query-language.html) query language. Vespa allows combining the structured application logic expressed by YQL with a user query language called [Vespa simple query language](https://docs.vespa.ai/en/reference/simple-query-language-reference.html).

In this case we use *type=any* so matching any of our 3 terms is enough to retrieve the document. In the YQL statement we select the fields we want to return. Only fields which are marked as *summary* in the schema can be returned with the hit result.

We don’t mention which fields we want to search, so Vespa uses the fieldset defined earlier called default, which will search both the title and the description fields.

```
query = {
    'yql': 'select documentid, asin,title,imUrl,price from sources * where userQuery();',
    'query': 'mens wrist watch',
    'ranking': 'bm25',
    'type': 'any',
    'presentation.timing': True,
    'hits': 2

display_hits(app.query(body=query).json, "bm25")
```
```
Found 3285 hits in 4.00 ms.
Showing top 2, ranked by bm25

Geekbuying 814 Analog Alloy Quartz Men's Wrist Watch - Black (White)
```

```
documentid: id:demo:product::B00GLP1GTW
asin: B00GLP1GTW
price: 8.99
relevance score: 10.27

Popular Quality Brand New Fashion Mens Boy Leatheroid Quartz Wrist Watch Watches
```

```
documentid: id:demo:product::B009EJATDQ
asin: B009EJATDQ
relevance score: 9.67
```

So there we have our basic search functionality.

## Related products using nearest neighbor search in image feature spaces

Now we have basic search functionality up and running, but the Amazon Product dataset also includes image features which we can also index in Vespa and use approximate nearest neighbor search on. Let us load the image feature data. We reduce the vector dimensionality to something more practical and use 256 dimensions.

```
vectors = []
reduced = iter_vectors_reduced("image_features_Amazon_Fashion.b", 256, 1000)
for asin,v in tqdm(reduced("image_features_Amazon_Fashion.b")):
    vectors.append((asin,v))
```
```
22929it [00:04, 4739.67it/s]
```

We need to re-configure our application to add our image vector field. We also define a *HNSW* index for it and using *angular* as our [distance metric](https://docs.vespa.ai/en/reference/schema-reference.html#distance-metric).

We also need to define the input query vector in the application package. Without defining our query input tensor we won’t be able to perform our nearest neighbor search, so make sure you remember to include that.

Most changes like adding or remove a field is a [live change](https://docs.vespa.ai/en/reference/schema-reference.html#modifying-schemas) in Vespa, no need to re-index the data.

```
from vespa.package import HNSW
app_package.schema.add_fields(
    Field(name = "image_vector", 
          type = "tensor<float>(x[256])", 
          indexing = ["attribute","index"],
          ann=HNSW(
            distance_metric="angular",
            max_links_per_node=16,
            neighbors_to_explore_at_insert=200)
         )
)
from vespa.package import QueryTypeField
app_package.query_profile_type.add_fields(
    QueryTypeField(name="ranking.features.query(query_image_vector)", type="tensor<float>(x[256])")
)
```

We also need to define a ranking profile on how we want to score our documents. We use the *closeness* [ranking feature](https://docs.vespa.ai/en/reference/rank-features.html). Note that it’s also possible to retrieve results using approximate nearest neighbor search operator and use the first phase ranking function as a re-ranking stage (e.g by sales popularity etc).

```
app_package.schema.add_rank_profile(
    RankProfile(
        name = "vector_similarity", 
        first_phase = "closeness(field,image_vector)")
)
```

Now, we need to re-deploy our application package to make the changes effective.

```
app = vespa_docker.deploy(
    application_package = app_package,
    disk_folder="/home/centos/product_search" # include the desired absolute path here
)
```

## Update the index with image vectors

Now we are ready to feed and index the image vectors.

We update the documents in the index by running partial update operations, adding the vectors using real time updates of the existing documents. Partially updating a tensor field, with or without tensor, does not trigger re-indexing.

```
for asin,vector in tqdm(vectors):
    update_doc = {
        "fields":  {
            "image_vector": {
                "assign": {
                    "values": vector
                }
            }
        }
    }
    url = "http://localhost:8080/document/v1/demo/product/docid/{}".format(asin)
    response = session.put(url, json=update_doc)
```
```
100%|██████████| 22929/22929 [01:40<00:00, 228.94it/s]
```

We now want to get similar products using the image feature data. We do so by first fetching the vector of the product we want to find similar products for, and use this vector as input to the nearest neighbor search operator of Vespa. First we define a simple get vector utility to fetch the vector of a given product *asin*.

```
def get_vector(asin):
    resource = "http://localhost:8080/document/v1/demo/product/docid/{}".format(asin)
    response = session.get(resource)
    response.raise_for_status()
    document = response.json()
    
    cells = document['fields']['image_vector']['cells']
    vector = {}
    for i,cell in enumerate(cells):
        v = cell['value']
        adress = cell['address']['x']
        vector[int(adress)] = v
    values = []
    for i in range(0,256):
        values.append(vector[i])
    return values
```

Let us repeat the query from above to find an image to find similar products for

```
query = {
    'yql': 'select documentid, asin,title,imUrl,price from sources * where userQuery();',
    'query': 'mens wrist watch',
    'ranking': 'bm25',
    'type': 'any',
    'presentation.timing': True,
    'hits': 1
}
display_hits(app.query(body=query).json, "bm25")
```
```
Found 3285 hits in 4.00 ms.
Showing top 1, ranked by bm25

Geekbuying 814 Analog Alloy Quartz Men's Wrist Watch - Black (White)
```

```
documentid: id:demo:product::B00GLP1GTW
asin: B00GLP1GTW
price: 8.99
relevance score: 10.27
```

Let us search for similar images using **exact** nearest neighbor search. We ask for 3 most similar to the product image with asin id **B00GLP1GTW**

```
query = {
    'yql': 'select documentid, asin,title,imUrl,description,price from sources * where \
    ([{"targetHits":3,"approximate":false}]nearestNeighbor(image_vector,query_image_vector));',
    'ranking': 'vector_similarity',
    'hits': 3, 
    'presentation.timing': True,
    'ranking.features.query(query_image_vector)': get_vector('B00GLP1GTW')
}
display_hits(app.query(body=query).json, "vector_similarity")
```
```
Found 46 hits in 10.00 ms.
Showing top 3, ranked by vector_similarity

Geekbuying 814 Analog Alloy Quartz Men's Wrist Watch - Black (White)
```

```
documentid: id:demo:product::B00GLP1GTW
asin: B00GLP1GTW
price: 8.99
relevance score: 1.00

Avalon EZC Unisex Low-Vision Silver-Tone Flex Bracelet One-Button Talking Watch, # 2609-1B
```

```
documentid: id:demo:product::B000M9GQ0M
asin: B000M9GQ0M
price: 44.95
relevance score: 0.63

White Rubber Strap Digital Watch
```

```
documentid: id:demo:product::B003ZYXF1Y
asin: B003ZYXF1Y
relevance score: 0.62
```

Let us repeat the same query but this time using the faster approximate version. When there is a HNSW index on the tensor, the default behavior is to use approximate:true, so we remove the approximation flag.

```
query = {
    'yql': 'select documentid, asin,title,imUrl,description,price from sources * where \
    ([{"targetHits":3}]nearestNeighbor(image_vector,query_image_vector));',
    'ranking': 'vector_similarity',
    'hits': 3, 
    'presentation.timing': True,
    'ranking.features.query(query_image_vector)': get_vector('B00GLP1GTW')
}
display_hits(app.query(body=query).json, "vector_similarity")
```
```
Found 3 hits in 6.00 ms.
Showing top 3, ranked by vector_similarity

Geekbuying 814 Analog Alloy Quartz Men's Wrist Watch - Black (White)
```

```
documentid: id:demo:product::B00GLP1GTW
asin: B00GLP1GTW
price: 8.99
relevance score: 1.00

Avalon EZC Unisex Low-Vision Silver-Tone Flex Bracelet One-Button Talking Watch, # 2609-1B
```

```
documentid: id:demo:product::B000M9GQ0M
asin: B000M9GQ0M
price: 44.95
relevance score: 0.63

White Rubber Strap Digital Watch
```

```
documentid: id:demo:product::B003ZYXF1Y
asin: B003ZYXF1Y
relevance score: 0.62
```

## Combining nearest neighbor search with filters

If we look at the results for the above exact and approximate nearest neighbor searches, we got the same results using the approximate version (perfect recall). But naturally the first listed product was the same product that we used as input, and the closeness score was 1.0 simply because the angular distance is 0. Since the user is already presented with the product, we want to remove it from the result. We can do that by combining the search for nearest neighbors with a filter, expressed by the YQL query language using **and**.

```
query = {
    'yql': 'select documentid, asin,title,imUrl,description,price from sources * where \
    ([{"targetHits":3}]nearestNeighbor(image_vector,query_image_vector)) and \
    !(asin contains "B00GLP1GTW");',
    'ranking': 'vector_similarity',
    'hits': 3, 
    'presentation.timing': True,
    'ranking.features.query(query_image_vector)': get_vector('B00GLP1GTW')
}
display_hits(app.query(body=query).json, "vector_similarity")
```
```
Found 3 hits in 5.00 ms.
Showing top 3, ranked by vector_similarity

Avalon EZC Unisex Low-Vision Silver-Tone Flex Bracelet One-Button Talking Watch, # 2609-1B
```

```
documentid: id:demo:product::B000M9GQ0M
asin: B000M9GQ0M
price: 44.95
relevance score: 0.63

White Rubber Strap Digital Watch
```

```
documentid: id:demo:product::B003ZYXF1Y
asin: B003ZYXF1Y
relevance score: 0.62

Suunto Men's D6i W/ TRANSMITTER Athletic Watches
```

```
documentid: id:demo:product::B007963FS2
asin: B007963FS2
relevance score: 0.61
```

That is better. The original product is removed from the list of similar products.

If we want to add a price filter, we can do that too. In the below example we filter also by price, to limit the search for nearest neighbors by a price filter.

We still ask for the 3 nearest neighbors. We could do so automatically or giving the user a choice of price ranges using [Vespa’s grouping and aggregation support](https://docs.vespa.ai/en/grouping.html).

```
query = {
    'yql': 'select documentid, asin,title,imUrl,description,price from sources * where \
    ([{"targetHits":3}]nearestNeighbor(image_vector,query_image_vector)) and \
    !(asin contains "B00GLP1GTW") and \
    price > 100;',
    'ranking': 'vector_similarity',
    'hits': 3, 
    'presentation.timing': True,
    'ranking.features.query(query_image_vector)': get_vector('B00GLP1GTW')
}
display_hits(app.query(body=query).json, "vector_similarity")
```
```
Found 19 hits in 7.00 ms.
Showing top 3, ranked by vector_similarity

Hamilton Men's H64455133 Khaki King II Black Dial Watch
```

```
documentid: id:demo:product::B001F7MIY8
asin: B001F7MIY8
price: 400.0
relevance score: 0.60

Wenger Men's 62800 Knife Combo Watch Set
```

```
documentid: id:demo:product::B00CM1RPW6
asin: B00CM1RPW6
price: 150.71
relevance score: 0.59

Deporte Ardmore Mens Watch
```

```
documentid: id:demo:product::B00KY992QU
asin: B00KY992QU
price: 789.0
relevance score: 0.59
```

In the result above the search for nearest neighbors have been filtered by price. This search also removes products which have no price value. Ranking is still done by the the closeness ranking feature. We could also use a better ranking profile taken into account more signals, like the salesRank of the product by changing our ranking profile to use a linear combination of features.

```
RankProfile(
        name = "vector_similarity_", 
        first_phase = "12.0 + 23.24*closeness(field,image_vector) + 12.4*(1/attribute(popularity))")
)
```

## Keeping the index fresh by true partial updates

In retail and e-commerce search, one important aspect is to be able to update the search index to keep it fresh, so that we can use the latest information at search time. Examples of updates which Vespa can perform at scale:

- inventory status, which could be used as a *hard* filter so that our results only includes products which are in stock, or as a feature to be used when ranking products.
- Product attributes which can used as ranking signals, for example category popularity (salesRank), click through rate and conversion rate.

Vespa, with its true partial update of **attribute** fields, can support high volumes of updates per node, as updates of attribute fields are performed in-place, without having to re-index the entire document.

To demonstrate this, we will add a new field to our product index which we call *inventory* and which keeps track of the inventory or in stock status of our product index. We want to ensure that the products we display have a positive inventory status. In this case we use it as a hard filter but this can also be a soft filter, used as a ranking signal.

Let us change our application:

```
app_package.schema.add_fields(        
    Field(name = "inventory", type = "int", indexing = ["attribute", "summary"])
)
```
```
app = vespa_docker.deploy(
    application_package = app_package,
    disk_folder="/home/centos/product_search" # include the desired absolute path here
)
```

We iterate over our products and assign a random inventory count. We use partial update to do this. Vespa can handle up to 50K updates of integer fields per node and the partial update is performed in place so the document is not re-indexed in any way.

```
import random
for product in tqdm(iter_products("meta_Amazon_Fashion.json.gz")):
    asin = product['asin']
    update_doc = {
        "fields":  {
            "inventory": {
                "assign": random.randint(0,10)
            }
        }
    }
    url = "http://localhost:8080/document/v1/demo/product/docid/{}".format(asin)
    response = session.put(url, json=update_doc)
```
```
24145it [01:30, 268.25it/s]
```

Let us repeat our query for expensive similar products using image similarity, now we also display the inventory status

```
query = {
    'yql': 'select documentid, inventory, asin,title,imUrl,description,price from sources * where \
    ([{"targetHits":3}]nearestNeighbor(image_vector,query_image_vector)) and \
    !(asin contains "B00GLP1GTW") and \
    price > 100;',
    'ranking': 'vector_similarity',
    'hits': 3, 
    'presentation.timing': True,
    'ranking.features.query(query_image_vector)': get_vector('B00GLP1GTW')
}
display_hits(app.query(body=query).json, "vector_similarity")
```
```
Found 19 hits in 9.00 ms.
Showing top 3, ranked by vector_similarity

Hamilton Men's H64455133 Khaki King II Black Dial Watch
```

```
documentid: id:demo:product::B001F7MIY8
Inventory: 3
asin: B001F7MIY8
price: 400.0
relevance score: 0.60

Wenger Men's 62800 Knife Combo Watch Set
```

```
documentid: id:demo:product::B00CM1RPW6
Inventory: 1
asin: B00CM1RPW6
price: 150.71
relevance score: 0.59

Deporte Ardmore Mens Watch
```

```
documentid: id:demo:product::B00KY992QU
Inventory: 10
asin: B00KY992QU
price: 789.0
relevance score: 0.59
```

So as we can see the second hit, B00CM1RPW6 has inventory status 1. Let us update the inventory count for document **B00CM1RPW6** in real time. In this case we assign it the value 0 (out of stock). We could also use “increment”, “decrement”. Immidately after we have performed the update we perform our search. We now expect that the displayed inventory is 0.

```
update_doc = {
    "fields": {
        "inventory": {
            "assign": 0
        }
    }
}
resource = "http://localhost:8080/document/v1/demo/product/docid/{}".format('B00CM1RPW6')
response = session.put(resource, json=update_doc)
print("Got response {}".format(response.json()))
display_hits(app.query(body=query).json, "vector_similarity")
```
```
Got response {'pathId': '/document/v1/demo/product/docid/B00CM1RPW6', 'id': 'id:demo:product::B00CM1RPW6'}
Found 19 hits in 4.00 ms.
Showing top 3, ranked by vector_similarity

Hamilton Men's H64455133 Khaki King II Black Dial Watch
```

```
documentid: id:demo:product::B001F7MIY8
Inventory: 3
asin: B001F7MIY8
price: 400.0
relevance score: 0.60

Wenger Men's 62800 Knife Combo Watch Set
```

```
documentid: id:demo:product::B00CM1RPW6
Inventory: 0
asin: B00CM1RPW6
price: 150.71
relevance score: 0.59

Deporte Ardmore Mens Watch
```

```
documentid: id:demo:product::B00KY992QU
Inventory: 10
asin: B00KY992QU
price: 789.0
relevance score: 0.59
```

As we can see, product **B00CM1RPW6** now displays an inventory status of 0. We can also add inventory as a hard filter and re-do our query, but this time with a inventory > 0 filter:

```
query = {
    'yql': 'select documentid, inventory, asin,title,imUrl,description,price from sources * where \
    ([{"targetHits":3}]nearestNeighbor(image_vector,query_image_vector)) and \
    !(asin contains "B00GLP1GTW") and \
     price > 100 and inventory > 0;',
    'ranking': 'vector_similarity',
    'hits': 3, 
    'presentation.timing': True,
    'ranking.features.query(query_image_vector)': get_vector('B00GLP1GTW')
}
display_hits(app.query(body=query).json, "vector_similarity")
```
```
Found 20 hits in 5.00 ms.
Showing top 3, ranked by vector_similarity

Hamilton Men's H64455133 Khaki King II Black Dial Watch
```

```
documentid: id:demo:product::B001F7MIY8
Inventory: 3
asin: B001F7MIY8
price: 400.0
relevance score: 0.60

Deporte Ardmore Mens Watch
```

```
documentid: id:demo:product::B00KY992QU
Inventory: 10
asin: B00KY992QU
price: 789.0
relevance score: 0.59

Seiko Quartz Stainless Steel SXDB37P1
```

```
documentid: id:demo:product::B001TDOILY
Inventory: 2
asin: B001TDOILY
price: 216.9
relevance score: 0.58
```

That’s better. Now all related items have inventory status > 0 and price > 100$. Using it as a hard filter, or as a ranking signal is up to you.

## Summary

In this notebook we have demonstrated Vespa’s nearest neighbor search and approximate nearest neighbor search and how Vespa allows combining nearest neighbor search with filters. To learn more see [https://vespa.ai](https://vespa.ai/)

## Read more

[« Q and A from The Great Search Engine Debate - Elasticsearch, Solr or Vespa? Meetup](https://blog.vespa.ai/the-great-search-engine-debate-elasticsearch-solr-or-vespa/) [Build a basic text search application from python with Vespa »](https://blog.vespa.ai/build-basic-text-search-app-from-python-with-vespa/)