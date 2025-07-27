import os
import json
import fitz  # PyMuPDF
from pathlib import Path

def score_paragraph(paragraph, persona, task):
    combined_keywords = (persona + " " + task).lower().split()
    para = paragraph.lower()
    score = sum(1 for word in combined_keywords if word in para)
    return score

def extract_from_pdf(pdf_path, persona, task):
    doc = fitz.open(pdf_path)
    relevant_sections = []
    refined_subsections = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        page_text = ""

        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    page_text += span["text"] + " "

        score = score_paragraph(page_text, persona, task)

        if score > 1:
            relevant_sections.append({
                "document": os.path.basename(pdf_path),
                "section_title": f"Page {page_num}",
                "importance_rank": score,
                "page_number": page_num
            })
            refined_subsections.append({
                "document": os.path.basename(pdf_path),
                "refined_text": page_text.strip()[:500],
                "page_number": page_num
            })

    return relevant_sections, refined_subsections

def process_collection(folder_name):
    folder = Path(folder_name)
    input_file = folder / "challenge1b_input.json"
    output_file = folder / "challenge1b_output.json"
    pdf_folder = folder / "PDFs"

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    persona = data["persona"]["role"]
    task = data["job_to_be_done"]["task"]
    documents = data["documents"]

    all_sections = []
    all_subsections = []

    for doc in documents:
        pdf_path = pdf_folder / doc["filename"]
        if not pdf_path.exists():
            print(f" PDF not found: {pdf_path}")
            continue
        sections, subs = extract_from_pdf(pdf_path, persona, task)
        all_sections.extend(sections)
        all_subsections.extend(subs)

    all_sections = sorted(all_sections, key=lambda x: -x["importance_rank"])[:5]

    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona,
            "job_to_be_done": task
        },
        "extracted_sections": all_sections,
        "subsection_analysis": all_subsections
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f" Output written to {output_file}")

if __name__ == "__main__":
    for collection in ["Collection 1", "Collection 2", "Collection 3"]:
        print(f" Processing {collection}...")
        process_collection(collection)
import os
import json
import fitz  # PyMuPDF
from pathlib import Path

def score_paragraph(paragraph, persona, task):
    combined_keywords = (persona + " " + task).lower().split()
    para = paragraph.lower()
    score = sum(1 for word in combined_keywords if word in para)
    return score

def extract_from_pdf(pdf_path, persona, task):
    doc = fitz.open(pdf_path)
    relevant_sections = []
    refined_subsections = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        page_text = ""

        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    page_text += span["text"] + " "

        score = score_paragraph(page_text, persona, task)

        if score > 1:
            relevant_sections.append({
                "document": os.path.basename(pdf_path),
                "section_title": f"Page {page_num}",
                "importance_rank": score,
                "page_number": page_num
            })
            refined_subsections.append({
                "document": os.path.basename(pdf_path),
                "refined_text": page_text.strip()[:500],
                "page_number": page_num
            })

    return relevant_sections, refined_subsections

def process_collection(folder_name):
    folder = Path(folder_name)
    input_file = folder / "challenge1b_input.json"
    output_file = folder / "challenge1b_output.json"
    pdf_folder = folder / "PDFs"

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    persona = data["persona"]["role"]
    task = data["job_to_be_done"]["task"]
    documents = data["documents"]

    all_sections = []
    all_subsections = []

    for doc in documents:
        pdf_path = pdf_folder / doc["filename"]
        if not pdf_path.exists():
            print(f" PDF not found: {pdf_path}")
            continue
        sections, subs = extract_from_pdf(pdf_path, persona, task)
        all_sections.extend(sections)
        all_subsections.extend(subs)

    all_sections = sorted(all_sections, key=lambda x: -x["importance_rank"])[:5]

    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona,
            "job_to_be_done": task
        },
        "extracted_sections": all_sections,
        "subsection_analysis": all_subsections
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f" Output written to {output_file}")

if __name__ == "__main__":
    for collection in ["Collection 1", "Collection 2", "Collection 3"]:
        print(f" Processing {collection}...")
        process_collection(collection)