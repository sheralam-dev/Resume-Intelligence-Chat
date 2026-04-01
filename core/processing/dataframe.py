import pandas as pd
from core.parsing.schema import Resume

def resume_to_df(resume: Resume):
    # r = resume.dict()
    r = resume.model_dump() # Dictionary -> key, value pairs

    base = {
        "full_name": r["full_name"],
        "summary": r["summary"],
        **{f"contact_{k}": v for k, v in r["contact"].items() if v != None},
        "ai_ml_skills": ", ".join(r.get("ai_ml_skills", []) or []),
        "technical_skills": ", ".join(r.get("technical_skills", []) or []),
        "certifications": ", ".join(r.get("certifications", []) or [])
    }

    rows = []

    # max length among lists
    max_len = max(
        len(r.get("education") or []),
        len(r.get("experience") or []),
        len(r.get("projects") or []),
        1 # atleast one row.
    )

    for i in range(max_len):
        row = {} #base.copy()

        # education
        educations = r.get("education", []) or []
        if i < len(educations):
            e = educations[i]
            row.update({  # row |= {}
                "edu_institution": e["institution"],
                "edu_degree": e["degree"],
                "edu_start": e["start_date"],
                "edu_end": e["end_date"],
            })

        # experience
        experiences = r.get("experience", []) or []
        if i < len(experiences):
            ex = experiences[i]
            row.update({
                "exp_title": ex["title"],
                "exp_company": ex["company"],
                "exp_start": ex["start_date"],
                "exp_end": ex["end_date"],
            })

        # projects
        projects = r.get("projects", []) or []
        if i < len(projects):
            p = projects[i]
            row.update({
                "proj_name": p["name"],
                "proj_desc": p["description"],
                "proj_tech": ", ".join(p["technologies"]),
                "proj_score": p["difficulty_score"],
            })

        rows.append(row)

    return pd.DataFrame(rows)




def resume_to_dfs(resume: Resume):
    r = resume.model_dump()
    
    # 1. Base Info (Contact, Skills, Summary)
    # Flattens the top-level fields and the nested 'contact' dict
    base_data = {
        "full_name": r.get("full_name"),
        "summary": r.get("summary"),
        **{f"contact_{k}": v for k, v in (r.get("contact") or {}).items()},
        "ai_ml_skills": ", ".join(r.get("ai_ml_skills") or []),
        "technical_skills": ", ".join(r.get("technical_skills") or []),
        "certifications": ", ".join(r.get("certifications") or [])
    }
    df_base = pd.DataFrame([base_data])

    # 2. Education DataFrame
    df_edu = pd.DataFrame(r.get("education") or [])

    # 3. Experience DataFrame
    df_exp = pd.DataFrame(r.get("experience") or [])

    # 4. Projects DataFrame
    # We handle the 'technologies' list by joining it into a string for the CSV/Table view
    projects = r.get("projects") or []
    for p in projects:
        if isinstance(p.get("technologies"), list):
            p["technologies"] = ", ".join(p["technologies"])
    df_proj = pd.DataFrame(projects)

    return {
        "base": df_base,
        "education": df_edu,
        "experience": df_exp,
        "projects": df_proj
    }
