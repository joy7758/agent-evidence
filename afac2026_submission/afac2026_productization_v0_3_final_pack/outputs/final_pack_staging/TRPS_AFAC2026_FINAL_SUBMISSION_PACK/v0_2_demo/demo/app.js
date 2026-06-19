const data = JSON.parse(document.getElementById("trps-data").textContent);

const metricLabels = {
  scenario_count: "覆盖的风险场景数量",
  blocked_unsafe_action_count: "危险动作拦截次数",
  mandatory_review_count: "强制人工复核触发次数",
  receipt_completeness_rate: "审计凭证完整率",
  policy_violation_count: "策略约束违规次数",
  audit_trace_linkage_rate: "审计链路关联率",
  average_decision_latency_ms: "单次决策耗时",
};

const selectedMetricKeys = [
  "scenario_count",
  "blocked_unsafe_action_count",
  "mandatory_review_count",
  "receipt_completeness_rate",
  "policy_violation_count",
  "audit_trace_linkage_rate",
  "average_decision_latency_ms",
];

function formatValue(value) {
  if (typeof value === "number") {
    return Number.isInteger(value) ? String(value) : String(value.toFixed(2));
  }
  return String(value);
}

function renderMetrics() {
  const grid = document.getElementById("metrics-grid");
  grid.innerHTML = selectedMetricKeys
    .map((key) => {
      const value = data.metrics[key];
      return `
        <div class="metric-card">
          <div class="metric-label">${metricLabels[key]}</div>
          <div class="metric-value">${formatValue(value)}</div>
        </div>
      `;
    })
    .join("");
}

function field(title, value, className = "") {
  const rendered =
    typeof value === "string" ? value : JSON.stringify(value, null, 2);
  return `
    <section class="field ${className}">
      <h3>${title}</h3>
      <pre>${rendered}</pre>
    </section>
  `;
}

function renderDetail(scenario) {
  document.getElementById("detail-title").textContent = scenario.name_zh;
  document.getElementById("detail-body").innerHTML = [
    field("belief_state", scenario.belief_state, "full"),
    field("risk_distribution", scenario.risk_distribution),
    field("triggered_constraints", scenario.triggered_constraints),
    field("gate_decision", scenario.gate_decision),
    field("human_review_status", scenario.human_review_status),
    field("final_action", scenario.final_action),
    field("receipt_id", scenario.receipt_id),
    field("rationale", scenario.rationale, "full"),
  ].join("");
  document
    .querySelectorAll(".scenario-card")
    .forEach((button) => button.classList.remove("active"));
  document
    .querySelector(`[data-scenario="${scenario.scenario_id}"]`)
    .classList.add("active");
}

function renderScenarios() {
  const cards = document.getElementById("scenario-cards");
  cards.innerHTML = data.scenarios
    .map(
      (scenario) => `
      <button class="scenario-card" data-scenario="${scenario.scenario_id}">
        <div class="scenario-name">${scenario.name_zh}</div>
        <span class="scenario-action gate-${scenario.gate_decision}">
          ${scenario.gate_decision}
        </span>
      </button>
    `
    )
    .join("");
  cards.querySelectorAll(".scenario-card").forEach((button) => {
    button.addEventListener("click", () => {
      const scenario = data.scenarios.find(
        (item) => item.scenario_id === button.dataset.scenario
      );
      renderDetail(scenario);
    });
  });
  renderDetail(data.scenarios[0]);
}

renderMetrics();
renderScenarios();
document.getElementById("boundary").textContent = data.boundary_statement;
