import os
import json

input_path = "feedback_log.jsonl"
output_path = "data/fine_tune.jsonl"

os.makedirs("data", exist_ok=True)
count = 0

with open(input_path, "r") as infile, open(output_path, "w") as outfile:
    for line in infile:
        log = json.loads(line)
        if log.get("rating") == 1:
            formatted = {
                "prompt": f"Question: {log['query']}\n\n",
                "completion": log["answer"]
            }
            json.dump(formatted, outfile)
            outfile.write("\n")
            count += 1

print(f"✅ Saved {count} prompt-completion pairs to {output_path}")
