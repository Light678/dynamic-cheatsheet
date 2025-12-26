import json
import re


def normalize(s: str) -> str:
    if s is None:
        return ""

    s = s.strip().lower()

    s = re.sub(r"\$+", "", s)
    s = s.replace("^", "")
    s = s.replace("~", "")
    s = s.replace("(", "")
    s = s.replace(")", "")
    s = re.sub(r"\\text\s*\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\mathrm\s*\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\,", " ", s)  # \, -> space
    s = re.sub(r"\\;", " ", s)
    s = re.sub(r"\\:", " ", s)
    s = re.sub(r"\\ ", " ", s)
    s = s.replace("×", " x ")
    s = s.replace("·", " x ")
    s = s.replace("*", " x ")
    s = re.sub(r"\\times", " x ", s)
    s = re.sub(r"\btimes\b", " x ", s)
    s = s.replace("\\", " ")

    # ---------- LaTeX-Exponenten vereinheitlichen ----------
    # 10^{k}  -> 10^k   und ähnliche Patterns
    s = re.sub(r"10\s*\^\s*\{\s*([+-]?\d+)\s*\}", r"10^\1", s)  # 10^{+3} -> 10^3
    s = re.sub(r"10\^\{\s*([+-]?\d+)\s*\}", r"10^\1", s)  # 10^{3} -> 10^3

    # auch Formen wie 10 ^ -19  -> 10^-19
    s = re.sub(r"10\s*\^\s*([+-]?\d+)", r"10^\1", s)

    s = " ".join(s.split())

    return s


def extract_tuples(file_path):
    results = []
    flag_correct_answer = False
    with open(file_path, 'r') as f:
        for idx, line in enumerate(f):
            data = json.loads(line)
            target = data["target"].replace("(", "").replace(")", "")
            model_answer = data["final_answer"].replace("(", "").replace(")", "")
            target_context = data["input"]
            escaped_target = re.escape(target)
            check_correct_letter = re.findall(f"\\({escaped_target}\\) (.*?)(?=\n|$)", target_context)
            normalized_model_answer = normalize(model_answer)
            normalized_gold_answer = normalize(check_correct_letter[0])
            if target != model_answer:
                # print(escaped_target, idx)
                # print(model_answer, " and ", normalized_model_answer)
                # print(check_correct_letter[0], " and ", normalized_gold_answer)
                if len(model_answer) == 1 and model_answer.isalpha():
                    # print("false", end="\n")
                    results.append((target, "?", idx))
                    flag_correct_answer = False
                    continue
                if normalized_model_answer in normalized_gold_answer or normalized_gold_answer in normalized_model_answer:
                    flag_correct_answer = True
                    # print("correct", end="\n")

            if flag_correct_answer:
                results.append((target, target, idx))
                flag_correct_answer = False
            else:
                if target == model_answer:
                    results.append((target, model_answer, idx))
                    flag_correct_answer = False
                else:
                    results.append((target, "?", idx))
                    flag_correct_answer = False

    return results


def extract_cheatsheet_length(file_path):
    """
    Calculates the length of the cheatsheet.
    """
    results = []

    with open(file_path, "r") as f:
        for idx, line in enumerate(f):
            data = json.loads(line)
            cheatsheet = data["final_cheatsheet"]

            results.append((len(cheatsheet), idx))

    return results


if __name__ == "__main__":
    file_path = r"C:\Users\jonas\Documents\Code Files\repo_suzgun\dynamic-cheatsheet\TEST_RESULTS\GPQA_Diamond\openai\Cumulative\gpt-4o-mini_DynamicCheatsheet_Cumulative_2025-12-24-15-02_DCCU_GPQA_100.jsonl"
    results = extract_tuples(file_path)
    print(results)
    cs_length = extract_cheatsheet_length(file_path)
    print(cs_length)

