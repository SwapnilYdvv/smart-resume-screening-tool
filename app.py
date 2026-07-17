"""
TalentLens — Resume Screening & Candidate Ranking (Python / Streamlit version)

This is a Python conversion of the original HTML/CSS/JS TalentLens project.
It keeps the exact same idea: paste a job description, add candidates,
choose score weights, and get a transparent, human-reviewable ranking
based on simple keyword matching.

IMPORTANT: This is an educational tool. It supports human review of
candidates. It must never be used to make an automatic hiring decision,
and it must never score people using protected characteristics such as
age, gender, religion, caste, disability, race, nationality, or marital
status.

Run it with:
    streamlit run app.py
"""

import re
import io
import pandas as pd
import streamlit as st

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


# ---------------------------------------------------------------------------
# Built-in knowledge (same lists as the original script.js)
# ---------------------------------------------------------------------------

SKILL_BANK = [
    "python", "sql", "excel", "power bi", "tableau", "javascript", "html",
    "css", "react", "java", "c++", "machine learning", "data analysis",
    "data visualization", "communication", "leadership", "project management",
    "aws", "azure", "docker", "git", "figma", "salesforce", "marketing",
    "accounting", "finance", "recruitment", "customer service",
]

EDUCATION_WORDS = [
    "bachelor", "b.tech", "b.e.", "bsc", "master", "m.tech", "mba", "msc",
    "phd", "degree",
]

YEARS_PATTERN = re.compile(r"\b(\d+)\+?\s*(?:years?|yrs?)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Core logic (same rules as the original script.js — kept deliberately simple
# and easy to explain, exactly like the original project)
# ---------------------------------------------------------------------------

def find_terms(value: str, terms: list) -> list:
    """Return every term from `terms` that appears inside `value`."""
    lower = value.lower()
    return [term for term in terms if term in lower]


def extract_years(value: str):
    """Pull out a stated number of years of experience, if any."""
    match = YEARS_PATTERN.search(value)
    return match.group(1) if match else None


def job_criteria(job_description: str, custom_skills_raw: str) -> dict:
    """Work out which skills, education words, and years of experience
    the job description is asking for."""
    custom_skills = [s.strip().lower() for s in custom_skills_raw.split(",") if s.strip()]
    skills = list(dict.fromkeys(find_terms(job_description, SKILL_BANK) + custom_skills))
    education = find_terms(job_description, EDUCATION_WORDS)
    years = extract_years(job_description)
    return {"skills": skills, "education": education, "years": years}


def score_candidate(candidate: dict, criteria: dict, weights: dict) -> dict:
    """Score one candidate against the job criteria and chosen weights."""
    found = find_terms(candidate["resume"], criteria["skills"])
    missing = [skill for skill in criteria["skills"] if skill not in found]

    skill_score = (len(found) / len(criteria["skills"])) * weights["skills"] if criteria["skills"] else 0

    education_score = 0
    if criteria["education"] and find_terms(candidate["resume"], criteria["education"]):
        education_score = weights["education"]

    listed_years = extract_years(candidate["resume"])
    experience_score = 0
    if criteria["years"] and listed_years:
        experience_score = min(int(listed_years) / int(criteria["years"]), 1) * weights["experience"]

    total = round(skill_score + education_score + experience_score)

    return {
        **candidate,
        "value": total,
        "found": found,
        "missing": missing,
        "experience": listed_years if listed_years else "Not stated",
        "skill_score": round(skill_score),
        "education_score": round(education_score),
        "experience_score": round(experience_score),
    }


def extract_pdf_text(uploaded_file) -> str:
    """Pull plain text out of an uploaded PDF resume."""
    if PdfReader is None:
        return ""
    reader = PdfReader(uploaded_file)
    parts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(parts).strip()


def sample_job_description() -> str:
    return (
        "Data Analyst needed with Python, SQL, Excel, Power BI, data analysis "
        "and communication skills. A bachelor's degree and 2 years of "
        "experience are preferred."
    )


def sample_candidates() -> list:
    return [
        {
            "name": "Ananya Sharma",
            "resume": "Bachelor's degree in Computer Science. 3 years of experience as a "
                      "Data Analyst using Python, SQL, Excel, Power BI and data analysis. "
                      "Strong communication skills.",
        },
        {
            "name": "Rahul Verma",
            "resume": "BSc graduate with 2 years of experience in SQL, Excel, Tableau and "
                      "data visualization. Good communication and project management skills.",
        },
        {
            "name": "Meera Iyer",
            "resume": "Bachelor degree in Statistics. Intern with Python, Excel, machine "
                      "learning and data analysis projects. Strong presentation skills.",
        },
    ]


# ---------------------------------------------------------------------------
# Streamlit app / UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="TalentLens | Resume Screening", page_icon="🔎", layout="centered")

if "candidates" not in st.session_state:
    st.session_state.candidates = []          # list of {"name":..., "resume":...}
if "last_ranked" not in st.session_state:
    st.session_state.last_ranked = []          # list of scored candidate dicts
if "resume_text_box" not in st.session_state:
    st.session_state.resume_text_box = ""

st.markdown(
    """
    <div style="background:#1d2940;color:white;padding:34px 28px;border-radius:14px;margin-bottom:20px;">
        <p style="letter-spacing:2px;font-size:.72rem;font-weight:700;color:#f4a261;margin:0 0 8px;">
            RESPONSIBLE HIRING ASSISTANT
        </p>
        <h1 style="margin:0;font-size:2.6rem;">Talent<span style="color:#f4a261;">Lens</span></h1>
        <p style="color:#cbd5e1;margin:10px 0 0;">
            Compare candidates against a job description with clear, human-reviewable criteria.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- STEP 1: Describe the role --------------------------------------------
st.header("01 · Describe the role")
st.caption("Paste the job description. We identify important job-related skills and experience.")

job_description = st.text_area("Job description", height=150, key="job_description",
                                placeholder="Example: We need a Data Analyst with Python, SQL, Excel and "
                                            "Power BI. A bachelor's degree and 2 years of experience are preferred.")

custom_skills_raw = st.text_input("Add extra skills to look for (optional)", key="custom_skills",
                                   placeholder="e.g. Zendesk, SEO, negotiation — separate with commas")
st.caption("Use this for skills that aren't in our built-in list. They'll be added every time you find job criteria.")

if st.button("Find job criteria", type="primary"):
    if not job_description.strip():
        st.warning("Please paste a job description first.")
    else:
        st.session_state.criteria_preview = job_criteria(job_description, custom_skills_raw)

if st.session_state.get("criteria_preview"):
    c = st.session_state.criteria_preview
    tags = " ".join(f"`{s}`" for s in c["skills"]) or "No common skills found—try adding skill names."
    st.info(f"**Criteria found:** {tags}" + (f"  \n**{c['years']}+ years experience**" if c["years"] else ""))

st.subheader("Choose score weights")
st.caption("Set how important each job-related factor should be. The three values should total 100.")
w1, w2, w3 = st.columns(3)
skills_weight = w1.number_input("Skills %", min_value=0, max_value=100, value=70, key="skills_weight")
experience_weight = w2.number_input("Experience %", min_value=0, max_value=100, value=15, key="experience_weight")
education_weight = w3.number_input("Education %", min_value=0, max_value=100, value=15, key="education_weight")
weight_total = skills_weight + experience_weight + education_weight
if weight_total == 100:
    st.success("Total: 100% ✓")
else:
    st.error(f"Total: {weight_total}% — please make it 100%.")

st.divider()

# --- STEP 2: Add candidates -------------------------------------------------
st.header("02 · Add candidates")
st.caption("Use resume text only. Names and contact details are not used in the score.")

col_name, col_upload, col_csv = st.columns(3)
with col_name:
    candidate_name = st.text_input("Candidate name", key="candidate_name", placeholder="e.g. Ananya Sharma")
with col_upload:
    resume_file = st.file_uploader("Or upload a .txt or .pdf resume", type=["txt", "pdf"], key="resume_file")
    if resume_file is not None:
        if resume_file.type == "application/pdf" or resume_file.name.lower().endswith(".pdf"):
            with st.spinner("Reading PDF…"):
                pdf_text = extract_pdf_text(resume_file)
            if pdf_text:
                st.session_state.resume_text_box = pdf_text
                st.caption("PDF text loaded. Please check it looks right before adding the candidate.")
            else:
                st.caption("Could not find readable text in this PDF—it may be a scanned image.")
        else:
            st.session_state.resume_text_box = resume_file.read().decode("utf-8", errors="ignore")
with col_csv:
    csv_file = st.file_uploader("Or import a candidate CSV", type=["csv"], key="csv_file")
    if csv_file is not None:
        try:
            df = pd.read_csv(csv_file)
            df.columns = [c.strip().lower() for c in df.columns]
            if "candidate_name" not in df.columns or "resume_text" not in df.columns:
                st.error("Your CSV needs candidate_name and resume_text columns.")
            else:
                imported = [
                    {"name": str(row["candidate_name"]), "resume": str(row["resume_text"])}
                    for _, row in df.iterrows()
                    if pd.notna(row["candidate_name"]) and pd.notna(row["resume_text"])
                ]
                if st.button(f"Confirm import of {len(imported)} candidates"):
                    st.session_state.candidates.extend(imported)
                    st.session_state.last_ranked = []
                    st.rerun()
        except Exception:
            st.error("Could not read that CSV file. Please check the format.")

resume_text = st.text_area("Resume text", height=180, key="resume_text_box",
                            placeholder="Paste a resume here. Include skills, education, projects and experience.")

b1, b2, b3 = st.columns(3)
if b1.button("Add candidate", type="secondary"):
    if not candidate_name.strip() or not resume_text.strip():
        st.warning("Please enter both a candidate name and resume text.")
    else:
        st.session_state.candidates.append({"name": candidate_name.strip(), "resume": resume_text.strip()})
        st.session_state.last_ranked = []
        st.rerun()

if b2.button("Load sample data"):
    st.session_state.job_description = sample_job_description()
    st.session_state.candidates = sample_candidates()
    st.session_state.last_ranked = []
    st.session_state.criteria_preview = job_criteria(sample_job_description(), "")
    st.rerun()

if b3.button("Reset all data"):
    st.session_state.candidates = []
    st.session_state.last_ranked = []
    st.session_state.job_description = ""
    st.session_state.candidate_name = ""
    st.session_state.resume_text_box = ""
    st.session_state.criteria_preview = None
    st.rerun()

if st.session_state.candidates:
    st.write("**Candidates added:**")
    for i, c in enumerate(st.session_state.candidates):
        cc1, cc2 = st.columns([5, 1])
        cc1.write(f"• {c['name']}")
        if cc2.button("Remove", key=f"remove_{i}"):
            st.session_state.candidates.pop(i)
            st.session_state.last_ranked = []
            st.rerun()

st.caption("Tip: add at least two candidates, then rank them below.")

st.divider()

# --- STEP 3: Review the ranking --------------------------------------------
st.header("03 · Review the ranking")
st.caption("Scores are an aid—not a hiring decision. Always review candidates yourself.")

if st.button("Rank candidates", type="primary"):
    if not job_description.strip() or not st.session_state.candidates:
        st.warning("Add a job description and at least one candidate first.")
    else:
        criteria = job_criteria(job_description, custom_skills_raw)
        if not criteria["skills"]:
            st.warning("Please include at least one skill from the job description, such as Python, SQL, or Excel.")
        elif weight_total != 100:
            st.warning("Your score weights must add up to 100%.")
        else:
            weights = {"skills": skills_weight, "experience": experience_weight, "education": education_weight}
            ranked = [score_candidate(c, criteria, weights) for c in st.session_state.candidates]
            ranked.sort(key=lambda c: c["value"], reverse=True)
            st.session_state.last_ranked = ranked

if st.session_state.last_ranked:
    name_filter = st.text_input("Find a candidate in the results", key="result_filter",
                                 placeholder="Type a candidate name")
    f1, f2 = st.columns(2)
    min_score = f1.number_input("Minimum match score %", min_value=0, max_value=100, value=0, key="min_score_filter")
    min_experience = f2.number_input("Minimum years of experience", min_value=0, value=0, key="min_experience_filter")

    ranked = st.session_state.last_ranked
    shown = [
        c for c in ranked
        if name_filter.lower() in c["name"].lower()
        and c["value"] >= min_score
        and (int(c["experience"]) if str(c["experience"]).isdigit() else 0) >= min_experience
    ]

    total = len(ranked)
    average = round(sum(c["value"] for c in ranked) / total)
    top = ranked[0]
    s1, s2, s3 = st.columns(3)
    s1.metric("CANDIDATES", total)
    s2.metric("AVERAGE MATCH", f"{average}%")
    s3.metric("TOP MATCH", f"{top['name']} ({top['value']}%)")

    if not shown:
        st.info("No candidate matches those filters.")
    else:
        for c in shown:
            rank_number = ranked.index(c) + 1
            with st.container(border=True):
                r1, r2 = st.columns([1, 6])
                r1.markdown(f"### #{rank_number}")
                r2.markdown(f"**{c['name']}** — {c['value']}% match")
                r2.progress(min(c["value"], 100) / 100)
                r2.caption(f"Matched: {', '.join(c['found']) or 'No listed skills'}")
                r2.caption(f"Missing: {', '.join(c['missing']) or 'No listed skills missing'}")
                r2.caption(
                    f"Score breakdown — Skills: {c['skill_score']}% · "
                    f"Experience: {c['experience_score']}% · Education: {c['education_score']}%"
                )

        # Chart: stacked score comparison
        chart_df = pd.DataFrame(
            [
                {"Candidate": c["name"], "Skills": c["skill_score"],
                 "Experience": c["experience_score"], "Education": c["education_score"]}
                for c in shown
            ]
        ).set_index("Candidate")
        st.subheader("Score comparison")
        st.bar_chart(chart_df, color=["#2a9d8f", "#f4a261", "#8ab6d6"])

        # CSV export
        export_rows = [
            {
                "Rank": ranked.index(c) + 1,
                "Candidate": c["name"],
                "Match score": f"{c['value']}%",
                "Matched skills": "; ".join(c["found"]),
                "Missing skills": "; ".join(c["missing"]),
                "Stated experience": c["experience"],
            }
            for c in shown
        ]
        export_df = pd.DataFrame(export_rows)
        csv_bytes = export_df.to_csv(index=False).encode("utf-8")
        st.download_button("Export results as CSV", data=csv_bytes,
                            file_name="talentlens-candidate-ranking.csv", mime="text/csv")

    if not name_filter:
        st.warning(
            "**Human review required:** This is a simple keyword comparison, not an automated hiring "
            "decision. Check each resume fairly, consider transferable skills, and never use protected "
            "personal characteristics to rank people."
        )
else:
    st.info("Add a role and one or more candidates, then click **Rank candidates** to see the comparison.")

st.markdown(
    "<p style='text-align:center;color:#64748b;font-size:.82rem;margin-top:30px;'>"
    "This demo uses simple keyword matching. All data stays on your own computer while the app runs."
    "</p>",
    unsafe_allow_html=True,
)
