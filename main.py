import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

subjects = ["Maths", "DBMS", "CN", "OS", "AI"]

# Create folders
os.makedirs("data", exist_ok=True)
os.makedirs("charts", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Generate 200 students
np.random.seed(42)

num_students = 200

student_ids = [
    f"S{i:03d}" for i in range(1, num_students + 1)
]

student_names = [
    f"Student_{i:03d}" for i in range(1, num_students + 1)
]

genders = np.random.choice(
    ["Male", "Female"],
    num_students
)

departments = np.random.choice(
    ["CSE", "ISE", "ECE", "EEE"],
    num_students
)

semesters = np.random.choice(
    [5, 6, 7, 8],
    num_students
)

attendance = np.random.randint(
    50, 101, num_students
)

maths = np.random.randint(
    30, 101, num_students
)

dbms = np.random.randint(
    30, 101, num_students
)

cn = np.random.randint(
    30, 101, num_students
)

os_marks = np.random.randint(
    30, 101, num_students
)

ai = np.random.randint(
    30, 101, num_students
)

# Create dataframe
df = pd.DataFrame({
    "Student_ID": student_ids,
    "Student_Name": student_names,
    "Gender": genders,
    "Department": departments,
    "Semester": semesters,
    "Attendance": attendance,
    "Maths": maths,
    "DBMS": dbms,
    "CN": cn,
    "OS": os_marks,
    "AI": ai
})

# Save dataset
df.to_csv(
    "data/student_results.csv",
    index=False
)

# Calculate student results for analysis and charts
df["Total_Marks"] = df[subjects].sum(axis=1)
df["Percentage"] = df["Total_Marks"] / len(subjects)
df["Result"] = np.where(
    (df[subjects] >= 35).all(axis=1),
    "Pass",
    "Fail"
)
df["Grade"] = pd.cut(
    df["Percentage"],
    bins=[-np.inf, 35, 50, 60, 70, 85, np.inf],
    labels=["F", "D", "C", "B", "A", "A+"],
    right=False
)
df["Performance_Category"] = pd.cut(
    df["Percentage"],
    bins=[-np.inf, 50, 70, 85, np.inf],
    labels=["Needs Improvement", "Average", "Good", "Excellent"],
    right=False
)
df.to_csv(
    "output/cleaned_student_results.csv",
    index=False
)

print("====================================")
print("STUDENT DATASET CREATED SUCCESSFULLY")
print("====================================")
print("Number of students:", len(df))

print("\nFirst 5 records:")
print(df.head())
# ==================================
# CHART 1 - PASS VS FAIL
# ==================================

result_counts = df["Result"].value_counts()

plt.figure(figsize=(6, 6))

plt.pie(
    result_counts.values,
    labels=result_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Student Pass vs Fail")

plt.tight_layout()

plt.savefig("charts/pass_fail.png")

plt.close()

print("Pass vs Fail chart created.")


# ==================================
# CHART 2 - SUBJECT PERFORMANCE
# ==================================

subject_averages = df[subjects].mean()

plt.figure(figsize=(8, 5))

subject_averages.plot(kind="bar")

plt.title("Average Marks by Subject")
plt.xlabel("Subject")
plt.ylabel("Average Marks")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("charts/subject_performance.png")

plt.close()

print("Subject performance chart created.")


# ==================================
# CHART 3 - GENDER PERFORMANCE
# ==================================

gender_performance = (
    df.groupby("Gender")["Percentage"].mean()
)

plt.figure(figsize=(7, 5))

gender_performance.plot(kind="bar")

plt.title("Average Percentage by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Percentage")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("charts/gender_performance.png")

plt.close()

print("Gender performance chart created.")


# ==================================
# CHART 4 - DEPARTMENT PERFORMANCE
# ==================================

department_performance = (
    df.groupby("Department")["Percentage"].mean()
)

plt.figure(figsize=(8, 5))

department_performance.plot(kind="bar")

plt.title("Average Percentage by Department")
plt.xlabel("Department")
plt.ylabel("Average Percentage")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("charts/department_performance.png")

plt.close()

print("Department performance chart created.")


# ==================================
# CHART 5 - ATTENDANCE VS PERFORMANCE
# ==================================

plt.figure(figsize=(8, 5))

plt.scatter(
    df["Attendance"],
    df["Percentage"]
)

plt.title("Attendance vs Academic Performance")

plt.xlabel("Attendance (%)")
plt.ylabel("Percentage (%)")

plt.grid(True)

plt.tight_layout()

plt.savefig("charts/attendance_performance.png")

plt.close()

print("Attendance performance chart created.")


print("\n=================================")
print("ALL CHARTS CREATED SUCCESSFULLY!")
print("=================================")