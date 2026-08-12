import sqlite3, pandas as pd

tables = {
    "students": "students_clean.csv",
    "teachers": "teachers_clean.csv",
    "courses": "courses_clean.csv",
    "enrollments": "enrollments_clean.csv",
}

conn = sqlite3.connect(":memory:")
for name, path in tables.items():
    df = pd.read_csv(path)
    df.to_sql(name, conn, index=False, if_exists="replace")

sql_text = open("analysis.sql").read()
raw_statements = [s.strip() for s in sql_text.split(";")]
queries = [s for s in raw_statements if "SELECT" in s.upper()]

titles = [
    "1. Avg score and pass rate by subject",
    "2. At-risk students (low attendance + low score)",
    "3. Attendance band vs avg score",
    "4. Teacher-wise avg score",
    "5. Semester-over-semester score change by subject",
    "6. Grade distribution by gender",
    "7. Top 10 highest-enrollment courses",
]

results = {}
for title, q in zip(titles, queries):
    res = pd.read_sql_query(q, conn)
    results[title] = res

for title, res in results.items():
    print("="*70)
    print(title)
    print(res.to_string(index=False))
    print()

results["1. Avg score and pass rate by subject"].to_csv("result_subject_performance.csv", index=False)
results["2. At-risk students (low attendance + low score)"].to_csv("result_at_risk_students.csv", index=False)
results["3. Attendance band vs avg score"].to_csv("result_attendance_band.csv", index=False)
results["4. Teacher-wise avg score"].to_csv("result_teacher_performance.csv", index=False)
