---
title: "Rethinking Spotify Search"
source: "https://engineering.atspotify.com/2021/4/rethinking-spotify-search"
author:
  - "[[Hugo Galvão]]"
  - "[[Daniel Doro]]"
published:
created: 2026-05-16
description: "Search is a well-established functionality across different industries, devices, and applications. When users come to any kind of search, they already have something in mind, whether they come looking for one thing in particular or are open to becoming inspired. Spotify Search is no exception, helping a vast majority of users find joy through search, regardless of the language or method used to search, both typed and spoken."
tags:
  - "clippings"
---
**Spotify Portal for Backstage is now GA!** [Read the announcement](https://backstage.spotify.com/discover/blog/spotify-portal-ga-webinar-october-2025/)

![Feature Image](https://engineering.atspotify.com/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fp762jor363g1%2Fattachment_2e41f5ba516150b097a8f7b25649ba88%2F7a37ec2953092103a8e6b2998d573676%2FEN14X_1200_x_630.png&w=1920&q=75)

## Search @ Spotify

Search is a well-established functionality across different industries, devices, and applications. When users come to any kind of search, they already have something in mind, whether they come looking for one thing in particular or are open to becoming inspired. Spotify Search is no exception, helping a vast majority of users find joy through search, regardless of the language or method used to search, both typed and spoken.

Since Spotify’s launch in 2008, Search has been a core piece of the user journey, and it’s where we’ve increased our investment and focus over time. Earlier on, only a small group of people were responsible for the end-to-end experience that encompassed the infrastructure that held Search together, the backend system that powered the personalized results, and the desktop and mobile interface that delighted our users. Spotify continued to grow, reaching 345 million users in December 2020, and Search grew with it. This post details the challenges that emerged as teams began to scale.

## When more doesn’t mean more

In the beginning of 2019, we already had a handful of teams working across the Search infrastructure, as well as the machine learning and backend systems. Given the increasing number of user issues we were trying to solve at the time, we decided to organize ourselves around these problems. But we quickly learned that problems come and go, new problems arise, and priorities can change unexpectedly. This meant that we were creating new teams all the time (well, not all the time, but almost every quarter).

![image5](https://images.ctfassets.net/p762jor363g1/attachment_963d45406c36aac438eae670a95ac415/f9e7d272cba79b1667f496f9ea312553/attachment_963d45406c36aac438eae670a95ac415.jpg)

2020 was the year for us to try something new. We decided to take a different approach to organizing our teams. Each team would become responsible for one piece of our Search stack — meaning one team would be responsible for getting data into Search, another team would be responsible for the quality of personalized Search results, another team would be responsible for our Search APIs, another team for insights, and finally, a team would be focused on our company bet, podcast Search. You might be wondering, “ *If each team were responsible for one part of the Search stack, how would we solve problems that required the expertise of different parts of our time around specific issues such as query intent, retrieval, and ranking?”* That is a great question — one that was highlighted as one of the original risks when we formed this organization. But we believed that nurturing our tech stack was the way to go. And guess what? We learned new things, which made us reconsider old ways of thinking. Or better, made us want to try something different.

![image2](https://images.ctfassets.net/p762jor363g1/attachment_c7db3b3d0f7fccc374af005bbc91f7ae/cd19411321a519afb36417f54ecd13b6/attachment_c7db3b3d0f7fccc374af005bbc91f7ae.jpg)

By the end of 2020, we had grown our internal efforts by more than 100% compared to 2018, and 500% compared to 2016. But we were not seeing the same boom in terms of speed of delivery, experimentation, and number of problems we were solving. Each time a team outside our Search area wanted to collaborate with us or use our systems to solve their problems, they would need to involve multiple experts from each Search stack part, meaning sometimes five different Search teams. There were also varied rhythms and maturities among teams and systems, despite having the same priorities.

We were experiencing these problems on a daily basis, but we weren’t sure if we were blindsided by our previous learnings and our own beliefs or if we were biased because of the people we asked for feedback. We decided to check some numbers. Supported by Spotify’s Chief Architect Niklas Gustavsson’s latest research, we focused on two data points: system centrality and system congestion.

![Frame-15](https://images.ctfassets.net/p762jor363g1/attachment_8a5462e4f83041de1babb385d8f13bf9/b92651fbe8d0fe8d43299be64f66d1a6/attachment_8a5462e4f83041de1babb385d8f13bf9.jpg)

In the image above, congestion represents the unique teams contributing to the codebase over a period of time. Centrality is subdivided into two buckets: indegree centrality — how many teams have a dependency on a given service; and outdegree centrality — how many teams the service depends on. Search was in high demand across all these dimensions.

## Search as a platform

Great — we received feedback from users, from other teams, from our own Search teams, and we also had data from our own systems. Was there something else we could use to have a better understanding and make a more informed decision on how to make our Search better? We knew that users from different markets were experiencing different levels of Search satisfaction, and that the forecast was that new-user growth would come from outside North America and Western Europe. We also knew that we had dedicated Spotify teams focused on improving the overall experience for these new markets. Spotify had, as well, much experience building internal tools and platforms to scale our business and improve productivity. So we wondered, should we build a Search platform? We believed so.

## From user obsession to developer satisfaction

With insights about Spotify’s growth, system centrality and system congestion, along with team and user feedback, we decided, in 2021, to evolve our organization to try to solve for the needs of both external (Spotify end users) and internal (Spotify developers) users. In order to accomplish that, we created two groups inside our Search area — one focused on our personalized core Search experience, with Spotify end user satisfaction as the measure of success, and the other aiming to improve Spotify developer happiness, encouraging experimentation while maintaining the services SLOs. Below you can see what our Search organization looks like today.

![image3](https://images.ctfassets.net/p762jor363g1/attachment_0bf9e445d40d767969cde1d24faf98db/a5abf3096498ad763f9488af4b342ce0/attachment_0bf9e445d40d767969cde1d24faf98db.jpg)

While these two groups don’t necessarily share the same metrics, we believe that they do share the same goal: “ *\[T\]o unlock the potential of human creativity — by giving a million creative artists the opportunity to live off their art and billions of fans the opportunity to enjoy and be inspired by it.*” Making these groups autonomous and independent in ways of working and goal setting — leading with context instead of control — is what we believe makes us better prepared to support Spotify users and growth.

## Conclusion

Katarina Berg, Chief HR Officer, says “ *Growth is our mantra* ” and “ *Change is our constant.”* This means that our Search journey will not end here. Nor will this be the last iteration of our organization. But we are eager to give it a try, learn new things, tweak them, and try again — especially now that we are expanding into more markets and languages, investing in podcast topic search, podcast understanding, and retrieval, and rolling out many other new features in the future.

**References**

Ang Li et al., “Search Mindsets:Understanding Focused and Non-Focused Information Seeking inMusic Search,” [publication](https://research.atspotify.com/publications/search-mindsets-understanding-focused-and-non-focused-information-needs-in-music-search/) *WWW ’19: The World Wide Web Conference* (May 2019): 2971–2977. [https://doi.org/10.1145/3308558.3313627](https://doi.org/10.1145/3308558.3313627)

“Shareholder Letter Q4 2020” (February 3, 2021) [https://s22.q4cdn.com/540910603/files/doc\_financials/2020/q4/Shareholder-Letter-Q4-2020\_FINAL.pdf](https://s22.q4cdn.com/540910603/files/doc_financials/2020/q4/Shareholder-Letter-Q4-2020_FINAL.pdf)

“Spotify — Company Info,” For the Record, [https://newsroom.spotify.com/company-info/](https://newsroom.spotify.com/company-info/)

“The Band Manifesto.” [https://www.spotifyjobs.com/culture/the-band-manifesto](https://www.spotifyjobs.com/culture/the-band-manifesto)

“Spotify Expands International Footprint, Bringing Audio to 80+ New Markets,” For the Record (February 22, 2021).

“Today’s Spotify Stream On Announcements,” For the Record (February 22, 2021) [https://newsroom.spotify.com/2021-02-22/todays-spotify-stream-on-announcements/](https://newsroom.spotify.com/2021-02-22/todays-spotify-stream-on-announcements/)

“SPOTIFY PODCASTS DATASET.” [https://podcastsdataset.byspotify.com/](https://podcastsdataset.byspotify.com/)

Tags: [backend](https://engineering.atspotify.com/tag/backend)