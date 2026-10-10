"""Analyze student results and create report data and visualizations."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT_DIR / "data" / "student_results.csv"
DEFAULT_OUTPUT = ROOT_DIR / "output"
DEFAULT_CHARTS = ROOT_DIR / "charts"

SUBJECTS = ["Maths", "DBMS", "CN", "OS", "AI"]
REQUIRED_COLUMNS = [
    "Student_ID",
    "Student_Name",
    "Gender",
    "Department",
    "Semester",
    "Attendance",
    *SUBJECTS,
]
TEXT_COLUMNS = ["Student_ID", "Student_Name", "Gender", "Department"]
NUMERIC_COLUMNS = ["Semester", "Attendance", *SUBJECTS]


def generate_sample_data(path: Path, student_count: int = 200) -> None:
    """Write a reproducible sample student dataset to ``path``."""
    rng = np.random.RandomState(42)
    data = {
        "Student_ID": [f"S{i:03d}" for i in range(1, student_count + 1)],
        "Student_Name": [
            f"Student_{i:03d}" for i in range(1, student_count + 1)
        ],
        "Gender": rng.choice(["Male", "Female"], student_count),
        "Department": rng.choice(
            ["CSE", "ISE", "ECE", "EEE"], student_count
        ),
        "Semester": rng.choice([5, 6, 7, 8], student_count),
        "Attendance": rng.randint(50, 101, student_count),
    }
    for subject in SUBJECTS:
        data[subject] = rng.randint(30, 101, student_count)

    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(data).to_csv(path, index=False)


def load_student_data(path: Path) -> pd.DataFrame:
    """Read and validate the student input CSV."""
    if not path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {path}")

    df = pd.read_csv(path)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df]
    if missing_columns:
        raise ValueError(
            "Input CSV is missing required columns: "
            + ", ".join(missing_columns)
        )
    if df.empty:
        raise ValueError(f"Input CSV contains no student records: {path}")

    df = df[REQUIRED_COLUMNS].copy()
    for column in TEXT_COLUMNS:
        df[column] = df[column].astype("string").str.strip()
        invalid = df[column].isna() | df[column].eq("")
        if invalid.any():
            raise ValueError(
                f"Input column {column!r} contains blank values "
                f"at CSV row(s): {', '.join(map(str, df.index[invalid] + 2))}"
            )

    duplicates = df["Student_ID"].duplicated(keep=False)
    if duplicates.any():
        duplicate_ids = sorted(df.loc[duplicates, "Student_ID"].unique())
        raise ValueError(
            "Student_ID values must be unique; duplicates: "
            + ", ".join(duplicate_ids)
        )

    for column in NUMERIC_COLUMNS:
        original = df[column]
        converted = pd.to_numeric(original, errors="coerce")
        invalid = converted.isna() | ~np.isfinite(converted)
        if invalid.any():
            raise ValueError(
                f"Input column {column!r} contains missing or non-numeric "
                f"values at CSV row(s): "
                f"{', '.join(map(str, df.index[invalid] + 2))}"
            )
        if column != "Semester" and not converted.between(0, 100).all():
            raise ValueError(f"Values in {column!r} must be between 0 and 100.")
        if column == "Semester" and (
            (converted <= 0).any() or not converted.mod(1).eq(0).all()
        ):
            raise ValueError("Semester values must be positive whole numbers.")
        df[column] = converted.astype("int64")

    return df


def prepare_results(df: pd.DataFrame) -> pd.DataFrame:
    """Add calculated result, grade, and performance fields."""
    results = df.copy()
    results["Total_Marks"] = results[SUBJECTS].sum(axis=1)
    results["Percentage"] = results["Total_Marks"] / len(SUBJECTS)
    results["Result"] = np.where(
        results[SUBJECTS].ge(35).all(axis=1), "Pass", "Fail"
    )
    results["Grade"] = pd.cut(
        results["Percentage"],
        bins=[-np.inf, 35, 50, 60, 70, 85, np.inf],
        labels=["F", "D", "C", "B", "A", "A+"],
        right=False,
    )
    results["Performance_Category"] = pd.cut(
        results["Percentage"],
        bins=[-np.inf, 50, 70, 85, np.inf],
        labels=["Needs Improvement", "Average", "Good", "Excellent"],
        right=False,
    )
    return results


def create_charts(df: pd.DataFrame, charts_dir: Path) -> None:
    """Save the project visualizations as PNG files."""
    charts_dir.mkdir(parents=True, exist_ok=True)

    result_counts = df["Result"].value_counts().reindex(
        ["Pass", "Fail"], fill_value=0
    )
    fig, axis = plt.subplots(figsize=(6, 6))
    axis.pie(
        result_counts.values,
        labels=result_counts.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    axis.set_title("Student Pass vs Fail")
    fig.tight_layout()
    fig.savefig(charts_dir / "pass_fail.png")
    plt.close(fig)

    subject_averages = df[SUBJECTS].mean().sort_values(ascending=False)
    fig, axis = plt.subplots(figsize=(8, 5))
    subject_averages.plot(kind="bar", ax=axis, color="#4472C4")
    axis.set_title("Average Marks by Subject")
    axis.set_xlabel("Subject")
    axis.set_ylabel("Average Marks")
    axis.set_ylim(0, 100)
    axis.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(charts_dir / "subject_performance.png")
    plt.close(fig)

    gender_averages = df.groupby("Gender", observed=True)["Percentage"].mean()
    fig, axis = plt.subplots(figsize=(7, 5))
    gender_averages.plot(kind="bar", ax=axis, color="#70AD47")
    axis.set_title("Average Percentage by Gender")
    axis.set_xlabel("Gender")
    axis.set_ylabel("Average Percentage")
    axis.set_ylim(0, 100)
    axis.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(charts_dir / "gender_performance.png")
    plt.close(fig)

    department_averages = (
        df.groupby("Department", observed=True)["Percentage"]
        .mean()
        .sort_values(ascending=False)
    )
    fig, axis = plt.subplots(figsize=(8, 5))
    department_averages.plot(kind="bar", ax=axis, color="#ED7D31")
    axis.set_title("Average Percentage by Department")
    axis.set_xlabel("Department")
    axis.set_ylabel("Average Percentage")
    axis.set_ylim(0, 100)
    axis.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(charts_dir / "department_performance.png")
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(8, 5))
    for department, group in df.groupby("Department", observed=True):
        axis.scatter(
            group["Attendance"],
            group["Percentage"],
            label=department,
            alpha=0.75,
        )
    axis.set_title("Attendance vs Academic Performance")
    axis.set_xlabel("Attendance (%)")
    axis.set_ylabel("Percentage (%)")
    axis.set_xlim(0, 100)
    axis.set_ylim(0, 100)
    axis.grid(True, alpha=0.3)
    axis.legend(title="Department")
    fig.tight_layout()
    fig.savefig(charts_dir / "attendance_performance.png")
    plt.close(fig)


def write_analysis_report(df: pd.DataFrame, report_path: Path) -> None:
    """Write summary metrics and breakdowns to a readable text report."""
    result_counts = df["Result"].value_counts()
    subject_averages = df[SUBJECTS].mean().sort_values(ascending=False)
    department_averages = (
        df.groupby("Department", observed=True)["Percentage"]
        .mean()
        .sort_values(ascending=False)
    )

    lines = [
        "STUDENT RESULT ANALYSIS REPORT",
        "===============================",
        f"Total students: {len(df)}",
        f"Passed students: {int(result_counts.get('Pass', 0))}",
        f"Failed students: {int(result_counts.get('Fail', 0))}",
        f"Pass percentage: {df['Result'].eq('Pass').mean() * 100:.2f}%",
        f"Average percentage: {df['Percentage'].mean():.2f}%",
        f"Average attendance: {df['Attendance'].mean():.2f}%",
        "",
        "Subject-wise average marks:",
        subject_averages.to_string(float_format=lambda value: f"{value:.2f}"),
        "",
        "Department average percentages:",
        department_averages.to_string(
            float_format=lambda value: f"{value:.2f}"
        ),
        "",
        "Grade distribution:",
        df["Grade"].value_counts(sort=False).to_string(),
        "",
    ]

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def run_analysis(input_path: Path, output_dir: Path, charts_dir: Path) -> None:
    """Run the full CSV-to-report analysis pipeline."""
    source_data = load_student_data(input_path)
    results = prepare_results(source_data)

    output_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_dir / "cleaned_student_results.csv", index=False)
    create_charts(results, charts_dir)
    write_analysis_report(results, output_dir / "analysis_report.txt")

    print(f"Analyzed {len(results)} students from {input_path}")
    print(f"Cleaned results: {output_dir / 'cleaned_student_results.csv'}")
    print(f"Analysis report: {output_dir / 'analysis_report.txt'}")
    print(f"Charts: {charts_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze student marks, attendance, and results."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Input student CSV (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Directory for cleaned CSV and report (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--charts-dir",
        type=Path,
        default=DEFAULT_CHARTS,
        help=f"Directory for chart PNGs (default: {DEFAULT_CHARTS})",
    )
    parser.add_argument(
        "--generate-sample",
        action="store_true",
        help="Generate a reproducible sample CSV at --input before analysis.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.generate_sample:
        generate_sample_data(args.input)
        print(f"Generated sample input: {args.input}")
    run_analysis(args.input, args.output_dir, args.charts_dir)


if __name__ == "__main__":
    main()
