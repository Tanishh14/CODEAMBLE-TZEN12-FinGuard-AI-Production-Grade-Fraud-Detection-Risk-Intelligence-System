# FinGuard-AI-Production-Grade-Fraud-Detection-Risk-Intelligence-System
AI-powered fraud detection and risk intelligence platform combining machine learning, graph analytics, behavioral signals, and explainable AI for real-time financial threat detection.

# FinGuard AI

**Adaptive, explainable, real-time fraud detection for financial systems.**

FinGuard AI combines graph neural networks, anomaly detection, and an evidence-bound LLM explainability layer to catch coordinated fraud rings — not just individually suspicious transactions — while keeping every decision auditable and regulator-replayable.


## Table of Contents

- [Problem](#problem)
- [Architecture](#architecture)
- [Key Design Principles](#key-design-principles)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [How a Transaction Flows Through the System](#how-a-transaction-flows-through-the-system)
- [Recognition](#recognition)
- [Roadmap](#roadmap)
- [License](#license)

---

## Problem

Traditional fraud systems fail in three specific ways:

- **Rule-based, easily bypassed** — static thresholds don't adapt to new fraud patterns
- **Blind to coordinated fraud** — can't detect multi-account, multi-device fraud rings, only single-transaction anomalies
- **Not explainable** — a "risk score" with no reasoning behind it doesn't survive regulatory review

FinGuard AI is built around solving all three at once, without trading real-time performance for it.

---

## Architecture

```
Transaction Input
      │
      ▼
PII Isolation Boundary  ──  raw data sealed, never leaves this zone
      │
      ▼
Kafka Streaming Layer  ──  durable, replayable event log
      │
      ▼
Flink Feature Engine  ──  velocity, device-switching, time-window features
      │
      ▼
AI Core (parallel)
   ├── GNN            ──  fraud rings via relationship graph
   └── Anomaly Models  ──  autoencoder + isolation forest
      │
      ▼
Calibrated Fraud Probability  ──  Platt scaling / isotonic regression
      │
      ▼
8-Check Validation Gate  ──  schema · range · confidence · GNN-vs-anomaly ·
      │                       PII leak scan · score stability · velocity · rule alignment
      ▼
Decision Engine  ──  Approved  │  Escalated to analyst
      │
      ▼
Evidence Pack Builder  ──  strips to anonymized, aggregated signals
      │
      ▼
LLM Explainability Layer  ──  evidence-bound, sentence-level validated
      │
      ▼
Immutable Audit Log (Postgres)  ──  replayable by Case ID
```

---

## Key Design Principles

**PII isolation is architectural, not configurable.** The LLM explanation layer has no code path or credentials that reach raw PII (user ID, account, device ID, IP). It only ever receives the output of the Evidence Pack Builder, whose schema is fixed and PII-free by construction.

**The LLM explains decisions — it never makes them.** Fraud decisions come from the deterministic decision engine + validation gate. The LLM's only job is producing a human-readable, evidence-bound explanation of a decision that has already been made, with sentence-level validation ensuring every claim traces back to the evidence pack.

**Every decision is replayable.** Given a Case ID, the system can reload the original evidence, reload the prompt, re-run the model, and compare outputs — the basis for regulator-style audit replay.

**Two models, not one, because fraud isn't one shape.** The GNN catches relational fraud (shared devices, IP overlap, circular money flow between accounts). The anomaly models (autoencoder + isolation forest) catch individual-transaction outliers a graph model can't see. The validation gate explicitly checks their agreement.

---

## Tech Stack

| Layer                   | Technology                         | Why                                                                           |
|                         |                                    |                                                                               |
| Backend API             | FastAPI                            | Async-native for I/O-bound orchestration; Pydantic validation at the boundary |
| ML / Graph              | PyTorch, PyTorch Geometric         | GNN for relational fraud-ring detection                                       |
| Streaming               | Kafka + Flink                      | Durable, replayable event log; real-time windowed feature computation         |
| Explainability          | LangChain + LLM                    | Evidence-bound natural-language decision explanations                         |
| Cache                   | Redis                              | Sub-ms velocity counters and hot-path lookups                                 |
| Database                | PostgreSQL                         | ACID-compliant, append-only audit log with relational integrity               |
| Containerization        | Docker / docker-compose            | Reproducible local orchestration across services                              |

---

## Repository Structure

```
.
├── backend/     # FastAPI service — transaction explanation & NLP query endpoints
├── frontend/    # Dashboard UI — GNN detection, anomaly detection, explainability, live transactions
├── Redis/       # Redis configuration and caching layer
├── data/        # Project data assets
├── docker-compose.yml
├── STARTUP_GUIDE.md
└── LICENSE
```

---

## Getting Started

Full setup instructions are in [`STARTUP_GUIDE.md`](./STARTUP_GUIDE.md).


## How a Transaction Flows Through the System

1. A user submits a transaction; the event enters the ingestion layer immediately — no polling delay.
2. Raw PII stays sealed inside the decision layer; Kafka streams the event, Flink computes real-time behavioral features.
3. The GNN and anomaly models score the transaction in parallel — relational signals and individual-transaction signals respectively.
4. Both scores are calibrated into a single, human-interpretable fraud probability.
5. The 8-check validation gate must pass before any decision is acted on; any failure escalates to a human analyst.
6. The decision engine approves or escalates the transaction.
7. The Evidence Pack Builder strips the decision to anonymized signals; the LLM generates a bounded explanation.
8. Everything — evidence, model version, prompt hash, decision — is written to an immutable, replayable audit log.

---


## Roadmap

- [ ] Automated test suite + CI pipeline
- [ ] Network-level enforcement of the PII isolation boundary (beyond schema-level enforcement)
- [ ] Production deployment with load-tested latency benchmarks
- [ ] Differential privacy layer on top of the federated learning simulation

---

## License

MIT — see [`LICENSE`](./LICENSE).
