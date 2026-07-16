# TalentLens — Smart Resume Screening and Candidate Ranking Tool

TalentLens is a beginner-friendly front-end project that compares resume text with a job description and produces a transparent candidate ranking.

## What it does

- Extracts common skills from a job description
- Lets a recruiter paste or upload `.txt` resume content
- Ranks candidates by job-related skill match, education keywords, and stated experience
- Lets the user set the score weight for skills, experience, and education
- Shows both matched and missing skills for each candidate
- Includes one-click sample data for a polished project demonstration
- Exports ranked results as a CSV file, which opens in Excel
- Includes a synthetic dataset with one job description and ten fictional candidate resumes
- Imports multiple candidates from a CSV file
- Shows a results dashboard with candidate count, average match score, and top match
- Lets the recruiter search within the final candidate ranking
- Runs entirely in the browser: no database, login, or resume upload is required

## How to run it

1. Download or clone this project.
2. Double-click `index.html`.
3. It opens in your web browser. Paste a job description and candidate resumes to try it.

## Technology used

- HTML
- CSS
- JavaScript

## Sample dataset

The `data` folder contains a ready-to-use dataset for demonstrating the project:

- `sample_job_description.txt` — a Data Analyst job description
- `sample_candidates.csv` — ten fictional candidate resumes

All dataset content is synthetic and contains no real candidate information.

## Important responsible-use note

This project is an educational demo. It uses simple keyword matching and should only support—not replace—fair human review. It must not be used to make automatic hiring decisions or to evaluate protected personal characteristics.

## Future improvements

- Support PDF and DOCX file parsing
- Add user accounts and secure data storage
