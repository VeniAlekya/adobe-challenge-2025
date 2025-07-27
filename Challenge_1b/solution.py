import fitz
import os
import json
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class PersonaDrivenDocumentAnalyzer:
    def __init__(self, pdf_paths, persona, job_to_be_done):
        self.pdf_paths = pdf_paths
        self.persona = persona
        self.job = job_to_be_done
        self.context_query = persona + " " + job_to_be_done
        self.sections = []

    def extract_sections(self):
        for pdf_path in self.pdf_paths:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                blocks = page.get_text("dict")["blocks"]
                for b in blocks:
                    if "lines" not in b:
                        continue
                    for line in b["lines"]:
                        text = " ".join([span["text"] for span in line["spans"] if span["text"].strip()])
                        if not text or len(text.split()) < 3:
                            continue
                        font_sizes = [round(span["size"]) for span in line["spans"]]
                        avg_size = sum(font_sizes) / len(font_sizes)
                        self.sections.append({
                            "document": os.path.basename(pdf_path),
                            "text": text.strip(),
                            "page_number": page_num + 1,
                            "font_size": avg_size
                        })
            doc.close()

    def rank_sections(self, top_k=5):
        texts = [sec["text"] for sec in self.sections]
        tfidf = TfidfVectorizer().fit_transform([self.context_query] + texts)
        scores = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
        for idx, sec in enumerate(self.sections):
            sec["score"] = scores[idx]

        ranked = sorted(self.sections, key=lambda x: (-x["score"], -x["font_size"]))
        top_sections = ranked[:top_k]

        extracted = []
        analysis = []

        for rank, sec in enumerate(top_sections, 1):
            extracted.append({
                "document": sec["document"],
                "section_title": sec["text"][:80],
                "importance_rank": rank,
                "page_number": sec["page_number"]
            })
            analysis.append({
                "document": sec["document"],
                "refined_text": sec["text"],
                "page_number": sec["page_number"]
            })

        return extracted, analysis

    def build_output(self):
        self.extract_sections()
        extracted_sections, subsection_analysis = self.rank_sections()

        return {
            "metadata": {
                "input_documents": [os.path.basename(p) for p in self.pdf_paths],
                "persona": self.persona,
                "job_to_be_done": self.job,
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analysis
        }


# ---------- 🔽 Example Usage ----------
if __name__ == "__main__":
    folder = "D:/sem/6th sem/Term Paper"
    pdf_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".pdf")]

    persona = "Travel Planner"
    job = "Plan a trip of 4 days for a group of 10 college friends."

    analyzer = PersonaDrivenDocumentAnalyzer(pdf_files, persona, job)
    output = analyzer.build_output()

    with open("../../challenge1b_output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("✅ challenge1b_output.json generated.")
