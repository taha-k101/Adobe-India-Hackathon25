# import os
# import json
# from pathlib import Path

# def process_pdfs():
#     # Get input and output directories
#     input_dir = Path("/app/input")
#     output_dir = Path("/app/output")
    
#     # Create output directory if it doesn't exist
#     output_dir.mkdir(parents=True, exist_ok=True)
    
#     # Get all PDF files
#     pdf_files = list(input_dir.glob("*.pdf"))
    
#     for pdf_file in pdf_files:
#         # Create dummy JSON data
#         dummy_data = {
#             "title": "Understanding AI",
#             "outline": [
#                 {
#                     "level": "H1",
#                     "text": "Introduction",
#                     "page": 1
#                 },
#                 {
#                     "level": "H2",
#                     "text": "What is AI?",
#                     "page": 2
#                 },
#                 {
#                     "level": "H3",
#                     "text": "History of AI",
#                     "page": 3
#                 }
#             ]
#         }
        
#         # Create output JSON file
#         output_file = output_dir / f"{pdf_file.stem}.json"
#         with open(output_file, "w") as f:
#             json.dump(dummy_data, f, indent=2)
        
#         print(f"Processed {pdf_file.name} -> {output_file.name}")

# if __name__ == "__main__":
#     print("Starting processing pdfs")
#     process_pdfs() 
#     print("completed processing pdfs")

import os
import json
import fitz  # PyMuPDF
from pathlib import Path

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_sizes = []

    # First pass: collect all font sizes
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    font_sizes.append(span["size"])

    # Sort and reduce to unique font sizes
    font_sizes = sorted(list(set(font_sizes)), reverse=True)

    # Heuristic: Largest = H1, next = H2, next = H3
    size_to_level = {}
    if len(font_sizes) >= 1: size_to_level[font_sizes[0]] = "H1"
    if len(font_sizes) >= 2: size_to_level[font_sizes[1]] = "H2"
    if len(font_sizes) >= 3: size_to_level[font_sizes[2]] = "H3"

    # Second pass: extract headings based on size
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    size = span["size"]
                    if not text or len(text) < 4:
                        continue
                    level = size_to_level.get(size)
                    if level:
                        headings.append({
                            "level": level,
                            "text": text,
                            "page": page_num
                        })

    title = os.path.basename(pdf_path).replace(".pdf", "")
    return {
        "title": title,
        "outline": headings
    }

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))
    for pdf_file in pdf_files:
        try:
            outline_data = extract_outline(pdf_file)
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(outline_data, f, indent=2, ensure_ascii=False)
            print(f" Processed: {pdf_file.name}")
        except Exception as e:
            print(f" Failed to process {pdf_file.name}: {e}")

if __name__ == "__main__":
    print(" Starting PDF processing...")
    process_pdfs()
    print(" Finished processing.")