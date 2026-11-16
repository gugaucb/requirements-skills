# SPEC-001: Order status for owners

**Status:** Draft | **Serves:** GOAL-001, CAP-001, CAP-002

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
