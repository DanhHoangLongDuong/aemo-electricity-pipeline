SET @@location = 'australia-southeast1';

CREATE SCHEMA IF NOT EXISTS `aemo-pipeline.raw`
    OPTIONS (
    location = 'australia-southeast1'
);
CREATE SCHEMA IF NOT EXISTS `aemo-pipeline.staging`
    OPTIONS (
    location = 'australia-southeast1'
);
CREATE SCHEMA IF NOT EXISTS `aemo-pipeline.marts`
    OPTIONS (
    location = 'australia-southeast1'
);