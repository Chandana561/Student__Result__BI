let
    Source = Students,
    UnpivotedSubjects = Table.Unpivot(
        Source,
        {"Maths", "DBMS", "CN", "OS", "AI"},
        "Subject",
        "Marks"
    ),
    SelectedColumns = Table.SelectColumns(
        UnpivotedSubjects,
        {"Student_ID", "Subject", "Marks"}
    ),
    TypedColumns = Table.TransformColumnTypes(
        SelectedColumns,
        {
            {"Student_ID", type text},
            {"Subject", type text},
            {"Marks", Int64.Type}
        }
    )
in
    TypedColumns
