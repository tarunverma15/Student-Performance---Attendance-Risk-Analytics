import pandas as pd
import matplotlib.pyplot as plt

subject_perf = pd.read_csv("result_subject_performance.csv")
attendance_band = pd.read_csv("result_attendance_band.csv")
teacher_perf = pd.read_csv("result_teacher_performance.csv")
enrollments = pd.read_csv("enrollments_clean.csv")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Student Performance & Academic Risk Dashboard", fontsize=18, fontweight="bold", y=0.98)

# Panel 1: Attendance band vs avg score (the key insight)
band_order = ["Below 60%","60-69%","70-79%","80-89%","90-100%"]
attendance_band["attendance_band"] = pd.Categorical(attendance_band["attendance_band"], categories=band_order, ordered=True)
attendance_band = attendance_band.sort_values("attendance_band")
colors = ["#dc2626","#f59e0b","#facc15","#84cc16","#16a34a"]
axes[0,0].bar(attendance_band["attendance_band"], attendance_band["avg_score"], color=colors)
axes[0,0].set_title("Avg Score by Attendance Band", fontweight="bold")
axes[0,0].set_ylabel("Average Score")
axes[0,0].set_ylim(50, 75)

# Panel 2: Pass rate by subject
subject_perf_sorted = subject_perf.sort_values("pass_rate_pct", ascending=True)
axes[0,1].barh(subject_perf_sorted["Subject"], subject_perf_sorted["pass_rate_pct"], color="#2563eb")
axes[0,1].set_title("Pass Rate by Subject (%)", fontweight="bold")
axes[0,1].set_xlabel("Pass Rate (%)")
axes[0,1].set_xlim(60, 75)

# Panel 3: Score distribution histogram
axes[1,0].hist(enrollments["Score"].dropna(), bins=25, color="#7c3aed", edgecolor="white")
axes[1,0].set_title("Score Distribution (All Enrollments)", fontweight="bold")
axes[1,0].set_xlabel("Score"); axes[1,0].set_ylabel("# of Enrollments")
axes[1,0].axvline(enrollments["Score"].mean(), color="#dc2626", linestyle="--", label=f"Mean: {enrollments['Score'].mean():.1f}")
axes[1,0].legend()

# Panel 4: Top 8 teachers by avg score
top_teachers = teacher_perf.nlargest(8, "avg_score").sort_values("avg_score")
axes[1,1].barh(top_teachers["TeacherName"], top_teachers["avg_score"], color="#059669")
axes[1,1].set_title("Top 8 Teachers by Avg Student Score", fontweight="bold")
axes[1,1].set_xlabel("Average Score")
axes[1,1].set_xlim(63, 68)

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("dashboard.png", dpi=150, bbox_inches="tight")
print("Dashboard saved")
