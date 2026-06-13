# BioInfo-Scientist Starter

这是一个面向 **macOS 主力机 + WSL GPU 服务器** 的 Codex 辅助生物信息学/AIDD 论文系统模板。

目标：把论文项目拆成可审计的工程流：idea → 文献 → 实验协议 → pipeline → 结果 → claim ledger → manuscript → internal review。

## 推荐工作模式

- Mac：日常写作、文献、VS Code、Codex、GitHub、轻量测试。
- WSL GPU：训练深度学习模型、运行大计算、保存大数据和 MLflow 结果。
- GitHub：代码和小配置的唯一事实源。
- DVC/rsync：大数据和模型产物不进 Git。
- Codex：只做可验证任务，不凭空写结果或引用。

## 第一次使用

```bash
# 1. 进入项目
cd bioinfo-scientist-starter

# 2. 建议先初始化 git
git init
git add .
git commit -m "Initialize BioInfo-Scientist starter"

# 3. 创建核心环境
mamba env create -f envs/core.yml
conda activate paper-core

# 4. 安装本项目为可编辑包
pip install -e .
pre-commit install

# 5. 跑最小检查
make test
make smoke
make snakemake-dry
make figures
make audit
```

## 推荐目录含义

```text
AGENTS.md                 # Codex 项目宪法
.agents/skills/           # Codex 科研技能
configs/                  # 项目和实验配置
data/                     # 数据；大文件不要提交 Git
docs/                     # project brief, protocol, decision log, AI use log
literature/               # BibTeX, paper cards, reading matrix
manuscript/               # Quarto/LaTeX 论文源文件
results/                  # metrics, tables, figures, claim ledger
scripts/                  # 可执行脚本
src/                      # 可复用 Python 包
tests/                    # 测试
workflows/                # Snakemake/Nextflow workflow
```

## 典型 Codex 任务

```text
使用 $experiment-design skill。请根据 docs/project_brief.md 生成 docs/experiment_protocol.md，
包含数据来源、拆分策略、baseline、统计检验、多重校正、批次效应检查、负对照和预期图表。
不要写代码，不要编造数据。
```

```text
使用 $bioinfo-pipeline skill。请实现一个最小 Snakemake dry-run pipeline：
读取 data/metadata/samples.csv，生成 results/tables/qc_summary.csv 和 results/figures/fig1_qc.pdf。
新增测试并运行 make test 和 make snakemake-dry。
```

```text
使用 $manuscript-writing skill。请只根据 results/claim_ledger.yml 中 status=verified 的 claims
起草 Results 的第一个小节。没有证据的地方写 TODO。
```

## Idea Generator / Literature Scout

给一个研究方向，系统会：检索当前文献 → 整理 paper cards → 画 gap map → 生成并排序 idea →
推荐 top idea → （人工批准后）生成 project brief / experiment protocol。完整流程见
`docs/idea_generation_protocol.md`。检索只走 PubMed (NCBI E-utilities) 和 Semantic Scholar
等公开接口，绝不编造文献。

```bash
# 1. 检索文献（写入 literature/raw/literature_results.json）
python scripts/literature_search.py \
  --query "anti-biofilm antimicrobial peptide machine learning" \
  --max-results 25 --email you@example.com

# 2. 生成结构化 paper cards（已验证元数据自动填，分析字段留 TODO）
python scripts/build_paper_cards.py --input literature/raw/literature_results.json

# 3. 根据 cards + gap_map 生成 idea 脚手架（idea 内容由 idea-generator skill 填）
python scripts/generate_ideas.py --direction "anti-biofilm AMP design with ML" --n-ideas 10
```

配套两个 Codex skill：`.agents/skills/literature-scout/` 和 `.agents/skills/idea-generator/`。
脚本只做检索与脚手架，真正的文献阅读、gap 判断和 idea 生成由 Codex 按 skill 填空，确保可审计、不造假。
