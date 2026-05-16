---
type: company
tags: [company, search, e-commerce, spain, relevance]
category: technology-provider
industry: e-commerce search
products: [EmpathyBroker search platform, Contextualize (behavioral ranking)]
search_domain: [e-commerce search, behavioral ranking, relevance]
use_cases: []
people:
  - "[[David Argüello Sánchez]]"
---

# Empathy (EmpathyBroker)

Spanish e-commerce search company providing search technology to European retailers. Now trading as Empathy.co.

## Notable Work

**TF-IDF in E-commerce** — demonstrated how standard TF-IDF relevance assumptions break in product catalog search:
- iPad accessories outrank actual iPads (term frequency inflates accessory scores)
- "Polo Ralph Lauren" brand items outrank polo shirts (IDF favors rare brand-field matches)

**Fix**: Disable TF-IDF similarity (`similarity: boolean`) for structured product data. Field weights then behave predictably. Multiple merchandising rules become unnecessary.

**Contextualize** — behavioral data product that uses click/purchase signals to improve ranking models.

## Key Articles

- [[The Influence of TF-IDF Algorithms in E-commerce Search]]
