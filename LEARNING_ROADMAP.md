# 8 周 Training Engineer 学习与作品集路线

目标：从 AI 应用工程背景转到能独立搭建 **数据 → SFT → DPO/RLHF → Eval → 迭代** 的 LLM 后训练工程师。

## Week 1：PyTorch 与 Transformer 训练底座

学习：tensor/autograd、Dataset/DataLoader、optimizer、scheduler、mixed precision、gradient accumulation、checkpoint；Transformer attention、causal LM、tokenizer、chat template。

输出：手写一个最小 PyTorch 训练循环；能解释 forward/backward、loss、batch、显存为什么变化。

验收：不用复制模板，能把一个小文本数据集训练起来，并画出 train loss。

## Week 2：SFT 数据与 LoRA/QLoRA

学习：instruction/chat 数据格式、assistant-only loss、padding/masking、packing、LoRA 原理、rank/alpha/dropout、QLoRA/NF4。

输出：扩充 `01_trajectory_builder`，生成 500–3000 条 finance/tool-use SFT JSONL；使用 `05_sft_lora` 完成一次开源小模型 LoRA SFT。

验收：README 记录 base 与 SFT 的至少 50 条固定评估结果。

## Week 3：Agent / Function Calling 后训练

学习：tool schema、tool selection、argument generation、observation consumption、多步 trajectory、ReAct、错误恢复。

输出：扩充 `03_tool_use_excel`：read_cell/write_cell/sum/rate_of_change/npv/irr 等工具；自动生成 200+ 条多步轨迹。

验收：统计 tool selection accuracy、argument exact match、execution success rate、task success rate。

## Week 4：金融 Excel 领域能力

学习：三张表基础、现金流、利润率、财务比率、WACC、DCF、倍数估值；Excel 公式、引用、表格错误类型。

输出：制作 100–300 个金融任务 eval set，覆盖正常样本、边界样本和故意错误样本。

验收：对每个任务给出唯一可验证答案或容差规则，避免“看起来对”式评估。

## Week 5：Evaluation Harness

学习：exact match、numeric tolerance、LLM-as-judge 的风险、pairwise eval、pass@k、稳定性、分层指标、error taxonomy。

输出：扩充 `02_finance_eval`，支持 JSONL 批量评估、CSV 报告、按任务类型聚合。

验收：能回答“模型提升了多少、提升在哪里、退化在哪里、是否显著”。

## Week 6：DPO / Preference Optimization

学习：preference data、chosen/rejected、DPO objective、beta、reference model、数据质量；理解 PPO/RLHF 的 reward model 与 policy optimization 流程。

输出：用 `04_preference_data` 从候选回答构造偏好对，完成一次小规模 DPO。

验收：对比 Base → SFT → DPO 三个 checkpoint 的同一 eval set。

## Week 7：完整 Post-Training Pipeline

学习：数据版本、实验配置、seed、checkpoint、评估门禁、失败样本回流、训练成本和复现。

输出：一个命令串起 prepare_data → train_sft → eval → build_preferences → train_dpo → eval。

验收：换一台机器只看 README 也能复现实验。

## Week 8：岗位面试与开源包装

完成：

1. README 加实验表：模型、数据量、GPU、显存、耗时、SFT loss、numeric accuracy、tool success、overall score。
2. 写一篇 `POST_TRAINING_REPORT.md`，说明失败类型与第二轮训练策略。
3. 准备 10 分钟项目演示：问题 → 数据 → 训练 → Eval → 失败案例 → 改进。
4. 准备常见面试题：SFT vs DPO vs PPO、LoRA、mask、packing、reward hacking、KL、工具调用训练、数值评估、数据泄漏。

## 每天建议节奏

- 1 小时：理论/论文/官方文档
- 2 小时：代码与实验
- 1 小时：整理实验结果、错误样本和 README

不要只“学完课程”。每周必须产生一个 GitHub commit、一组可复现结果和一段能在面试中解释的结论。

## 最终胜任标准

你应该能够白板讲清并实际完成：

`raw traces → cleaning/filtering → SFT dataset → LoRA SFT → fixed eval → error analysis → preference pairs → DPO/RLHF → regression eval → next-round data strategy`

并且能针对 Excel/金融 Agent 解释为什么仅看语言流畅度不够，必须单独衡量数值正确性、公式/工具执行、稳定性和可解释性。
