"""Worker that executes queued jobs and materializes due schedules."""

from __future__ import annotations

import logging
import time

from src.main import execute_job, materialize_due_schedules, pop_job_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("job_worker")


def main() -> None:
    logger.info("job worker started")
    while True:
        materialize_due_schedules()
        job_id = pop_job_id(timeout=1)
        if job_id is not None:
            logger.info("executing job %s", job_id)
            execute_job(job_id)
        else:
            time.sleep(0.2)


if __name__ == "__main__":
    main()
