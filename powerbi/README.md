# Build the Student Result Power BI report

The project-side implementation is ready: Power Query files load and prepare the generated CSV, `Measures.dax` contains the KPI formulas, and the instructions below describe the four report pages. The actual `.pbix` must be created and saved in Power BI Desktop; Desktop is not installed or available on this machine, so this workspace does not contain a `.pbix`.

## 1. Generate or refresh the source CSV

From the VS Code terminal, run:

```powershell
.\venv\Scripts\python.exe .\main.py
```

This writes `output\cleaned_student_results.csv`. Keep the project in its current location, or update the `CsvPath` near the top of `Students.pq` if you move it.

## 2. Create the Power BI model

1. Open Power BI Desktop and select **Blank report**.
2. On the **Home** ribbon, select **Transform data** to open Power Query Editor.
3. Select **Home → New Source → Blank Query**. In the Queries pane, rename the new query to `Students`.
4. With `Students` selected, choose **Home → Advanced Editor**. Replace the editor contents with all the text from `powerbi\Students.pq`, then select **Done**. Confirm the preview shows 200 rows and columns including `Student_ID`, `Percentage`, `Attendance Band`, and `Improvement Status`.
5. Select **Home → New Source → Blank Query** again. Rename it `SubjectResults`.
6. Open **Advanced Editor** for `SubjectResults`, replace its contents with all the text from `powerbi\SubjectResults.pq`, and select **Done**. Confirm the preview shows 1,000 rows with `Student_ID`, `Subject`, and `Marks`.
7. Select **Home → Close & Apply** and wait for the tables to load.
8. Open **Model** view. Create a relationship by dragging `Students[Student_ID]` onto `SubjectResults[Student_ID]`. Confirm it is **One to many (1:*)**, with `Students` on the `1` side and single-direction filtering from `Students` to `SubjectResults`. If Power BI created this relationship automatically, check it instead of creating a duplicate.

The source query currently reads:

`C:\Users\Chandana H M\OneDrive\Desktop\Student_Result_BI\output\cleaned_student_results.csv`

## 3. Add the measures

1. Select the `Students` table in the Data or Model pane.
2. Select **Table tools** or **Modeling → New measure**.
3. In `Measures.dax`, copy one measure at a time, starting with its name and `=` through the end of that formula. Paste it in the formula bar and press **Enter**.
4. Repeat for every measure in the file. Create the measures in `Students` (or a dedicated measures table); the formulas refer to the table names `Students` and `SubjectResults`.
5. Select `Average Percentage`, `Average Attendance`, and `Pass Percentage` measures, then choose **Measure tools → Format → Percentage**. The underlying source values use a 0–100 scale; these measures return 0–1 for percentage formatting.
6. Set `Average Subject Marks` to a decimal number (or whole number) format. It remains on a 0–100 scale.

## 4. Build the report pages

Use the **Report** view. To add a visual, select its icon in **Visualizations**, then drag fields from the Data pane into the visual's **Build visual** wells. To rename a page, double-click its tab. Add pages with the **+** beside the tabs. For each percentage measure, use percentage format; keep marks and raw attendance on a 0–100 axis.

### Page 1 — Overall Dashboard

1. Rename the first page `Overall Dashboard`.
2. Add four **Card** visuals with `Total Students`, `Average Percentage`, `Pass Percentage`, and `Failed Students`, one measure per card.
3. Add a **Donut chart**. Put `Result` in **Legend** and `Total Students` in **Values**.
4. Add a **Clustered bar chart**. Put `Department` on the category axis and `Average Percentage` in **Values**.
5. Add an optional Card for `Average Attendance`.
6. Add **Slicer** visuals for `Department`, `Semester`, and `Gender` if there is room.

### Page 2 — Subject Analysis

1. Add a page named `Subject Analysis`.
2. Add a **Clustered column chart** with `SubjectResults[Subject]` on the X-axis and `Average Subject Marks` on the Y-axis.
3. In the visual's **Format** pane, set the Y-axis minimum to `0` and maximum to `100`.
4. Add a **Matrix** with `Department` in **Rows**, `SubjectResults[Subject]` in **Columns**, and `Average Subject Marks` in **Values**.
5. Add Cards for `Best Subject` and `Worst Subject`.
6. Add Department, Semester, and Gender slicers if there is room.

### Page 3 — Student Analysis

1. Add a page named `Student Analysis`.
2. Add a **Table** with `Student_ID`, `Student_Name`, `Department`, `Percentage`, and `Grade`.
3. In that visual's **Filters** pane, add `Student_ID`; change its filter type to **Top N**, enter `10`, drag `Percentage` into **By value**, and select **Apply filter**. Sort the table by Percentage descending.
4. Add another **Table** with `Student_ID`, `Student_Name`, `Department`, `Percentage`, and `Result`. In its visual-level filters, keep only `Result = Fail`.
5. Add a third **Table** with `Student_ID`, `Student_Name`, `Attendance`, `Percentage`, and `Result`. Filter `Improvement Status` to `Needs Improvement`.
6. Add Department, Semester, and Gender slicers if there is room.

### Page 4 — Attendance Analysis

1. Add a page named `Attendance Analysis`.
2. Add a **Scatter chart**. Set `Attendance` to the X-axis, `Percentage` to the Y-axis, `Student_ID` to **Details/Values**, and optionally `Department` to **Legend**. If Power BI aggregates either axis, open that field's dropdown and choose **Don't summarize**.
3. Add a **Clustered column chart** with `Attendance Band` on the X-axis and `Average Percentage` in **Values**.
4. Add a **Clustered bar chart** with `Department` on the category axis and `Average Percentage` in **Values**.
5. Add Department and Semester slicers.

## 5. Save and check the report

1. Select **File → Save as** and save the report as `Student_Result_BI.pbix` in the project folder.
2. Check that Page 1 shows 200 students and a pass percentage of 80.50% for the generated dataset before applying slicers.
3. Check that Subject Analysis shows five subjects and Attendance Analysis shows the attendance bands.
4. For later updates, rerun `main.py`, open the report, and choose **Home → Refresh**.

## Files in this folder

- `Students.pq` — imports the cleaned CSV and adds attendance and improvement categories.
- `SubjectResults.pq` — unpivots the five subject columns into student-subject rows.
- `Measures.dax` — measures for the KPI cards and subject analysis.
