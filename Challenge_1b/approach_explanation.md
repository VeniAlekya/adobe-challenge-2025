# Challenge 1B: Persona-Driven Document Intelligence

### 🧠 Problem Statement

The goal of this challenge is to build a generic, intelligent document analysis system that extracts and ranks relevant sections from a set of 3–10 diverse PDFs, guided by a given **persona** and their **job-to-be-done**. These PDFs can span a wide range of domains (research papers, textbooks, financial reports, etc.).

---

### ⚙️ Solution Overview

Our system simulates how a domain expert might read and prioritize sections based on relevance to their goal. It accepts a **persona definition**, a **task**, and a **PDF document collection**, and outputs a structured JSON file with:
- Metadata (input files, persona, task, timestamp)
- Top-ranked relevant sections
- Sub-section analysis (refined content)

---

### 🛠️ Key Components

#### 1. **Text Extraction using PyMuPDF**
We use PyMuPDF (`fitz`) to extract structured text from PDFs, preserving layout and metadata like:
- Page numbers
- Font sizes (for hinting heading importance)
- Paragraph blocks

#### 2. **Semantic Matching with TF-IDF + Cosine Similarity**
We create a **composite query** using the persona and job-to-be-done. Then:
- Represent each candidate section and the query using **TF-IDF vectors**
- Score all sections via **cosine similarity**
- Use these scores + font size heuristics to rank sections

#### 3. **Section Filtering and Ranking**
We filter out short or uninformative lines and keep only those with enough content to be meaningful. Then we:
- Select the top 5 most relevant sections (configurable)
- Provide both heading-level (`section_title`) and full-text (`refined_text`) output

---

### 🚀 Offline + Docker-Friendly Design

- No internet calls
- Uses only small, local models (TF-IDF)
- Runs entirely on CPU
- Dockerized with `/app/input` and `/app/output` volume structure

---

### 💡 Generalizability

- Works across domains (novels, textbooks, reports)
- Requires no fine-tuning or domain-specific logic
- Automatically adapts to the persona and task context

---

### ✅ Output Format

JSON structured like:
```json
{
  "metadata": {...},
  "extracted_sections": [...],
  "subsection_analysis": [...]
}
