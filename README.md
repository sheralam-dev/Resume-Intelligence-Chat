title: Caption Gen
emoji: 📸
sdk: streamlit
sdk_version: 1.43.0
app_file: app.py


# CV Analyzer (AI-Powered Resume Parser)

A Streamlit-based app that extracts structured data from CVs (PDF) using **Docling + Agentic AI + Pydantic schema**, and converts it into a clean, downloadable CSV.

---

## Features

- Upload CV (PDF)
- Parse document using Docling
- Extract structured data using LLM agent
- Validate with Pydantic schema
- Convert to Pandas DataFrame
- View extracted data in UI
- Download as CSV

---

## Tech Stack

- **Streamlit** – UI
- **Docling** – PDF parsing
- **Pydantic / pydantic-ai** – structured extraction
- **Hugging Face / LLM** – inference
- **Pandas** – data processing

---

## Setup

### 1. Clone repo
```bash
git clone https://github.com/your-username/cv-analyzer.git
cd cv-analyzer
````

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Create a `.env` file:

```
HF_TOKEN=your_huggingface_token
```

> `.env` is ignored via `.gitignore`

---

## Run App

```bash
streamlit run app.py
```

---

## How it works

1. User uploads CV (PDF)
2. Docling converts PDF → structured text/markdown
3. LLM agent extracts data using predefined schema
4. Output is validated via Pydantic
5. Data is converted into a DataFrame
6. User can view and download CSV

---

## Notes

* Schema is designed for **AI/ML-focused resumes**
* Missing fields are returned as `null` (no hallucination policy)
* Dates are stored as strings to avoid parsing errors
* Validation is relaxed to improve LLM compatibility

---

## Limitations

* LLM may still produce inconsistent outputs for poorly formatted CVs
* Complex layouts (tables, multi-column PDFs) may affect parsing quality
* Requires internet access for model inference

---

## Future Improvements

* Multi-CV batch processing
* Candidate scoring & ranking
* Semantic search over resumes (FAISS)
* UI improvements (filters, charts)
* Export to JSON / Excel

---

## License

MIT License

```
```