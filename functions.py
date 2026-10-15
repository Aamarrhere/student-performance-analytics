"""
functions.py
Reusable calculation / processing functions for the
Student Performance Analytics System.
"""

import numpy as np
import pandas as pd

# ---------- Project settings (the "rules" of the system) ----------
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer_Science"]
PASS_MARK = 40            # a student must score >= 40 in EVERY subject to pass
MIN_ATTENDANCE = 75       # attendance (%) below this is flagged as "Low"
MAX_MARKS_PER_SUBJECT = 100

# Grading rule based on the student's AVERAGE marks (highest first)
GRADE_RULES = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (40, "E"),
]


def load_data(file_path):
    """Read the student CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def calculate_total_and_average(df):
    """Add Total_Marks and Average_Marks columns using NumPy."""
    marks = df[SUBJECTS].to_numpy()                       # DataFrame -> NumPy array
    df["Total_Marks"] = np.sum(marks, axis=1)             # row-wise total
    df["Average_Marks"] = np.round(np.mean(marks, axis=1), 2)
    return df


def assign_grade(average):
    """Return the grade for one average value using GRADE_RULES."""
    for minimum, grade in GRADE_RULES:                    # loop through the rules
        if average >= minimum:
            return grade
    return "F"


def add_grades(df):
    """Add a Grade column by applying assign_grade to each average."""
    grades = []
    for avg in df["Average_Marks"]:                       # loop over every student
        grades.append(assign_grade(avg))
    df["Grade"] = grades
    return df


def add_pass_fail(df):
    """Pass only if the student scored >= PASS_MARK in every subject."""
    marks = df[SUBJECTS].to_numpy()
    passed = np.all(marks >= PASS_MARK, axis=1)           # True if ALL subjects pass
    df["Result"] = np.where(passed, "Pass", "Fail")
    return df


def add_attendance_status(df):
    """Flag students whose attendance is below MIN_ATTENDANCE."""
    df["Attendance_Status"] = np.where(
        df["Attendance"] >= MIN_ATTENDANCE, "OK", "Low"
    )
    return df


def find_failed_subjects(df):
    """Return a dict {student name: [subjects failed]} using nested loops."""
    failed = {}
    for _, row in df.iterrows():
        subjects_failed = []
        for subject in SUBJECTS:
            if row[subject] < PASS_MARK:
                subjects_failed.append(subject)
        if subjects_failed:
            failed[row["Name"]] = subjects_failed
    return failed


def class_summary(df):
    """Highest, lowest and average performance of the whole class."""
    avg = df["Average_Marks"].to_numpy()
    return {
        "highest_avg": np.max(avg),
        "lowest_avg": np.min(avg),
        "class_avg": round(float(np.mean(avg)), 2),
        "median_avg": round(float(np.median(avg)), 2),
        "std_dev": round(float(np.std(avg)), 2),
        "topper": df.loc[df["Average_Marks"].idxmax(), "Name"],
        "lowest_scorer": df.loc[df["Average_Marks"].idxmin(), "Name"],
    }


def pass_fail_statistics(df):
    """Count of passed / failed students and the pass percentage."""
    total = len(df)
    passed = int((df["Result"] == "Pass").sum())
    failed = total - passed
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_percentage": round(passed / total * 100, 2),
    }


def subject_analysis(df):
    """Average, highest, lowest and pass-rate for every subject."""
    rows = []
    for subject in SUBJECTS:                              # loop through each subject
        scores = df[subject].to_numpy()
        rows.append({
            "Subject": subject,
            "Average": round(float(np.mean(scores)), 2),
            "Highest": int(np.max(scores)),
            "Lowest": int(np.min(scores)),
            "Pass_%": round(float(np.mean(scores >= PASS_MARK) * 100), 1),
            "Topper": df.loc[df[subject].idxmax(), "Name"],
        })
    return pd.DataFrame(rows)


def department_analysis(df):
    """Group by department: number of students, avg marks, avg attendance, pass count."""
    summary = df.groupby("Department").agg(
        Students=("Student_ID", "count"),
        Avg_Marks=("Average_Marks", "mean"),
        Avg_Attendance=("Attendance", "mean"),
        Passed=("Result", lambda r: (r == "Pass").sum()),
    ).round(2)
    return summary.sort_values("Avg_Marks", ascending=False)


def grade_distribution(df):
    """How many students got each grade (in a fixed order)."""
    order = ["A+", "A", "B", "C", "D", "E", "F"]
    return df["Grade"].value_counts().reindex(order, fill_value=0)


def top_performers(df, n=5):
    """Return the top n students ranked by average marks."""
    top = df.sort_values("Average_Marks", ascending=False).head(n).copy()
    top["Rank"] = np.arange(1, len(top) + 1)
    return top[["Rank", "Student_ID", "Name", "Department",
                "Total_Marks", "Average_Marks", "Grade"]]


def attendance_correlation(df):
    """Correlation between attendance and average marks (NumPy corrcoef)."""
    return round(float(np.corrcoef(df["Attendance"], df["Average_Marks"])[0, 1]), 3)
