-- AstroMine Athena EXAMPLE ONLY. Not executed.
-- Replace <YOUR_BUCKET> with the name of a private S3 bucket.
-- Intended for a long-form CSV exported using scripts/export_spectra.py.
CREATE DATABASE IF NOT EXISTS astromine;

CREATE EXTERNAL TABLE IF NOT EXISTS astromine.spectral_points (
    spectrum_id STRING,
    wavelength_um STRING,
    reflectance STRING,
    uncertainty STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    'separatorChar' = ',',
    'quoteChar' = '"'
)
STORED AS TEXTFILE
LOCATION 's3://<YOUR_BUCKET>/astromine/curated/spectral_points_csv/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- When querying, TRY_CAST(wavelength_um AS DOUBLE) and
-- TRY_CAST(reflectance AS DOUBLE). Consider Glue/Parquet for typed values.
