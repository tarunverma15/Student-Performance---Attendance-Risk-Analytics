"""
Cleaning / prep step for the Student Performance dataset.
Standardizes categorical text, removes duplicate enrollment records,
handles missing attendance values with a documented, defensible rule.
"""
import pandas as pd

students = pd.read_csv("raw_students.csv")
teachers = pd.read_csv("raw_teachers.csv")
courses = pd.read_csv("raw_courses.csv")
enrollments = pd.read_csv("raw_enrollments.csv")

# 1. Standardize Gender casing
students["Gender"] = students["Gender"].str.strip().str.title()

# 2. Remove duplicate enrollment records (same EnrollmentID)
before = len(enrollments)
enrollments = enrollments.drop_duplicates(subset="EnrollmentID", keep="first")
dupes_removed = before - len(enrollments)

# 3. Missing attendance: impute with that student's average attendance
#    across their other courses (more defensible than a global mean,
#    since attendance is a personal trait, not a course-level one)
missing_before = enrollments["AttendancePct"].isna().sum()
student_avg_attendance = enrollments.groupby("StudentID")["AttendancePct"].transform("mean")
enrollments["AttendancePct"] = enrollments["AttendancePct"].fillna(student_avg_attendance)

# 4. Referential integrity check
valid_students = set(students["StudentID"])
valid_courses = set(courses["CourseID"])
before_ref = len(enrollments)
enrollments = enrollments[
    enrollments["StudentID"].isin(valid_students) & enrollments["CourseID"].isin(valid_courses)
]
ref_dropped = before_ref - len(enrollments)

students.to_csv("students_clean.csv", index=False)
teachers.to_csv("teachers_clean.csv", index=False)
courses.to_csv("courses_clean.csv", index=False)
enrollments.to_csv("enrollments_clean.csv", index=False)

print(f"Duplicate enrollments removed: {dupes_removed}")
print(f"Missing attendance values imputed (student-level avg): {missing_before}")
print(f"Rows dropped for failed referential integrity: {ref_dropped}")
print(f"Final enrollments: {len(enrollments):,}")
