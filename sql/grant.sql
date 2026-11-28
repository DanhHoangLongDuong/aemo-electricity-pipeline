-- Create service account and insert it into <service-account>
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