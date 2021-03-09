## LTR

#### John
hi all :wave: these aren’t nuts-and-bolts question for LTR, but more about some of the upshots and general approach:
how are you handling pagination?
i tend to see the approach of 100 documents for 10 end results. does the 10:1 ratio stand at other page sizes or do you opt to use a log function of some sort?

#### Max
Hi John, IMO the rerank window should be enough to cover all the pages that folks are likely to see.  So if you have 10 results on a page, and you rerank 100 docs, that's 10 pages deep of results.   In other words, pagination is 'baked in'.

#### John
ah, right right. that makes sense. at what point in the paging does one hit a refresh on the fetch, then, in order to have a new set of reranked docs that are “anchored’ (poor word choice :sweat_smile: ) at the new position, e.g. page 6? or is it a moot point until a user wants to see beyond that initial 100 results / 10 pages? 

#### Max
I think that if someone even gets to the sixth page, the ranking must be pretty bad anyway and LTR won't save you :)
