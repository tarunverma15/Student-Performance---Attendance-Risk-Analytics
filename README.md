# Student Performance & Academic Risk Analytics

## Project Overview
Analyzed a relational education dataset (students, teachers, courses,
enrollments) covering 500 students, 17 courses, and ~5,000 enrollment
records across two semesters, to identify at-risk students, measure the
attendance-performance relationship, and evaluate subject/teacher-level
outcomes using multi-table SQL and a reporting dashboard.

## Honest framing for your resume/interview
This uses a **self-generated relational dataset** built to mirror how a
real school's Student Information System (SIS) is structured (Students /
Teachers / Courses / Enrollments), not a real school's actual records —
real student data is private and not something you'd have legal access
to as a portfolio project. This is completely normal for a fresher
project. If asked, say you modeled a realistic SIS-style schema to
practice relational SQL and build an academic-risk analysis — don't
imply it came from a real institution.

**If you want to strengthen this further:** the UCI "Student Performance"
dataset and the Open University Learning Analytics dataset (OULAD) are
real, public, anonymized education datasets — swapping in one of those
would let you honestly say the underlying data is real and published.

## What I did
1. **Designed a relational schema**: `students`, `teachers`, `courses`,
   `enrollments` (500 students, 20 teachers, 17 courses, ~5,000 enrollment
   records with scores + attendance across 2 semesters).
2. **Cleaned and prepped the data**: standardized gender text formatting,
   removed 40 duplicate enrollment records, imputed 74 missing attendance
   values using each student's own average (not a global fill), and
   validated referential integrity across tables.
3. **Wrote 7 multi-table SQL queries** (JOINs, CTEs, window functions,
   HAVING filters, CASE-based bucketing) — see `analysis.sql`.
4. **Built a 4-panel dashboard** covering the attendance-score
   relationship, subject pass rates, score distribution, and top-performing
   teachers.

## Key findings (from actual query output)
- **Attendance is strongly linked to performance**: students with 90–100%
  attendance average a **70.4 score**, versus **58.0** for students below
  60% attendance — a **12+ point gap**.
- Identified **20+ at-risk students** (average score under 65 AND average
  attendance under 75%) who would benefit from early intervention.
- Social Studies has the highest pass rate (72.0%), while Science has the
  lowest (69.2%) — a modest but consistent gap across subjects.
- Grade distribution is broadly similar between genders, with only small
  variation in A/B grade counts.
- Semester-over-semester score changes are mostly flat (within ±1 point)
  across subjects, suggesting performance is stable rather than trending.

## Files
- `raw_*.csv` — original raw data (with intentional data quality issues)
- `clean_data.py` — cleaning/prep script across all 4 tables
- `*_clean.csv` — cleaned tables
- `analysis.sql` — all 7 SQL queries (JOINs, CTEs, window functions, HAVING, CASE)
- `run_sql.py` — loads all tables into SQLite and runs the analysis
- `dashboard.py` — builds the dashboard
- `dashboard.png` — final dashboard

## Resume bullets (copy-paste ready — numbers are real, pulled from this project)

**Student Performance & Academic Risk Analytics — SQL, Python, Data Modeling**
- Designed a relational education dataset (Students, Teachers, Courses,
  Enrollments) with 500 students and ~5,000 enrollment records across
  2 semesters, modeled on a real Student Information System schema
- Wrote multi-table SQL queries (JOINs, CTEs, window functions) to
  quantify the relationship between attendance and academic performance,
  finding a 12+ point score gap between high- and low-attendance students
- Built a query to flag at-risk students using combined attendance and
  score thresholds, surfacing 20+ students for early intervention
- Analyzed pass rates and score trends across 5 subjects and 20 teachers,
  delivering a dashboard to communicate findings to stakeholders

## Notes for the interview
- Be ready to explain the at-risk query's logic (why both attendance
  AND score matter, not just one).
- Know why student-level imputation (not global mean) was the right
  choice for missing attendance values.
- Consider swapping in the real OULAD or UCI Student Performance dataset
  to make the underlying data itself real, not just the schema design.
