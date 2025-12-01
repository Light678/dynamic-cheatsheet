import json
import os
import re
import sys


def norm(s: str) -> str:
    """Lowercase + remove all whitespace for robust substring checks."""
    return "".join(s.lower().split())


def parse_options(raw_input: str):
    """
    Parse the options block from raw_input.

    Expects something like:
    Options:
    (A) 2/3
    (B) 1/3
    (C) 1/2
    (D) 1/6

    Returns: dict like {"A": "2/3", "B": "1/3", ...}
    """
    if "Options:" not in raw_input:
        return {}

    part = raw_input.split("Options:", 1)[1]
    lines = [ln.strip() for ln in part.splitlines() if ln.strip()]

    opts = {}
    for ln in lines:
        m = re.match(r"^\(([A-Z])\)\s*(.+)$", ln)
        if m:
            letter = m.group(1)
            text = m.group(2)
            opts[letter] = text
    return opts


def get_target_letter(target: str):
    """
    Extract the letter (A/B/C/...) from target, which may look like '(C)' or 'C'.
    """
    t = target.strip()
    m = re.match(r"^\(([A-Z])\)$", t)
    if m:
        return m.group(1)
    m = re.match(r"^([A-Z])$", t)
    if m:
        return m.group(1)

    # fallback: first capital letter
    m = re.search(r"[A-Z]", t)
    if m:
        return m.group(0)
    return None


def is_correct_entry(obj):
    target = obj.get("target", "")
    final = obj.get("final_answer", "") or ""

    target_letter = get_target_letter(target)
    if not target_letter:
        return False

    nfinal = norm(final)

    # explizit "(C)" suchen
    if norm(f"({target_letter})") in nfinal:
        return True

    # oder nur "C" (falls das Modell nur den Buchstaben schreibt)
    if nfinal == norm(target_letter):
        return True

    return False


def eval_file(path: str):
    total = 0
    correct = 0

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            total += 1
            if is_correct_entry(obj):
                correct += 1

    accuracy = correct / total if total else 0.0
    return total, correct, accuracy


if __name__ == "__main__":
    if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        # Single file mode
        path = sys.argv[1]
        total, correct, acc = eval_file(path)
        print(f"File: {path}")
        print(f"Total samples: {total}")
        print(f"Correct: {correct}")
        print(f"Accuracy: {acc * 100:.2f}%")
    else:
        # Folder mode: evaluate all .jsonl in TEST_RESULTS (or current folder)
        folder = "TEST_RESULTS"
        if not os.path.isdir(folder):
            folder = "."

        print(f"Evaluating all .jsonl files in: {folder}")
        for filename in os.listdir(folder):
            if not filename.endswith(".jsonl"):
                continue
            path = os.path.join(folder, filename)
            total, correct, acc = eval_file(path)
            print(f"{filename}: {correct}/{total} = {acc * 100:.2f}%")

