# Adobe “Connecting the Dots” Challenge 2025

This repository contains Dockerized solutions for:

- ✅ **Challenge 1A**: Extract Title + H1, H2, H3 Headings from PDFs.
- ✅ **Challenge 1B**: Persona-Driven Section Extraction from 3–10 PDFs.

Both solutions run inside Docker, without internet, and process PDFs placed in `/app/input`.

---

## 🐳 Docker Instructions

### 🔹 Challenge 1A: Heading Detection

#### 📁 Folder: `Challenge_1a/`

#### 🔨 Build Image
```bash
docker build --platform linux/amd64 -t challenge1a:sol123 Challenge_1a
