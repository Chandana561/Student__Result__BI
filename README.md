# Student Result BI

Student Result BI analyzes academic performance with Python and Power BI. It
reads student data from `data/student_results.csv`, calculates result and
performance metrics, and writes a cleaned dataset, a text summary, and charts.
The Power BI files in `powerbi/` load the cleaned data and provide measures and
report-building instructions.

## Run the analysis

Requirements: Python 3.10 or newer.

In Windows PowerShell, from the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\main.py
```

The analysis uses the existing CSV by default. It does not replace or modify
the source data. To analyze another file:

```powershell
.\.venv\Scripts\python.exe .\main.py --input .\data\my_results.csv
```

To create the same 200-row sample dataset used by this project and analyze it:

```powershell
.\.venv\Scripts\python.exe .\main.py --generate-sample
```

`--generate-sample` replaces the CSV at the selected `--input` path. The
default is `data/student_results.csv`.

Optional output locations can be set independently:

```powershell
.\.venv\Scripts\python.exe .\main.py `
  --input .\data\student_results.csv `
  --output-dir .\output `
  --charts-dir .\charts
```

The input CSV must contain these columns:

`Student_ID`, `Student_Name`, `Gender`, `Department`, `Semester`,
`Attendance`, `Maths`, `DBMS`, `CN`, `OS`, `AI`

Student IDs must be unique. Attendance and marks must be numeric values from
0 to 100, and semester values must be positive whole numbers. A student passes
when every subject mark is at least 35. Percentage is the average across the
five subjects.

## Generated files

- `output/cleaned_student_results.csv` — source columns plus total marks,
  percentage, pass/fail result, grade, and performance category.
- `output/analysis_report.txt` — overall KPIs, subject and department averages,
  and grade distribution.
- `charts/pass_fail.png` — pass/fail distribution.
- `charts/subject_performance.png` — average marks by subject.
- `charts/gender_performance.png` — average percentage by gender.
- `charts/department_performance.png` — average percentage by department.
- `charts/attendance_performance.png` — attendance compared with percentage.

## Power BI

Open [powerbi/README.md](powerbi/README.md) for instructions to import the
Power Query scripts, create the data model and report pages, and add the DAX
measures. Power BI Desktop is required to create and save the `.pbix` report.
If the project is moved, update the CSV path near the top of
`powerbi/Students.pq` before refreshing the report.
