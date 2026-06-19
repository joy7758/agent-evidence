# Five-Minute Demo Storyboard

## Demo Path

1. Select the "market shock plus misleading input" scenario.
2. The system forms a `belief_state` from synthetic scenario facts.
3. The system builds a `risk_distribution` across market, liquidity,
   evidence, intent, and operational risk.
4. The policy gate triggers `BLOCK` or `DEGRADE_TO_SAFE_MODE`.
5. A human review entry appears with the required control role.
6. Simulated execution records the outcome without creating actual
   transactions.
7. The system outputs a receipt and audit report.
8. The metrics panel shows that unsafe actions were stopped, receipts were
   complete, and `policy_violation_count` remained `0`.

## Narration

### 0:00-0:40 Scenario Selection

Start from Scenario C. The input mixes market stress, missing evidence, and an
over-authorized execution intent. The point is not to maximize return. The
point is to show whether the governance layer can stop a dangerous action.

### 0:40-1:20 Belief State

TRPS normalizes the scenario into a belief state. The belief state states what
is known, what is uncertain, which evidence is missing, and which intent is
unsafe for the current review context.

### 1:20-2:00 Risk Distribution

TRPS converts the belief state into a risk distribution. In Scenario C,
evidence risk, intent risk, and operational risk dominate the aggregate risk.
The model does not need real-market connectivity to demonstrate this gate.

### 2:00-2:50 Policy Gate

The policy layer checks constraints: no autonomous live trade, block on missing
evidence, degrade on conflicting signals, audit receipt required, and kill
switch required. The selected action is `BLOCK` for Scenario C.

### 2:50-3:30 Human Review

The output includes a human review object. The required role is a control owner
or risk manager, and the review status is recorded before any next step.

### 3:30-4:20 Simulated Execution

The demo records an offline synthetic execution outcome. It does not connect to
external execution venues and does not create actual transactions.

### 4:20-5:00 Receipt and Metrics

The final screen shows the receipt and metrics: unsafe action count,
mandatory-review count, receipt completeness, policy violation count, average
decision latency, and audit trace linkage.
