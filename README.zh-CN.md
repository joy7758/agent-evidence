<!-- language-switch:start -->
[English](./README.md) | [中文](./README.zh-CN.md)
<!-- language-switch:end -->

# 代理证据

面向可验证 AI agent run 的具体 execution-evidence 入口，支持离线验证。

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19334062.svg)](https://doi.org/10.5281/zenodo.19334062)
[![CI](https://github.com/joy7758/agent-evidence/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/joy7758/agent-evidence/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![语义事件](https://img.shields.io/badge/semantic%20events-v2.0.0-1f6feb)
![状态](https://img.shields.io/badge/status-experimental-orange)

Agent Evidence 是 Digital Biosphere Architecture 的具体 execution-evidence 主入口。

它把 agent/runtime 执行打包成可离线验证的证据 bundle。它不是完整的架构总仓，不是 audit control plane，也不只是 tracing 或 logging。要看系统上下文，请先去 [digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)；要走最短演练路径，请看 [verifiable-agent-demo](https://github.com/joy7758/verifiable-agent-demo)；要做执行后审阅，请看 [aro-audit](https://github.com/joy7758/aro-audit)。

## 角色

`agent-evidence` 是具体的 execution-evidence 入口，用来把 agent/runtime 的执行过程打包成可移植、可离线验证的证据包。

## 不是这个仓库

- 不是完整的架构总仓
- 不是 audit control plane
- 不只是 tracing 或 logging
- 不是 walkthrough demo
- 不是 execution-integrity kernel

## 从这里开始

- architecture context -> [digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)
- 当前主 package -> `spec/execution-evidence-operation-accountability-profile-v0.1.md`、`schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- 当前可运行入口 -> [examples/README.md](examples/README.md)、[demo/README.md](demo/README.md)、`agent-evidence validate-profile <file>`
- 历史脉络 -> [docs/lineage.md](docs/lineage.md)
- walkthrough -> [verifiable-agent-demo](https://github.com/joy7758/verifiable-agent-demo)
- post-execution review -> [aro-audit](https://github.com/joy7758/aro-audit)

## 当前 v0.1 package

当前主 package surface 是
`Execution Evidence and Operation Accountability Profile v0.1`。

它冻结在 GitHub Release `v0.2.0` 中。

当前 package DOI：https://doi.org/10.5281/zenodo.19334062

该 release 内部冻结的 package 版本仍是 `v0.1`。

当前 v0.1 路径从这里开始：

- 规范：`spec/execution-evidence-operation-accountability-profile-v0.1.md`
- Schema：`schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- Validator CLI：`agent-evidence validate-profile <file>`
- Examples：[examples/README.md](examples/README.md)
- Demo：[demo/README.md](demo/README.md)
- 状态与验收：`docs/STATUS.md`、`docs/ACCEPTANCE-CHECKLIST.md`
- 提交交付：`submission/package-manifest.md`、`submission/final-handoff.md`

实现说明：JSONL、SQLite 和 PostgreSQL 后端仍然可用，但它们从属于本仓库作为 evidence-entry 的定位。

![存储](https://img.shields.io/badge/storage-JSONL%20%7C%20SQLite%20%7C%20Postgres-0a7b83)

### Minimal v0.1 walkthrough

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

验证最小 valid / invalid 样例：

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
agent-evidence validate-profile examples/invalid-missing-required.json
agent-evidence validate-profile examples/invalid-unclosed-reference.json
agent-evidence validate-profile examples/invalid-policy-link-broken.json
```

运行最小 demo：

```bash
python3 demo/run_operation_accountability_demo.py
```

预期结果：

- valid 样例返回 JSON，其中 `"ok": true`
- 每个 invalid 样例返回 JSON，其中 `"ok": false`，并给出一个主错误码
- demo 会把工件写到 `demo/artifacts/`，最后输出一行 `PASS` 摘要

已知环境说明：

- 仓库 `.venv` 在 Python 3.14 下跑更大范围测试时，可能出现一条 `langchain_core` warning；它不影响最小 profile、validator 或 demo 路径

## 历史脉络

历史上的 `Execution Evidence Object`、较早的 `Agent Evidence Profile` 命名、旧版 FDO mapping 表述以及会议样品说明仍然保留在仓库里，但它们已经不是当前主入口。历史脉络请统一看 [docs/lineage.md](docs/lineage.md)。

历史样品轨道继续保留原始 DOI：
https://doi.org/10.5281/zenodo.19055948

## 最快证明

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,langchain,sql]"
python integrations/langchain/export_evidence.py
agent-evidence verify-bundle --bundle-dir integrations/langchain/langchain-evidence-bundle
```

这条路径会运行仓库中现成的 LangChain exporter，并对生成的 bundle 做离线验证。

如果你想看一个更短的 callback/export 示例，可直接读
`docs/cookbooks/langchain_minimal_evidence.md`。

## 为什么这不只是 tracing

Tracing 和 logs 主要帮助操作者检查一次运行。Agent Evidence 把运行时
事件打包成可移植工件，让另一方之后可以验证，而且可以离线验证。

证据路径：

`runtime events -> evidence bundle -> signed manifest -> detached anchor (when present) -> offline verify`

这个仓库当前实现了 bundle、manifest、signatures 和 offline verification
这些步骤。外部 anchoring 不在 AEP v0.1 的范围内，默认也不会启用。

该工具包现在支持两种存储模式：

- 仅附加本地 JSONL 文件
- SQLAlchemy 支持的 SQLite/PostgreSQL 数据库

当前模型将每个记录视为语义事件信封：

- `event.event_type` 与框架无关，例如 `chain.start` 或 `tool.end`
- `event.context.source_event_type` 保留原始框架事件名称
- `hashes.previous_event_hash` 链接到先前的事件
- `hashes.chain_hash` 提供累积链 tip 以做完整性检查

### 安全序列化

证据序列化层实现了：

- 敏感字段默认脱敏
- 最大递归深度
- 循环引用保护
- 对象大小限制

这些保护可以避免证据 bundle 泄露敏感信息，也能减少序列化层面的拒绝服务风险。

## 为什么是这个形状

该项目的组织方式让证据捕获保持模块化：

- `agent_evidence`：核心模型与记录逻辑
- `agent_evidence/crypto`：规范哈希与链式辅助工具
- `agent_evidence/storage`：仅追加的本地存储后端
- `agent_evidence/integrations`：外部 agent framework 适配器
- `agent_evidence/cli`：命令行入口
- `agent_evidence/schema`：持久化 envelope 的 JSON Schema
- `examples`：可执行示例
- `tests`：基线回归覆盖

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,langchain,sql]"
agent-evidence schema
```

## Agent Evidence Profile v0.1 MVP

当前 MVP 路径是一条具备完整性验证能力、支持离线校验的证据 bundle 路径。它作为 Agent Evidence Profile 实现，先保留一条 LangChain-first 集成面，并为后续 OpenInference / OpenTelemetry 兼容映射留出空间。

AEP v0.1 是完整性可验证的证据 profile，不是不可否认系统。

AEP 面向自主 agent run，强调离线验证和运行时 provenance 捕获。

```bash
python integrations/langchain/export_evidence.py
agent-evidence verify-bundle --bundle-dir integrations/langchain/langchain-evidence-bundle
```

针对一个 valid fixture 和一个 tampered fixture 跑 gate：

```bash
python scripts/run_profile_gate.py
```

## 自动机边车出口商

下一个只读路径是康威中立的自动机边车/导出器。它
读取 `state.db`、git 历史记录和持久的链上引用，然后发出
AEP 捆绑包加上 `fdo-stub.json` 和 `erc8004-validation-stub.json`。

```bash
agent-evidence export automaton \
  --state-db /path/to/state.db \
  --repo /path/to/state/repo \
  --runtime-root /path/to/automaton-checkout \
  --out ./automaton-aep-bundle
```

`agent-evidence export automaton` 已针对现场隔离住宅进行了验证
自动机运行并保持标记为实验性，而实时数据合约是
仍在解决。

当提供 `--runtime-root` 时，导出器尝试解析
`source_runtime_version`、`source_runtime_commit` 和 `source_runtime_dirty`
从自动机结账而不更改导出路径。

## 受控释放表面

位于 [v0.1-live-chain](/Users/zhangbin/GitHub/agent-evidence/release/v0.1-live-chain/README.md) 的受控样品发布属于历史 lineage surface，并不是当前主入口。

该历史样品轨道在 Zenodo 上保留原始 DOI：
https://doi.org/10.5281/zenodo.19055948

它冻结了：

- AEP 架构
- 验证 CLI
- 浪链出口商
- 自动机出口商
- 实时运行手册
- 公共带电/被篡改的固定装置
- AEP 边界声明

它与当前 Agent Evidence / AEP v0.1 package 路径的关系，统一见 [docs/lineage.md](docs/lineage.md)。

正式的样本发布说明是[RELEASE_NOTE.md](/Users/zhangbin/GitHub/agent-evidence/release/v0.1-live-chain/RELEASE_NOTE.md)。

## CLI 示例

```bash
agent-evidence record \
  --store ./data/evidence.jsonl \
  --actor planner \
  --event-type tool.call \
  --input '{"task":"summarize"}' \
  --output '{"status":"ok"}' \
  --context '{"source":"cli","component":"tool"}'

agent-evidence list --store ./data/evidence.jsonl
agent-evidence show --store ./data/evidence.jsonl --index 0
agent-evidence verify --store ./data/evidence.jsonl
```

SQL 存储使用 SQLAlchemy URL 而不是文件路径：

```bash
agent-evidence record \
  --store sqlite+pysqlite:///./data/evidence.db \
  --actor planner \
  --event-type tool.call \
  --context '{"source":"cli","component":"tool"}'

agent-evidence query \
  --store sqlite+pysqlite:///./data/evidence.db \
  --event-type tool.call \
  --source cli

agent-evidence query \
  --store sqlite+pysqlite:///./data/evidence.db \
  --span-id tool-1 \
  --parent-span-id root \
  --offset 0 \
  --limit 50

agent-evidence query \
  --store sqlite+pysqlite:///./data/evidence.db \
  --previous-event-hash <event-hash> \
  --event-hash-from <lower-bound-hash> \
  --event-hash-to <upper-bound-hash>

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format json \
  --output ./exports/evidence.bundle.json

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format csv \
  --output ./exports/evidence.csv \
  --manifest-output ./exports/evidence.csv.manifest.json \
  --private-key ./keys/manifest-private.pem \
  --key-id evidence-demo

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format xml \
  --output ./exports/evidence.xml \
  --manifest-output ./exports/evidence.xml.manifest.json \
  --private-key ./keys/manifest-private.pem \
  --key-id evidence-demo

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format json \
  --archive-format tar.gz \
  --output ./exports/evidence-package.tgz \
  --private-key ./keys/manifest-private.pem \
  --key-id evidence-demo

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format json \
  --output ./exports/evidence.multisig.json \
  --required-signatures 2 \
  --required-signature-role approver=1 \
  --required-signature-role attestor=1 \
  --signer-config ./keys/operations-q2.signer.json \
  --signer-config ./keys/compliance-q1.signer.json

agent-evidence verify-export \
  --bundle ./exports/evidence.bundle.json \
  --public-key ./keys/manifest-public.pem

agent-evidence verify-export \
  --bundle ./exports/evidence.multisig.json \
  --keyring ./keys/manifest-keyring.json

agent-evidence verify-export \
  --bundle ./exports/evidence.multisig.json \
  --keyring ./keys/manifest-keyring.json \
  --required-signature-role approver=1

agent-evidence verify-export \
  --xml ./exports/evidence.xml \
  --manifest ./exports/evidence.xml.manifest.json \
  --public-key ./keys/manifest-public.pem

agent-evidence verify-export \
  --archive ./exports/evidence-package.tgz \
  --public-key ./keys/manifest-public.pem
```

## 发展

```bash
make install
make test
make lint
make hooks
```

该仓库包括带有基线空白的 `.pre-commit-config.yaml`，
JSON 和 Ruff 检查。

对于 PostgreSQL 支持，请安装额外的驱动程序依赖项：

```bash
pip install -e ".[dev,postgres]"
```

## 语义事件模型

每个持久记录都遵循以下形式：

```json
{
  "schema_version": "2.0.0",
  "event": {
    "event_id": "...",
    "timestamp": "2026-03-16T00:00:00+00:00",
    "event_type": "tool.end",
    "actor": "search-tool",
    "inputs": {},
    "outputs": {},
    "context": {
      "source": "langchain",
      "component": "tool",
      "source_event_type": "on_tool_end",
      "span_id": "...",
      "parent_span_id": null,
      "ancestor_span_ids": [],
      "name": "search-tool",
      "tags": ["langchain", "tool"],
      "attributes": {}
    },
    "metadata": {}
  },
  "hashes": {
    "event_hash": "...",
    "previous_event_hash": "...",
    "chain_hash": "..."
  }
}
```

`event_type` 是稳定语义层。 `source_event_type`保持
用于无损调试的原始回调或跟踪事件。

## 浪链整合

Agent Evidence 支持当前 LangChain 运行时的两种集成路径：

- 用于执行期间实时捕获的回调处理程序
- `Runnable.astream_events(..., version="v2")` 的流事件适配器

回调用法示例：

```python
from agent_evidence import EvidenceRecorder, LocalEvidenceStore
from agent_evidence.integrations import EvidenceCallbackHandler
from langchain_core.runnables import RunnableLambda

store = LocalEvidenceStore("data/evidence.jsonl")
recorder = EvidenceRecorder(store)
handler = EvidenceCallbackHandler(recorder)

chain = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})
result = chain.invoke(
    "hello",
    config={"callbacks": [handler], "metadata": {"session_id": "demo"}},
)
```

流事件捕获示例：

```python
import asyncio

from agent_evidence import EvidenceRecorder, LocalEvidenceStore
from agent_evidence.integrations import record_langchain_event
from langchain_core.runnables import RunnableLambda

async def main() -> None:
    store = LocalEvidenceStore("data/evidence.jsonl")
    recorder = EvidenceRecorder(store)
    chain = RunnableLambda(lambda text: text[::-1]).with_config({"run_name": "reverse"})

    async for event in chain.astream_events("hello", version="v2"):
        record_langchain_event(recorder, event)

asyncio.run(main())
```

两种集成路径都规范了 LangChain 回调名称，例如
`on_chain_start` 和 `on_tool_end` 转换为语义事件类型，例如
`chain.start` 和 `tool.end`。

## OpenAI 智能体s SDK 集成

OpenAI 智能体s SDK 已通过自定义跟踪公开跟踪扩展点
处理器，因此 Agent Evidence 可以将跟踪并将生命周期事件镜像到
相同的语义证据模型，无需修补运行时。

安装可选依赖项：

```bash
pip install -e ".[openai-agents]"
```

跟踪处理器使用示例：

```python
from agents import trace
from agents.tracing import custom_span

from agent_evidence import EvidenceRecorder, LocalEvidenceStore, export_json_bundle
from agent_evidence.integrations import install_openai_agents_processor

store = LocalEvidenceStore("data/openai-agents.evidence.jsonl")
recorder = EvidenceRecorder(store)
install_openai_agents_processor(recorder)

with trace(
    "support-workflow",
    group_id="session-001",
    metadata={"session_id": "session-001"},
):
    with custom_span("collect_context", {"channel": "chat"}):
        pass

export_json_bundle(
    store.query(source="openai_agents"),
    "exports/openai-agents.bundle.json",
)
```

默认情况下，`install_openai_agents_processor()` 会添加特工证据
SDK 的活动处理器。如果您希望 SDK 发出，请传递 `replace=True`
仅进入该过程的特工证据。

参见[`examples/openai_agents/basic_export.py`](examples/openai_agents/basic_export.py)
获取完整的本地示例。

## 确认

捕获后使用 CLI 验证链：

```bash
agent-evidence verify --store ./data/evidence.jsonl
```

这将重新计算每个 `event_hash`，检查 `previous_event_hash`，并验证
累计`chain_hash`。

## SQL存储

`SqlEvidenceStore` 将语义事件信封持久保存到关系表中
同时保留索引列以进行有效过滤：

- `event_type`
- `actor`
- `timestamp`
- `source`
- `component`
- `span_id`
- `parent_span_id`
- `previous_event_hash`
- `event_hash`
- `chain_hash`

查询接口支持：

- 语义过滤器，例如 `event_type`、`actor`、`source` 和 `component`
- 通过 `previous_event_hash` 进行链遍历
- 使用 `span_id` 和 `parent_span_id` 进行跨度范围检查
- 通过 `since` 和 `until` 的时间窗口
- 通过 `event_hash_from/to` 和 `chain_hash_from/to` 的字典哈希窗口
- 通过 `offset` 和 `limit` 分页

哈希窗口过滤器对固定宽度小写 SHA-256 十六进制摘要进行操作，因此
字典范围清晰地映射到索引查找的摘要排序。

该商店接受标准 SQLAlchemy URL，例如：

- `sqlite+pysqlite:///./data/evidence.db`
- `postgresql+psycopg://user:password@localhost:5432/agent_evidence`

## 迁移

您可以将现有 JSONL 证据迁移到 SQLite 或 PostgreSQL：

```bash
agent-evidence migrate \
  --source ./data/evidence.jsonl \
  --target sqlite+pysqlite:///./data/evidence.db
```

`query` 命令适用于本地存储和 SQL 存储，尽管 SQL 存储
一旦记录量增长到超出简单的本地检查范围，就更可取。

## 捆绑出口

Agent Evidence 支持三种导出形状：

- 包含 `records`、`manifest` 和一个或多个独立签名的 JSON 捆绑包
- CSV 工件加上 JSON sidecar 清单
- XML 工件加上 JSON sidecar 清单

导出也可以通过以下方式打包为单个 `.zip` 或 `.tar.gz` 存档
`--archive-format`。包装出口包括：

- 导出的工件
- 边车清单
- 一个小的 `package-manifest.json` 用于在验证期间定位这些文件

两种格式都包含一个清单：

- `artifact_digest` 用于导出的字节
- 有序事件哈希和链哈希列表摘要
- 第一个/最后一个事件哈希值和最新链哈希值
- 用于生成工件的导出过滤器

每个签名还可以携带：

- `key_id` 和 `key_version` 用于密钥轮换
- `signer` 和 `role` 用于审计归因
- `signed_at` 和任意 JSON 元数据

清单还可以携带阈值策略：

- `signature_policy.minimum_valid_signatures` 为 `N-of-M`
- `signature_policy.minimum_valid_signatures_by_role` 用于角色阈值，例如
如 `{"approver": 1, "attestor": 1}`

如果两者都不存在，则验证默认要求每个签名
要验证的工件。如果仅存在角色阈值，则有效
总阈值默认为这些角色要求的总和。

如果捆绑包带有签名，验证将失败关闭：您必须提供
`--public-key` 或 `--keyring`，否则验证返回 `ok=false`。

清单签名使用 Ed25519 PEM 密钥。启用开发外部签名
环境：

```bash
pip install -e ".[signing]"
```

使用 OpenSSL 生成密钥的示例：

```bash
openssl genpkey -algorithm Ed25519 -out ./keys/manifest-private.pem
openssl pkey -in ./keys/manifest-private.pem -pubout -out ./keys/manifest-public.pem
```

签名者配置文件允许您在导出期间附加多个签名。例子
`operations-q2.signer.json`：

```json
{
  "private_key": "./operations-q2-private.pem",
  "key_id": "operations",
  "key_version": "2026-q2",
  "signer": "Operations Bot",
  "role": "approver",
  "metadata": {
    "environment": "prod"
  }
}
```

要将签名策略嵌入导出的清单中，请传递：

- `--required-signatures N` 用于全局 `N-of-M` 规则
- `--required-signature-role <role>=<count>` 角色规则一次或多次

`verify-export` 默认情况下将遵循清单策略，或者您可以覆盖
验证时的全局阈值和角色阈值具有相同的
旗帜。

密钥环让 `verify-export` 解析 `key_id` 的旋转密钥，并且
`key_version`。示例 `manifest-keyring.json`：

```json
{
  "keys": [
    {
      "key_id": "operations",
      "key_version": "2026-q1",
      "public_key": "./operations-q1-public.pem"
    },
    {
      "key_id": "operations",
      "key_version": "2026-q2",
      "public_key": "./operations-q2-public.pem"
    }
  ]
}
```

当您导出 CSV 时，Agent Evidence 会写入 CSV 工件和清单
边车如 `evidence.csv.manifest.json`。面向电子表格的 CSV 导出
清理以公式前缀（例如 `=`、`+`、`-` 或 `@`）开头的单元格
降低人工审核期间配方奶粉注射风险。 `verify-export`
验证清单摘要、导出的工件摘要和每个签名
来自提供的公钥或密钥环。

存档验证还强制对每个文件的成员数进行解包限制
大小以及解压后的总大小，因此不受信任的 `.zip` 和 `.tar.gz` 捆绑包失败
在完全提取之前关闭。

## PostgreSQL 集成验证

对于可重复的真实数据库验证路径，请使用捆绑的 Docker 支持
集成脚本：

```bash
make install-postgres
make test-postgres
```

这将启动一个临时 PostgreSQL 容器，导出
`AGENT_EVIDENCE_POSTGRES_URL`，并运行 `tests/test_postgres_integration.py`
针对实时数据库。
