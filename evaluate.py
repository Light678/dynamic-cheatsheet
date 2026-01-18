import matplotlib.pyplot as plt
import extract_answer as ExAs
import numpy as np


def is_correct(item):
    gt, pred, _ = item
    return gt == pred


def plot_cumulative_accuracy_multi(method_results: dict):
    """
    method_results = {
        "DCRS": results_dcrs,
        "DCCU": results_dccu,
        ...
    }
    """

    plt.figure()

    for method_name, results in method_results.items():
        correct = 0
        cumulative_accuracy = []

        for i, item in enumerate(results, start=1):
            if is_correct(item):
                correct += 1
            cumulative_accuracy.append(correct / i)

        plt.plot(cumulative_accuracy, label=method_name)

    plt.xlabel("Question Index")
    plt.ylabel("Cumulative Accuracy")
    plt.title("Cumulative Accuracy Over Time")
    plt.legend()
    plt.show()


def plot_absolute_accuracy_table_multi(method_results: dict):
    rows = []

    for method_name, results in method_results.items():
        total = len(results)
        correct = sum(1 for item in results if is_correct(item))
        accuracy = correct / total
        rows.append([method_name, correct, total, round(accuracy, 3)])

    plt.figure()
    plt.axis("off")
    plt.table(
        cellText=rows,
        colLabels=["Method", "Correct", "Total", "Accuracy"],
        loc="center"
    )
    plt.title("Table 1: Absolute Accuracy")
    plt.show()


def plot_interval_accuracy_multi(method_results: dict, interval_size=25):
    """
    method_results = {
        "DCRS": results_dcrs,   # z.B. 100 items
        "DCCU": results_dccu,   # z.B. 100 items
        "FH": results_fh        # z.B. 38 items
    }
    """
    
    max_len = max(len(results) for results in method_results.values())

    intervals = [
        (start, min(start + interval_size, max_len))
        for start in range(0, max_len, interval_size)
    ]

    interval_labels = [f"{s}-{e}" for s, e in intervals]

    x = np.arange(len(intervals))
    n_methods = len(method_results)
    width = 0.8 / n_methods

    plt.figure()

    for i, (method_name, results) in enumerate(method_results.items()):
        accuracies = []
        positions = []

        for idx, (start, end) in enumerate(intervals):
            if start >= len(results):
                continue

            segment = results[start:min(end, len(results))]
            correct = sum(1 for gt, pred, _ in segment if gt == pred)
            accuracy = correct / len(segment)

            accuracies.append(accuracy)
            positions.append(x[idx] + i * width)

        plt.bar(
            positions,
            accuracies,
            width=width,
            label=method_name
        )

    plt.xticks(
        x + width * (n_methods - 1) / 2,
        interval_labels
    )

    plt.xlabel("Memory Interval")
    plt.ylabel("Accuracy")
    plt.title("Accuracy by Memory Interval")
    plt.legend()
    plt.show()


def plot_cheatsheet_word_length_multi(method_cs_lengths: dict):
    """
    method_cs_lengths = {
        "DCRS": cs_length_dcrs,
        "DCCU": cs_length_dccu,
        ...
    }
    """

    plt.figure()

    for method_name, cs_length in method_cs_lengths.items():
        lengths = [length for length, _ in cs_length]
        indices = [idx for _, idx in cs_length]
        plt.plot(indices, lengths, label=method_name)

    plt.xlabel("Question Index")
    plt.ylabel("Cheatsheet Word Length")
    plt.title("Cheatsheet Memory Length Over Time")
    plt.legend()
    plt.show()


def plot_correct_instances_multi(method_results: dict):

    methods = list(method_results.keys())

    plt.figure(figsize=(12, 2 + len(methods)))

    for idx_y, results in enumerate(method_results.items()):

        for item in results[1]:
            correct = is_correct(item)
            color = "green" if correct else "red"

            _, _, idx = item
            plt.scatter(idx, idx_y, c=color, s=30)

    plt.yticks(range(len(methods)), methods)
    plt.xlabel("Example Index")
    plt.ylabel("Method")
    plt.title("Correct (green) vs Wrong (red) Predictions per Example")

    plt.grid(axis="x", linestyle="--", alpha=0.4)
    plt.show()


if __name__ == "__main__":

    file_path_dcrs = r"C:\Users\jonas\Documents\Code Files\repo_suzgun\dynamic-cheatsheet\TEST_RESULTS\CommonsenseQA\openai\Retrieval&Synthesis\gpt-4o-mini_DynamicCheatsheet_RetrievalSynthesis_2026-01-18-20-10_DCRS_GPQA_100.jsonl"
    file_path_dccu = r"C:\Users\jonas\Documents\Code Files\repo_suzgun\dynamic-cheatsheet\TEST_RESULTS\CommonsenseQA\openai\Cumulative\gpt-4o-mini_DynamicCheatsheet_Cumulative_2026-01-18-17-49_DCCU_GPQA_100.jsonl"
    file_path_base = r"C:\Users\jonas\Documents\Code Files\repo_suzgun\dynamic-cheatsheet\TEST_RESULTS\CommonsenseQA\openai\Baseline\gpt-4o-mini_default_2026-01-17-19-01_BL_GPQA_100.jsonl"
    file_path_dr = r"C:\Users\jonas\Documents\Code Files\repo_suzgun\dynamic-cheatsheet\TEST_RESULTS\CommonsenseQA\openai\Retrieval\gpt-4o-mini_Dynamic_Retrieval_2026-01-17-19-40_DR_GPQA_100.jsonl"
    file_path_dcempty = r"C:\Users\jonas\Documents\Code Files\repo_suzgun\dynamic-cheatsheet\TEST_RESULTS\CommonsenseQA\openai\EmptyM\gpt-4o-mini_default_2026-01-17-19-09_DCEMPTY_GPQA_100.jsonl"
    file_path_fh = r"C:\Users\jonas\Documents\Code Files\repo_suzgun\dynamic-cheatsheet\TEST_RESULTS\CommonsenseQA\openai\FullHistory\gpt-4o-mini_FullHistoryAppending_2026-01-17-19-22_FH_GPQA_100.jsonl"

    results_dcrs = ExAs.extract_tuples(file_path_dcrs)
    results_dccu = ExAs.extract_tuples(file_path_dccu)
    results_base = ExAs.extract_tuples(file_path_base)
    results_dr = ExAs.extract_tuples(file_path_dr)
    results_dcempty = ExAs.extract_tuples(file_path_dcempty)
    results_fh = ExAs.extract_tuples(file_path_fh)

    cs_length_dcrs = ExAs.extract_cheatsheet_length(file_path_dcrs)
    cs_length_dccu = ExAs.extract_cheatsheet_length(file_path_dccu)
    cs_length_dr = ExAs.extract_cheatsheet_length(file_path_dr)

    method_results = {
        "DCRS": results_dcrs,
        "DCCU": results_dccu,
        "BASELINE": results_base,
        "DR": results_dr,
        "DC-EMPTY": results_dcempty,
        "FH": results_fh
    }

    method_cs_lengths = {
        "DCRS": cs_length_dcrs,
        "DCCU": cs_length_dccu,
        "DR": cs_length_dr
    }

    plot_cumulative_accuracy_multi(method_results)
    plot_absolute_accuracy_table_multi(method_results)
    plot_interval_accuracy_multi(method_results, interval_size=25)
    plot_cheatsheet_word_length_multi(method_cs_lengths)
    plot_correct_instances_multi(method_results)

    # print(results_dcrs)
    # print("---")
    # print(results_base)
    # print("---")
    # print(results_dr)
    # print("---")
    # print(cs_length_dcrs)
