# Challenge 1b: Multi-Collection PDF Analysis

## Overview
Advanced PDF analysis solution that processes multiple document collections and extracts relevant content based on specific personas and use cases.

## Project Structure
```
Challenge_1b/
├── Collection 1/                    # Travel Planning
│   ├── PDFs/                       # South of France guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 2/                    # Adobe Acrobat Learning
│   ├── PDFs/                       # Acrobat tutorials
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/                       # Cooking guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
└── README.md
```

## Collections

### Collection 1: Travel Planning
- **Challenge ID**: round_1b_002
- **Persona**: Travel Planner
- **Task**: Plan a 4-day trip for 10 college friends to South of France
- **Documents**: 7 travel guides

### Collection 2: Adobe Acrobat Learning
- **Challenge ID**: round_1b_003
- **Persona**: HR Professional
- **Task**: Create and manage fillable forms for onboarding and compliance
- **Documents**: 15 Acrobat guides

### Collection 3: Recipe Collection
- **Challenge ID**: round_1b_001
- **Persona**: Food Contractor
- **Task**: Prepare vegetarian buffet-style dinner menu for corporate gathering
- **Documents**: 9 cooking guides

## Input/Output Format

### Input JSON Structure
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case"
  },
  "documents": [{"filename": "doc.pdf", "title": "Title"}],
  "persona": {"role": "User Persona"},
  "job_to_be_done": {"task": "Use case description"}
}
```

### Output JSON Structure
```json
{
  "metadata": {
    "input_documents": ["list"],
    "persona": "User Persona",
    "job_to_be_done": "Task description"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```

## Key Features
- Persona-based content analysis
- Importance ranking of extracted sections
- Multi-collection document processing
- Structured JSON output with metadata

---

**Note**: This README provides a brief overview of the Challenge 1b solution structure based on available sample data.

# 1. My Approach
We designed a persona-driven content extraction pipeline to analyze multiple PDF documents across three collections. For each collection:

The input JSON specifies the task, user persona, and documents to analyze.

Our script parses each PDF and scans its text content page by page.

We score each page's relevance based on keyword overlap with the persona and task.

The most relevant sections are ranked by importance and structured into the required JSON format.

The solution is fully automated and works for any number of PDFs and personas.

# 2. Models or Libraries Used
Python 3.10

PyMuPDF (fitz) – for extracting text from PDFs

JSON – for reading and writing input/output files

No machine learning model was used; the solution is based on rule-based text scoring using keyword overlap.

# 3. How to Build and Run the Solution
🛠 Build the Docker image:

bash
Copy
Edit
docker build -t adobe1b-runner .
🚀 Run the container (from inside Challenge_1b folder on Windows PowerShell):

powershell
Copy
Edit
docker run --rm `
  -v "${PWD}\Collection 1:/app/Collection 1" `
  -v "${PWD}\Collection 2:/app/Collection 2" `
  -v "${PWD}\Collection 3:/app/Collection 3" `
  --network none `
  adobe1b-runner
📂 Each collection will generate a file:

Collection 1/challenge1b_output.json

Collection 2/challenge1b_output.json

Collection 3/challenge1b_output.json

These contain the extracted and ranked sections in the required schema.