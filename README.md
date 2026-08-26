# ⚖️ ProofBountyJudge

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-GenLayer-8A2BE2.svg)](https://genlayer.com)
[![Language](https://img.shields.io/badge/Language-Python-3776AB.svg?logo=python&logoColor=white)](https://python.org)

ProofBountyJudge is a GenLayer intelligent contract for Web3 bounty verification. It lets creators define bounty criteria, contributors submit proof URLs, and authorized validators trigger an AI-assisted review flow that checks submitted work against the bounty requirements.

The contract uses GenLayer’s native web access and Equivalence Principle-based validation to compare AI evaluation results, reducing reliance on centralized manual review while recording an auditable on-chain status: `APPROVED`, `REJECTED`, or an error/flag state.

---

## 🌟 Key Features

- 🌐 **Native web proof review** — fetches and sanitizes submitted proof URLs (text/HTML) for evaluation via `gl.get_webpage`.
- 🤖 **AI-assisted judging** — evaluates bounty descriptions, acceptance criteria, and submitted evidence using an LLM prompt.
- ⚖️ **Equivalence Principle validation** — cross-checks the AI decision via GenLayer’s Equivalence Principle helpers so validators agree on the approval outcome while allowing equivalent reasoning.
- ⚡ **Batch verification** — supports checking multiple submissions in a single transaction (`cross_check_batch`) up to a configurable batch limit.
- 🔐 **Validator-gated execution** — restricts verification execution to an authorized validator registry managed by the contract owner.
- 🧾 **Audit-friendly views** — exposes lightweight status queries and detailed audit endpoints for frontend integration.

---

## 🔄 End-to-End Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Creator as Bounty Creator
    actor Submitter as Contributor
    actor Validator as Authorized Validator
    participant Contract as ProofBountyJudge
    participant Web as Web Access
    participant AI as AI Evaluation

    Creator->>Contract: create_bounty(description, criteria, reward)
    Submitter->>Contract: submit_work(bounty_id, proof_url)
    Validator->>Contract: cross_check(submission_id)
    Contract->>Web: Fetch submitted proof URL
    Web-->>Contract: Sanitized evidence text
    Contract->>AI: Evaluate evidence against criteria
    AI-->>Contract: Verdict + reasoning
    Contract->>Contract: Store status and audit result
