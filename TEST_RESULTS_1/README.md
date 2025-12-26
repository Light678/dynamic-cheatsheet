Baseline:
```
python run_benchmark.py `
  --task "GPQA_Diamond" `
  --approach "default" `
  --model_name "openai/gpt-4o-mini" `
  --generator_prompt_path "prompts/generator_prompt.txt" `
  --max_n_samples 50 `
  --save_directory "TEST_RESULTS" `
  --additional_flag_for_save_path "BL_GPQA_20"
```

Full History:
```
python run_benchmark.py `
  --task "GPQA_Diamond" `
  --approach "FullHistoryAppending" `
  --model_name "openai/gpt-4o-mini" `
  --generator_prompt_path "prompts/generator_prompt.txt" `
  --max_n_samples 50 `
  --save_directory "TEST_RESULTS" `
  --additional_flag_for_save_path "FH_GPQA_20"
```


Retrieval:
```
python run_benchmark.py `
  --task "GPQA_Diamond" `
  --approach "Dynamic_Retrieval" `
  --model_name "openai/gpt-4o-mini" `
  --generator_prompt_path "prompts/generator_prompt.txt" `
  --max_n_samples 50 `
  --save_directory "TEST_RESULTS" `
  --additional_flag_for_save_path "DR_GPQA_20"
```


Cummulative:
```
python run_benchmark.py `
  --task "GPQA_Diamond" `
  --approach "DynamicCheatsheet_Cumulative" `
  --model_name "openai/gpt-4o-mini" `
  --generator_prompt_path "prompts/generator_prompt.txt" `
  --cheatshet_prompt_path "prompts/curator_prompt_for_dc_retrieval_synthesis.txt" `
  --max_n_samples 50 `
  --save_directory "TEST_RESULTS" `
  --additional_flag_for_save_path "DCCU_GPQA_20"
```


Retrieval and Synthesis:
```
python run_benchmark.py `
  --task "GPQA_Diamond" `
  --approach "DynamicCheatsheet_RetrievalSynthesis" `
  --model_name "openai/gpt-4o-mini" `
  --generator_prompt_path "prompts/generator_prompt.txt" `
  --cheatshet_prompt_path "prompts/curator_prompt_for_dc_retrieval_synthesis.txt" `
  --max_n_samples 50 `
  --max_num_rounds 3 `
  --save_directory "TEST_RESULTS" `
  --additional_flag_for_save_path "DCRS_GPQA_20"
```


Empty Memory:
```
python run_benchmark.py `
  --task "GPQA_Diamond" `
  --approach "default" `
  --model_name "openai/gpt-4o-mini" `
  --generator_prompt_path "prompts/generator_prompt_dc_empty.txt" `
  --max_n_samples 50 `
  --save_directory "TEST_RESULTS" `
  --additional_flag_for_save_path "DCEMPTY_GPQA"
```
