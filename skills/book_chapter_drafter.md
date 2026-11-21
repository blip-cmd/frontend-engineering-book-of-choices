# Skill: Book Chapter Drafter

## Mission
Draft clear, engaging, and high-density chapters for *Frontend Engineering as a Book of Choices*.

## Style and Tone Guidelines
1. **Engaging and Concise:** Avoid fluff, conversational filler, and robotic transitions. Every paragraph must advance architectural clarity.
2. **Punctuation Standards:** Zero em dashes. Never use unicode em dashes or double hyphens as dashes. Use colons, commas, parentheses, semicolons, or distinct sentences.
3. **High Density & Readability:** Structure content with tables, annotated code snippets, callouts, and explicit decision trees. A reader should be able to skim once and grasp the decision boundaries, or read thoroughly to study deep mechanics.
4. **Reference Anchors:** Every chapter must link back to foundational research, RFCs, and landmark literature stored in `library/`.

## Chapter Blueprint Structure
Each chapter in `book/` must adhere to this uniform layout:

1. **The Core Dilemma:**
   Define the engineering conflict (e.g., "Where does code run?" or "How is UI kept in sync with state?").

2. **The Decision Landscape:**
   Outline the spectrum of available choices, from industry standard to emerging research.

3. **Comparative Analysis Matrix:**
   A structured markdown table evaluating all choices against identical constraint metrics.

4. **Deep Dive on Paradigms:**
   Exploration of each paradigm:
   * The Mental Model.
   * How it Works Under the Hood.
   * The Hidden Costs.
   * Enabling Libraries and Tooling.

5. **Decision Playbook & Rule of Thumb:**
   A quick diagnostic guide:
   * If [Constraint Set A] -> Choose [Paradigm X].
   * If [Constraint Set B] -> Choose [Paradigm Y].

6. **Further Reading & Research Citations:**
   Links to authoritative specifications, papers, and books in the `library/` corpus.
