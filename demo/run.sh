#!/bin/bash
conda activate demo
echo "Start Bot"
export HF_TOKEN=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
python3 chatbot.py --path "m-a-p/OpenCodeInterpreter-DS-6.7B"