import json

def evaluate_jsonl(path):
    total = 0
    correct = 0

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total += 1
            example = json.loads(line)
            if example.get("is_correct") is True:
                correct += 1

    accuracy = correct / total if total > 0 else 0
    return total, correct, accuracy


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python evaluate_jsonl.py <file.jsonl>")
        exit(1)

    path = sys.argv[1]
    total, correct, accuracy = evaluate_jsonl(path)

    print(f"File: {path}")
    print(f"Total samples: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy*100:.2f}%")
