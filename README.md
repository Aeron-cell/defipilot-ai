# LLM Post-Training Engineer Portfolio

面向 **Training Engineer / LLM 后训练工程师 / Agent Training Engineer** 岗位的可验证作品集，重点覆盖金融 Excel Agent 场景中的：数据构造、SFT、偏好优化、工具调用、评估与回归。

## 为什么做这个仓库

目标岗位要求从零搭建 post-training pipeline，而不是只在现有 pipeline 上调参。因此本仓库按完整闭环拆成 5 个可独立讲解的项目：

1. **Trajectory Builder**：把 Claude/Agent 交互轨迹转成可训练 SFT 数据。
2. **Finance Eval Harness**：对数值准确性、公式/关键字段、工具成功率、稳定性进行自动评估。
3. **Excel Tool-Use Harness**：构建确定性 Excel-like 工具环境，生成与复现多步工具调用轨迹。
4. **Preference Data Builder**：把候选回答与评估分数转成 DPO chosen/rejected 偏好对。
5. **SFT + LoRA Trainer**：使用 Transformers + TRL + PEFT 进行监督微调。

## 目录

```text
projects/
├── 01_trajectory_builder/trajectory_builder.py
├── 02_finance_eval/eval_harness.py
├── 03_tool_use_excel/mock_excel_agent.py
├── 04_preference_data/build_dpo_pairs.py
└── 05_sft_lora/train_sft_lora.py
```

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

python projects/02_finance_eval/eval_harness.py
python projects/03_tool_use_excel/mock_excel_agent.py
```

如需训练：

```bash
pip install -e '.[train]'
python projects/05_sft_lora/train_sft_lora.py \
  --model <your-open-model> \
  --data <sft-jsonl> \
  --output outputs/sft-lora
```

## 岗位能力映射

| JD 能力 | 仓库证明 |
|---|---|
| 从数据构造到训练的完整 pipeline | 01 + 05 |
| SFT / DPO / RLHF 思维 | 01 + 04 + 05 |
| PyTorch/训练工程能力 | 05 |
| Agent / Function Calling | 01 + 03 |
| Excel / 精确数值任务 | 02 + 03 |
| 评估体系设计 | 02 |
| 可解释性和稳定性 | 02 的 token/数值/工具/稳定性指标 |

## 面试前必须补齐的实验

当前仓库已经搭好了代码骨架，但真正能把简历从“转型候选人”提升到“可用 Training Engineer”的关键，是补齐真实训练结果：

- 选择一个 0.5B–3B 级开源模型；
- 自己构造 500–3000 条 finance/tool-use SFT 数据；
- 跑一次 LoRA SFT；
- 使用固定 eval set 对比 base vs SFT；
- 构造 200–1000 对 preference data，再跑一次 DPO；
- README 中记录：GPU、显存、训练时间、loss、准确率、工具成功率、失败案例；
- 至少挑 10 个失败样本做 error taxonomy，并说明下一轮如何改数据。

## 推荐演示任务

- 给定收入、成本和增长率，构建 3 年现金流预测表；
- 根据无风险利率、Beta、ERP、债务成本计算 WACC；
- 完成简化 DCF 并返回关键公式与最终估值；
- 从表格中定位错误公式并修复；
- 用工具调用完成“读取 → 计算 → 写回 → 校验”的多步任务。

## 技术栈

Python · PyTorch · Transformers · TRL · PEFT · Pandas · Agent Tool Use · Function Calling · Evaluation · SFT · DPO

## 下一步

见 `LEARNING_ROADMAP.md`：按照 8 周路线把仓库从代码骨架升级为真正可用于面试的训练实验作品集。
