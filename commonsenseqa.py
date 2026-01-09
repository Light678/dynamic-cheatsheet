from datasets import load_dataset, DatasetDict
import os

def format_example(ex):
    stem = ex["question"]  # tau/commonsense_qa: string

    choices = ex["choices"]

    # Fall 1: dict-of-lists: {"label":[...], "text":[...]}
    if isinstance(choices, dict) and "label" in choices and "text" in choices:
        labels = choices["label"]
        texts = choices["text"]
        options = "\n".join([f"({l}) {t}" for l, t in zip(labels, texts)])

    # Fall 2: list-of-dicts: [{"label":"A","text":"..."}, ...]
    elif isinstance(choices, (list, tuple)) and len(choices) > 0 and isinstance(choices[0], dict):
        options = "\n".join([f"({c['label']}) {c['text']}" for c in choices])

    else:
        raise TypeError(f"Unexpected choices format: {type(choices)} -> {choices}")

    inp = f"{stem}\nOptions:\n{options}"
    tgt = f"({ex['answerKey']})"
    return {"input": inp, "target": tgt}


def main():
    ds = load_dataset("tau/commonsense_qa")  # train/validation/test
    ex = ds["train"][0]
    print(type(ex["choices"]), ex["choices"])
    ds2 = DatasetDict()
    for split in ds.keys():
        ds2[split] = ds[split].map(format_example, remove_columns=ds[split].column_names)

    out_path = "data/CommonsenseQA"
    os.makedirs(out_path, exist_ok=True)
    ds2.save_to_disk(out_path)
    print("Saved to:", out_path)

if __name__ == "__main__":
    main()

