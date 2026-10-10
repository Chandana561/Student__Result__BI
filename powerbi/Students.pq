let
    CsvPath = "C:\Users\Chandana H M\OneDrive\Desktop\Student_Result_BI\output\cleaned_student_results.csv",
    Source = Csv.Document(
        File.Contents(CsvPath),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    TypedColumns = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"Student_ID", type text},
            {"Student_Name", type text},
            {"Gender", type text},
            {"Department", type text},
            {"Semester", Int64.Type},
            {"Attendance", Int64.Type},
            {"Maths", Int64.Type},
            {"DBMS", Int64.Type},
            {"CN", Int64.Type},
            {"OS", Int64.Type},
            {"AI", Int64.Type},
            {"Total_Marks", Int64.Type},
            {"Percentage", type number},
            {"Result", type text},
            {"Grade", type text},
            {"Performance_Category", type text}
        }
    ),
    AddedAttendanceBand = Table.AddColumn(
        TypedColumns,
        "Attendance Band",
        each
            if [Attendance] <= 60 then "0-60%"
            else if [Attendance] <= 70 then "61-70%"
            else if [Attendance] <= 80 then "71-80%"
            else if [Attendance] <= 90 then "81-90%"
            else "91-100%",
        type text
    ),
    AddedImprovementStatus = Table.AddColumn(
        AddedAttendanceBand,
        "Improvement Status",
        each
            if [Percentage] < 50 or [Attendance] < 75
            then "Needs Improvement"
            else "On Track",
        type text
    )
in
    AddedImprovementStatus
