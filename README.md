# TalentLens — Smart Resume Screening and Candidate Ranking Tool

TalentLens is a beginner-friendly web application that helps a recruiter compare candidates against a job description. It looks for job-related skills, education keywords, and stated experience, then creates a clear candidate ranking that a human can review.

> **Important:** TalentLens is an educational project. It supports human review; it must never make automatic hiring decisions.

## Table of contents

- [Project overview](#project-overview)
- [Key features](#key-features)
- [How the ranking works](#how-the-ranking-works)
- [How to use the application](#how-to-use-the-application)
- [Sample dataset](#sample-dataset)
- [CSV import format](#csv-import-format)
- [Project structure](#project-structure)
- [Technology used](#technology-used)
- [Run the project](#run-the-project)
- [Responsible-use statement](#responsible-use-statement)
- [Results](#Results)
- [Limitations](#limitations)
- [Future improvements](#future-improvements)

## Project overview

Recruiters often need to compare many resumes with the same job description. TalentLens makes that first comparison easier and more transparent. A user pastes a job description, adds candidate resume text, chooses score weights, and reviews the generated ranking.

The tool is designed to be easy to demonstrate:

- It runs directly in a browser.
- It does not require a login, database, or server.
- Resume text stays in the browser and is not uploaded anywhere.
- Its sample data is fictional and safe to show in a class project or portfolio.

## Key features

### Job criteria detection

TalentLens checks the job description for common job-related skills such as Python, SQL, Excel, Power BI, JavaScript, communication, and project management. It also recognises common education terms and a stated number of years of experience.

You can also type in your own extra skills (for example, "Zendesk, SEO, negotiation") in the **Add extra skills to look for** box. These are added to the built-in list every time you click **Find job criteria** or **Rank candidates**, so you're never limited to the default skill bank.

### Candidate management

The user can:

- Add one candidate by entering a name and pasting resume text.
- Upload a single `.txt` **or `.pdf`** resume file — text is pulled out of the PDF automatically so you can review it before adding the candidate.
- Import many candidates from a CSV file.
- Remove an individual candidate.
- Reset all job and candidate data safely.

### Transparent, custom ranking

The user controls how much each factor matters:

| Factor | Default weight | What it checks |
| --- | ---: | --- |
| Skills | 70% | Matching job-related skills in the resume |
| Experience | 15% | Stated years of experience compared with the role |
| Education | 15% | Education keywords requested in the job description |

The three weights must total 100%. This makes the scoring rule visible and adjustable instead of hidden.

### Clear results

After ranking, TalentLens shows:

- Candidate rank and overall match percentage
- Matched skills
- Missing job-related skills
- A score breakdown for Skills, Experience, and Education
- Number of candidates, average match score, and the top candidate
- A colour-coded chart comparing every shown candidate's Skills, Experience, and Education scores side by side
- Candidate-name search, plus **minimum match score** and **minimum years of experience** filters, in the final results
- CSV export for opening the ranking in Microsoft Excel — the export follows whatever filters are currently applied

### Built-in demonstration material

Click **Load sample data** for an instant Data Analyst demonstration. The project also contains downloadable sample files inside the `data` folder.

## How the ranking works

TalentLens uses simple keyword matching. It is deliberately easy to explain.

1. The application identifies known skills in the job description.
2. It looks for those same skills in each resume.
3. It checks whether requested education keywords and experience are stated.
4. It applies the user-selected weights and creates a score out of 100.

The simplified formula is:

```text
Total score = Skill score + Experience score + Education score

Skill score      = (matched skills / required skills) × Skills weight
Experience score = (candidate years / required years, maximum 1) × Experience weight
Education score  = Education weight when a requested education keyword is found
```

For example, if a role has four listed skills and a candidate has three of them, their Skills score is `3 ÷ 4 × Skills weight`.

## How to use the application

1. Open `index.html` in a web browser.
2. Paste a job description in **Describe the role**.
3. Click **Find job criteria** to view the detected skills and experience requirement.
4. Adjust Skills, Experience, and Education weights if needed. Make sure they total 100%.
5. Add candidates manually, upload `.txt` resumes, or import a CSV dataset.
6. Click **Rank candidates**.
7. Review every candidate fairly. Use the matched and missing skills as discussion points, not as a final hiring decision.
8. Use **Export results as CSV** to download the ranking.

For a fast demo, click **Load sample data**, then click **Rank candidates**.

## Sample dataset

The `data` folder contains synthetic, fictional data for demonstrations:

- `sample_job_description.txt` — a Data Analyst job description
- `sample_candidates.csv` — ten fictional candidate resumes

No real candidate data is included in this repository.

## CSV import format

To import candidates, the CSV file must contain these two column headings:

```csv
candidate_name,resume_text
Ananya Sharma,"Bachelor degree with Python, SQL and Excel experience."
Rahul Verma,"BSc graduate with SQL, Excel and Power BI projects."
```

The candidate resume text should be wrapped in quotation marks if it includes commas.

## Project structure

```text
smart-resume-screening-tool/
│
├── index.html                     # Page layout and application controls
├── style.css                       # Colours, layout, responsive design
├── script.js                       # Ranking, importing, export, and UI logic
├── README.md                       # Project documentation
├── .gitignore
│
└── data/
    ├── sample_candidates.csv       # Synthetic candidate dataset
    └── sample_job_description.txt  # Sample job description
```

## Technology used

- **HTML** — page structure
- **CSS** — visual design and mobile-friendly layout
- **JavaScript** — screening logic, CSV import/export, search, and interactions

No external framework, database, or API key is required.

## Run the project

### Simple method

1. Download or clone this repository.
2. Double-click `index.html`.
3. The TalentLens application opens in your default web browser.

### With Visual Studio Code

1. Open the project folder in Visual Studio Code.
2. Open `index.html`.
3. You may use the **Live Server** extension if you prefer an auto-refreshing browser preview, but it is optional.
   
### With VS Code Using The python App   
1. Open the project folder in Visual Studio Code
2. then in the terminal Use These
3. pip install -r requirements.txt
   streamlit run app.py

## Responsible-use statement

Hiring decisions affect people’s lives. This project must be used responsibly.

- A human must review every candidate and make the final decision.
- Do not score candidates using protected characteristics such as age, gender, religion, caste, disability, race, nationality, or marital status.
- Consider transferable skills and real project work, not only exact keywords.
- Check the quality and accuracy of resume information yourself.
- Do not upload private or sensitive real resumes to a public version of this project.
## Results 
<img width="1613" height="841" alt="Image" src="https://github.com/user-attachments/assets/f8e6e054-a2bd-47e5-84f2-b0d8d730ac6e" />

## Limitations

- The application uses simple keyword matching; it does not understand the full meaning of a resume.
- It currently supports pasted text, `.txt` files, and text-based `.pdf` files. Scanned/image-only PDFs will not produce readable text.
- PDF reading uses the pdf.js library loaded from a CDN, so an internet connection is needed the first time a PDF is uploaded in a session.
- Education matching is based on words, not verified qualifications.
- Experience is estimated only when the resume clearly states a number of years.
- Data is not saved after the browser page is refreshed.

## Future improvements

- Add PDF and DOCX resume parsing
- Add custom skill lists for different job roles
- Add filters for minimum score and experience
- Add charts showing candidate-skill comparison
- Add secure user accounts, database storage, and role-based access
- Add multi-language support
- Add more accessibility improvements

## Author

Created as a beginner-friendly academic and portfolio project on smart resume screening and candidate ranking.
