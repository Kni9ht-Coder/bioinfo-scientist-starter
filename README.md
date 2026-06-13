<p align="center">
  <img src="assets/logo.png" alt="BioInfo-Scientist Starter" width="215"/>
</p>

<h1 align="center">BioInfo-Scientist Starter</h1>

<p align="center">
  面向 <b>macOS 主力机 + WSL GPU 服务器</b> 的、Codex 辅助的<br/>
  <b>可复现</b>生物信息学 / AIDD 论文系统模板
</p>

<p align="center">
  研究方向 → 文献 → 实验协议 → pipeline → 结果 → claim ledger → manuscript → internal review
</p>

本项目把一篇论文拆成**可审计的工程流水线**：每一步都有命令、配置、数据版本、环境、种子、git commit 和输出位置可追溯。它借鉴了 AI-Scientist 式的「idea → 实验 → 写作」自动化思路，但刻意保留人类在科学决策上的最终权力。

> **Note**
> 这不是一个全自动论文生成器。与全自主系统不同，本模板在 `AGENTS.md` 中明确**禁止**：全自动投稿、执行未沙箱化的 LLM 代码、以及无证据的 manuscript 断言。Codex 只做**可验证**的任务；研究问题、生物学解读、伦理、署名与投稿由人类研究者决定。

> **Caution**
> 绝不可提交或上传人类/临床等隐私数据，也不可将其暴露给外部服务（见 `AGENTS.md` 规则 5）。大文件（fastq/bam/vcf/h5ad 等）和可再生产物不进 Git，用 DVC/rsync 管理。

## 目录

1. [核心理念](#核心理念)
2. [环境要求与安装](#环境要求与安装)
3. [外部 API 与密钥](#外部-api-与密钥)
4. [生成研究 idea（Literature Scout + Idea Generator）](#生成研究-idea)
5. [运行实验与论文流水线](#运行实验与论文流水线)
6. [工作流阶段](#工作流阶段)
7. [项目结构](#项目结构)
8. [Codex Skills](#codex-skills)
9. [常用命令](#常用命令)
10. [常见问题](#常见问题)
11. [负责任使用](#负责任使用)

## 核心理念

| 原则 | 实现 |
| --- | --- |
| 不造假 | 引用、DOI/PMID、数据、指标、机制等一律不得编造；缺证据写 `TODO: evidence needed` |
| 证据驱动写作 | manuscript 断言必须由 `results/claim_ledger.yml` 中 `verified` 的 claim 支撑 |
| 可复现 | 每次实验记录命令/配置/数据哈希/环境/种子/commit/输出（`results/run_registry.yml`） |
| 人类权威 | idea 选择、协议批准、投稿等关键节点设置 human approval gate |
| 小步提交 | 一个 PR 只做一件事：一个 loader / 一个 QC / 一个 baseline / 一个图 / 一个小节 |

## 环境要求与安装

推荐工作模式：**Mac** 负责写作、文献、轻量测试；**WSL GPU** 负责训练大模型与重计算；**GitHub** 是代码和小配置的唯一事实源。

```bash
# 1. 克隆并进入项目
cd bioinfo-scientist-starter

# 2. 初始化 git（如果还没有）
git init && git add . && git commit -m "Initialize BioInfo-Scientist starter"

# 3. 创建核心环境（Mac/Linux 通用，约几分钟）
mamba env create -f envs/core.yml
conda activate paper-core

# 4. 安装本项目为可编辑包 + 启用 pre-commit
pip install -e .
pre-commit install

# 5. 跑最小检查，确认环境健康
make lint && make test && make smoke && make snakemake-dry
```

可选的领域环境（按需创建）：

| 环境文件 | 名称 | 用途 |
| --- | --- | --- |
| `envs/core.yml` | `paper-core` | 写作、统计、pipeline、CI（必装） |
| `envs/bioinfo.yml` | `paper-bioinfo` | 测序工具链（fastqc/samtools/STAR/salmon…） |
| `envs/scrna.yml` | `paper-scrna` | 单细胞（scanpy/anndata/scvi-tools） |
| `envs/aidd-gpu.yml` | `paper-aidd-gpu` | GPU + AIDD（rdkit/PyTDC/lightning，PyTorch 按官网命令装） |

## 外部 API 与密钥

文献检索只使用**公开**接口，无密钥也能运行基础检索：

- **PubMed（NCBI E-utilities）**：建议在调用时加 `--email you@example.com` 以符合 NCBI 礼仪；高频访问可申请 NCBI API key（`--api-key`）。
- **Semantic Scholar Academic Graph API**：基础检索免密钥；如需更高配额可申请 S2 API key。

不要把任何密钥写入仓库；用环境变量或本地 `.env`（已被 `.gitignore` 忽略）。

## 生成研究 idea

给一个研究方向，系统会：**检索当前文献 → 生成结构化 paper cards → 画 gap map → 生成并排序 idea → 推荐 top idea →（人工批准后）生成 project brief / experiment protocol**。脚本只负责「检索 + 脚手架」，真正的文献阅读、gap 判断、idea 生成由 Codex 按 skill 填空——确保可审计、不造假。完整流程见 `docs/idea_generation_protocol.md`。

```bash
# 1) 检索文献（PubMed + Semantic Scholar）→ literature/raw/literature_results.json
python scripts/literature_search.py \
  --query "anti-biofilm antimicrobial peptide machine learning" \
  --max-results 25 --email you@example.com

# 2) 生成 paper cards（已验证元数据自动填，分析字段留 TODO）→ literature/paper_cards/
python scripts/build_paper_cards.py --input literature/raw/literature_results.json

# 3) 生成 idea 脚手架（17 字段 + 打分表）→ literature/idea_bank.md, docs/top_idea_recommendation.md
python scripts/generate_ideas.py --direction "anti-biofilm AMP design with ML" --n-ideas 10
```

配套两个 Codex skill：`literature-scout`（检索→cards→gap map→novelty risk）和 `idea-generator`（按证据填 idea、打分、排序、推荐）。典型用法：

```text
使用 literature-scout skill。
研究方向：基于机器学习与生成模型的抗生物膜抗菌肽设计（复发性尿路感染 / 革兰氏阴性菌生物膜）。
请先设计检索策略并运行检索，生成 paper cards 与 gap map。不要编造具体文献。
```

```text
使用 idea-generator skill。
请基于 literature/paper_cards/ 与 literature/gap_map.md 生成 10 个候选 idea，
按数据可得性/创新性/可行性/可复现性等打分并选出 top 3。没有证据的地方写 TODO。
```

## 运行实验与论文流水线

idea 经人工批准后，进入实验与写作阶段（每步都可被 `make` 复现）：

```bash
# 设计协议（experiment-design skill 产出 docs/project_brief.md + docs/experiment_protocol.md）
# 实现最小 pipeline（bioinfo-pipeline skill）：读取 metadata → QC 表 → 图
make snakemake-dry      # Snakemake 干跑，检查 DAG
make snakemake-run      # 真正执行
make figures            # 由数据/结果生成图（图必须由代码生成）

# 记录证据：results/run_registry.yml（provenance）+ results/claim_ledger.yml（claims）
# 只根据 verified claims 写 manuscript（manuscript-writing skill）
make paper-html         # 渲染 Quarto 论文

# 投稿前审计与内部评审
make review             # claims/manuscript/figures 评审 + 三项审计
make audit              # 仅跑 claim/citation/reproducibility 审计
```

## 工作流阶段

定义在 `configs/agent_workflow.yaml`，每个阶段有所需文件、允许/禁止动作和审批门：

```text
idea       → docs/idea_bank.yml, docs/project_brief.md           [需人工批准]
protocol   → docs/experiment_protocol.md, configs/experiment.yaml [需人工批准]
code       → 一次一个模块/脚本，必须带测试与命令日志
results    → results/run_registry.yml, results/claim_ledger.yml  [需真实产物]
manuscript → 无证据的 Results 一律禁止
review     → make review / make audit，产出 4 份审计报告
```

## 项目结构

```text
AGENTS.md                 # 项目宪法：不可造假、证据驱动、人类权威
.agents/skills/           # Codex 科研技能（见下）
configs/                  # project / experiment / agent_workflow 配置
data/                     # 数据；大文件与隐私数据不进 Git
docs/                     # project brief, protocol, idea bank, 审计报告, decision log
literature/               # 检索式, 原始结果, paper cards, gap map, idea bank, BibTeX
manuscript/               # Quarto 论文源文件（main + sections）
results/                  # metrics / tables / figures / claim ledger / run registry
scripts/                  # 可执行脚本（检索、QC、绘图、审计、评审）
src/bioinfo_scientist/    # 可复用、受测试与 mypy 检查的 Python 包
tests/                    # 单元测试（不联网）
workflows/                # Snakemake / Nextflow 流水线
envs/                     # conda 环境定义
```

## Codex Skills

`.agents/skills/` 下的技能各管一段流程：

| Skill | 用途 |
| --- | --- |
| `literature-scout` | 研究方向 → 检索 → paper cards → gap map → novelty risk |
| `idea-generator` | 由文献地图生成、打分、排序 idea，推荐 top idea |
| `idea-novelty` | idea 创新性 / 可行性审计与人工审批门 |
| `experiment-design` | project brief 与 experiment protocol（数据/拆分/baseline/统计） |
| `bioinfo-pipeline` | Snakemake/Nextflow、QC、数据 schema、baseline 模型 |
| `figure-generation` | 由数据/指标/表格生成 manuscript 图 |
| `manuscript-writing` | 由 claim ledger 控制的论文写作 |
| `literature-audit` | 引用核验与 paper cards |
| `statistics-audit` | p 值、多重检验、批次、泄漏、不确定性审计 |
| `reproducibility-audit` | 投稿前的可复现性检查 |
| `reviewer-response` | 模拟同行评审与 rebuttal |

## 常用命令

| 命令 | 作用 |
| --- | --- |
| `make lint` / `make format` | ruff + black + mypy 检查 / 自动格式化 |
| `make test` / `make smoke` | 单元测试 / 最小冒烟 |
| `make snakemake-dry` / `make snakemake-run` | 流水线干跑 / 执行 |
| `make figures` | 由数据生成图 |
| `make review` / `make audit` | 内部评审 / 三项审计 |
| `make paper-html` / `make paper-pdf` | 渲染 Quarto 论文 |
| `make mlflow` | 启动 MLflow UI |

## 常见问题

**Codex 会自动联网检索文献吗？**
不会。Codex 默认不实时联网；文献检索通过 `scripts/literature_search.py`（PubMed + Semantic Scholar）显式执行，结果落盘后再供 skill 使用。

**`generate_ideas.py` 会直接写出 idea 吗？**
不会。它只生成带证据清单的**空槽脚手架**（全是 `TODO`）。真正的 idea 由人类或 Codex 按 `idea-generator` skill、依据 paper cards 与 gap map 填写，避免代码"编造"创新点。

**没有 Semantic Scholar / NCBI API key 能用吗？**
能。基础检索免密钥；高频或大批量时建议加 `--email`（NCBI 礼仪）或申请 API key 以避免限流。

**为什么 `make lint` 里有 mypy？**
`src/` 下的可复用逻辑受 mypy 检查；脚本是薄封装，解析逻辑都在 `src/` 并有不联网的单元测试覆盖。

**大数据 / 模型产物怎么管理？**
不进 Git。用 DVC 或 rsync（见 `scripts/sync_results_from_wsl.sh`、`docs/mac_wsl_workflow.md`）。fastq/bam/vcf/h5ad 等已在 `.gitignore` 中忽略。

## 负责任使用

- 在任何由本系统协助产出的论文中，**明确披露 AI 的使用**（记录于 `docs/ai_use_log.md`）。
- 不提交/上传隐私或临床数据；ML/AIDD 任务检查数据泄漏并使用公平 baseline；omics 统计检查批次/混杂并做多重检验校正。
- Codex 不得自行投稿、联系期刊或做最终科学决策——这些权力始终属于人类研究者与导师。
