---
title: "Metarank: Personalized Ranking That Actually Reads Your Clicks"
source: "https://www.codeline.co/thoughts/repo-review/2025/metarank-personalized-ranking-that-actually-reads-your-clicks"
author:
  - "[[Florian Narr]]"
published: 2025-12-15
created: 2026-06-11
description: "An open-source learn-to-rank service written in Scala that turns click signals into real-time personalized search and recommendations — with a surprisingly clean streaming architecture under the hood."
tags:
  - "clippings"
---
## What it does

[Metarank](https://github.com/metarank/metarank) is a real-time personalization service. Feed it user events — clicks, purchases, impressions — and it reranks your search results or recommendations on the fly. It sits between your search engine and your users, learning what works and adjusting item scores per session.

## Why I starred it

Most ranking systems I have seen fall into two camps: either they are massive internal platforms at big companies that you will never get to use, or they are thin wrappers around a single ML model with no opinion on feature engineering. Metarank sits in a rare middle ground. It ships with 20+ built-in feature extractors (CTR, user agent, referer, interaction counts, time decay), handles the entire feedback loop from event ingestion to model training to serving, and does it all as a single stateless service you can run in Docker. The YAML-driven config means you can go from zero to a working LambdaMART ranker without writing Scala.

## How it works

The entry point is `Main.scala`, which parses CLI args into commands: `import`, `train`, `serve`, `standalone` (all three combined). The interesting path is `standalone`, which chains the full pipeline.

The core abstraction is `FeatureMapping` in `src/main/scala/ai/metarank/FeatureMapping.scala`. It takes your YAML feature definitions and model configs, instantiates the right feature extractors and predictors, and wires them together:

```scala
case class FeatureMapping(

    features: List[BaseFeature],

    schema: Schema,

    models: Map[String, Predictor[_ <: ModelConfig, _ <: Context, _ <: Model[_ <: Context]]]

)
```

Each model config gets matched to a predictor — `LambdaMARTPredictor`, `ShufflePredictor`, `TrendingPredictor`, `MFPredictor` (collaborative filtering via ALS), or `BertSemanticPredictor` for neural search. The `makeDatasetDescriptor` method translates feature types into `ltrlib` dataset descriptors, bridging Metarank's feature system with the underlying LTR library.

The event processing pipeline lives in `MetarankFlow.scala`. It is built on fs2 streams and cats-effect, and the design is clean:

```scala
source

  .evalTapChunk(e => IO(store.ticker.tick(e)))

  .flatMap(event =>

    Stream.evalSeq[IO, List, Event](

      clickthrough.process(event)

        .map(cts => event +: cts.flatMap {

          case TrainValues.ClickthroughValues(ct, _) => ImpressionInject.process(ct)

          case _ => Nil

        })

    )

  )

  .through(event.process)

  .through(sink.write)
```

Events flow through a `TrainBuffer` that collects clickthrough data (which items were shown, which were clicked). When a clickthrough is complete, `ImpressionInject` synthesizes impression events for items that were shown but not clicked — negative signals. This is the feedback loop that makes the model learn.

The feature computation in `FeatureValueFlow.scala` uses a Scaffeine cache with a custom ticker to decide when feature values need refreshing. Each `Write` operation gets dispatched by type — `Put`, `PutTuple`, `Increment`, `PeriodicIncrement`, `Append` — to the appropriate feature store backend. The `shouldRefresh` check compares timestamps against a per-feature refresh interval, so high-frequency features like click counts can update on every event while slower-moving features skip redundant recomputation.

The ranking endpoint in `RankApi.scala` is straightforward http4s. A POST to `/rank/{model}` deserializes a `RankingEvent`, passes it to `ranker.rerank()`, and returns scored items. There is an `?explain=true` query param that exposes feature values per item — useful for debugging why a particular item ranked where it did.

## Using it

The quickest path is Docker with the built-in demo dataset:

```bash
curl -O -L https://github.com/metarank/metarank/raw/master/src/test/resources/ranklens/events/events.jsonl.gz

curl -O -L https://raw.githubusercontent.com/metarank/metarank/master/src/test/resources/ranklens/config.yml

docker run -i -t -p 8080:8080 -v $(pwd):/opt/metarank \

  metarank/metarank:latest standalone \

  --config /opt/metarank/config.yml \

  --data /opt/metarank/events.jsonl.gz
```

Then rank some items:

```bash
curl http://localhost:8080/rank/xgboost \

  -d '{"event":"ranking","id":"id1",

       "items":[{"id":"72998"},{"id":"67197"},{"id":"77561"}],

       "user":"alice","session":"alice1",

       "timestamp":1661431886711}'
```

Send a click event and re-rank — the scores shift based on the interaction. That feedback loop is the whole point.

## Rough edges

The README has several `TODO` links for semantic search and recommendation guides that go nowhere. Some internal doc links are broken (`configuration/recommendations/similar.md` is missing the `doc/` prefix). The last meaningful code commit was September 2025 — dependency bumps aside, active development has slowed.

The feature extractor list is impressive but the 21 built-in features are somewhat rigid. Writing a custom feature extractor means extending `BaseFeature` in Scala, compiling a new JAR, and deploying it. No plugin system, no scripting layer.

State management is Redis-only for production. The in-memory store works for demos but the jump to requiring a Redis cluster for anything real is a gap. There is a file-based store for training data (`TrainStore`) but not for serving state.

The Scala/JVM stack means the Docker image is heavy and startup is not instant. If you are already running a JVM shop this is fine. If not, it is one more thing to operate.

## Bottom line

If you need to add click-based personalization to an existing search system and don't want to build the feature engineering, feedback loop, and model training pipeline from scratch, Metarank is the most complete open-source option I have seen. Best suited for teams already comfortable with JVM services and Redis who want learn-to-rank without the multi-month build.