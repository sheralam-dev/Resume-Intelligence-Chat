import pandas as pd

def resume_to_df(resume):
    r = resume.dict()

    base = {
        "full_name": r["full_name"],
        "summary": r["summary"],
        **{f"contact_{k}": v for k, v in r["contact"].items()},
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
        1
    )
    print('max_len: ', max_len)

    for i in range(max_len):
        row = base.copy()

        # education
        educations = r.get("education", []) or []
        if i < len(educations):
            e = educations[i]
            row.update({
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