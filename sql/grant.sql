-- Create service account and insert it into <service-account>
-- Job User is granted on the project in IAM, not in this query
SET @@location = 'australia-southeast1';

GRANT `roles/bigquery.dataEditor`
ON SCHEMA `aemo-pipeline.raw`
TO "serviceAccount:<service-account>";

GRANT `roles/bigquery.dataEditor`
ON SCHEMA `aemo-pipeline.staging`
TO "serviceAccount:<service-account>";

GRANT `roles/bigquery.dataEditor`
ON SCHEMA `aemo-pipeline.marts`
TO "serviceAccount:<service-account>";