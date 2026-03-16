import duckdb

duckdb.execute("""
    COPY (SELECT * FROM read_csv_auto('raw/Students-Social-Media-Addiction.csv'))
    TO 'processed/Students-Social-Media-Addiction.parquet' (FORMAT PARQUET)
""")