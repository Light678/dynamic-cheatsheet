import os
import time
import pandas as pd
from datasets import load_from_disk
from openai import OpenAI

<<<<<<< HEAD

def normalize_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


=======
>>>>>>> 5b27e88 (Synchronized Repo)
MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
TASK = "CommonsenseQA"


def main():
    ds = load_from_disk(f"data/{TASK}")

    split = os.getenv("SPLIT", "validation")
    ds_split = ds[split]

    inputs = [normalize_newlines(ex["input"]) for ex in ds_split]

    client = OpenAI()

    rows = []
    for i, text in enumerate(inputs):
        if i > 0 and i % 200 == 0:
            time.sleep(1.0)

        emb = client.embeddings.create(model=MODEL, input=text).data[0].embedding
        rows.append({"input": text, "embedding": str(emb)})

        if (i + 1) % 50 == 0:
            print(f"Embedded {i+1}/{len(inputs)}")

    os.makedirs("embeddings", exist_ok=True)
    out_path = f"embeddings/{TASK}.csv"
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print("Saved:", out_path)


if __name__ == "__main__":
    main()
