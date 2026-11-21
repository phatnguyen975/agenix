---
name: agx-guide
description: Explain how to use Agenix workflows, choose a step, resume work or troubleshoot plugin access. Use when someone asks for Agenix guidance.
metadata:
  author: phatnguyen975
  version: "1.0"
---

# Agenix Guide

## Purpose and Scope

Help people and agents understand Agenix and choose an appropriate human-invoked workflow step. This guide is available before project setup and during an open step. It is read-only: do not change files, project state, checkpoints, tracker records, session markers or the active workflow step. Never invoke another workflow on the user's behalf.

## Route the Question

- For an overview, first use or workflow navigation, read [Workflow Guide](references/workflow.md). For a particular phase or step, read its linked skill entry and the relevant procedure only when detail is needed.
- For host, plugin or browser tool access, read [Troubleshooting](references/troubleshooting.md). If the guide is unavailable because the plugin is inactive, point the person to the installation and recovery guidance in the distribution README.
- For approval, step closure, amendments or handoff, consult [Workflow Control](../../references/workflow-control.md). For tracker, status, exception or delivery questions, load the relevant [work-item rules](../../references/work-items-and-evidence.md), [publication rules](../../references/git-publication.md) or selected tracker guide linked from the workflow guide. Read only what the answer needs.

## Answer

Answer in the user's language, or the approved conversation language when known and applicable. For a broad request, give a brief purpose, the workflow map, how to invoke and close a step, and the main human decisions; then show how to request details. For a focused request, lead with the direct answer and use a small table or ordered steps when useful. Explain the relevant inputs, outputs, authority and next action without reproducing entire instructions.

For a question about the current project, use only available read-only evidence. Distinguish stated state from verified completion and identify missing or stale evidence. Suggest a next invocation only when its prerequisites and item ID are known; otherwise say what must be checked. Present commands as instructions for the human or examples, not as actions already performed. Do not fetch, change configuration, invoke helpers with side effects or inspect private credentials. Do not claim a plugin, server, browser or workflow has been verified merely because its configuration exists.

Answer the question and stop. Do not emit workflow `BEGIN`, `DURING` or `END` markers, close or advance an open step, request an artifact approval, or perform publication, merge or exposure.
