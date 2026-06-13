---
created: 2026-05-16
type: article
tags: [article, spotify, team-structure, organization, search-platform, company-blog]
source: "https://engineering.atspotify.com/2021/4/rethinking-spotify-search"
author: [Hugo Galvão, Daniel Doro]
company: [Spotify]
concepts: [Search Architecture]
topics: [Managing a Search Team]
---

# Rethinking Spotify Search

**[[Hugo Galvão]] and [[Daniel Doro]]** document Spotify's three iterations of search team organization as the team grew 5× between 2016 and 2021.

## Evolution

### Phase 1: Problem-Oriented Teams (2019)
Teams organized around specific user problems. Issue: problems are transient — new problems arise quarterly, forcing constant reorganization.

### Phase 2: Stack-Oriented Teams (2020)
Each team owns one layer of the search stack (data ingestion, quality/ML, API, insights, podcast search). Revealed the **centrality problem**: cross-stack features required coordinating 5 different teams. High congestion + high centrality → slow delivery despite team growth.

### Phase 3: Platform + Core (2021)
**Two groups**:
1. **Core Search** — personalized search experience; metric: Spotify end-user satisfaction
2. **Search Platform** — developer-facing infrastructure; metric: Spotify developer happiness + SLO compliance

Rationale: different users (end users vs. internal developers), different success measures, but shared mission. Platform autonomy enables other teams to experiment without coordinating with core search.

## Key Data Points
- 2021 internal contribution teams: 100%+ growth vs. 2018, 500%+ vs. 2016
- System congestion and centrality metrics guided the decision to restructure

## Key Insight

Growth in headcount does not translate to velocity if coordination costs grow faster. The platform model decouples infrastructure development from product experimentation.

## Related Concepts

[[Search Architecture]] · [[Managing a Search Team]]
