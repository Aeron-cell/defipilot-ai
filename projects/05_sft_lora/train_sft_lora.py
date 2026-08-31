"""Minimal TRL/PEFT SFT + LoRA training entrypoint.

Install optional training dependencies from pyproject.toml first.
This script is intentionally model-agnostic: pass any compatible causal LM.
"""
from __future__ import annotations

import argparse
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTConfig, SFTTrainer


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--data", required=True)
    p.add_argument("--output", default="outputs/sft-lora")
    args = p.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(args.model)
    dataset = load_dataset("json", data_files=args.data, split="train")

    peft_config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM")
    config = SFTConfig(
        output_dir=args.output,
        num_train_epochs=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=2e-5,
        logging_steps=5,
        save_steps=100,
        max_seq_length=4096,
    )
    trainer = SFTTrainer(model=model, tokenizer=tokenizer, train_dataset=dataset, peft_config=peft_config, args=config)
    trainer.train()
    trainer.save_model(args.output)


if __name__ == "__main__":
    main()
