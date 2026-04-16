import pandas as pd
import sqlite3
import uuid
from core.parsing.schema import Resume

def resume_to_sqlite(resume: Resume, db_path: str = "resumes.db"):
    r = resume.model_dump()
    resume_id = str(uuid.uuid4())[:8]

    # 1. Prepare Data
    base_data = {
        "resume_id": resume_id,
        "name": r.get("full_name"),
        # **{f"contact_{k}": v for k, v in (r.get("contact") or {}).items()},
        "summary": r.get("summary"),
    }

    # Helper to create DF with resume_id
    def create_df(key):
        data = r.get(key) or []
        # Special handling for project technologies list
        if key == "projects":
            for p in data:
                if isinstance(p.get("technologies"), list):
                    p["technologies"] = ", ".join(p["technologies"])
        if key == "contact":
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame(data)
        if not df.empty:
            df.insert(0, 'resume_id', resume_id)
        return df

    # 2. Write to SQLite
    with sqlite3.connect(db_path) as conn:
        # Save base info
        pd.DataFrame([base_data]).to_sql("resume_base", conn, if_exists="append", index=False)
        # pd.DataFrame([r.get("contact" or [])]).to_sql('contact', conn, if_exists='append', index=False)
        # Save nested lists
        tables = ["contact", "skills", "certifications", "education", "experience", "projects"]
        for table in tables:
            df = create_df(table)
            if not df.empty:
                df.to_sql(table, conn, if_exists="append", index=False)

    return resume_id
