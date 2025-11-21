---
title: Codex Agents for CeibaTory
kind: meta
source: documentation/Agents.md
---

# Codex Configuration for the CeibaTory Repository

This file defines how Codex must behave when editing this repository.

CeibaTory is a writing tool that transforms **text → graph → tree → Obsidian canvas → draft**.  
The global architecture (graph → tree → layout → canvas) is **already designed** and must not be changed unless the user explicitly requests it.

Codex will often be run on **separate git branches** for different experiments, so it must keep changes **local and minimal** to avoid merge conflicts.

---

## 1. Global Principles (apply to every task)

1. **Preserve the Architecture**

   - Do **not** redesign the overall pipeline (`Graph → Tree → Layout → Canvas → Draft`) unless the user explicitly asks for an architectural change.
   - Prefer local changes inside the relevant function/module over moving or renaming files.

2. **Minimal, Targeted Edits**

   - Change only what is needed to fulfill the current request.
   - Avoid:
     - large-scale reformatting of whole files,
     - renaming functions or files,
     - reorganizing folders,
     unless the user clearly requests it.
   - This is essential to **minimize git merge conflicts** between branches.

3. **Respect Existing Style & Structure**

   - Keep the current function layout and naming scheme unless asked otherwise.
   - Prefer small, single-responsibility helpers and explicit parameters, following the existing code’s style.
   - If a refactor seems “nice” but wasn’t requested, describe it in comments or notes instead of implementing it.

4. **Ask When in Doubt**

   - If the task description is ambiguous, contradictory, or would require a large structural change:
     - **stop** and ask the user one or two precise clarification questions,
     - do **not** guess the intent or perform broad changes.

5. **Do Not Change Behavior Silently**

   - If a change would alter numerical, structural, or layout behavior (e.g., how trees are built, how coordinates are computed), you must:
     - either avoid it, or
     - clearly state what will change and why, and implement it only if the user explicitly approves.

6. **Keep the Graph/Tree/Canvas Mapping Intact**

   - Functions that map between:
     - graphs ↔ trees,
     - trees ↔ branches/heart/leaves,
     - branches ↔ canvas coordinates,
     must preserve their input/output contracts and data formats, unless the user authorizes changes.

---

## 2. Task Types (lightweight “modes”)

Codex can treat tasks as one or more of these modes. Do not announce modes to the user; just follow the rules.

1. **Documentation Mode**

   - When the user asks to write or improve docs:
     - Explain what the function/module does in the CeibaTory pipeline (graph, tree, layout, canvas, draft).
     - Keep documentation consistent with existing behavior and naming.
     - Do **not** change code behavior in this mode unless explicitly requested.

2. **Feature/Refactor Mode**

   - When the user asks to add a feature or adjust behavior:
     - Work in the smallest possible scope (only the functions/files mentioned or obviously required).
     - Prefer adding helpers over rewriting existing logic.
     - Keep function names, file names, and folder structure unchanged unless the user explicitly asks to reorganize them.

3. **Planning/Proposal Mode**

   - When the user asks for ideas, roadmaps, or big changes:
     - Propose plans in text or comments first.
     - Clearly separate “plan” from “implemented code”.
     - Do not implement large refactors unless explicitly approved.

---

## 3. Rules to Minimize Merge Conflicts

When Codex edits this repo, it must:

1. **Avoid Global Reformatting**

   - Do not reindent or reformat entire files just for style.
   - Only touch lines that are required for the current task.

2. **Avoid Unnecessary Renames**

   - Do not rename functions, variables, or files unless the user explicitly requests a rename or reorganization.

3. **Keep One Logical Change per Branch**

   - Implement only the requested change (or a closely related small set of changes) in a given branch.
   - If additional changes seem useful but are not clearly requested, describe them instead of implementing them.

4. **Be Explicit About Non-trivial Changes**

   - If implementing a feature requires modifying several related functions, explain the impact in comments or in the response so the user understands what changed.

---

## 4. When the Prompt Is Not Clear

If any of the following is true:

- the requested behavior conflicts with existing structure,
- the instructions are vague (“improve everything”, “clean up a bit”),
- or the change would affect many files or core algorithms,

Codex must:

1. Pause implementation.
2. Ask **one to three concise clarification questions** to the user.
3. Only proceed after the ambiguity is resolved.

Codex must never infer a large refactor from a short or ambiguous request.

---

## 5. Philosophy

The goal of this configuration is to keep CeibaTory:

- **Stable** – the graph/tree/canvas architecture remains intact;
- **Predictable** – small, targeted changes do exactly what was asked;
- **Merge-friendly** – different branches can be merged with minimal conflicts;
- **Collaborative** – Codex asks the user instead of guessing when tasks are unclear.

Codex should act as a careful collaborator that extends CeibaTory step by step, not as an automatic rewriter of the entire project.

