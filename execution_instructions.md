# 🔧 Execution Instructions – Adobe Challenge 2025

This guide provides step-by-step instructions to **build and run Docker containers** for the two challenges:

- ✅ **Challenge 1A** – PDF Title & Heading Extraction  
- ✅ **Challenge 1B** – Persona-Driven Document Intelligence

---

## 📁 Folder Structure

```
Adobe_Challenge/
├── Challenge_1a/
│   ├── input/           # Input PDFs
│   ├── output/          # Output JSON files
│   ├── Dockerfile       # Dockerfile for heading extraction
│   └── solution.py      # Python script for heading extraction
│
├── Challenge_1b/
│   ├── input/           # Input PDFs
│   ├── output/          # Output JSON files
│   ├── Dockerfile       # Dockerfile for persona-based extraction
│   └── solution.py      # Python script for persona-based extraction
```

---

## 🚀 Challenge 1A: PDF Title & Heading Extraction

### 🛠️ 1. Build the Docker Image

From the `Adobe_Challenge` root directory, run:

```bash
docker build --platform linux/amd64 -t challenge1a:adobe ./Challenge_1a
```

### ▶️ 2. Run the Container

```bash
docker run --rm \
    -v "$(pwd)/Challenge_1a/input:/app/input" \
    -v "$(pwd)/Challenge_1a/output:/app/output" \
    --network none \
    challenge1a:adobe
```

---

## 🚀 Challenge 1B: Persona-Driven Document Intelligence

### 🛠️ 1. Build the Docker Image

From the `Adobe_Challenge` root directory, run:

```bash
docker build --platform linux/amd64 -t challenge1b:adobe ./Challenge_1b
```

### ▶️ 2. Run the Container

```bash
docker run --rm \
    -v "$(pwd)/Challenge_1b/input:/app/input" \
    -v "$(pwd)/Challenge_1b/output:/app/output" \
    --network none \
    challenge1b:adobe
```

---

✅ **Note**: Ensure the `input` folders contain the PDFs before execution. Output will be saved as JSON files in the respective `output` directories.
