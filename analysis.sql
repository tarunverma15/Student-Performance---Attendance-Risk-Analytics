-- =========================================================
-- Student Performance & Academic Risk Analytics
-- Tables: students, teachers, courses, enrollments
-- =========================================================

-- 1. Average score and pass rate by subject (join + conditional aggregation)
SELECT
    c.Subject,
    COUNT(*) AS total_enrollments,
    ROUND(AVG(e.Score), 2) AS avg_score,
    ROUND(100.0 * SUM(CASE WHEN e.LetterGrade != 'F' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pass_rate_pct
FROM enrollments e
JOIN courses c ON e.CourseID = c.CourseID
GROUP BY c.Subject
ORDER BY avg_score DESC;


-- 2. At-risk students: low attendance AND low average score (CTE + HAVING)
WITH student_perf AS (
    SELECT
        s.StudentID, s.StudentName, s.GradeLevel,
        ROUND(AVG(e.Score), 2) AS avg_score,
        ROUND(AVG(e.AttendancePct), 2) AS avg_attendance
    FROM enrollments e
    JOIN students s ON e.StudentID = s.StudentID
    GROUP BY s.StudentID
)
SELECT *
FROM student_perf
WHERE avg_score < 65 AND avg_attendance < 75
ORDER BY avg_score ASC
LIMIT 20;


-- 3. Attendance-band vs average score (bucketed correlation, CASE + CTE)
WITH banded AS (
    SELECT
        CASE
            WHEN AttendancePct >= 90 THEN '90-100%'
            WHEN AttendancePct >= 80 THEN '80-89%'
            WHEN AttendancePct >= 70 THEN '70-79%'
            WHEN AttendancePct >= 60 THEN '60-69%'
            ELSE 'Below 60%'
        END AS attendance_band,
        Score
    FROM enrollments
)
SELECT
    attendance_band,
    COUNT(*) AS enrollments,
    ROUND(AVG(Score), 2) AS avg_score
FROM banded
GROUP BY attendance_band
ORDER BY avg_score DESC;


-- 4. Teacher-wise average score and student count (multi-table join)
SELECT
    t.TeacherName, t.Department,
    COUNT(DISTINCT e.StudentID) AS students_taught,
    ROUND(AVG(e.Score), 2) AS avg_score
FROM enrollments e
JOIN courses c ON e.CourseID = c.CourseID
JOIN teachers t ON c.TeacherID = t.TeacherID
GROUP BY t.TeacherID
ORDER BY avg_score DESC;


-- 5. Semester-over-semester average score change by subject (window function)
WITH subj_sem AS (
    SELECT c.Subject, e.Semester, ROUND(AVG(e.Score), 2) AS avg_score
    FROM enrollments e
    JOIN courses c ON e.CourseID = c.CourseID
    GROUP BY c.Subject, e.Semester
)
SELECT
    Subject, Semester, avg_score,
    ROUND(avg_score - LAG(avg_score) OVER (PARTITION BY Subject ORDER BY Semester), 2) AS change_vs_prior_semester
FROM subj_sem
ORDER BY Subject, Semester;


-- 6. Grade distribution by gender (join + conditional aggregation)
SELECT
    s.Gender,
    SUM(CASE WHEN e.LetterGrade = 'A' THEN 1 ELSE 0 END) AS grade_a,
    SUM(CASE WHEN e.LetterGrade = 'B' THEN 1 ELSE 0 END) AS grade_b,
    SUM(CASE WHEN e.LetterGrade = 'C' THEN 1 ELSE 0 END) AS grade_c,
    SUM(CASE WHEN e.LetterGrade = 'D' THEN 1 ELSE 0 END) AS grade_d,
    SUM(CASE WHEN e.LetterGrade = 'F' THEN 1 ELSE 0 END) AS grade_f,
    COUNT(*) AS total
FROM enrollments e
JOIN students s ON e.StudentID = s.StudentID
GROUP BY s.Gender;


-- 7. Top 10 highest-enrollment courses and their pass rate (join + subquery filter)
WITH course_stats AS (
    SELECT
        c.CourseID, c.CourseName, c.Subject,
        COUNT(*) AS enrollments,
        ROUND(100.0 * SUM(CASE WHEN e.LetterGrade != 'F' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pass_rate_pct
    FROM enrollments e
    JOIN courses c ON e.CourseID = c.CourseID
    GROUP BY c.CourseID
)
SELECT *
FROM course_stats
ORDER BY enrollments DESC
LIMIT 10;
