# ⚖️ ProofBountyJudge

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform: GenLayer](https://img.shields.io/badge/Platform-GenLayer-purple.svg)
![Language: Python](https://img.shields.io/badge/Language-Python-informational.svg)

ProofBountyJudge is a GenLayer intelligent contract for Web3 bounty verification. It lets creators define bounty criteria, contributors submit proof URLs, and authorized validators trigger an AI-assisted review flow that checks submitted work against the bounty requirements.

The contract uses GenLayer’s native web access and Equivalence Principle-based validation to compare AI evaluation results, reducing reliance on centralized manual review while recording an auditable on-chain status: `APPROVED`, `REJECTED`, or an error/flag state.

---

## 🌟 Key Features

* 🌐 **Native web proof review** — fetches and sanitizes submitted proof URLs (text/HTML fallback) for evaluation via `gl.get_webpage`.
* 🤖 **AI-assisted judging** — evaluates bounty descriptions, acceptance criteria, and submitted evidence using an LLM prompt.
* ⚖️ **Equivalence Principle validation** — cross-checks the AI decision via GenLayer’s Equivalence Principle helpers so validators agree on the approval outcome while allowing equivalent reasoning.
* 🛡️ **Strict Boolean & Resolution Guards** — enforces strict runtime boolean validation (`_ensure_bool`) to prevent truthy string vulnerabilities and blocks duplicate re-evaluations on non-pending submissions.
* ⚡ **Batch verification** — supports checking multiple submissions in a single transaction (`cross_check_batch`) up to a configurable batch limit (`MAX_BATCH_SIZE` = 20).
* 🔐 **Validator-gated execution** — restricts verification execution to an authorized validator registry managed by the contract owner.
* 🔄 **State Migration Support** — includes a dedicated migration endpoint (`migrate_submission_types`) to normalize legacy text-based status representations into native types across updates.
* 📑 **Audit-friendly views** — exposes lightweight status queries and detailed audit endpoints (`SCHEMA_VERSION` = 4):
  * Includes the `migrate_submission_types` endpoint to normalise legacy data.

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

    Creator->>Contract: create_bounty(desc, criteria, reward)
    Submitter->>Contract: submit_work(bounty_id, proof_url)
    Validator->>Contract: cross_check(submission_id)
    Contract->>Web: Fetch submitted proof URL (text/html)
    Web-->>Contract: Sanitized evidence text
    Contract->>AI: Evaluate evidence against criteria
    AI-->>Contract: Verdict + reasoning
    Contract->>Contract: Validate boolean type (_ensure_bool)
    Contract->>Contract: Store status (APPROVED/REJECTED) & emit audit data

# Create a new bounty with description, criteria, and reward
create_bounty(description: str, criteria: str, reward_amount: str) -> str

# Toggle bounty active status (Creator or Owner only)
set_bounty_active(bounty_id: str, is_active: bool) -> None

# Submit work evidence for an active bounty
submit_work(bounty_id: str, proof_url: str) -> str

# AI & consensus evaluation of a single submission (Validator only)
cross_check(submission_id: str) -> bool

# Batch evaluation of multiple submissions (Validator only)
cross_check_batch(submission_ids_json: str) -> str

# Migrate legacy 'true'/'false' strings to native booleans (Owner only)
migrate_submission_types() -> str

# Add a validator address to the registry (Owner only)
add_validator(address: str) -> None

# Remove a validator address from the registry (Owner only)
remove_validator(address: str) -> None
