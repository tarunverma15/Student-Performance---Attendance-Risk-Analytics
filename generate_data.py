"""
Generates a realistic synthetic student performance dataset for the
'Student Performance & Academic Risk Analytics' project.
Relational schema: students, teachers, courses, enrollments (scores + attendance).
"""
import numpy as np
import pandas as pd

np.random.seed(21)

# ---- Master data: Teachers ----
DEPARTMENTS = ["Mathematics", "Science", "English", "Social Studies", "Computer Science"]
N_TEACHERS = 20
teachers = pd.DataFrame({
    "TeacherID": [f"T{str(i).zfill(3)}" for i in range(1, N_TEACHERS+1)],
    "TeacherName": [f"Teacher {i}" for i in range(1, N_TEACHERS+1)],
    "Department": np.random.choice(DEPARTMENTS, N_TEACHERS),
})

# ---- Master data: Courses ----
SUBJECT_COURSES = {
    "Mathematics": ["Algebra", "Geometry", "Calculus", "Statistics"],
    "Science": ["Physics", "Chemistry", "Biology", "Environmental Science"],
    "English": ["Literature", "Composition", "Grammar Fundamentals"],
    "Social Studies": ["World History", "Geography", "Civics"],
    "Computer Science": ["Intro to Programming", "Data Structures", "Web Development"],
}
course_rows = []
cid = 1
for subj, course_list in SUBJECT_COURSES.items():
    dept_teachers = teachers[teachers.Department == subj]["TeacherID"].tolist()
    for cname in course_list:
        teacher = np.random.choice(dept_teachers) if len(dept_teachers) else np.random.choice(teachers["TeacherID"])
        course_rows.append([f"CRS{str(cid).zfill(3)}", cname, subj, teacher])
        cid += 1
courses = pd.DataFrame(course_rows, columns=["CourseID","CourseName","Subject","TeacherID"])

# ---- Master data: Students ----
GRADE_LEVELS = [9, 10, 11, 12]
N_STUDENTS = 500
# give each student a latent "ability" and "engagement" trait to drive realistic correlations
ability = np.random.normal(70, 12, N_STUDENTS)
engagement = np.clip(np.random.normal(80, 15, N_STUDENTS), 30, 100)

students = pd.DataFrame({
    "StudentID": [f"S{str(i).zfill(4)}" for i in range(1, N_STUDENTS+1)],
    "StudentName": [f"Student {i}" for i in range(1, N_STUDENTS+1)],
    "Gender": np.random.choice(["Male","Female"], N_STUDENTS),
    "GradeLevel": np.random.choice(GRADE_LEVELS, N_STUDENTS),
    "_ability": ability,
    "_engagement": engagement,
})

SEMESTERS = ["2025-Fall", "2026-Spring"]

# ---- Transactional: Enrollments (scores + attendance) ----
enroll_rows = []
eid = 1
for _, stu in students.iterrows():
    # each student takes 4-6 courses per semester
    for sem in SEMESTERS:
        n_courses = np.random.randint(4, 7)
        chosen = courses.sample(n_courses)
        for _, course in chosen.iterrows():
            attendance_pct = np.clip(np.random.normal(stu["_engagement"], 8), 40, 100)
            # score depends on ability + engagement/attendance + noise
            score = (0.6 * stu["_ability"] + 0.3 * (attendance_pct) + np.random.normal(0, 7))
            score = float(np.clip(score, 0, 100))
            if score >= 90: grade = "A"
            elif score >= 80: grade = "B"
            elif score >= 70: grade = "C"
            elif score >= 60: grade = "D"
            else: grade = "F"
            enroll_rows.append([eid, stu["StudentID"], course["CourseID"], sem,
                                 round(attendance_pct,1), round(score,1), grade])
            eid += 1

enrollments = pd.DataFrame(enroll_rows, columns=[
    "EnrollmentID","StudentID","CourseID","Semester","AttendancePct","Score","LetterGrade"
])

students = students.drop(columns=["_ability","_engagement"])

# ---- Inject realistic messiness ----
messy_idx = students.sample(frac=0.04, random_state=1).index
students.loc[messy_idx, "Gender"] = students.loc[messy_idx, "Gender"].str.lower()
dup_rows = enrollments.sample(frac=0.008, random_state=2)
enrollments = pd.concat([enrollments, dup_rows], ignore_index=True)
null_idx = enrollments.sample(frac=0.015, random_state=3).index
enrollments.loc[null_idx, "AttendancePct"] = None

students.to_csv("raw_students.csv", index=False)
teachers.to_csv("raw_teachers.csv", index=False)
courses.to_csv("raw_courses.csv", index=False)
enrollments.to_csv("raw_enrollments.csv", index=False)

print("students:", len(students))
print("teachers:", len(teachers))
print("courses:", len(courses))
print("enrollments:", len(enrollments))
