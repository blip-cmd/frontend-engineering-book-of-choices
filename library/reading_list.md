# Further Reading

> Published books that shaped the thinking in this volume. This project does not reproduce or summarise them; each entry says in a few lines why it is worth your time. Please buy or borrow the originals.

---

## Networking and Performance

### *High Performance Browser Networking*
* **Author:** Ilya Grigorik (O'Reilly, 2013)
* **Read it:** [hpbn.co](https://hpbn.co/) (the author publishes the full text free online)
* **Why it matters here:** The clearest explanation of why latency, not bandwidth, limits most web pages: TCP and TLS handshakes, congestion windows, and what HTTP/2 and HTTP/3 change. It is the background for the "first 14 KB" budget in [Chapter 7](../book/07_delivery_and_build_pipeline.md) and the transport discussion in [Chapter 4](../book/04_the_networking_contract.md).

### *Web Performance in Action*
* **Author:** Jeremy L. Wagner (Manning, 2016)
* **Publisher page:** [manning.com/books/web-performance-in-action](https://www.manning.com/books/web-performance-in-action)
* **Why it matters here:** A practical, hands-on walk through the critical rendering path, image and font optimisation, and resource hints. Some tooling has moved on since 2016, but the reasoning about what blocks rendering still holds.

---

## Data and State

### *Designing Data-Intensive Applications* (2nd edition)
* **Authors:** Martin Kleppmann and Chris Riccomini (O'Reilly, 2026)
* **Publisher page:** [O'Reilly](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/) · [Author's announcement](https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html)
* **Why it matters here:** It is a backend book, but its chapters on replication, consistency and conflict resolution explain the problems frontend developers meet when a browser tab holds its own copy of server data. Read it alongside [Chapter 3](../book/03_state_and_cache_topologies.md) and [Chapter 8](../book/08_local_first_and_offline_resilience.md).

---

## Design Systems

### *Frontend Architecture for Design Systems*
* **Author:** Micah Godbolt (O'Reilly, 2016)
* **Publisher page:** [O'Reilly](https://www.oreilly.com/library/view/frontend-architecture-for/9781491926772/)
* **Why it matters here:** Frames frontend architecture as four pillars (code, process, testing, documentation), with case studies from Red Hat's design system. It predates design tokens as a standard, but its argument that a design system is a process, not just a component library, underpins [Chapter 5](../book/05_design_engineering_and_ui.md).

---

## Suggest a Book

Know a book that belongs here? [Open an issue](https://github.com/blip-cmd/frontend-engineering-book-of-choices/issues/new) with the title, author, and two or three sentences on which chapter it supports and why.
