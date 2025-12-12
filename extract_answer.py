import json

def extract_tuples(file_path):
    targets = []
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            target = data["target"].replace("(", "").replace(")", "")
            model_answer = data["final_answer"].replace("(", "").replace(")", "")
            targets.append((target, model_answer))
    
    return targets

if __name__ == "__main__":
    file_path = r"C:\Users\jonas\Documents\Code Files\repo_suzgun\dynamic-cheatsheet\TEST_RESULTS\GPQA_Diamond\openai\1_GPQA_test_Baseline\gpt-4o-mini_default_2025-12-01-20-21_BL_GPQA_20.jsonl"

    results = extract_tuples(file_path)
    print(results)