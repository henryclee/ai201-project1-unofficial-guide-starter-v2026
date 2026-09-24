# Run log — after-hybrid-rerank

- Produced by: `run_eval.py::main`
- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`
- Corpus: `city_guides` (index variant `default`)
- top-k: 7 · relevance cutoff: 0.65
- Runs per question: 3, caching off
- When: 2026-09-24 15:28

This table is one row per QUESTION. The run log your README asks for is
one row per CRITERION, so aggregate these into it — criterion 1 is how many
of your questions had the answer in the retrieved chunks, and so on.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Where can I go to eat at Givens Mill? | pass | pass | pass |
| How expensive is it to stay at Thornby Wells? | pass | pass | pass |
| What is the tram schedule in Marchwood on the weekend? | fail | fail | fail |
| What are good places to visit with limited mobility? | pass | pass | pass |
| Where can I go for bird watching? | pass | pass | pass |

---

## The relevance gate on out-of-corpus questions

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.65. Refused 5 of 5.

Retrieval is deterministic and the gate is a comparison against a
fixed number, so these do not vary between runs — one pass over the
list is the whole measurement.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.808 | refused |
| How do I change the oil in a diesel engine? | 0.915 | refused |
| Who won the 1994 World Cup? | 1.014 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.860 | refused |
| How do I write a for loop in Rust? | 0.859 | refused |

---

## Real output

This is what the system actually produced. Paste the relevant parts
into your README underneath the table — the rubric asks for real
output as text, not a description of it.

### Where can I go to eat at Givens Mill? — run 1

- Best distance: 0.3546 (passed the gate)
- Sources retrieved: guide_eating.md, guide_givens_mill.md

```
Based on the provided documents, you can go to eat at Givens Mill at:

* **A tearoom** attached to the mill, which sells bread made from the flour ground twenty metres away.
* **One pub**, where food is served at lunchtimes and Thursday to Saturday evenings.

Sources:
- `guide_givens_mill.md`
- `guide_eating.md`
```

### Where can I go to eat at Givens Mill? — run 2

- Best distance: 0.3546 (passed the gate)
- Sources retrieved: guide_eating.md, guide_givens_mill.md

```
Based on the provided documents, you can go to eat at Givens Mill at:
- A tearoom attached to the mill (which sells bread made from the flour ground twenty metres away).
- One pub, where food is served lunchtimes and Thursday to Saturday evenings.

Sources:
- `guide_givens_mill.md`
- `guide_eating.md`
```

### Where can I go to eat at Givens Mill? — run 3

- Best distance: 0.3546 (passed the gate)
- Sources retrieved: guide_eating.md, guide_givens_mill.md

```
Based on the provided documents, you can go to eat at Givens Mill at:

* **A tearoom** attached to the mill, which sells bread made from the flour ground twenty metres away (Source: `guide_givens_mill.md` and `guide_eating.md`).
* **One pub**, where food is served at lunchtimes and on Thursday to Saturday evenings (Source: `guide_givens_mill.md`).
```

### How expensive is it to stay at Thornby Wells? — run 1

- Best distance: 0.3158 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_thornby_wells.md

```
Prices are moderate and stable year-round.

Source: guide_thornby_wells.md
```

### How expensive is it to stay at Thornby Wells? — run 2

- Best distance: 0.3158 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_thornby_wells.md

```
Based on the provided document (`guide_thornby_wells.md`), prices for staying at Thornby Wells are moderate and stable year-round.
```

### How expensive is it to stay at Thornby Wells? — run 3

- Best distance: 0.3158 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_thornby_wells.md

```
Prices for staying at Thornby Wells are moderate and stable year-round.

Source: guide_thornby_wells.md
```

### What is the tram schedule in Marchwood on the weekend? — run 1

- Best distance: 0.2075 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md, guide_thornby_wells.md

```
Based on the provided documents, the tram network in Marchwood runs every 15 minutes at weekends. 

Source: `guide_marchwood.md`
```

### What is the tram schedule in Marchwood on the weekend? — run 2

- Best distance: 0.2075 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md, guide_thornby_wells.md

```
Based on the provided document, the tram network in Marchwood runs every 15 minutes at weekends. 

Source: `guide_marchwood.md`
```

### What is the tram schedule in Marchwood on the weekend? — run 3

- Best distance: 0.2075 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md, guide_thornby_wells.md

```
Based on the provided documents, the tram network in Marchwood runs every 15 minutes at weekends. 

Source: `guide_marchwood.md`
```

### What are good places to visit with limited mobility? — run 1

- Best distance: 0.4979 (passed the gate)
- Sources retrieved: guide_accessibility.md

```
Based on the provided documents, the towns/places discussed in terms of accessibility for limited mobility are:

* **Thornby Wells**: Described as the easiest town in the region. It is flat, compact, everything is within three minutes of everything else, and the pump room and gardens are level throughout. (Source: guide_accessibility.md)
* **Givens Mill**: Described as one flat street along the river. The tearoom and riverside are accessible (though the mill tour involves stairs and the machinery floor is not accessible). (Source: guide_accessibility.md)
* **Brightwater**: Level along the river and through the centre, and the mill museum is step-free. (Source: guide_accessibility.md)
* **Marchwood**: Has a modern tram network with level boarding on all four lines (running every 8 minutes on weekdays), and both the city museum and covered market are step-free (though distances between districts are the main consideration). (Source: guide_accessibility.md)
```

### What are good places to visit with limited mobility? — run 2

- Best distance: 0.4979 (passed the gate)
- Sources retrieved: guide_accessibility.md

```
Based on the provided documents, the towns and places mentioned in the context of getting around with limited mobility are:

* **Thornby Wells**: Described as "the easiest town in the region," it is flat, compact, and everything is within three minutes of everything else; the pump room and gardens are level throughout (guide_accessibility.md).
* **Brightwater**: Level along the river and through the centre, and the mill museum is step-free (guide_accessibility.md).
* **Givens Mill**: One flat street along the river; the tearoom and riverside are accessible, though the mill tour involves stairs and the machinery floor is not accessible (guide_accessibility.md).
* **Marchwood**: Has a modern tram network with level boarding on all four lines (running every 8 minutes on weekdays), and the city museum and covered market are both step-free, with distances between districts being the main consideration (guide_accessibility.md).

Source: guide_accessibility.md
```

### What are good places to visit with limited mobility? — run 3

- Best distance: 0.4979 (passed the gate)
- Sources retrieved: guide_accessibility.md

```
Based on the provided documents, the towns/places mentioned in the guide for getting around the region with limited mobility are:

* **Thornby Wells**: Described as the easiest town in the region, it is flat, compact, and everything is within three minutes of everything else. The pump room and gardens are level throughout. (Source: `guide_accessibility.md`)
* **Givens Mill**: Described as one flat street along the river. The tearoom and riverside are accessible (though the mill tour involves stairs and the machinery floor is not accessible). (Source: `guide_accessibility.md`)
* **Brightwater**: Level along the river and through the centre. The mill museum is step-free, and the station is a 15-minute walk from campus on flat ground, or the shuttle meets the four busiest arrivals. (Source: `guide_accessibility.md`)
* **Marchwood**: Has a modern tram network with level boarding on all four lines (running every 8 minutes on weekdays), and the city museum and covered market are both step-free (though distances between districts are the main consideration). (Source: `guide_accessibility.md`)
```

### Where can I go for bird watching? — run 1

- Best distance: 0.6006 (passed the gate)
- Sources retrieved: guide_elder_ness.md, guide_halden_bay.md, guide_kestrelford.md, guide_marchwood.md

```
Based on the provided document, you can go to Elder Ness for bird watching. People come to Elder Ness for birds (with spring and autumn migration, specifically April to May and September to October, being the reasons to come), and it features a bird observatory. 

Source: `guide_elder_ness.md`
```

### Where can I go for bird watching? — run 2

- Best distance: 0.6006 (passed the gate)
- Sources retrieved: guide_elder_ness.md, guide_halden_bay.md, guide_kestrelford.md, guide_marchwood.md

```
Based on the provided documents, you can go to Elder Ness for bird watching (spring and autumn migration are the reasons to come, and birds are what most visitors come for).

Source: `guide_elder_ness.md`
```

### Where can I go for bird watching? — run 3

- Best distance: 0.6006 (passed the gate)
- Sources retrieved: guide_elder_ness.md, guide_halden_bay.md, guide_kestrelford.md, guide_marchwood.md

```
You can go to Elder Ness for bird watching (spring and autumn migration, April to May and September to October, which is what most visitors come for).

Source: `guide_elder_ness.md`
```
