---
title: Resume-Intelligence-Chat
emoji: 📸
sdk: streamlit
sdk_version: 1.37.1
app_file: app.py
---
## Resume Intelligence Chat

A Streamlit app that ingests resumes, structures them into a schema, stores them in a SQLite database, and enables natural language querying using LLM-generated SQL.

---

## Features

* **Resume Parsing**: Uses Docling to extract raw text from PDF resumes
* **Structured Extraction**: Pydantic AI agent converts text into a typed `Resume` schema
* **Database Storage**: Extracted data is stored in SQLite
* **Natural Language Queries**:

  * User asks a question
  * LLM generates SQL query
  * Query runs on database
  * Result is fed back to LLM for final answer
* **Chat Interface**: Streamlit-based conversational UI
* **Database Control**: Option to delete/reset database

---

## Architecture

```
PDF Resume
   ↓
Docling Parser
   ↓
Pydantic AI Agent → Resume Schema
   ↓
SQLite Database
   ↓
User Query (NL)
   ↓
LLM → SQL Query
   ↓
Execute on DB
   ↓
LLM → Final Answer
```

---

## Project Structure

```
.
├── app.py
├── core/
│   ├── ingestion/
│   │   └── docling_loader.py
│   ├── parsing/
│   │   ├── extractor.py
│   │   └── schema.py
│   ├── processing/
│   │   └── database.py
│   └── chains/
│       ├── generate_sql_query
│       └── generate_nl_answer
├── data/db/
│   └── resumes.db
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run app

```bash
streamlit run app.py
```

---

## Usage

### Upload & Index

1. Upload one or more PDF resumes
2. Click **"Process & Index Resumes"**
3. Data is parsed, structured, and stored

### Query

* Ask questions like:

  * `List all candidate names`
  * `List complex projects with candidate name`
  * `Show candidates with 5+ years experience`

### Database Reset

* Check **Confirm delete database**
* Click **Delete Database**

---

## Core Components

### 1. Docling Loader

Extracts clean text from PDF resumes.

### 2. Resume Extractor

Uses Pydantic AI agent to map text → structured `Resume` object.

### 3. SQLite Storage

Stores structured resume data for querying.

### 4. SQL Generator

LLM converts user query → SQL statement.

### 5. Answer Generator

LLM converts DB results → natural language response.

---

## Safety Checks

* Only allows `SELECT` / `WITH` queries
* Rejects irrelevant or unsafe queries
* Handles empty results (`NO_DATA`)

---

## Notes

* Minimizes LLM calls by separating SQL generation and response generation
* Works with multiple resumes
* Designed for local/offline LLM setups (e.g., Ollama)

---

## Future Improvements

* Human-in-the-loop SQL approval
* Multi-table schema support
* Better handling of missing/empty fields
* Query caching for performance

---
