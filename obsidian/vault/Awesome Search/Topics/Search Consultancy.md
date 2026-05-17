---
type: topic
tags: [topic, consulting, search-business, search-strategy]
related_concepts: [Search Evaluation, Relevance Program Setup, Search Quality Assurance]
related_topics: [Relevance Program Setup, Managing a Search Team, Hiring for Search]
companies: [OpenSource Connections, Sease, The Search Juggler]
people: [Charlie Hull, Doug Turnbull, Giovanni Fernandez-Kincade, Nicolò Rinaldi]
created: 2026-05-17
---

# Search Consultancy

Search consultancy as a practice — who does it, what they offer, and how to run one effectively.

---

## Known Consultancies & Firms

| Company | Focus | People |
|---------|-------|--------|
| [[OpenSource Connections]] | Search relevance consulting + evaluation tooling (Quepid, RRE) | [[Doug Turnbull]], [[Giovanni Fernandez-Kincade]] |
| [[Sease]] | Apache Solr, Elasticsearch, neural IR (LTR, ColBERT, reranking) | [[Nicolò Rinaldi]] |
| [[The Search Juggler]] | Vendor-neutral strategy & audit, market positioning, events | [[Charlie Hull]] |
| BigData Boutique | Elasticsearch consulting | — |

---

## Individual Consultants

- [[Charlie Hull]] — 25+ years, vendor-neutral solo practitioner, Haystack organizer
- [[Doug Turnbull]] — OSC founder, *Relevant Search* author, relevance methodology
- [[Giovanni Fernandez-Kincade]] — OSC principal, search relevance
- [[Nicolò Rinaldi]] — Sease, neural IR and LTR specialist

---

## What Search Consultants Typically Offer

### Strategy & Audit
Diagnose why search is underperforming — relevance issues, missing measurement infrastructure, wrong technology fit, poor team structure. Deliver a prioritized improvement roadmap.

### Hands-On Technical Work
- Technology selection (Solr vs. Elasticsearch vs. Vespa vs. OpenSearch)
- Query design, relevance tuning, ranking model development
- Learning to Rank and neural reranking implementation
- Search quality evaluation setup ([[Relevance Program Setup]])

### Organizational Advisory
- Building a search team — roles, hiring criteria, structure
- Stakeholder communication: translating relevance metrics to business outcomes
- Relevance program governance: keeping eval infrastructure alive across quarters

### Training & Knowledge Transfer
- Relevance fundamentals for engineering teams
- LTR and embedding-based search workshops
- "Search Optimization 101" style walkthroughs

### Market Positioning (for vendors)
- Helping search product companies articulate differentiation
- Reviewing product offerings against competitive landscape
- Raising community visibility through speaking, writing, events

---

## How to Run a Search Consultancy

### Positioning
- **Pick a lane**: pure relevance/evaluation (OSC model), engineering-heavy neural IR (Sease model), or broad strategic advisory ([[The Search Juggler]] model). Generalists lose deals to specialists; specialists miss broad engagements.
- **Vendor neutrality is a feature**: clients trust advisors who have nothing to sell. Explicitly not being a platform SI partner commands a premium for unbiased guidance.
- **Build in public**: blogging, conference talks, open source tools (Quepid, RRE) create inbound without sales effort. The best search consultants are known before they pitch.

### Engagement Models
- **Hourly / day-rate** — low commitment for clients, good for audits and quick advice; easiest to sell
- **Fixed-scope project** — audit + roadmap deliverable; sets clear expectations, easier to price
- **Retained advisory** — monthly hours for ongoing guidance; highest LTV but requires established trust first
- Offer Calendly or similar for frictionless first contact — remove barriers to "just a quick call"

### What Clients Actually Need (vs. What They Ask For)
- They ask: "Is our search engine the right one?" — They need: a measurement baseline before switching anything
- They ask: "Can you fix our ranking?" — They need: a judgment set and an eval loop first
- They ask: "Should we add AI?" — They need: to quantify current relevance gaps before adding complexity

Key principle ([[Charlie Hull]]): *"Even the most sophisticated search system will fail in some cases"* — the goal is graceful failure handling and categorized understanding of problems, not perfection.

### Specialist vs. Generalist
- Specialist (neural IR, LTR, e-commerce) earns more per project and wins RFPs in their domain
- Generalist with a network ([[The Search Juggler]] model) can cover broad engagements by subcontracting or referring specialists

### Network as Infrastructure
- Actively maintain a network of specialists to refer work to and receive overflow from
- Contribute to the community (conferences, Slack groups, open source) — this is pipeline, not altruism
- Haystack, Berlin Buzzwords, and London Search & AI Meetup are core gathering points

### What Makes a Good Search Consultant
- Understand that search is a *product problem* as much as a *technical problem*
- Measure before recommending — resist tuning before establishing a baseline
- Translate between engineering (NDCG, precision@K) and business (revenue per search, abandonment rate)
- Know your limits: refer out rather than bluff in unfamiliar territory
- Write and speak publicly — thought leadership compounds over time

---

## Further Reading

- [[Relevance Program Setup]] — foundational methodology clients need before any tuning
- [[OpenSource Connections]] — dominant consultancy; Quepid tool; Doug Turnbull's writing
- [[The Search Juggler]] — Charlie Hull's solo practice; vendor-neutral model
- [[Sease]] — Italian firm; neural IR and Solr specialist
- [[Managing a Search Team]] — organizational context consultants work within
