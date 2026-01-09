import os
import time
import pandas as pd
from datasets import load_from_disk
from openai import OpenAI

MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")  # 1536 dims üblich
TASK = "CommonsenseQA"

def main():
    # 1) Dataset laden (muss vorher in input/target Schema konvertiert und save_to_disk gemacht worden sein)
    ds = load_from_disk(f"data/{TASK}")

    # Nimm denselben Split, den ihr benchmarken wollt (oft validation)
    split = os.getenv("SPLIT", "validation")
    inputs = [ex["input"] for ex in ds[split]]

    client = OpenAI()

    rows = []
    for i, text in enumerate(inputs):
        # einfache Rate-limit Freundlichkeit
        if i > 0 and i % 200 == 0:
            time.sleep(1.0)

        emb = client.embeddings.create(
            model=MODEL,
            input=text
        ).data[0].embedding

        rows.append({"input": text, "embedding": str(emb)})

        if (i + 1) % 50 == 0:
            print(f"Embedded {i+1}/{len(inputs)}")

    os.makedirs("embeddings", exist_ok=True)
    out_path = f"embeddings/{TASK}.csv"
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print("Saved:", out_path)

if __name__ == "__main__":
    main()

