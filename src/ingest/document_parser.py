import os
import fitz  # PyMuPDF
import json
from email import policy
from email.parser import BytesParser

unstructured_dir = "data/unstructured"
output_file = os.path.join(unstructured_dir, "parsed.jsonl")
parsed_docs = []

# --- PDF PARSING ---
for file in os.listdir(unstructured_dir):
    if file.lower().endswith(".pdf"):
        path = os.path.join(unstructured_dir, file)
        with fitz.open(path) as doc:
            text = "".join(page.get_text() for page in doc)
            parsed_docs.append({
                "type": "pdf",
                "filename": file,
                "text": text
            })

# --- EMAIL PARSING (.eml) ---
for file in os.listdir(unstructured_dir):
    if file.lower().endswith(".eml"):
        path = os.path.join(unstructured_dir, file)
        with open(path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
            subject = msg["subject"]
            body = msg.get_body(preferencelist=('plain')).get_content()
            parsed_docs.append({
                "type": "email",
                "filename": file,
                "subject": subject,
                "body": body
            })

# --- Write to parsed.jsonl ---
with open(output_file, "w") as f:
    for doc in parsed_docs:
        f.write(json.dumps(doc) + "\n")

print(f"✅ Parsed {len(parsed_docs)} documents into {output_file}")
