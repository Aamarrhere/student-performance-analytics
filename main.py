"""
main.py
Student Performance Analytics System
Runs the full pipeline: load -> process -> analyse -> display -> save.
"""

import pandas as pd
import functions as fn

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def print_heading(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    # ---------- STEP 1: Load the data ----------
    df = fn.load_data("students.csv")

    print_heading("1. DATASET OVERVIEW")
    print(f"Number of records : {df.shape[0]}")
    print(f"Number of columns : {df.shape[1]}")
    print(f"Columns           : {list(df.columns)}")
    print(f"Missing values    : {int(df.isnull().sum().sum())}")
    print("\nFirst 5 records:")
    print(df.head().to_string(index=False))

    # ---------- STEP 2: Process the data ----------
    df = fn.calculate_total_and_average(df)
    df = fn.add_grades(df)
    df = fn.add_pass_fail(df)
    df = fn.add_attendance_status(df)

    print_heading("2. PROCESSED STUDENT REPORT")
    report_cols = ["Student_ID", "Name", "Department", "Total_Marks",
                   "Average_Marks", "Grade", "Result", "Attendance",
                   "Attendance_Status"]
    print(df[report_cols].to_string(index=False))

    # ---------- STEP 3: Analysis ----------
    summary = fn.class_summary(df)
    print_heading("3. CLASS PERFORMANCE SUMMARY")
    print(f"Highest average : {summary['highest_avg']}  ({summary['topper']})")
    print(f"Lowest average  : {summary['lowest_avg']}  ({summary['lowest_scorer']})")
    print(f"Class average   : {summary['class_avg']}")
    print(f"Median average  : {summary['median_avg']}")
    print(f"Std deviation   : {summary['std_dev']}")

    stats = fn.pass_fail_statistics(df)
    print_heading("4. PASS / FAIL STATISTICS")
    print(f"Total students  : {stats['total']}")
    print(f"Passed          : {stats['passed']}")
    print(f"Failed          : {stats['failed']}")
    print(f"Pass percentage : {stats['pass_percentage']}%")
    print(f"(Rule: pass only if marks >= {fn.PASS_MARK} in every subject)")

    failed = fn.find_failed_subjects(df)
    print("\nSubjects failed by each failing student:")
    for name, subjects in failed.items():
        print(f"  - {name}: {', '.join(subjects)}")

    print_heading("5. GRADE DISTRIBUTION")
    for grade, count in fn.grade_distribution(df).items():
        print(f"  {grade:<3} : {'#' * int(count)} ({int(count)})")

    print_heading("6. SUBJECT-WISE ANALYSIS")
    subj = fn.subject_analysis(df)
    print(subj.to_string(index=False))
    best = subj.loc[subj["Average"].idxmax(), "Subject"]
    worst = subj.loc[subj["Average"].idxmin(), "Subject"]
    print(f"\nBest subject (highest average)   : {best}")
    print(f"Weakest subject (lowest average) : {worst}")

    print_heading("7. DEPARTMENT-WISE ANALYSIS")
    print(fn.department_analysis(df).to_string())

    print_heading("8. TOP 5 PERFORMING STUDENTS")
    print(fn.top_performers(df, n=5).to_string(index=False))

    print_heading("9. ATTENDANCE INSIGHTS")
    low = df[df["Attendance_Status"] == "Low"]
    print(f"Students with attendance below {fn.MIN_ATTENDANCE}%: {len(low)}")
    print(low[["Name", "Attendance", "Average_Marks", "Result"]].to_string(index=False))
    print(f"\nCorrelation (attendance vs average marks): "
          f"{fn.attendance_correlation(df)}")

    # ---------- STEP 4: Save the results ----------
    df.to_csv("student_results.csv", index=False)
    print_heading("DONE")
    print("Full results saved to 'student_results.csv'")


if __name__ == "__main__":
    main()
