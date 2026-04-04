# Cursor Prompt Pack — hexstrike_lab

This document provides phase-based prompts for building an AI-assisted security testing framework in an **authorized internal lab** environment.

---

## Phase Overview

| Phase | Lab | Focus |
|------|-----|------|
| Phase 0 | Lab00 | Understand repo |
| Phase 1 | Lab01 | Adapter abstraction |
| Phase 2 | Lab02 | Orchestrator |
| Phase 3 | Lab03 | Pipeline |
| Phase 4 | Lab04 | RFP → scanning |
| Phase 5 | Lab05 | RFP → pentest |

---

## General Rules

- Use only authorized internal lab targets
- Avoid real production systems
- Focus on design, automation, and structured output
- Prefer modular, reusable architecture

---

## Phase 0 — Repo Understanding

### Prompt
Explain this repository as a modular security testing framework.

Focus on:
- folder structure
- execution flow
- role of profiles
- difference between run / assess / pipeline

---

## Phase 1 — Adapter

### Prompt
Create a ToolAdapter module.

Requirements:
- validate target input
- run tool via subprocess
- capture output
- return normalized JSON

---

## Phase 2 — Orchestrator

### Prompt
Design an Orchestrator.

Requirements:
- run discovery first
- decide next steps
- support profiles
- merge results

---

## Phase 3 — Pipeline

### Prompt
Create an end-to-end pipeline.

Steps:
- config
- orchestrator
- output collection
- JSON normalization
- markdown report

---

## Phase 4 — RFP Scanning

### Prompt
Translate vulnerability scanning requirements into a pipeline.

Include:
- discovery
- conditional web checks
- structured output

---

## Phase 5 — Pentest System

### Prompt
Design a multi-step testing workflow.

Requirements:
- decision-based flow
- structured evidence
- modular design

---

## Advanced — System Thinking

### Prompt
Refactor into a reusable execution framework.

Explain:
- architecture
- module responsibilities
- extension points
