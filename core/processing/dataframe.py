import pandas as pd
from core.parsing.schema import Resume
import uuid


def resume_to_dfs(resume: Resume):
    r = resume.model_dump()

    # Flattens the top-level fields and the nested 'contact' dict
    base_data = {
        "name": r.get("full_name"),
        **{f"contact_{k}": v for k, v in (r.get("contact") or {}).items()},
        "summary": r.get("summary"),
    }

    df_base = pd.DataFrame([base_data])

    df_skl = pd.DataFrame(r.get("skills") or [])

    df_cert = pd.DataFrame(r.get("certifications") or [])

    df_edu = pd.DataFrame(r.get("education") or [])

    df_exp = pd.DataFrame(r.get("experience") or [])

    # We handle the 'technologies' list by joining it into a string for the CSV/Table view
    projects = r.get("projects") or []
    for p in projects:
        if isinstance(p.get("technologies"), list):
            p["technologies"] = ", ".join(p["technologies"])
    df_proj = pd.DataFrame(projects)

    dfs = {
        "base": df_base,
        "skills": df_skl,
        "certifications": df_cert,
        "education": df_edu,
        "experience": df_exp,
        "projects": df_proj
    }

    resume_id = str(uuid.uuid4())[:8]  # Short unique ID
    for df in dfs:
        df.insert(0, 'resume_id', resume_id)

    return dfs
