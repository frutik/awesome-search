---
title: "Fine Tuning an Embedding Model for Semantic Search"
source: "https://medium.com/@venkat.ramrao/fine-tuning-a-sentence-transformer-for-semantic-search-7c7a57f4db2f"
author:
  - "[[Venkat Ram Rao]]"
published: 2023-12-23
created: 2026-06-01
description: "More"
tags:
  - "clippings"
---
==A quick introduction to fine tuning Models for Semantic Search using Sentence Transformers.==

![](https://miro.medium.com/v2/resize:fit:1146/format:webp/1*DeF-5Y-6vYXekb39bXclKQ.png)

Searching for the correct text can he harder than it looks (Image Source: Self — Created by DALL-E2)

## Introduction

Here is a quick introduction to fine tuning embedding Models for Semantic Search. I will walk through common methods of fine tuning, alternatives and then walk through a simple fine tuning of an existing model from Hugging Face.

### Sentence Transformers

Sentence Transformers is a Python framework and library which allows you to easily access and train a vast variety of Vector Embedding models. It is one way to create embeddings for text. Embedding Models have received renewed attention over the past year for use in RAG pipelines, filling a requirement to identify text to feed to an LLM for processing. In this context, they are typically used to measure *semantic similarity* between pieces to text and retrieve appropriate pieces of text based on a given input text.

This is, by no means, the only way to access Embeddings. There are other alternatives (e.g. API access to models like *ada*, libraries like *FlagEmbeddings* for models like *bge* etc.). However, this provides a great way to access a wide variety of industry leading Embedding Models hosted on Hugging Face.

One note, the framework is not limited to text and can be used for images, tables and other data types. However, for this article, I will focus on finetuning a text embedding model.

This would be helpful for use cases involving improving performance of RAG pipelines for information retrieval.

![](https://miro.medium.com/v2/resize:fit:1128/format:webp/1*CYUdJNGDPx2RunwljdGDsQ.jpeg)

Vector Space representation of a Question Answer search. Answers in Blue and Question in Green. (Source: Self)

### General Concepts

There are a wide variety of methods to train Embedding Models depending on what you are trying to do and the kind of data you have. There are a variety of loss functions for training which can cause wide differences in model performance.

One way to categorize the training methods would be by loss function. Here are some common ones.

1\. [Multiple Negative Ranking Loss](https://arxiv.org/pdf/1705.00652.pdf) (MNR Loss)— when your training data has pairs of related pieces of text.  
2\. Triplet Loss — when you have an anchor text with positive and negative texts tied to it.  
3\. Contrastive Loss — when you have both positive and negative pairs.

There are many more Loss functions than these. The full list of loss functions supported by the Sentence Transformer library can be found [here](https://www.sbert.net/docs/package_reference/losses.html).

Note that a single model can be trained using multiple methods — for example, you could train a model with MNR Loss and then fine tune the model by passing it negatives and using Contrastive Loss. The documentation for the [model](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2) I finetuned states that it was trained initially with Cross Entropy loss on sentence pairs from a vast array of datasets and here I am fine tuning it with MNR Loss.

### Additional tips…

Also, fine tuning is not magic — your dataset, loss function, epochs and other parameters play a huge role in efficacy. In some of my tests, especially when passing negative examples, my training caused **catastrophic forgetting** and I ended up totally destroying the model's ability to differentiate between texts and had all the generated embeddings clustered together with low separation.

I also found that, for the training, brevity is your friend. The model seemed to do better after training with smaller texts than with larger texts.

### Alternatives

There are, of course, alternative ways to train Embedding models. LlamaIndex has a great blog post on how to do this using their libraries which can be found [here](https://docs.llamaindex.ai/en/latest/examples/finetuning/embeddings/finetune_embedding.html).

Libraries like Flag Embeddings have associated [fine tuning functions](https://github.com/FlagOpen/FlagEmbedding/blob/master/examples/finetune/README.md) as well.

As I said earlier, I like Sentence Transformers since the library is easy to use and provides a framework to access a broad variety of excellent models hosted on Hugging Face.

## Fine Tuning

On to the fine tuning…

In the example below, I fine-tuned an existing model on the [*databricks/databricks-dolly-15k*](https://huggingface.co/datasets/databricks/databricks-dolly-15k) dataset from Hugging Face. The dataset has pairs of related texts — questions with their answers and (for about 1700 records) related context from which the answer was derived.

The model I used is [sentence-transformers/all-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L12-v2)

Since the train dataset consisted of positive pairs of text, the loss function I used was the [Multiple Negatives Ranking Loss](https://www.sbert.net/docs/package_reference/losses.html#multiplenegativesrankingloss).

I got decent results training with 1200 examples. I did my training on the free Coogle Colab GPU instance (T4). Results would, of course vary based on exactly what your use case is, what data you have and the model you started with. My code is available on my GitHub [here](https://github.com/vvr-rao/Fine-tuning-a-Sentence-Transformer-for-RAG).

### Testing the base model:

Before fine tuning, I did a basic test on the base model. The test involved giving the model a question and calculating the cosine similarity with a bunch of possible answers. (not all of which made sense)

The results were…

```c
QUESTION: What color is the Sky?
ANSWERS(with Cosine Similarity to the Question): 
The sky is blue ------------> 0.60815
I ate eggs for breakfast ---> 0.13605708
What color is the sea? -----> 0.70404685
How high is the sky? -------> 0.6920786
```

As you can see, the answer “the sky is blue” has a lower cosine similarity (0.60815) than other questions like “What color is the sea?” (0.70404685)

Ideally, for a RAG pipeline where we are trying to find answers to a question, we would want the answer to have a higher score.

**(Note:** This is a very simplistic example -and somewhat contrived- since we will usually be searching for larger pieces of text than this in the real world, but this is an illustration, so I am going to run with it.)

### The Train Dataset…

The train data set has a variety of examples for closed (with context) and open (without context) question answering. I decided to use the former. That gave me about 1700 examples. Here is some sample data;

> **Question**: Based on this passage about Ted Kennedy, at the time of his death, who were the three longest-serving senators of all time?  
> **Context:** When Kennedy died in August 2009, he was the second-most senior member of the Senate (after President pro tempore Robert Byrd of West Virginia) and the third longest-serving senator of all time, behind Byrd and Strom Thurmond of South Carolina. Later that same year, he was passed by Daniel Inouye of Hawaii. Kennedy therefore held the record as the longest-serving Democratic member of Congress to solely serve as a senator until October 2021, when he was surpassed by fellow Democrat Patrick Leahy of Vermont.  
> **Answer:** Based on this passage, Robert Byrd, Strom Thurmond and Kennedy were the three longest-serving senators of all time.

Since I was looking for a model which I could use for retrieval of text to answer a question, I kept the *Question* and *Context* and dropped the rest of the data. I also split the dataset and kept about 30% of the data aside for testing and trained with the other 70%. Therefore, I had about 1200 examples in my Train set.

```c
from datasets import load_dataset
dataset = load_dataset("databricks/databricks-dolly-15k", split="train")
dataset = dataset.filter(lambda example: example['category'] == "closed_qa")

dataset = dataset.train_test_split(test_size=0.3)
train_examples = []

for row in dataset["train"]:
  i = InputExample(texts=[ row["instruction"],  row["context"]  ]) #training the model to find the right contexts
  train_examples.append(i)

from torch.utils.data import DataLoader
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
```

### Training…

The key parameters in the training are the loss function (heavily driven by data). You can play with things like epochs, batch size etc.

```c
from sentence_transformers import SentenceTransformer, losses, InputExample

model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')

train_loss = losses.MultipleNegativesRankingLoss(model=model) #use if you have related sentence pairs
#train_loss = losses.TripletLoss(model=model)  # use this if you have an achor, positive, negative triplets

model.fit(train_objectives=[(train_dataloader, train_loss)],
          epochs=num_epochs,
          warmup_steps=warmup_steps)
```

I had tried a number of loss functions and datasets. I did have cases of CATESTROPHIC FORGETTING, where the training absolutely ruined the ability of the model to differentiate between text. This seemed to happen the most which I tried to add in negative examples and the positive and negative examples were semantically similar to each other. I’m guessing the model got confused with what I was giving it.

I would encourage you to experiment with the above.

### Results of training…

I ran the training for 10 epochs on a T4 (free Google Colab). Here are some examples on how the model changed scores after training.

```c
QUESTION:What color is the Sky?
ANSWERS(with Cosine Similarity to the Question BEFORE and AFTER training): 
The sky is blue -----------AFTER--> 0.69154847 --BEFORE--> 0.60815
I ate eggs for breakfast --AFTER--> 0.11108883 --BEFORE--> 0.13605708
What color is the sea? ----AFTER--> 0.6336577 -- BEFORE--> 0.70404685
How high is the sky? ------AFTER--> 0.70599794 --BEFORE--> 0.6920786
```

As you can see, with minimal training, the cosine similarity between the question asked and the right answer shot up (from **0.60815** to **0.69154847**) while the similarity to other questions/incorrect answers either stayed the same or dropped slightly.

Another test:

```c
QUESTION:When was Virat Kohli born?
ANSWERS (with Cosine Similarity to the Question BEFORE and AFTER training):
Virat Kohli was born on 5 November 1988 ----> 0.95706403 --WAS-> 0.8673086
When was Sachin Tendulkar born? ------------> 0.54486597 --WAS-> 0.73575497
Sachin Tendulkar was born on Apr 24, 1973---> 0.4693868 ---WAS-> 0.5586925
```

I decided to run a test against the entire test set I had set aside. On average the Cosine Similarity between the question and the right context increased from **0.6200** to **0.6942** after fine tuning.

I also did a test for retrieval accuracy, but the model was pretty good to begin with, so the accuracy was 100% both before and after fine tuning.

## Conclusion

That was a quick and simple test on Embedding Model finetuning. Needless to say, results will vary based on the parameters chosen, data available and intended end use case. You might find that Sentence Transformers are not suitable for some use cases, and you will need to search for alternative mechanisms for your semantic search needs. Testing and experimentation is your friend.

As always, feedback is welcome, and all my code is on my [github](https://github.com/vvr-rao/Fine-tuning-a-Sentence-Transformer-for-RAG/tree/main).

## REFERENCES/ACKNOWNLEDGEMENTS:

1. [Train and Fine-Tune Sentence Transformers Models (huggingface.co)](https://huggingface.co/blog/how-to-train-sentence-transformers)
2. [Losses — Sentence-Transformers documentation (sbert.net)](https://www.sbert.net/docs/package_reference/losses.html)

Dataset used: [databricks/databricks-dolly-15k · Datasets at Hugging Face](https://huggingface.co/datasets/databricks/databricks-dolly-15k)

```c
@online{DatabricksBlog2023DollyV2,
    author    = {Mike Conover and Matt Hayes and Ankit Mathur and Jianwei Xie and Jun Wan and Sam Shah and Ali Ghodsi and Patrick Wendell and Matei Zaharia and Reynold Xin},
    title     = {Free Dolly: Introducing the World's First Truly Open Instruction-Tuned LLM},
    year      = {2023},
    url       = {https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm},
    urldate   = {2023-06-30}
}
```