---
id: SPEC-001
status: approved
version: 1.0.0
---
# SPEC-001: Order status for owners

**Status:** Approved by Ana (PO), 2026-05-20 | **Serves:** GOAL-001, CAP-001, CAP-002

## Problem
Customers phone support to ask where their order is.

## Outcome
An owner sees the current status and the history of each of their orders.

## Candidate stories
1. As an owner, I want to see the current status of my order, so that I do not need to contact support.
2. As an owner, I want to see the status history of my order, so that I understand how it progressed.

## Business rules
Statuses are those in DEC-001 and DEC-003. Owners see only their own orders.

## Out of scope
Payment processing (DEC-002, Pending).

## Open questions
DEC-004 blocks the success measure of GOAL-001.

## Strategy

Add the status "On hold" (DEC-003) to the current-status story, then re-check the history story, which shares the term.

## Plan of changes

| ID | Target | Kind | Change | Reason | Depends on | Status |
| --- | --- | --- | --- | --- | --- | --- |
| PLN-001 | US-001 | modify-story | Add FR, AC and TC for "On hold" | DEC-003 | | Done (CHG-001) |
| PLN-002 | US-002 | modify-story | Include "On hold" in the history rules | DEC-003 | PLN-001 | Pending |
| PLN-003 | GLOSSARY | modify-glossary | Add "On hold" to the Order status definition | DEC-003 | | Done (CHG-001) |
