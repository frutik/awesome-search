---
title: "How I learned Vespa by thinking in Solr"
source: "https://blog.vespa.ai/how-i-learned-vespa-by-thinking-in-solr/"
author:
  - "[[Sujit Pal]]"
published: 2021-02-24
created: 2026-07-01
description: "Learning Vespa in terms of Solr analogies can help flatten the learning curve."
tags:
  - "clippings"
---
{ }

## Vespa Blog

We Make AI Work

![Sujit Pal](https://blog.vespa.ai/assets/avatars/sujitpal.png)

[Sujit Pal](https://blog.vespa.ai/authors/sujitpal/ "Sujit Pal")  
Technology Research Director, Elsevier Labs

![How I learned Vespa by thinking in Solr](https://blog.vespa.ai/assets/2021-02-19-how-i-learned-vespa-by-thinking-in-solr/albert-WswqR4xIuH8-unsplash.jpg)

Photo by [Albert](https://unsplash.com/@picturesbyalbert?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/WswqR4xIuH8?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

Vespa is a modern search platform that offers structured search (with a SQL-like language), inverted index-based text search, and approximate nearest neighbors (ANN) based vector search. I have been mainly interested in Vespa for its vector search capabilities. However, the last couple of times I had considered Vespa for my application, I had been put off by what seemed like a pretty steep learning curve compared with Solr and Elasticsearch, two other platforms I had successfully used in the past. I realize now that the steepness is not an illusion, but it is justified, because Vespa offers many capabilities and customization opportunities. Unfortunately, that doesn’t help when you are just looking to get it integrated into your application without having to spend too much time figuring it out.

I had a little downtime between projects recently, so I decided to finally bite the bullet and spend time learning to use Vespa. I had in mind a tiny application, a minimal viable product (MVP) if you will, that I wanted to implement using Vespa. The application covered the features I most cared about, and would provide me a template for when I would use it in a “real” project.

Going through the steps outlined in the [Vespa Quick Start](https://docs.vespa.ai/en/vespa-quick-start.html) page, I realized that there were some loose correspondences with Solr. I believe that thinking of Vespa concepts and operations in terms of Solr analogies helped me get my MVP up and running quickly, although it might equally have been due to the awesome support from folks on the #vespa channel on the [Relevance Slack](https://relevancy.slack.com/) workspace. In any case, I share this insight here in the hope that it might be useful for other people who know Solr and are looking to learn Vespa. Obviously, such an approach glosses over many Vespa features, but from my experience, it is easier to learn these additional features incrementally once you have something running.

At a high level, getting a Solr platform integrated into your application involves the following steps, although not necessarily in the order provided. For example, you may want to destroy and recreate the core multiple times when designing and building your index. Similarly, you would stop and restart the server multiple times during normal operation.

1. Installing Solr
2. Starting the server
3. Checking server status
4. Creating a core
5. Configuring the core
6. Deploying the Configuration
7. Populating the index
8. Querying the index
9. Stopping the server
10. Deleting the core

So now let’s look at Vespa’s equivalents.

## Installing Vespa

Vespa is packaged as a Docker image, so the only prerequisite software needed is docker. It is also available as a CentOS RPM, but the docker image version is recommended. Minimum hardware requirement is 6 GB RAM and about 50 GB disk. I used a t2.xlarge Amazon EC2 instance (4 vCPU, 16 GB RAM) with 100 GB disk, running Ubuntu 18.04. This was adequate for my experiments (described later in the post).

To install docker, I used the [docker installation instructions for Ubuntu](https://docs.docker.com/engine/install/ubuntu/). Instructions for docker on other Linux distributions, as well as MacOS, are also available on the docker site.

To install Vespa, you need to clone the [vespa-engine/sample-apps](https://github.com/vespa-engine/sample-apps) repository. The repository contains the installation instructions for docker to spin up a Vespa image, as well as many different types of sample applications that can be used as references to build your own.

```
$ git clone https://github.com/vespa-engine/vespa.git
$ docker run --detach --name vespa --hostname vespa-container \
       --volume sample-apps:/vespa-sample-apps \
       --publish 8080:8080 vespaengine/vespa
```

At this point, the Vespa image is installed and running in the docker container. The Vespa server provides a number of services that are accessible on port 8080 of the machine (on which docker is running).

## Starting the Vespa Configuration Server

If you just installed Vespa using the commands above, the Vespa Configuration Server is already running in the docker container. However, if you have stopped the docker container (or the machine), then you can restart Vespa with the following command. This starts the Vespa configuration server. Once you deploy applications into Vespa (described below), this will also start up services for applications that were deployed already.

```
$ docker start vespa
```

## Checking server status

Vespa takes a while to start and respond to requests after the initial start, as well as after deploying an application. This is probably because it has to populate in-memory data structures that it needs to support the different services it offers. The following command hits an internal Vespa status page that returns HTTP status code 200 (OK) when Vespa is ready to handle requests.

```
$ docker exec vespa bash -c \
    "curl -s --head http://localhost:19071/ApplicationStatus"
```

## Create a Vespa application

A [Solr core](https://lucene.apache.org/solr/guide/8_5/solr-cores-and-solr-xml.html) encapsulates a single physical index, with its own configuration. The Vespa analog for a Solr core is an application. Unlike Solr cores, a Vespa application can consist of multiple physical indexes, but like a Solr core, it is governed by a single set of configuration files.

To create a Vespa application, the recommended approach is to find a sample application from the sample-apps repository (downloaded in the installation step) that is closest to your needs, and clone it as a sibling of the other applications in sample-apps. Choose a descriptive name for your project since you will be using it in subsequent requests to the Vespa server, similar to how you use the core name in Solr.

The application referenced in the Vespa Quick Start is the album-recommendation-selfhosted, so I cloned that into my application. I titled it, somewhat unimaginatively, as vespa-poc.

## Configure the Vespa application

The configuration files are everything under the directory tree src/main/application in your cloned project. Unlike Solr, where about the only things you need to customize for your configuration are the managed-schema and solrconfig.xml, in case of Vespa, you have an entire directory structure of configuration files!

For those with a Java background, the directory structure is vaguely reminiscent of a Maven project. Like Maven, which relies on convention over configuration, the directory structure of the Vespa configuration serves as clues to the purpose of each of the different configuration files. Here is the directory structure for my application configuration.

```
src
└── main
    └── application
        ├── hosts.xml
        ├── schemas
        │   └── doc.sd
        ├── search
        │   └── query-profiles
        │       ├── default.xml
        │       └── types
        │           └── root.xml
        └── services.xml
```

The configuration files are as follows.

- `hosts.xml` – defines the current hostname (node1). I did not make any change to this.
- `schemas/*.sd` – schema files, similar to Solr’s managed-schema. Vespa requires each document type in the index to be defined using a YAML-like language in its own schema (.sd) file. In my case I have a single document type called “doc”, which contains one ID field, two text fields, and one vector field. Similar to Solr’s field properties (indexable, storable, etc), each field has attribute, summary, and index properties. In addition, the.sd file defines some rank profiles that can be referenced from queries. Here is what my [doc.sd file](https://github.com/sujitpal/vespa-poc/blob/main/src/main/application/schemas/doc.sd) looks like.
- `services.xml` – maps the different document types in this application. The only change I made is to define a document type “doc” (as defined above).
- `search/query-profiles/*` – the default.xml and types/root.xml define a variable that is used in a nearest neighbor query, which I will talk about in more detail later.

## Deploy the Vespa application

Once the configuration files are created, the application can be deployed using the following command. If there are problems in the configurations, the command will report the problem and fail. It is safe to rerun the command after fixing the configuration error.

```
$ docker exec vespa bash -c "/opt/vespa/bin/vespa-deploy prepare \     
       /vespa-sample-apps/vespa-poc/src/main/application/ && \
       /opt/vespa/bin/vespa-deploy activate"
```

Vespa will take a little time to respond to the first requests following this command, similar to the lag we saw after starting Vespa. We can check for Vespa readiness similarly by querying the ApplicationStatus service as described in the “Checking server status” section.

## Populating the Vespa Indexes

Vespa offers a document endpoint, similar to the Solr update endpoint, to populate its indexes with documents. They must be of the document types declared in the configuration step above. The endpoint URL contains the application name and the document type name(s) to enable Vespa to route an incoming document to the correct index. An endpoint URL to insert a document of document type “doc” and document id 1 for the “vespa-poc” application is shown below. There is more information on the [Vespa Documents](https://docs.vespa.ai/en/documents.html) page.

```
http://localhost:8080/document/v1/vespa-poc/doc/docid/1
```

The request payload is a flat dictionary of field name-value pairs, converted to JSON format, and sent to Vespa using HTTP PUT (or POST). The docid can be any value that uniquely identifies the document, in my example I have used a (synthetic) field that is just a monotonically increasing sequence number.

Data for my MVP experiment came from the [CORD-19 dataset](https://allenai.org/data/cord-19), a collection of scientific papers around COVID-19, provided by Allen AI. Note that my experiment is completely different from the [CORD-19 Search](https://cord19.vespa.ai/) application, which incidentally is a great example of what you can do with datasets such as CORD-19 and Vespa.

The version of CORD-19 I used contained around 300,000 papers and their associated SPECTER document vectors. For my index I used the paper ID, title, abstract, and the SPECTER vector. An example of the request payload is shown below, and here is the [Python code](https://github.com/sujitpal/vespa-poc/blob/main/python-scripts/index/prepare-and-load-index.py) to parse this information out of CORD-19, compose the payload and issue HTTP POST queries to the Vespa document endpoint.

```
{
    "cord_uid": "xhyu5r5x",
    "doc_title": "High red blood cell composition in clots is associated with successful recanalization during intra-arterial thrombectomy.",
    "doc_abstract": "We evaluated the composition of individual clots retrieved during intra-arterial thrombectomy in relation to recanalization success, stroke subtype, and the presence of clot signs on initial brain images …",
    "specter_embedding": {
        "values": [ 
            0.35455647110939026, 
            -5.337108612060547, 
            2.201319932937622, 
            … 
        ]
    }
}
```

Vespa also offers its [HTTP Client](https://docs.vespa.ai/en/vespa8-release-notes.html#vespa-http-client), which is a faster and more robust alternative for batch inserts. To use this, the records to be inserted need to be JSON serialized into a flat file, and the path to the flat file passed to the HTTP Client.

## Querying the Index

The Vespa query language (YQL) is very similar to the SQL query language, so there will not be much of a learning curve for most people reading this blog. The query endpoint is available at:

```
http://localhost:8080/search/
```

It accepts both HTTP GET and POST requests. The YQL specifies the fields to return, the document types to look up, and the query condition. Additional information such as the rank profile (i.e. what scoring function to use for which field), the number of results to return, offset, etc., are provided as additional fields. These fields are specified as HTTP request parameters for GET requests or sent as a JSON-formatted dictionary of name-value pairs in the request body for POST requests. The [Query API](https://docs.vespa.ai/en/query-api.html) page contains more information about the available parameters.

Like configuration and population, queries are application dependent. In my case, my objectives were to set up:

1. Text search – return results based on a text search on the title field.
2. Vector search – return results based on vector search on a document’s SPECTER embedding, similar to a [Solr More Like This (MLT)](https://lucene.apache.org/solr/guide/8_5/morelikethis.html) search.

The first objective is super-simple and can be achieved quite easily using a simple YQL query as shown in [this code](https://github.com/sujitpal/vespa-poc/blob/main/python-scripts/search/simple-text-search.py).

The second one is slightly more complicated – I use the GET endpoint to retrieve the SPECTER embedding from a given document by document ID, then use the nearestNeighbor function to retrieve its 10 nearest neighbors in the vector space, as shown in [this code](https://github.com/sujitpal/vespa-poc/blob/main/python-scripts/search/mlt-vector-search.py).

One can think of the nearestNeighbor call as roughly analogous to a Solr function query or a SQL user-defined function (UDF). It takes two parameters, the first of which is a field defined within the document type, and the second is a variable representing the query vector. The query vector needs to be defined in the query-profiles/types/root.xml file.

Obviously, this just barely scratches the surface of the various query types that are possible with Vespa. The [YQL page](https://docs.vespa.ai/en/query-language.html) provides examples of various operations possible using YQL, and the [Nearest Neighbor Search](https://docs.vespa.ai/en/nearest-neighbor-search.html) and the [Approximate Nearest Neighbor Search with HNSW](https://docs.vespa.ai/en/approximate-nn-hnsw.html) pages provide more information around Vespa’s vector search capabilities.

## Stopping the server

You stop the Vespa server using the following command. This will preserve any application configuration and indexes you have created so far. This is equivalent to a Solr stop server command.

```
$ docker stop vespa
```

## Deleting the Vespa application

Finally, you can remove the Vespa image from docker using the following command. This will remove your application indexes from Vespa as well. This is equivalent to destroying a Solr core.

```
$ docker rm -f vespa
```

## Conclusion

The strategy of using Solr analogies and operations to support my Vespa learning experience has worked well for me. Vespa commands are of course longer, more complex and harder to remember since they are docker commands, so it helped to make them similar to Solr commands by wrapping them in [simple shell scripts](https://github.com/sujitpal/vespa-poc/tree/main/bash-scripts).

I realize that there is much more to Vespa than I have seen and described so far. However, the good news is that Vespa’s learning curve no longer feels quite as steep as it first appeared, and it feels easier to experiment and learn about other features as needed. Some functionality that I hope to explore in the near future are Vespa’s capability of using ML models for ranking, and its built-in support for two-phase queries.

---

*Sujit Pal is a Technology Research Director with Elsevier Labs, an advanced technology group within Elsevier. His areas of interest are Search, Natural Language Processing, Machine Learning and Distributed Data Processing.*

## Read more

[« Parent-child joins and tensors for content recommendation](https://blog.vespa.ai/parent-child-joins-tensors-content-recommendation/) [Run search engine experiments in Vespa from python »](https://blog.vespa.ai/run-search-engine-experiments-in-Vespa-from-python/)