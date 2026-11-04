# AWS analytics architecture

**Design status: planned, not deployed (4 November 2026).**

The connected AWS account authenticated successfully via STS, and Glue returned no databases. However:
- S3 `ListBuckets`: `NotSignedUp`
- Athena `ListWorkGroups`: `SubscriptionRequiredException`
- S3 Tables `ListTableBuckets`: `ForbiddenException`

**No buckets, S3 Tables, databases, ingestion jobs or model endpoints were created.**

## Intended architecture

```text
NASA PDS source archives
         │
         ▼
Amazon S3: private raw zone
         │
         ▼
AWS Glue: parse PDS, clean, align wavelengths, join labels
         │
         ▼
Amazon S3: curated Parquet datasets
         │
         ├──► Glue Data Catalog
         │            │
         │            ▼
         │          Athena ──► audits and exploration
         │
         └──► future managed training + model artefacts
```

The existing local notebook remains the reference machine-learning implementation until a reproducible data pipeline is established.

## Suggested storage layout

```
s3://<bucket>/astromine/raw/smass-ii/
s3://<bucket>/astromine/raw/taxonomy/
s3://<bucket>/astromine/curated/spectral_points/
s3://<bucket>/astromine/curated/taxonomy/
s3://<bucket>/astromine/experiments/<run-id>/
```

Use encryption, S3 Block Public Access, short-lived credentials, versioned artefacts, and narrow IAM permissions. Establish AWS Budgets notifications **before** provisioning managed services. Do not develop the pipeline as the AWS account root user.

## Migration sequence
1. Enable S3 and Athena and resolve S3 Tables authorization; choose a region, IAM roles and cost limits.
2. Upload source archives preserving original filenames and hashes.
3. Run Glue transformations to validated long-form Parquet; record sample counts and null statistics.
4. Register the curated datasets in Glue and query using Athena.
5. Compare per-class and per-spectrum totals with the notebook's recorded reference values.
6. Introduce managed ML services only after local reproducibility and cost evaluation.

## Illustrative Athena checks

```sql
SELECT COUNT(DISTINCT spectrum_id) FROM astromine.spectral_points;
SELECT spectrum_id, COUNT(*) AS spectral_rows
FROM astromine.spectral_points
GROUP BY spectrum_id
ORDER BY spectral_rows DESC
LIMIT 10;
```

See `aws/athena_schemas.sql` for an **unexecuted CSV staging schema**. Production analytics should favour typed Parquet.
