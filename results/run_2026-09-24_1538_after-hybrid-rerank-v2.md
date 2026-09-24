# Run log — after-hybrid-rerank-v2

- Produced by: `run_eval.py::main`
- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`
- Corpus: `city_guides` (index variant `default`)
- top-k: 7 · relevance cutoff: 0.65
- Runs per question: 3, caching off
- When: 2026-09-24 15:38

This table is one row per QUESTION. The run log your README asks for is
one row per CRITERION, so aggregate these into it — criterion 1 is how many
of your questions had the answer in the retrieved chunks, and so on.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Where can I go to eat at Givens Mill? | pass | pass | pass |
| How expensive is it to stay at Thornby Wells? | pass | pass | pass |
| What is the tram schedule in Marchwood on the weekend? | pass | pass | pass |
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
Based on the provided documents, you can go to:

* A tearoom attached to the mill (which sells bread made from the flour ground twenty metres away) (*guide_givens_mill.md* and *guide_eating.md*).
* One pub, where food is served at lunchtimes and Thursday to Saturday evenings (*guide_givens_mill.md*).
```

### Where can I go to eat at Givens Mill? — run 2

- Best distance: 0.3546 (passed the gate)
- Sources retrieved: guide_eating.md, guide_givens_mill.md

```
Based on the provided documents, you can go to eat at Givens Mill at:

* **A tearoom** attached to the mill (which sells bread made from the flour ground twenty metres away). *(Source: guide_givens_mill.md and guide_eating.md)*
* **One pub** (where food is served lunchtimes and Thursday to Saturday evenings). *(Source: guide_givens_mill.md)*
```

### Where can I go to eat at Givens Mill? — run 3

- Best distance: 0.3546 (passed the gate)
- Sources retrieved: guide_eating.md, guide_givens_mill.md

```
Based on the provided documents, you can go to:

* A tearoom attached to the mill (which sells bread made from the flour ground twenty metres away). *(Source: guide_givens_mill.md and guide_eating.md)*
* One pub, where food is served at lunchtimes and on Thursday to Saturday evenings. *(Source: guide_givens_mill.md)*
```

### How expensive is it to stay at Thornby Wells? — run 1

- Best distance: 0.3158 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_thornby_wells.md

```
Prices for staying in Thornby Wells (which includes two large hotels and several small guesthouses) are moderate and stable year-round (guide_thornby_wells.md).
```

### How expensive is it to stay at Thornby Wells? — run 2

- Best distance: 0.3158 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_thornby_wells.md

```
Prices for staying in Thornby Wells are moderate and stable year-round (guide_thornby_wells.md).
```

### How expensive is it to stay at Thornby Wells? — run 3

- Best distance: 0.3158 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_thornby_wells.md

```
Prices for staying at Thornby Wells are moderate and stable year-round (guide_thornby_wells.md).
```

### What is the tram schedule in Marchwood on the weekend? — run 1

- Best distance: 0.2075 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md, guide_thornby_wells.md

```
Based on the provided documents, the tram network in Marchwood runs every 15 minutes at weekends, until midnight (*guide_marchwood.md*).
```

### What is the tram schedule in Marchwood on the weekend? — run 2

- Best distance: 0.2075 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md, guide_thornby_wells.md

```
Based on the provided documents, the tram network in Marchwood runs every 15 minutes at weekends, until midnight (*guide_marchwood.md*).
```

### What is the tram schedule in Marchwood on the weekend? — run 3

- Best distance: 0.2075 (passed the gate)
- Sources retrieved: guide_accessibility.md, guide_eating.md, guide_marchwood.md, guide_thornby_wells.md

```
Based on the provided document, the tram network in Marchwood runs every 15 minutes at weekends, until midnight (guide_marchwood.md).
```

### What are good places to visit with limited mobility? — run 1

- Best distance: 0.4979 (passed the gate)
- Sources retrieved: guide_accessibility.md

```
Based on the provided documents, the places described regarding limited mobility are:

* **Thornby Wells:** Described as the easiest town in the region because it is flat, compact, and everything is within three minutes of everything else; the pump room and gardens are level throughout. (Source: `guide_accessibility.md`)
* **Brightwater:** Described as level along the river and through the centre, with a step-free mill museum. (Source: `guide_accessibility.md`)
* **Marchwood:** Features a modern tram network with level boarding on all four lines (running every 8 minutes on weekdays), and both the city museum and covered market are step-free, though the distances between districts are the main consideration. (Source: `guide_accessibility.md`)
* **Givens Mill:** Described as one flat street along the river, where the tearoom and riverside are accessible (though the mill tour involves stairs and the machinery floor is not accessible). (Source: `guide_accessibility.md`)
```

### What are good places to visit with limited mobility? — run 2

- Best distance: 0.4979 (passed the gate)
- Sources retrieved: guide_accessibility.md

```
Based on the provided documents, the towns and locations assessed for limited mobility include:

* **Thornby Wells**: Described as the easiest town in the region, it is flat, compact, and everything is within three minutes of everything else. The pump room and gardens are level throughout. *(guide_accessibility.md)*
* **Brightwater**: It is level along the river and through the centre, and the mill museum is step-free. *(guide_accessibility.md)*
* **Givens Mill**: Described as one flat street along the river, with an accessible tearoom and riverside (though the mill tour involves stairs and the machinery floor is not accessible). *(guide_accessibility.md)*
* **Marchwood**: Has a modern tram network with level boarding on all four lines, and both the city museum and covered market are step-free (though distances between districts are the main consideration). *(guide_accessibility.md)*

*(Source: guide_accessibility.md)*
```

### What are good places to visit with limited mobility? — run 3

- Best distance: 0.4979 (passed the gate)
- Sources retrieved: guide_accessibility.md

```
Based on the provided documents, the towns and locations assessed for limited mobility include:

* **Thornby Wells**, which is described as the easiest town in the region because it is flat, compact, everything is within three minutes of everything else, and the pump room and gardens are level throughout (guide_accessibility.md).
* **Givens Mill**, which is one flat street along the river, with an accessible tearoom and riverside, though the mill tour involves stairs and the machinery floor is not accessible (guide_accessibility.md).
* **Brightwater**, which is level along the river and through the centre, and has a step-free mill museum (guide_accessibility.md).
* **Marchwood**, which has a modern tram network with level boarding on all four lines (running every 8 minutes on weekdays), and a step-free city museum and covered market, though distances between districts are the main consideration (guide_accessibility.md).

Source: guide_accessibility.md
```

### Where can I go for bird watching? — run 1

- Best distance: 0.6006 (passed the gate)
- Sources retrieved: guide_elder_ness.md, guide_halden_bay.md, guide_kestrelford.md, guide_marchwood.md

```
Based on the provided document, you can go to Elder Ness for bird watching during the spring and autumn migration, specifically from April to May and September to October (guide_elder_ness.md).
```

### Where can I go for bird watching? — run 2

- Best distance: 0.6006 (passed the gate)
- Sources retrieved: guide_elder_ness.md, guide_halden_bay.md, guide_kestrelford.md, guide_marchwood.md

```
Based on the provided document, you can go to Elder Ness for spring and autumn migration, as birds are the reason most visitors come (guide_elder_ness.md).
```

### Where can I go for bird watching? — run 3

- Best distance: 0.6006 (passed the gate)
- Sources retrieved: guide_elder_ness.md, guide_halden_bay.md, guide_kestrelford.md, guide_marchwood.md

```
Based on the provided document, you can go to Elder Ness for spring and autumn migration, which is the reason to come for birds (which is what most visitors come for, specifically during April to May and September to October). 

Source: `guide_elder_ness.md`
```
