import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# --------- extraction helpers ---------

LETTER_RE = re.compile(r"\(([A-D])\)")  # (A) (B) (C) (D)
BARE_LETTER_RE = re.compile(r"\b([A-D])\b")  # A B C D

ANSWER_TAG_RE = re.compile(r"<answer>\s*(.*?)\s*</answer>", re.IGNORECASE | re.DOTALL)

def normalize_text(s: str) -> str:
    return " ".join(s.strip().split())

def extract_target_letter(obj: Dict[str, Any]) -> Optional[str]:
    """
    Extract the gold label letter from fields like:
      target: "(C)"   or  target: "C"
    """
    target = str(obj.get("target", "") or "").strip()
    if not target:
        return None

    m = LETTER_RE.search(target)
    if m:
        return m.group(1)

    m = re.search(r"\b([A-D])\b", target)
    if m:
        return m.group(1)

    return None

def extract_letter_from_text(text: str) -> Optional[str]:
    """
    Extract a predicted option letter from a blob of text.
    Priority:
    1) inside <answer>...</answer>
    2) explicit "(X)"
    3) bare "X" token
    """
    if not text:
        return None

    # 1) <answer> ... </answer>
    m = ANSWER_TAG_RE.search(text)
    if m:
        inside = normalize_text(m.group(1))
        m2 = LETTER_RE.search(inside)
        if m2:
            return m2.group(1)
        m2 = BARE_LETTER_RE.search(inside)
        if m2:
            return m2.group(1)

    # 2) (X)
    m = LETTER_RE.search(text)
    if m:
        return m.group(1)

    # 3) bare letter
    m = BARE_LETTER_RE.search(text)
    if m:
        return m.group(1)

    return None

def get_candidate_answer_text(obj: Dict[str, Any]) -> Tuple[str, str]:
    """
    Find the best field to read the model answer from.
    Returns (field_name, text).
    """
    candidates = [
        "final_answer",
        "model_output",
        "output",
        "response",
        "prediction",
        "generated_text",
        "answer",
        "completion",
    ]
    for k in candidates:
        v = obj.get(k)
        if isinstance(v, str) and v.strip():
            return k, v

    # sometimes nested
    for k in ["result", "data", "meta"]:
        v = obj.get(k)
        if isinstance(v, dict):
            for kk in candidates:
                vv = v.get(kk)
                if isinstance(vv, str) and vv.strip():
                    return f"{k}.{kk}", vv

    return "", ""

# --------- scoring ---------

def score_file(path: Path) -> None:
    total = 0
    correct = 0
    unparsable_pred = 0
    unparsable_gold = 0

    out_csv = path.with_suffix("")  # drop .jsonl
    out_csv = out_csv.with_name(out_csv.name + "_scored.csv")

    rows = []

    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            total += 1
            obj = json.loads(line)

            gold = extract_target_letter(obj)
            if not gold:
                unparsable_gold += 1

            field, ans_text = get_candidate_answer_text(obj)
            pred = extract_letter_from_text(ans_text)
            if not pred:
                unparsable_pred += 1

            is_correct = (gold is not None and pred is not None and gold == pred)
            if is_correct:
                correct += 1

            # keep a compact view of the question for debugging
            question_preview = ""
            for qk in ["raw_input", "input", "question"]:
                qv = obj.get(qk)
                if isinstance(qv, str) and qv.strip():
                    question_preview = normalize_text(qv)[:200]
                    break

            rows.append({
                "index": idx,
                "gold": gold or "",
                "pred": pred or "",
                "correct": "1" if is_correct else "0",
                "answer_field": field,
                "answer_text_preview": normalize_text(ans_text)[:200],
                "question_preview": question_preview,
            })

    # write CSV
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            w.writeheader()
            w.writerows(rows)

    # write per-item report (one line per question)
    out_txt = path.with_suffix("")  # drop .jsonl
    out_txt = out_txt.with_name(out_txt.name + "_per_item_report.txt")

    with out_txt.open("w", encoding="utf-8") as t:
        for r in rows:
            t.write(
                f"line {r['index']:>3} | gold={r['gold'] or '?'} | pred={r['pred'] or '?'} | "
                f"correct={r['correct']} | {r['question_preview']}\n"
            )

    print(f"Wrote per-item report: {out_txt}")

    # OPTIONAL: also print all lines to console (comment out if too long)
    print("\nPer-item results:")
    for r in rows:
        print(
            f"line {r['index']:>3} | gold={r['gold'] or '?'} | pred={r['pred'] or '?'} | "
            f"correct={r['correct']} | {r['question_preview']}"
        )

    acc = (correct / total) if total else 0.0

    print(f"File: {path}")
    print(f"Total: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {acc*100:.2f}%")
    print(f"Unparsable gold labels: {unparsable_gold}")
    print(f"Unparsable predictions: {unparsable_pred}")
    print(f"Wrote: {out_csv}")

    # show a few mismatches to sanity-check
    mismatches = [r for r in rows if r["correct"] == "0" and r["gold"] and r["pred"]]
    if mismatches:
        print("\nFirst 10 mismatches (gold vs pred):")
        for r in mismatches[:10]:
            print(f"  line {r['index']}: gold={r['gold']} pred={r['pred']} | {r['question_preview'][:120]}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python score_gpqa_jsonl.py <file.jsonl>")
        raise SystemExit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        raise SystemExit(1)

    score_file(path)
