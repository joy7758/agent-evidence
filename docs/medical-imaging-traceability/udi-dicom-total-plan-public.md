# UDI-DICOM 公开安全版总方案

> 本文件是面向公开仓库的总方案版本。它来自内部开发总结，但已经删除或抽象化以下内容：私有仓库提交号、完整私有一致性测试题库、真实样本处理细节、客户/合作方敏感策略、未公开服务交付细节。

## 1. 当前结论

本项目的当前主线应冻结为：

> 以 UDI-DICOM（Unique Device Identification–Digital Imaging and Communications in Medicine，唯一器械标识—医学数字成像与通信）医疗设备影像工作流证据闭合为核心，维护一个公开 Profile（配置文件）、公开 reference validator（reference validator，参考验证器）、公开 synthetic examples（synthetic examples，合成示例），并在受控环境中维护 conformance suite（conformance suite，一致性测试套件）和 sample validation service（sample validation service，样本验证服务）。

核心判断：

```text
公开层用于发现、引用、复现和智能体调用。
受控层用于保存测试基准、失败模式和适配经验。
服务层用于样本审阅、报告、培训和合作试点。
```

本项目不是医疗诊断系统，不是监管认证系统，不是医院级 PACS（Picture Archiving and Communication System，医学影像归档与通信系统）或 VNA（Vendor Neutral Archive，厂商中立归档）替代品。

---

## 2. 项目定位

中文名：

> 医疗设备影像工作流最小证据清单与验证器

英文名：

> A Minimal UDI-DICOM Evidence Manifest and Validator for Medical-Device Imaging Workflows

一句话定义：

> 本项目用于检查医疗影像工作流中的设备身份、DICOM（Digital Imaging and Communications in Medicine，医学数字成像与通信）影像对象、注册表查询结果、外部验收/校准证据，是否形成一个最小、可复验、可解释的证据闭合。

---

## 3. 明确不做事项

本项目必须持续排除以下事项：

```text
不做临床诊断。
不证明设备临床安全。
不替代监管审批。
不替代医院 PACS。
不替代医院 VNA。
不替代医院资产管理系统。
不声称法律意义上的合规认证。
不控制医疗设备动作。
不做患者治疗决策。
不接收未去标识化患者数据。
```

允许声明的范围：

```text
最小 Profile（配置文件）。
bounded validation path（有边界的验证路径）。
synthetic worked scenario（合成演示场景）。
machine-readable manifest（机器可读证据清单）。
deterministic validation receipt（确定性验证回执）。
review-support artifact（审阅支持工件）。
```

---

## 4. 三层架构

### 4.1 公开层

目标：让研究者、标准工作者、厂商工程师、医院信息化人员和代码智能体能够发现、引用、复现和试用。

公开层包括：

```text
README.md
CITATION.cff（Citation File Format，引用文件格式）
llms.txt（large language models text，大语言模型说明文本）
AGENTS.md（agents instruction file，智能体协作说明文件）
spec/（specification，规范）
schema/（schema，模式）
examples/public/（public examples，公开示例）
validator/（validator，验证器）
tests/（tests，测试）
openapi/（OpenAPI Specification，开放接口规范）
docs/boundary.md（边界说明）
docs/claims-to-avoid.md（禁止声明清单）
```

### 4.2 受控层

目标：保护真正难以复刻的能力。

受控层只公开类别，不公开完整资产：

```text
完整一致性测试题库。
真实或近真实失败模式。
厂商字段差异经验。
注册表解析容错策略。
审阅报告解释模板。
争议样本处理规则。
合作方材料包。
```

### 4.3 服务层

目标：把公开 Profile（配置文件）和受控测试能力转化为可交付服务。

服务层包括：

```text
去标识化样本接收。
字段扫描。
manifest（manifest，证据清单）生成。
receipt（receipt，验证回执）生成。
人工审阅支持报告。
失败项解释。
整改建议。
下一轮测试建议。
培训和试点支持。
```

---

## 5. 最小验证逻辑

reference validator（reference validator，参考验证器）至少执行四类检查。

### 5.1 存在性与可解析性

检查问题：

```text
DICOM（Digital Imaging and Communications in Medicine，医学数字成像与通信）元数据中是否存在 full UDI（full Unique Device Identification，完整唯一器械标识）。
manifest（manifest，证据清单）中是否保存同一个 full UDI。
full UDI 是否能解析出 UDI-DI（Unique Device Identification Device Identifier，唯一器械标识中的器械标识符）。
UDI-PI（Unique Device Identification Production Identifier，唯一器械标识中的生产标识符）是否被分离记录。
```

典型错误类别：

```text
missing_udi
truncated_udi
parser_failed
missing_udi_di
device_uid_used_as_udi_di
```

### 5.2 引用闭合

检查问题：

```text
manifest 是否指向正确 SOP Instance UID（Service-Object Pair Instance Unique Identifier，服务对象对实例唯一标识符）。
study_instance_uid（study instance unique identifier，检查实例唯一标识符）是否记录。
series_instance_uid（series instance unique identifier，序列实例唯一标识符）是否记录。
外部验收、校准或注册表证据是否可解析。
```

### 5.3 跨层一致性

检查问题：

```text
DICOM full UDI 是否等于 manifest full UDI。
DICOM serial number（serial number，序列号）是否和 manifest 一致。
model name（model name，型号名称）是否和 registry result（registry result，注册表结果）冲突。
Device UID（Device Unique Identifier，设备唯一标识符）是否被错误当成 UDI-DI。
```

关键边界：

> Device UID（Device Unique Identifier，设备唯一标识符）是 DICOM（Digital Imaging and Communications in Medicine，医学数字成像与通信）设备标识，不等于 UDI-DI（Unique Device Identification Device Identifier，唯一器械标识中的器械标识符），不能作为注册表查询 key（key，查询键）。

### 5.4 注册表解析

检查问题：

```text
parsed UDI-DI（parsed Unique Device Identification Device Identifier，解析出的唯一器械标识中的器械标识符）是否能在声明的 registry（registry，注册表）中解析。
registry provider（registry provider，注册表提供方）是否记录。
registry jurisdiction（registry jurisdiction，注册表管辖区）是否记录。
lookup timestamp（lookup timestamp，查询时间戳）是否记录。
lookup status（lookup status，查询状态）是否记录。
返回结果是否和 manifest / DICOM 描述一致。
```

---

## 6. 最小 Manifest 字段

manifest（manifest，证据清单）最小字段应覆盖：

```text
profile_name
profile_version
manifest_id
sop_instance_uid
study_instance_uid
series_instance_uid
full_udi
issuing_agency
parsed_udi_di
parsed_udi_pi
registry_provider
registry_jurisdiction
lookup_timestamp
lookup_status
registry_result_summary
manufacturer
model_name
serial_number
device_uid
evidence_items
manifest_sha256
artifact_hashes
validation_status
checks
```

可选扩展字段：

```text
pid（persistent identifier，持久标识符）
metadata_profile（metadata profile，元数据配置文件）
fdo_mapping（FAIR Digital Object mapping，公平数字对象映射）
fhir_mapping（Fast Healthcare Interoperability Resources mapping，快速医疗互操作资源映射）
```

---

## 7. 公开仓库最小结构

建议公开仓库保持如下结构：

```text
udi-dicom-evidence-validator/
├─ README.md
├─ LICENSE
├─ NOTICE
├─ CITATION.cff
├─ llms.txt
├─ AGENTS.md
├─ SECURITY.md
├─ CHANGELOG.md
├─ spec/
│  └─ udi-dicom-evidence-manifest-profile-v0.1.md
├─ schema/
│  ├─ udi-dicom-evidence-manifest-v0.1.schema.json
│  └─ udi-dicom-validation-receipt-v0.1.schema.json
├─ examples/
│  └─ public/
│     ├─ sample_dicom_metadata.pass.json
│     ├─ manifest.pass.json
│     ├─ manifest.fail_missing_udi.json
│     ├─ manifest.fail_wrong_sop_uid.json
│     └─ manifest.fail_registry_unresolved.json
├─ validator/
│  ├─ reference_validator.py
│  └─ cli.py
├─ tests/
│  └─ public_conformance_tests.py
├─ openapi/
│  └─ validator.openapi.yaml
├─ docs/
│  ├─ boundary.md
│  ├─ claims-to-avoid.md
│  ├─ cooperation-brief.md
│  ├─ reviewer-faq.md
│  └─ fdo-mapping.md
├─ demo/
│  └─ portable-ultrasound/
│     ├─ scenario.md
│     ├─ run_demo.py
│     ├─ expected-output.md
│     └─ artifacts/
└─ release/
   └─ v0.1.0-package-manifest.md
```

---

## 8. 智能体入口

### 8.1 llms.txt（large language models text，大语言模型说明文本）

作用：告诉大语言模型项目是什么、先读哪些文件、如何引用、能做什么、不能声称什么。

必须指向：

```text
README.md
spec/udi-dicom-evidence-manifest-profile-v0.1.md
schema/udi-dicom-evidence-manifest-v0.1.schema.json
examples/public/manifest.pass.json
docs/boundary.md
docs/claims-to-avoid.md
CITATION.cff
```

### 8.2 AGENTS.md（agents instruction file，智能体协作说明文件）

作用：告诉 Codex（Codex，代码智能体）、Claude Code（Claude Code，代码智能体）、Cursor（Cursor，智能代码编辑器）等工具如何修改项目。

核心规则：

```text
修改 schema（schema，模式）时必须同步修改 examples（examples，示例）、validator（validator，验证器）和 tests（tests，测试）。
保持 pass/fail（pass/fail，通过/失败）结果确定性。
不得加入临床安全声明。
不得加入患者数据。
不得暴露受控一致性测试套件。
不得把 Device UID 当成 UDI-DI。
```

### 8.3 OpenAPI Specification（OpenAPI Specification，开放接口规范）

公开接口只保留验证与只读查询：

```text
POST /v1/validate/manifest
POST /v1/validate/dicom-metadata
POST /v1/receipt/render
GET  /v1/profile
GET  /v1/schema
GET  /v1/examples
```

不公开：

```text
POST /v1/private/conformance
POST /v1/vendor-rules/apply
POST /v1/real-sample/assess
```

### 8.4 MCP（Model Context Protocol，模型上下文协议）

MCP（Model Context Protocol，模型上下文协议）入口先做只读和公开验证能力：

```text
list_profile
list_public_examples
validate_public_manifest
render_public_receipt
explain_failure_code
```

---

## 9. 对外版本策略

### 9.1 public v0.1.0

公开内容：

```text
Profile（配置文件）
schema（模式）
3–4 个公开示例
reference validator（参考验证器）
README（readme，项目说明）
llms.txt（大语言模型说明文本）
CITATION.cff（引用文件格式）
OpenAPI Specification（开放接口规范）
demo（demo，演示）
```

目标：

```text
建立源头。
让智能体引用。
让论文闭环。
让示例可复现。
```

### 9.2 controlled partner v0.1.0

受控合作后可提供：

```text
有限合作方测试用例。
golden outputs（golden outputs，黄金输出）。
错误码解释。
报告模板。
一次技术解释会。
```

目标：

```text
厂商或医院试跑。
验证真实字段适配需求。
沉淀受控失败模式。
```

### 9.3 public v0.2.0

公开增强：

```text
更多公开示例。
更完整 error code（error code，错误码）。
FHIR（Fast Healthcare Interoperability Resources，快速医疗互操作资源）映射草案。
FDO（FAIR Digital Object，公平数字对象）封装示例。
```

---

## 10. Codex 任务队列

以下任务可交给 Codex（Codex，代码智能体）或其他代码智能体执行。

### Task 1：公开仓库骨架

```text
Create repository skeleton for udi-dicom-evidence-validator.
Add README.md, LICENSE, CITATION.cff, llms.txt, AGENTS.md, SECURITY.md, CHANGELOG.md.
Add folders: spec, schema, examples/public, validator, tests, demo/portable-ultrasound, docs, openapi, release.
```

验收：文件存在，路径清晰，README（readme，项目说明）能够说明边界。

### Task 2：Profile v0.1（配置文件第一版）

```text
Create spec/udi-dicom-evidence-manifest-profile-v0.1.md.
Define scope, non-scope, required fields, validation checks, failure codes, claims-to-avoid.
Use the four checks: presence_parseability, reference_closure, cross_layer_consistency, registry_resolution.
```

验收：四类检查均被定义，禁止声明清楚。

### Task 3：Schema v0.1（模式第一版）

```text
Create schema/udi-dicom-evidence-manifest-v0.1.schema.json using JSON Schema draft 2020-12.
Include manifest_id, profile_version, sop_instance_uid, full_udi, issuing_agency, parsed_udi_di, registry fields, equipment descriptors, evidence_items, integrity, validation.
```

验收：公开 pass（pass，通过）示例通过，公开 fail（fail，失败）示例失败。

### Task 4：公开样例

```text
Create examples/public:
manifest.pass.json
manifest.fail_missing_udi.json
manifest.fail_wrong_sop_uid.json
manifest.fail_registry_unresolved.json
sample_dicom_metadata.pass.json
```

验收：每个失败样例只触发一个主错误码。

### Task 5：Reference Validator（参考验证器）

```text
Create validator/reference_validator.py.
Validate schema.
Run four validation stages.
Output receipt.json and report.md.
Return deterministic error codes.
```

验收：CLI（Command Line Interface，命令行界面）可一键运行；JSON（JavaScript Object Notation，JavaScript 对象表示法）输出可机器读取；Markdown（Markdown，轻量级标记语言）报告可人工审阅。

### Task 6：公开测试

```text
Create tests/public_conformance_tests.py.
Assert pass sample returns ok true.
Assert each fail sample returns ok false and one expected primary error code.
```

验收：测试结果稳定，不依赖外部真实注册表网络请求。

### Task 7：Demo（demo，演示）

```text
Create demo/portable-ultrasound/run_demo.py.
Read sample metadata and manifest.
Run validator.
Write artifacts/receipt.json and artifacts/report.md.
Print one PASS/FAIL summary line.
```

验收：5 分钟可讲清楚闭环。

### Task 8：合作材料

```text
Create docs/cooperation-brief.md.
Create docs/discovery-meeting-script.md.
Create docs/sample-intake-checklist.md.
Create docs/claims-to-avoid.md.
```

验收：可发给医院或厂商；不泄露受控测试套件；能说明对方需要提供什么。

---

## 11. 当前优先级

### 长期方向

```text
面向 FDO（FAIR Digital Object，公平数字对象）和数据空间环境，形成智能体执行证据、设备证据、操作证据的可验证配置文件体系。
```

### 当前主线

```text
UDI-DICOM（Unique Device Identification–Digital Imaging and Communications in Medicine，唯一器械标识—医学数字成像与通信）设备身份—影像对象—外部证据的最小闭合。
```

### 暂缓事项

```text
医疗机器人操作证据。
真实医院试点。
真实设备样本大规模收集。
clinical validation（clinical validation，临床验证）。
regulatory approval（regulatory approval，监管批准）。
certification（certification，认证）。
SaaS（Software as a Service，软件即服务）。
```

---

## 12. 最终一句话

> 本项目不是卖一个容易被智能体复刻的程序，而是维护一个面向 UDI-DICOM（Unique Device Identification–Digital Imaging and Communications in Medicine，唯一器械标识—医学数字成像与通信）医疗设备影像工作流的公开 Profile（配置文件）、受控一致性测试基准和样本验证服务；公开层让别人找到并引用你，受控层保留真正的测试能力，服务层负责形成可交付成果。
