# DSBD-Project
University project related to Distributed Systems and Big Data.

## Configuration
After cloning the repository, execute the command:

```bash
docker compose up
```

Upon the start of each container, routine operations necessary for the system's use will be performed: table creation, insertion of initial values, communication setup, process startup, etc.

<strong>An estimated startup time (for the reasons mentioned above) is approximately 3-4 minutes.</strong>

Refer to the `Configuration` section (<a href="https://github.com/matteopidone/DSBD-Project/blob/main/Relazione%20Progetto%20DSBD.pdf" target="_blank">Project Documentation</a>) for all details related to this phase.

In case of a failed building process (kafka errors, health check failed, etc.), it is necessary to execute:
```bash
docker compose down && docker compose up
```

### Requirements
It is recommended to allocate at least 3/4 GB of RAM to Docker Desktop to avoid sudden termination issues of processes within the `ETL Data Pipeline` (`Error 137, Error 0`)

## Data Retrieval
Port 9003
 - Metrics: `localhost:9003/` <a href="http://localhost:9003" target="_blank">Click here</a>

## SLA Manager
Port 9004
- Past violation count: `localhost:9004/pastViolation` <a href="http://localhost:9004/pastViolation" target="_blank">Click here</a>
- Indication of possible violations: `localhost:9004/futureViolation` <a href="http://localhost:9004/futureViolation" target="_blank">Click here</a>
