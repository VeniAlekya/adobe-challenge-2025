import fitz
import json
import re
import os
# Different types of conditions for heading detection
class PDFHeadingExtractor:
    def __init__(self, min_font_size=10):
        self.min_font_size = min_font_size

    def is_formula(self, text: str) -> bool:
        return bool(re.search(r'[=+\-*/^]|sin|cos|tan|log|\$|\\[a-zA-Z]+\{.*?\}', text))

    def is_caption(self, text: str) -> bool:
        return bool(re.search(r'\b(Table|Figure|Fig\.?|Listing)\s*\d+', text, re.IGNORECASE))

    def is_number_or_symbols(self, text: str) -> bool:
        return bool(re.fullmatch(r'[\d\s\W]+', text)) or bool(re.search(r'[():{}\[\]<>\d@#^+=_|~$%*\"\';]', text))

    def starts_with_uppercase(self, text: str) -> bool:
        return text and text.strip()[0].isupper()

    def is_bold(self, font_name: str, flags: int) -> bool:
        return ('bold' in font_name.lower()) or (flags & (2**4 | 2**5 | 2**16 | 2**18))

    def is_black(self, rgb, threshold=60):
        r, g, b = rgb
        return r < threshold and g < threshold and b < threshold

    def is_fiction_heading(self, text: str) -> bool:
        return bool(re.match(
            r'^(Prologue|Chapter\s+\d+|Trigger Warning|Playlist|Epilogue|Act\s+\w+|Part\s+\w+)\b',
            text.strip(), re.IGNORECASE
        ))

    def is_heading_candidate(self, text: str) -> bool:
        words = text.strip().split()
        return (
            1 <= len(words) <= 9 and
            not self.is_formula(text) and
            not self.is_caption(text) and
            not self.is_number_or_symbols(text) and
            self.starts_with_uppercase(text)
        )

    def extract_headings(self, pdf_path):
        doc = fitz.open(pdf_path)
        candidate_lines = []

        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    if not line["spans"]:
                        continue

                    text = "".join(s["text"] for s in line["spans"]).strip()
                    span = line["spans"][0]
                    font_size = round(span["size"], 1)
                    font_name = span["font"]
                    flags = span["flags"]
                    color_rgb = tuple(int(span["color"] >> i & 0xFF) for i in (16, 8, 0))

                    # Accept either fiction-style heading or a bold, large academic heading
                    is_fiction = self.is_fiction_heading(text)
                    is_academic = (
                        self.is_heading_candidate(text)
                        and self.is_bold(font_name, flags)
                        and font_size >= self.min_font_size
                    )

                    if (is_fiction or is_academic) and text:
                        candidate_lines.append({
                            "text": text,
                            "font_size": font_size,
                            "font": font_name,
                            "color": color_rgb,
                            "page": page_num + 1
                        })

        # Detect title and heading levels
        top_sizes = sorted({line["font_size"] for line in candidate_lines}, reverse=True)[:3]
        size_to_level = {size: f"H{i+1}" for i, size in enumerate(top_sizes)}

        title = ""
        seen = set()
        outline = []

        for line in candidate_lines:
            size = line["font_size"]
            level = size_to_level.get(size, "H3")

            if not title and line["page"] == 1 and self.is_black(line["color"]):
                title = line["text"]

            if line["text"] not in seen:
                outline.append({
                    "level": level,
                    "text": line["text"],
                    "page": line["page"]
                })
                seen.add(line["text"])

        return {"title": title, "outline": outline}


if __name__ == "__main__":
    PDF_PATH = "PDF path"
    extractor = PDFHeadingExtractor(min_font_size=10)
    result = extractor.extract_headings(PDF_PATH)
    print(json.dumps(result, indent=2, ensure_ascii=False))
