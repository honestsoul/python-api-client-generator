# Anatomy of an AI Agent  
*Comprehensive Technical Blueprint*

## 1. Overview
An AI agent is a system that **perceives → understands → plans → grounds → acts → observes → learns**, supported by tools, memory, guardrails, identity, and telemetry.
This document captures a production-grade architecture for designing and scaling enterprise AI agents.

## 2. Core Agent Loop (Diagram Added Separately)
> Note: Mermaid diagram should be added using Confluence's **/Mermaid** macro.

## 3. Agent Layer Stack
| Layer | Responsibilities | Examples |
|---|---|---|
| **Interface** | Chat, UI, API endpoints, events, multimodal IO | Slack bot, Web chat, voice IVR |
| **Identity & Persona** | Role, goals, constraints, system prompt | “Compliance Agent v2”, read-only |
| **Intent & Context Builder** | Parse task, slot filling, assemble state | Detect refund intent, attach context |
| **Planner / Orchestrator** | Build task plan, step graph, retries, fallback | Reflex, ReAct, Plan-Execute |
| **Tools & Skills** | Atomic capabilities with schema & auth | Search, SQL/Graph queries, RPA, email |
| **Knowledge Access** | RAG, structured DBs, APIs | Pinecone/Qdrant + Postgres + REST |
| **Memory** | Short-term, episodic, long-term, semantic | Session cache + KV store + embeddings |
| **Policies & Guardrails** | Safety, PII, auth scopes, approvals | Thresholds, allow/deny lists |
| **Execution Runtime** | Sandbox, timeouts, idempotency, rollback | Docker sandbox, SAGA |
| **Telemetry & Ops** | Logs, traces, cost/latency metrics | OpenTelemetry, dashboards |
| **Learning & Adaptation** | Evaluators, reward signals, prompt updates | Offline eval, prompt evolution |

## 4. Planner Patterns
### 1. Reflex (Single-Shot)
Used for simple, low-latency tasks.
### 2. ReAct (Reason + Act)
Interleaves reasoning and tool usage.
### 3. Plan & Execute
Planner generates a multi-step task graph; executor runs it with retries.
### 4. Multi-Agent Systems
Specialized agents: planner, solver, checker, router, memory.
### 5. Hierarchical Agents
Supervisor delegates to workers; evaluator validates output.

## 5. Agent Message & Tool Contracts
### Agent Message (JSON)
```json
{
  "id": "msg-uuid",
  "role": "user|agent|tool|evaluator",
  "intent": "summarize|book_meeting|refund",
  "context": {"session_id": "s-123", "user_id": "u-42"},
  "content": [{"type": "text", "text": "..."}],
  "plan": [{"step": "retrieve", "why": "verify order"}],
  "tool_call": {"name": "get_order", "args": {"order_id": "A123"}},
  "observations": [],
  "policy": {"risk": "medium"},
  "metrics": {"latency_ms": 312, "cost_usd": 0.002}
}
```

### Tool Manifest (YAML)
```yaml
name: get_order
in:
  order_id: {type: string, required: true}
out:
  status: {type: string}
  items: {type: array}
auth: oauth:orders.read
sla: {p95_ms: 400}
risk: low
```

## 6. Memory Architecture
### Short-Term Memory
- Rolling window of conversation  
- Working memory for current loop  
- Summaries → episodic memory  
### Episodic Memory
- Session-level summaries  
- Captures what happened, decisions made  
### Long-Term Memory
- User/org facts, preferences, historical data  
- Stored in KV + semantic vector store  
### Procedural Memory
- Routines, workflows, learned operations  
### Memory Hygiene
- Consolidation jobs  
- TTL-based cleanup  
- Hybrid retrieval (BM25 + vector)

## 7. Guardrails & Approvals
| Guardrail Type | Description | Example |
|---|---|---|
| **Monetary** | Threshold-driven approvals | Refund > $500 requires approval |
| **PII Controls** | Redaction, minimization, encryption | Mask SSN or email |
| **Auth Scopes** | Per-tool least-privilege access | OAuth scopes per tool |
| **Safety Filters** | Toxicity, hallucination checks | Require citations before acting |
| **Rate Limits** | Limit high-volume usage | 60 req/min per org |
| **Off-Hours** | Additional rules after business hours | After 6pm → approval needed |

## 8. Observability & KPIs
### Reliability
- Success rate  
- p95 latency  
- Retry & tool error rate  
### Quality
- Task completion rate  
- Evaluator score  
- Factual accuracy  
### Cost
- Tokens per task  
- $ per successful task  
- Cache hit-rate  
### Safety
- Policy violations prevented  
- Approval ratio  
### Drift
- Retrieval freshness  
- Prompt/version impact  

## 9. Failure Modes & Mitigations
| Failure | Symptom | Mitigation |
|---|---|---|
| **Hallucination** | Confident but false answers | Retrieval-first prompting, evaluator agent |
| **Tool Timeout** | Hanging or slow operations | Circuit breaker, fallback tool |
| **Planning Loop** | Repeating actions | Step cap, loop detection |
| **Privilege Creep** | Excessive tool access | Scoped auth, JIT tokens |
| **Context Overflow** | Lost instructions or data | Summaries, structured state |

## 10. Deployment Topologies
### Embedded Agent
- Integrated inside an app  
- Minimal latency  
### Agent Gateway
- Routing, policy enforcement, agent registry  
### Agent Mesh
- Micro-agents cooperating via contracts  
- High resilience  
### Batch/Offline Agents
- Summaries  
- Audits  
- Backfills  

## 11. Execution Pseudocode
```python
def agent_step(msg, state):
    intent = infer_intent(msg, state)
    ctx = build_context(state)
    plan = plan_steps(intent, ctx)

    for step in plan:
        enforce_policies(step, ctx)

        if step.requires_retrieval:
            ctx = retrieve(ctx, step)

        if step.tool:
            out = call_tool(step.tool, step.args)
            log_observation(step, out)
            if needs_validation(step):
                validate(out, ctx)

        if step.halt_for_approval:
            return request_approval(step, ctx)

    answer = compose_answer(ctx)
    learn(state, ctx, answer)
    return answer
```

## 12. Rollout Checklist
- [ ] Define tool contracts + auth scopes  
- [ ] Context policy implemented  
- [ ] Retrieval policy defined  
- [ ] Guardrails + approval rules active  
- [ ] Prompt registry + versioning  
- [ ] Tracing/logging/cost dashboards  
- [ ] Red-team testing suite  
- [ ] Memory retention & compliance policies  
- [ ] Feature-flag rollout  
- [ ] SLOs + monitoring live  

## 13. Appendix
### Example Approval Policy (JSON)
```json
{
  "name": "refund-policy-v3",
  "rules": [
    {"if": "amount > 500", "action": "require_approval"},
    {"if": "after_hours == true", "action": "require_approval"},
    {"if": "user_risk == 'high'", "action": "deny"}
  ]
}
```

### Retrieval-First Prompt Template
```
Before answering:
1. Retrieve relevant evidence.
2. Cite the top 2 sources.
3. If confidence is low, ask for clarification.
```
