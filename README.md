# Student Performance Analytics System

## 1. Project Title
**Student Performance Analytics System**

| | |
|---|---|
| **Student Name** | `<Your Name>` |
| **Course** | Python with AI – EWB Courses |
| **Submission Date** | `<Date>` (deadline: 15 October 2026) |

## 2. Objective
Teachers usually hold student marks in spreadsheets and calculate totals, grades and
rankings by hand, which is slow and error-prone. This project automates that work. It reads
student records, calculates totals, averages, grades and pass/fail status, and produces
class-level, subject-level and department-level analysis, plus a list of top performers.

## 3. Technologies Used
- **Python 3**: variables, data types, loops, conditions, functions
- **NumPy**: numerical calculations (sum, mean, max, min, median, std, corrcoef, where, all)
- **Pandas**: loading the CSV, DataFrame operations, filtering, sorting, groupby
- No other libraries were used.

## 4. Dataset Description
`students.csv` contains **20 student records** and **9 columns**:

| Column | Description |
|---|---|
| Student_ID | Unique ID (S001–S020) |
| Name | Student name |
| Department | CSE, ECE, Mechanical or Civil |
| Maths, Physics, Chemistry, English, Computer_Science | Marks out of 100 |
| Attendance | Attendance percentage |

The data was created for this project. It has a realistic spread: high scorers, average
students and a few who fail one or more subjects.

## 5. Implementation (Step by Step)
1. **Load data**: `load_data()` reads `students.csv` into a Pandas DataFrame. `main.py` prints the shape, columns and missing-value count.
2. **Total and average**: `calculate_total_and_average()` converts the subject columns to a NumPy array and uses `np.sum` and `np.mean` with `axis=1` (row-wise).
3. **Grades**: `assign_grade()` loops through a clearly defined rule list, and `add_grades()` applies it to every student.

   | Average | Grade |
   |---|---|
   | 90 and above | A+ |
   | 80 – 89.99 | A |
   | 70 – 79.99 | B |
   | 60 – 69.99 | C |
   | 50 – 59.99 | D |
   | 40 – 49.99 | E |
   | Below 40 | F |

4. **Pass/Fail**: a student **passes only if they score at least 40 in every subject** (`np.all` and `np.where`). `find_failed_subjects()` uses nested loops to list the subjects each failing student missed.
5. **Class summary**: highest, lowest, average, median and standard deviation of the average marks (NumPy).
6. **Subject-wise analysis**: a loop over subjects computes average, highest, lowest, pass rate and topper for each one.
7. **Department analysis**: Pandas `groupby` + `agg`.
8. **Top performers**: sort by average and take the top 5 with a rank column.
9. **Attendance insight**: students below 75% are flagged, and `np.corrcoef` measures the link between attendance and marks.
10. **Save**: the full processed table is written to `student_results.csv`.

## 6. Key Features
| Function | Purpose |
|---|---|
| `load_data` | Read CSV into a DataFrame |
| `calculate_total_and_average` | Total and average marks per student |
| `assign_grade` / `add_grades` | Grade using the grading rule |
| `add_pass_fail` | Pass/Fail using the pass condition |
| `add_attendance_status` | Flag low attendance |
| `find_failed_subjects` | Subjects failed per student |
| `class_summary` | Highest / lowest / average performance |
| `pass_fail_statistics` | Pass count and percentage |
| `subject_analysis` | Subject-wise statistics |
| `department_analysis` | Department comparison |
| `grade_distribution` | Count of each grade |
| `top_performers` | Top-N ranking |
| `attendance_correlation` | Attendance vs marks correlation |

## 7. Output
Full console output is in [`output.txt`](output.txt). Key results:

```
Highest average : 94.6  (Anjali Verma)
Lowest average  : 41.6  (Siddharth Iyer)
Class average   : 69.7
Passed 18 / 20  -> Pass percentage 90.0%

Best subject    : English (avg 73.45)
Weakest subject : Physics (avg 66.8)

Top 5:  1. Anjali Verma (94.6)   2. Kavya Reddy (90.0)   3. Aarav Sharma (88.0)
        4. Sneha Kulkarni (87.8) 5. Meera Pillai (86.8)

Correlation (attendance vs average marks): 0.982
```

> Optional: add screenshots of your terminal output in a `screenshots/` folder and link them here.

## 8. Final Outcome
The project reads the student dataset and produces a complete performance report without
manual calculation. It found that the class average is 69.7, 18 of 20 students passed
(90%), English is the strongest subject, and CSE and ECE are the best-performing
departments. Attendance and marks show a very strong positive correlation (0.98), and the
two students who failed were also among those with the lowest attendance.

## 9. Challenges & Learning
- **Defining a fair pass rule**: I chose "at least 40 in every subject" instead of using only the average, so a student cannot hide a failing subject behind high marks elsewhere.
- **Converting between Pandas and NumPy**: `.to_numpy()` made row-wise calculations with `axis=1` easy.
- **Keeping code reusable**: I moved all logic into `functions.py` so `main.py` only displays results.
- **Learning**: I practised loops, functions, NumPy array operations and Pandas groupby, and learned how to structure a project and publish it on GitHub.

## 10. GitHub Repository
`https://github.com/<your-username>/student-performance-analytics`

## How to Run
```bash
pip install -r requirements.txt
python main.py
```

## Project Structure
```
student-performance-analytics/
├── main.py              # runs the analysis and prints the report
├── functions.py         # reusable calculation functions
├── students.csv         # dataset (20 records)
├── student_results.csv  # generated output file
├── output.txt           # sample console output
├── requirements.txt
└── README.md            # project documentation
```
