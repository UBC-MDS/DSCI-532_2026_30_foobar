import duckdb

duckdb.execute(f"""
    COPY (
        SELECT 
            * EXCLUDE ("Affects_Academic_Performance"),
            CASE WHEN "Affects_Academic_Performance" = true THEN 'Yes' ELSE 'No' END AS "Affects_Academic_Performance"
        FROM read_csv_auto('raw/Students-Social-Media-Addiction.csv')
    )
    TO 'processed/Students-Social-Media-Addiction.parquet' (FORMAT PARQUET)
""")