---
title: "Milvus: Unlocking Your Data’s Hidden Relationships:"
source: "https://romellfudi.medium.com/milvus-unlocking-your-datas-hidden-relationships-92da9522d415"
author:
  - "[[Freddy Domínguez]]"
published: 2023-10-05
created: 2026-06-01
description: "More"
tags:
  - "clippings"
---
A Journey into Embedding Scalable Similarity Search

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*FPpl4k4bZvrPRHDCR8dKTw.png)

From unstructured chaos to structured insights: A journey into scalable similarity search

In today’s landscape, AI is a remarkable tools, big data, LLMs within companies are essential for competitiveness. Embedding is vital across domains like natural language processing, computer vision, and recommendation systems. Just because by simplifying complex data and pattern recognition, it's an essential technique for large dataset and insightful extraction.

Embeddings enable algorithms discover similarities and structures within the data that might not be immediately apparent in their original form. A common example is attempting to identify an individual frame within security video footage or extracting relevant details about a subject from a virtual library (text of books). These two scenarios are really complex to deal with searching information. This is where it becomes vitally important vector database, where you can transform your inquiry data into special vector, facilitating the comparasion with others vectors within the same dataset in order to retrieval mindful information.

In this article, we’ll embark on a journey through four basic sections:

1. What is Milvus?
2. The Advantages of Milvus as a Vector Database
3. Free and Easy: Embedding Any Plain Data
4. Effortless Retrieval of Similar Data with Embedding Search

## 1\. What is Milvus?

Milvus is an open-source vector database designed to empower similarity searches and AI applications based on embeddings. It aims to improve the accessibility of searching unstructured data while providing a consistent user experience across various deployment environments. Milvus is specifically engineered for the management of both structured and unstructured data using embedding vectors, which are numerical representations of data points.

## 2\. The Advantages of Milvus as a Vector Database

Milvus vector database is a great tool/engine which manage structured and non-unstrucred data related with an embedding vector. Vector Embeddings are designed to capture semantic relationships and similarities between data points. Of course the choice of using Milvus or any other vector embedding technology depends on your specific use case, requirements, and technology landscape. I will provide you some reasons why Milvus might be advantageous compared to others methods:

1. **Efficient Similarity Search:** The engine enables us to retrieve similar vectors from a large database such as massive information of news, reports, papers, and books. This can be crucial for a huge several applications, including recommendation systems, image search, and Natural language processing.
2. **Scalability:** Vector databases are been designed to deal large-scale datasets. In fact, they can scale horizontally, making applications to deal with massive amounts of data.
3. **Dimensionality Reduction:** Embedding technique reduces the dimensionality of data while preventing relevant information. This can lead to more efficient storage and computation, making it easier to work with high-dimensional data such as multimedia content.
4. **Semantic Understanding:** Vector Embedding are trained to capture *semantic* relationship between data points, making them useful for tasks that require processing of the underlying semantics. i.e. natural language understanding and image recognition.
5. **Ease of Use:** Milvus offers a friendly interface that can be easily integrated into any application. By using *pymilvus*, a python library, we can implement schemas and connections easily, significantly simplifying the development time.

## 3\. Free and Easy: Embedding Any Plain Data

Embedding is a representation of any kind of data into a vector, which is a list of numbers. This vector is a special representation of the data, which can be used to compare with others vectors. The similarity between two vectors is measured by a distance metric, which is a function that takes two vectors as input and returns a number. The smaller the distance, the more similar the vectors are. The distance metric is a special key component of the embedding, and it is chosen based on the application, so I always recommend you testing with your data in order to select the best measure for your case. For example, if we are embedding images, we might choose a distance metric that is robust to changes in lighting and orientation(This blog is pending to be release). If we are embedding text, we might choose a distance metric that is robust to changes in word order.

> Always check which measures you really need.

Having presented basic topics, I will see how to generate embeddings from text using a free transformer model, and then will use Milvus to search for similar embeddings. For this time we use the *gte-base* embedding model from hugging face [hub](https://huggingface.co/thenlper/gte-base), a free text embeddings to be consumed in any project. So, we need to install a library and then create a function:

```c
pip install sentence-transformers -q
```
```c
def embedding_text(input_text):
    # Initialize the Hugging Face tokenizer and model
    hf_tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-base")
    hf_model = AutoModel.from_pretrained("thenlper/gte-base")
    batch_dict = hf_tokenizer([input_text], max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = hf_model(**batch_dict)
    # do a masked mean over the dimension(average_pool)
    last_hidden = outputs.last_hidden_state.masked_fill(~batch_dict['attention_mask'][..., None].bool(), 0.0)
    torch_embeddings_list = last_hidden.sum(dim=1) / batch_dict['attention_mask'].sum(dim=1)[..., None]
    # return only the first element of the batch (since we only passed one sentence to the model)
    # and transform embedding numbers in pytorch into a simple list
    return torch_embeddings_list[0].tolist() # dimension of 768
```

The above Python function, `embedding_text`, takes an input text and generates embeddings using the Hugging Face transformer model "thenlper/gte-base." It initializes a tokenizer and model, processes the input text, and computes masked average pooling over the model's hidden states. The resulting embeddings are returned as a list of floating-points, this resulting embedding vector encompasses a dimensionality of 768 values. In case you haven't downloaded the model, the script starts doing the process.

Let's test it. We pass any text as a parameter to the function, and we can check the vector has the correct dimension.

```c
from pprint import pprint, pformat
whatever = 'Milvus Vector Database is an open-source, \
highly optimized database designed for managing and searching large-scale vector data. \
It is specifically designed to handle high-dimensional vectors, \
which are commonly used in machine learning and similarity search applications.'

embeddings = embedding_text(whatever);
print(f"The vector of embeddings has a dimension of {len(embeddings)}")
pformat(embeddings)

# The vector of embeddings has a dimension of 768
# [0.0763445571064949,\n 0.10579398274421692,\n 0.26722753047943115 ...]
```

## 4\. Retrieved Similar data by searching embeddings

How to utilize Milvus? To use Milvus in our environment, we must first install the necessary libraries. `milvus` is a library that facilitates the operation of a lite serverless database, while `pymilvus` is employed for managing data and embeddings, both libraries are included in [milvus-lite](https://github.com/milvus-io/milvus-lite/). if you are utilizing Jupyter, it might be neccessary to restart the runtime.

```c
pip install  "milvus[client]" -q
```

So, to begin, we initiate the sever within the Google Colab environment:

```c
from milvus import default_server
from pymilvus import connections, utility

default_server.start()
connections.connect(host="127.0.0.1", port=default_server.listen_port)
utility.get_server_version() # v2.2.12-lite
```

if everything works as expected, you should observe the current version.

Next we need to generate a collection schema called Dataset, which will contain the embeddings. A collection schema is a set of fields that define the collection’s structure. Each field has a name, a data type, and other properties. The data type can be one of the following: ***INT8, INT16, INT32, INT64, FLOAT, DOUBLE, STRING, BINARY\_VECTOR, FLOAT\_VECTOR, or BOOL***. Each field must be initialized with a dimension, which is the dimensionality of the vector fields is specified by the dim property. The following code snippet creates a collection schema with three fields: id, full\_text, and embedding. The id field is an auto-incremented integer, the full\_text field is a string with a maximum of characters to 4000, and the embedding field is a vector of floating-point numbers. The dimensionality of the embedding field is set to 768, which is the same as the dimensionality of the embeddings generated by the *embedding\_text* function.

```c
from pymilvus import FieldSchema, CollectionSchema, DataType, Collection
COLLECTION_NAME = "Dataset"
DIMENSION = 768
# Check that the collection does not yet exist
if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)

fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='full_text', dtype=DataType.VARCHAR, max_length=4000),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
]
schema = CollectionSchema(fields=fields)
collection = Collection(name=COLLECTION_NAME, schema=schema)
```

Following the process, we have already set the embedding dimension in the collection, so we need to create an index to improve the time retriving, to do it this we indicate the [index type](https://milvus.io/docs/index.md) and [metric type](https://milvus.io/docs/metric.md). The former is the process of efficiently organizing data, and it plays a major role in making similarity search useful by dramatically accelerating time-consuming queries on large datasets, and the latter is used to measure similarities among vectors. Choosing a good distance metric helps improve the classification and clustering performance significantly.

```c
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128},
}
collection.create_index(field_name="embedding", index_params=index_params)
collection.load() # the collection is ready to work
```

In the above code, we choose to use `IVF_FLAT` due to our scenario, which requires high-speed queries and a recall rate as high as possible. Our preference for the L2 metric is based on *empirical experimentation.* Through testing, it became evident that the gap between the target vector and its closest match diminishes, while the separation between the most similar vector and others.

Here our collection `News` is ready to be ingested with data, so let's do it.

We use the [kaggle dataset](https://www.kaggle.com/datasets/akash14/news-category-dataset) called `News Category Dataset`, which contains articles and their section. For this example we only read the articles:

```c
import csv
csv_file_path = 'Data_Train.csv'  # Replace with the actual path to your CSV file
with open(csv_file_path, 'r', encoding='latin-1') as csvfile:
    csvreader = csv.reader(csvfile)
    list_of_text = [row[0] for row in csvreader][1:]
```

Now we create a ==function== to ingest our data, for this example we generate a list of list, which means that we ingest a list of entities. Each entity has two fields one is the text and the other their embedding, This process usually takes around 10 minutes.:

```c
def ingest_plain_text(list_of_text, milvus_collection):
    # A list with entities
    list_of_entities = [
              [], # list of text
              [] # list of embedding of the text
    ]
    for extract_text in list_of_text:
      embeddings = embedding_text(extract_text) # A numerical vector
      list_of_entities[0].append(extract_text)
      list_of_entities[1].append(embeddings)
    
    ids = milvus_collection.insert(list_of_entities)
    if ids:
        milvus_collection.flush()
        print(f"{ids.succ_count} entities were inserted")
    else:
        print("No entity was inserted.")

ingest_plain_text(list_of_text, collection)
```

That’s it, we are enable to use the function and ingest our dataset of text. Now, we can search for the most similar vectors using the script. First, we generate an embedding from some inquiry text. This embedding is wrapped in a list since the search function only accepts a list of embeddings. We pass the same parameters for the metric type and two additional parameters: the limit (the number of most similar vectors to retrieve) and a list with output\_fields associated with entities, which could be any field defined in the schema, excluding the embedding which is already fetched.

```c
embeds = embedding_text("The artificial intelligence") # return an embedding
TOP_K = 3
result = collection.search([embeds], # wrap the embedding into an inquiry list
                  anns_field='embedding', 
                  param={"metric_type": "L2",
                        "params": {"nprobe": 10}}, 
                  limit=TOP_K, # numbers of most similar embeddings
                  output_fields=['full_text']) # fields associated with vectors
```

We examine the output, where *result* is a variable containing a list of the top TOP\_K hits(sorted by distance). Each hit contains three elements: the ID, the distance, and the entity (which is a dictionary with fields of the retrieved entity). To display them, simply execute the following code:

```c
for hits_i, hits in enumerate(result):
    for hit_it, hit in enumerate(hits):
        print(hit.entity)
```

the output looks like:

```c
id: 443786974669308876, distance: 106.756103515625, entity: {'full_text': 'Jeff BezosAmazon Incartificial intelligenceAImachine learningMLUSS EnterpriseBill AckmanJohn OverdeckDavid Siegel\n\n\nDid Bill Ackman, John Overdeck and David Siegel give a bunch of money to get kids building robots, only to see those kids displaced by machines when they grow up?\n\n\nAt a benefit for FIRST, the science and technology nonprofit they\x92ve supported, the answer was a resounding no, and it came from an authoritative source, Jeff Bezos, the guy who has more than 10,000 people working on Alexa, Amazon\x92s personal assistant voice service.\n\n\n\x93It\x92s in my view very unlikely that machine intelligence and artificial intelligence will make humans have no jobs," Bezos said Thursday night in a \x93fireside chat" with Walter Isaacson at Cipriani Wall Street, as waiters in white jackets placed ricotta cheesecakes at each guests\x92 plate and poured just a bit more wine into their glasses. \x93Every piece of productivity increases our wealth as a society, and increases the jobs, and makes the jobs more interesting and higher quality."\n\n\nBezos illustrated his point using Earth-moving equipment as an example. \x93We could have a lot of employment by getting rid of bulldozers," he said. \x93You could get rid of the shovels and force people to dig with teaspoons. This would not make our society wealthier."'}
id: 443786974669309075, distance: 109.61634826660156, entity: {'full_text': 'On the surface, it\x92s life as usual for most of those who work in Electronic City, which houses about 200 IT and IT-enabled services companies, including the main campuses of companies such as Infosys, Wipro, TCS, HCL, and Tech Mahindra, as well as bio-tech major Biocon. A significant number of those who work in these IT companies and startups are engineers or software developers, a number of whom are engaged in deep tech such as artificial intelligence technologies (machine learning, deep learning, natural language processing, reinforcement learning), Internet of Things, blockchain, 3D printing, robotic process automation, robotics, augmented reality-virtual reality, and building digital payments systems .\n\n\nBengaluru\x92s residents may be tech-savvy and vocal on social media but they are far from being armchair activists. Now millionaires and veterans of industry but once freshers in the startup world such as Infosys founders N.R. Narayana Murthy, Nandan Nilekani, Mohandas Pai, and Kris Gopalakrishnan, Wipro\x92s Azim Premji and Biocon founder Kiran Mazumdar-Shaw are not only known for their entrepreneurship and philanthropy but also their activism. They not only mentor young entrepreneurs but also actively help in improving the lives of Bengaluru residents through organizations such as the Bangalore Political Action Committee (B.PAC).'}
id: 443786974669308857, distance: 110.39875793457031, entity: {'full_text': '\x93Our onset prop people and decorators are so on it, 1,000%,\x94 she said in an interview with Alison Stewart on WNYC\x92s \x93All of it\n\n\n\x94\x93Nowadays you can\x92t believe what you see because people can put things into a photo that really doesn\x92t exist, but I guess maybe it was there, I\x92m not sure,\x94 she said'}
```

This output provides details on the ID, distance, and entity associated with each hit in the search results.

As demonstrated through the provided code snippets and explanations, Milvus simplifies the complex task of handling vectorized data, making it accessible and efficient for a wide range of use cases.

In the next article, I’ll illustrate the approach to handling images/frames (unstructured data), offering awesome insights into their integration within your visual applications.

## Conclusions

In conclusion, Milvus emerges as a powerful open-source vector database, designed to facilitate embedding similarity search and enhance AI applications. Its ability to manage structured and unstructured data through embedding vectors, along with efficient similarity search capabilities, scalability, dimensionality reduction, and semantic understanding, makes it a compelling choice for a range of tasks.

With Milvus, you can unlock the potential of vectorized data storage and retrieval, setting innovative solutions across various applications.

You can find the colab notebook [**here**](https://colab.research.google.com/github/romellfudi/medium/blob/main/vector_db/Milvus_Data's_Hidden_Relationships.ipynb).

**Thank you for being here,** please comment down your views, if any mistakes found the article will be updated