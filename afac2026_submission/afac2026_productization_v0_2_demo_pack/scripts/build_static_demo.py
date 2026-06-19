#!/usr/bin/env python3
"""Build the offline AFAC2026 TRPS static demo."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AFAC_ROOT = ROOT.parent
V1_ROOT = AFAC_ROOT / "afac2026_productization_v0_1"
DEMO_DIR = ROOT / "demo"
ASSET_DIR = DEMO_DIR / "assets"
DATA_PATH = ASSET_DIR / "trps_demo_data.json"
PROJECT_TITLE_ZH = "TRPS：面向金融机构交易前风险治理的可审计智能决策与模拟执行平台"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_demo_data() -> dict[str, object]:
    scenario_pack = load_json(V1_ROOT / "07_demo_scenarios.json")
    receipts = load_json(V1_ROOT / "outputs" / "demo_receipts.json")
    metrics = load_json(V1_ROOT / "outputs" / "demo_metrics.json")
    validation = load_json(V1_ROOT / "outputs" / "validation_report.json")
    assert isinstance(scenario_pack, dict)
    assert isinstance(receipts, dict)
    assert isinstance(metrics, dict)
    assert isinstance(validation, dict)

    decisions = {decision["scenario_id"]: decision for decision in receipts["decisions"]}
    cards: list[dict[str, object]] = []
    for index, scenario in enumerate(scenario_pack["scenarios"]):
        scenario_id = scenario["scenario_id"]
        decision = decisions[scenario_id]
        receipt = decision["receipt"]
        cards.append(
            {
                "index": index,
                "scenario_id": scenario_id,
                "name_zh": scenario["name_zh"],
                "expected_gate_decision": scenario["expected_gate_decision"],
                "belief_state": decision["belief_state"],
                "risk_distribution": decision["risk_distribution"],
                "triggered_constraints": decision["constrained_policy"]["triggered_constraints"],
                "gate_decision": decision["gate_decision"]["action_code"],
                "human_review_status": receipt["human_review_status"],
                "final_action": receipt["final_action"],
                "receipt_id": receipt["receipt_id"],
                "rationale": receipt["rationale"],
            }
        )

    return {
        "pack_id": "afac2026_trps_demo_pack_v0_2",
        "generated_from": "afac2026_productization_v0_1",
        "project_title_zh": PROJECT_TITLE_ZH,
        "tagline_en": (
            "Not an autonomous trading bot. A governance layer for pre-trade risk decisions."
        ),
        "scenarios": cards,
        "metrics": metrics,
        "validation": {
            "ok": validation["ok"],
            "forbidden_claim_hit_count": validation["forbidden_claim_hit_count"],
            "real_api_keyword_hit_count": validation["real_api_keyword_hit_count"],
            "policy_violation_count": validation["policy_violation_count"],
            "actual_transaction_generated_count": validation["actual_transaction_generated_count"],
            "external_execution_connected": validation["external_execution_connected"],
        },
        "boundary_statement": (
            "This demo uses synthetic controlled scenarios only. It does not "
            "establish real-market profitability, production readiness, "
            "autonomous trading suitability, or regulatory certification."
        ),
    }


def html_template(data_json: str) -> str:
    safe_data = data_json.replace("</", "<\\/")
    return textwrap.dedent(
        f"""\
        <!doctype html>
        <html lang="zh-CN">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <title>TRPS AFAC2026 Demo Pack v0.2</title>
          <link rel="stylesheet" href="style.css" />
        </head>
        <body>
          <main class="shell">
            <section class="hero" aria-labelledby="title">
              <div>
                <h1 id="title">
                  TRPS：面向金融机构交易前风险治理的
                  可审计智能决策与模拟执行平台
                </h1>
                <p class="lead">
                  Not an autonomous trading bot. A governance layer for
                  pre-trade risk decisions.
                </p>
              </div>
              <div class="hero-panel" aria-label="Demo status">
                <span class="status-dot"></span>
                <strong>Offline synthetic demo</strong>
                <span>scenario → decision → receipt → metrics</span>
              </div>
            </section>

            <section class="metrics" aria-labelledby="metrics-title">
              <h2 id="metrics-title">指标面板</h2>
              <div id="metrics-grid" class="metrics-grid"></div>
            </section>

            <section class="workspace" aria-labelledby="scenario-title">
              <div class="scenario-list">
                <h2 id="scenario-title">演示场景</h2>
                <div id="scenario-cards" class="scenario-cards"></div>
              </div>
              <article class="detail" aria-live="polite">
                <div class="detail-header">
                  <p class="small-label">Selected decision</p>
                  <h2 id="detail-title">选择一个场景</h2>
                </div>
                <div id="detail-body" class="detail-body"></div>
              </article>
            </section>

            <footer class="boundary" id="boundary"></footer>
          </main>
          <script id="trps-data" type="application/json">
        {safe_data}
          </script>
          <script src="app.js"></script>
        </body>
        </html>
        """
    )


CSS = textwrap.dedent(
    """\
    :root {
      --bg: #f8faf9;
      --surface: #ffffff;
      --text: #16201f;
      --muted: #5b6968;
      --line: #d8e2df;
      --accent: #0f766e;
      --accent-dark: #0f4f4a;
      --danger: #b42318;
      --warn: #a15c07;
      --ok: #167642;
      --shadow: 0 18px 50px rgba(18, 38, 35, 0.12);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background:
        linear-gradient(135deg, rgba(15, 118, 110, 0.08), transparent 32rem),
        var(--bg);
      color: var(--text);
      font-family:
        Inter, "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", Arial,
        sans-serif;
      letter-spacing: 0;
    }

    .shell {
      width: min(1180px, calc(100% - 40px));
      margin: 0 auto;
      padding: 34px 0 36px;
    }

    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 340px;
      gap: 24px;
      align-items: stretch;
      min-height: 220px;
    }

    h1,
    h2,
    h3,
    p {
      margin: 0;
    }

    h1 {
      max-width: 880px;
      font-size: clamp(32px, 5vw, 58px);
      line-height: 1.08;
      font-weight: 780;
    }

    .lead {
      max-width: 680px;
      margin-top: 18px;
      color: var(--muted);
      font-size: 18px;
      line-height: 1.55;
    }

    .hero-panel,
    .metrics,
    .detail,
    .scenario-card {
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.92);
      box-shadow: var(--shadow);
    }

    .hero-panel {
      display: grid;
      align-content: center;
      gap: 12px;
      padding: 24px;
      border-radius: 8px;
      font-size: 15px;
      color: var(--muted);
    }

    .hero-panel strong {
      color: var(--text);
      font-size: 18px;
    }

    .status-dot {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: var(--ok);
      box-shadow: 0 0 0 7px rgba(22, 118, 66, 0.12);
    }

    .metrics {
      margin-top: 28px;
      padding: 22px;
      border-radius: 8px;
    }

    .metrics h2,
    .scenario-list h2,
    .detail h2 {
      font-size: 22px;
      line-height: 1.2;
    }

    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 16px;
    }

    .metric-card {
      min-height: 104px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfdfc;
    }

    .metric-value {
      margin-top: 10px;
      color: var(--accent-dark);
      font-size: 28px;
      font-weight: 780;
    }

    .metric-label {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
      word-break: break-word;
    }

    .workspace {
      display: grid;
      grid-template-columns: 390px minmax(0, 1fr);
      gap: 18px;
      margin-top: 28px;
    }

    .scenario-list {
      display: grid;
      align-content: start;
      gap: 14px;
    }

    .scenario-cards {
      display: grid;
      gap: 12px;
    }

    .scenario-card {
      width: 100%;
      min-height: 112px;
      padding: 16px;
      border-radius: 8px;
      color: inherit;
      text-align: left;
      cursor: pointer;
      transition: border-color 160ms ease, transform 160ms ease;
    }

    .scenario-card:hover,
    .scenario-card:focus-visible,
    .scenario-card.active {
      border-color: var(--accent);
      outline: none;
      transform: translateY(-1px);
    }

    .scenario-name {
      font-size: 16px;
      font-weight: 720;
      line-height: 1.35;
    }

    .scenario-action {
      display: inline-flex;
      margin-top: 12px;
      padding: 5px 9px;
      border: 1px solid var(--line);
      border-radius: 6px;
      color: var(--accent-dark);
      font-size: 12px;
      font-weight: 700;
    }

    .detail {
      min-height: 520px;
      padding: 22px;
      border-radius: 8px;
    }

    .detail-header {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: start;
      border-bottom: 1px solid var(--line);
      padding-bottom: 16px;
    }

    .small-label {
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
    }

    .detail-body {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin-top: 18px;
    }

    .field {
      min-height: 108px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #fbfdfc;
    }

    .field.full {
      grid-column: 1 / -1;
    }

    .field h3 {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
    }

    pre,
    .field-value {
      margin-top: 10px;
      white-space: pre-wrap;
      word-break: break-word;
      color: var(--text);
      font-size: 13px;
      line-height: 1.5;
      font-family:
        "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    }

    .gate-BLOCK {
      color: var(--danger);
    }

    .gate-ESCALATE,
    .gate-REVIEW_REQUIRED {
      color: var(--warn);
    }

    .gate-WARN,
    .gate-ALLOW {
      color: var(--ok);
    }

    .boundary {
      margin-top: 26px;
      padding: 16px 0 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.55;
      border-top: 1px solid var(--line);
    }

    @media (max-width: 900px) {
      .hero,
      .workspace {
        grid-template-columns: 1fr;
      }

      .metrics-grid,
      .detail-body {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 580px) {
      .shell {
        width: min(100% - 24px, 1180px);
        padding-top: 22px;
      }

      .metrics-grid,
      .detail-body {
        grid-template-columns: 1fr;
      }

      h1 {
        font-size: 34px;
      }
    }
    """
)


JS = textwrap.dedent(
    """\
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
    """
)


def main() -> int:
    data = build_demo_data()
    data_json = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
    write_json(DATA_PATH, data)
    write_text(DEMO_DIR / "index.html", html_template(data_json))
    write_text(DEMO_DIR / "style.css", CSS)
    write_text(DEMO_DIR / "app.js", JS)
    print(json.dumps({"ok": True, "demo_index": str(DEMO_DIR / "index.html")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
