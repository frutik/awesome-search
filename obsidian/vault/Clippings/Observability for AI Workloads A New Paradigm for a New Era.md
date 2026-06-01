---
title: "Observability for AI Workloads: A New Paradigm for a New Era"
source: "https://horovits.medium.com/observability-for-ai-workloads-a-new-paradigm-for-a-new-era-b8972ba1b6ba"
author:
  - "[[Dotan Horovits (@horovits)]]"
published: 2026-01-04
created: 2026-06-01
description: "More"
tags:
  - "clippings"
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*kbCCHb12wdDNsbksNdkRSA.png)

Observability for AI Workloads: A New Paradigm for a New Era | @horovits | Medium

## The evolution of observability in the AI era

2025 was the year AI workflows moved from experimentation to production. What started as isolated proof-of-concepts became mission-critical systems powering customer support, content generation, code assistance, and decision-making across industries.

But as these LLM-based applications hit real-world traffic, a troubling pattern emerged: our observability practices weren’t keeping pace. Teams found themselves flying blind — unable to explain why costs suddenly spiked, struggling to reproduce bugs in non-deterministic systems, and lacking visibility into whether their models were actually performing well or slowly degrading. The CNCF AI Working Group captured this challenge perfectly in their [Cloud Native Artificial Intelligence white paper](https://www.cncf.io/wp-content/uploads/2024/03/cloud_native_ai24_031424a-2.pdf): *“Observability is vital to detect model drift, usage load, and more”* — yet the reality proved more nuanced than simply applying existing tools.

AI workloads introduce entirely new observability needs around model evaluation, cost attribution, and AI safety that didn’t exist before. Even more surprisingly, AI workloads force us to rethink fundamental assumptions baked into our “traditional” observability practices: assumptions about throughput, latency tolerances, and payload sizes.

As we enter 2026, I’d like to share my insights on what observability for AI workloads should look like — embracing both the familiar foundations and the new frontiers these systems demand.

## [OpenTelemetry for GenAI and the OpenLLMetry project](https://horovits.medium.com/opentelemetry-for-genai-and-the-openllmetry-project-81b9cea6a771?source=post_page-----b8972ba1b6ba---------------------------------------)

### OpenTelemetry for GenAI and the OpenLLMetry project Generative AI is everywhere, but how do we monitor and observe it…

horovits.medium.com

## The new observability imperatives for AI workflows

AI applications have introduced observability requirements that simply didn’t exist in traditional software workloads, as we started asking entirely new questions.

### Evaluation: measuring what matters

In traditional systems, we measure success with uptime, error rates, and latency. But for AI workloads, the question “Is it working?” is far more complex. Success is no longer binary, and many failures are semantic, rather than technical. You need to track response quality metrics like **accuracy, relevance, and hallucination rates** — measurements that exist on spectrums. Furthermore, constant evaluation is required to **detect model drifts** over time, as the real world evolves and shifts away from the baseline embedded within the training data.

Context retention analysis tells you whether your chatbot maintains conversation state across multiple turns. User feedback loops — thumbs up/down ratings, corrections, abandonment signals — provide ground truth that technical metrics can’t capture. Your observability system needs to detect when model outputs start deviating from expected patterns, even when technical metrics look fine.

### Cost tracking: the token economy

Tokens have become the most expensive resource in your IT bill. Token-level cost attribution is non-negotiable — you need to understand expenses per request, per user, per feature, and identify which parts of your application are burning budget.

API call optimization requires visibility into caching opportunities and batching potential, while model selection economics demands empirical data on cost-performance tradeoffs (does GPT-4’s accuracy justify its 10x price premium over GPT-3.5?).

For self-hosted models, GPU utilization and inference costs directly impact your bottom line. The ultimate goal is ROI analysis that connects technical metrics to business outcomes: what’s the cost per successful customer interaction, per generated article, per resolved support ticket?

### AI Safety: the need for ethical LLM

AI brought a whole set of safety concerns we haven’t encountered before, which we need to monitor and observe. There are various aspects of **ethical LLM** that arise in this new era: **Bias detection** requires instrumentation that identifies unfair or discriminatory outputs, not just obvious slurs but subtle patterns where the model treats different groups differently. **Content safety** involves flagging toxic, harmful, or inappropriate generations before they reach users, with metrics tracked over time.

Data handling also has several new aspects: privacy compliance monitoring means detecting when **PII leaks into prompts** or responses before it reaches third-party APIs or gets logged. Data handling audits ensure **secure processing**: where does data go, how long is it retained, who has access? As AI regulations emerge globally, regulatory compliance tracking becomes critical — you need audit trails showing what your AI did, when, and why.

### Debugging: the non-deterministic version

Traditional debugging assumes determinism — run the same code with the same input, get the same output. AI workflows shatter this assumption. When a user reports that “the chatbot gave a weird answer,” you can’t just replay the request and expect to see the same behavior. Standardizing LLM-specific log data becomes critical: you need to capture the full context including prompt templates, model parameters (temperature, top\_p, max\_tokens), generation settings, and the specific model version. Without this, reproduction is impossible.

Error reporting for non-deterministic systems requires rethinking what an “error” even means — is a hallucination an error? What about a response that’s technically correct but misses the user’s intent? You need structured logging that preserves the full prompt-response pair along with intermediate steps, traces of prompt engineering iterations. This also ties into explainability that keeps coming up as a “human” concerns that isn’t easy to settle with the logic of neural networks.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ykUUiKRmUYGO0zAtBTBAoQ.png)

Tracing AI workflows

## AI workflows flips “traditional” observability tradeoffs

What about “traditional” observability? It’s still needed, of course. However, AI workloads force us to question fundamental assumptions baked into our existing tools and practices. The scale characteristics of AI workloads are essentially inverted compared to classic cloud-native systems.

Traditional microservices handle millions of requests per second with millisecond latencies and kilobyte payloads. AI workloads flip this on its head:

- **lower throughput:** hundreds to thousands of requests per minute, not millions per second)
- **higher latency tolerance:** LLM calls take 2–30 seconds, not 2–30 milliseconds, making instrumentation overhead negligible
- **larger payloads:** prompts and completions routinely reach tens of kilobytes, with multimodal inputs pushing into megabytes.

This challenges some base assumptions baked into our current observability tooling, as well as our DevOps practices.

## Observability across the AI stack

The observability imperatives we’ve discussed — evaluation, cost tracking, safety, and debugging — along with the “traditional” observability, exists across multiple layers of the stack, each with its own characteristics and tooling requirements:

**Application Layer:** End-user feedback collection, session-level analytics, feature usage tracking, and user intent classification — the human experience that traditional APM tools miss.

**Orchestration Layer:** Guardrail effectiveness, chain performance across multi-step workflows, prompt caching hit rates, routing decisions between models, and fallback pattern execution.

**Agentic Layer:** Agent-to-agent communication patterns, command execution monitoring in the real world, tool usage and external API invocations, protocol compliance, and decision tree analysis.

**Model Layer:** Token usage and costs per invocation, model stability across versions, inference latency (time to first token and total generation time), invocation errors and rate limiting, and resource utilization.

**RAG and Vector Database Layer:** Retrieval performance and query latency, retrieval accuracy and relevance scoring, semantic similarity quality, index health and freshness, and context assembly effectiveness.

**Infrastructure Layer:** GPU monitoring (utilization, memory, temperature, throttling), network bandwidth to model APIs and vector databases, compute resource allocation for supporting services, and capacity planning based on usage patterns — what the CNCF white paper emphasizes as essential for “long running workloads” where “anomalies in GPUs and networking may happen at times.”

## Telemetry signals for AI workloads

The observability signals, such as metrics, logs, and traces, remain the pillars also for AI workloads, but their implementation and emphasis shift significantly from what we know in traditional observability.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*i30UpmVmcde8glRNP4QXxw.png)

Tracing an AI workflow

### Traces: the complete journey

While traditional tracing focuses on service boundaries, timing, and dependencies between microservices, AI tracing must capture *content* — the actual reasoning and execution path of the agent.

A full chat run with your friendly chatbot will generate a complete session, comprised of multiple traces for the individual interactions in the chat. The trace’s root span captures the user-facing interaction — a chat message, a content generation request, a code completion — but the child spans tell a richer story than mere service calls. They must capture prompts (both system and user), completions generated at each step, tool calls and their arguments, tool responses, and iterative LLM calls within an agent’s decision-making process.

This means an AI trace is effectively the full reasoning and execution path: you see not just that the agent called a weather API, but what it asked for, what it received, and how it incorporated that information into its next LLM call. The attributes become the story itself: model name and version, prompt template IDs, token counts (input and output), cost per call, temperature and generation parameters, retrieved context

### Metrics: beyond rate, errors, and duration

AI workloads require both traditional and entirely novel metrics. Traditional metrics still apply but need adaptation: request rate and error rate remain relevant, but what constitutes an “error” is more nuanced; latency percentiles (p50, p95, p99) still matter, but the thresholds are measured in seconds, not milliseconds; availability and uptime are still critical.

AI-specific metrics become equally important: cost metrics (tokens per request, cost per request/user, token count) often drive more operational decisions than performance metrics; quality metrics (hallucination rate, relevance scores, user satisfaction) measure what traditional monitoring can’t see; efficiency metrics (cache hit rates, retrieval accuracy, token efficiency) identify optimization opportunities; safety metrics (PII detection rate, content filter triggers, bias indicators) ensure responsible AI operation.

What’s fundamentally different is that token costs — the API charges for LLM inference — often dominate total system cost, making infrastructure costs secondary. In 2025, I watched organizations where a single poorly-optimized prompt could cost more per day than the entire Kubernetes cluster running it. This elevation of cost observability transforms it from an engineering concern into a leadership-level priority.

### Logs: from debugging aid to primary data source

Logs provide vital observability into AI workflows. Structured prompt and response data must be captured in full, along with all parameters and settings; Model selection reasoning needs logging; Guardrail decisions and rejections should be recorded; User feedback and corrections provide ground truth for quality assessment; Safety and compliance events need detailed audit trails.

## Open standardization: the path forward with OpenTelemetry

As the observability challenges of AI workloads became clear throughout 2025, the community recognized that proprietary, vendor-specific approaches would fragment the ecosystem and lock teams into inflexible solutions.

The OpenTelemetry project has been the de-facto [standard for IT observability](https://horovits.medium.com/the-rise-of-open-standards-in-observability-highlights-from-kubecon-13694e732c97), unifying logs, metrics, traces and most recently even [profiles](https://horovits.medium.com/charting-new-territory-opentelemetry-embraces-profiling-4a9b407e48cc). Adapting OpenTelemetry for observability of GenAI applications is only a natural step.

## [The Rise of Open Standards in Observability: Highlights from KubeCon](https://horovits.medium.com/the-rise-of-open-standards-in-observability-highlights-from-kubecon-13694e732c97?source=post_page-----b8972ba1b6ba---------------------------------------)

### Discover how open source standards are revolutionizing observability, with key updates on OpenTelemetry, Prometheus…

horovits.medium.com

The OpenTelemetry Generative AI Special Interest Group (a.k.a. OTel GenAI instrumentation SIG) emerged to address this gap, working to establish semantic conventions for AI-specific telemetry. The new SIG, along with open source projects such as Langfuse and OpenLLMetry that adapt OpenTelemetry Collector tool for these workflows, help converge the community around a common open path, as I covered in my [recent blog post](https://horovits.medium.com/opentelemetry-for-genai-and-the-openllmetry-project-81b9cea6a771).

## Time to rethink observability

As we progress through 2026, observability for AI applications becomes existential. We’ll see more dashboards that combine what were previously separate concerns: performance metrics, cost metrics, and quality metrics forming an inseparable triad that defines AI system health. This convergence of traditional observability with AI-specific requirements represents one of the most significant evolutions in our field.

The organizations I believe will succeed with AI in production share a common trait: they invest in observability from day one, and they understand that AI systems are fundamentally different from traditional software—and aren’t afraid to revisit their tools, practices and base assumptions.

The future of AI is observable. The question is: are you ready to observe it?