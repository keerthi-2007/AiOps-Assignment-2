"""
validate_shard.py — AI Operations (AIOps)

Entry point for each pod of the Kubernetes Indexed Job.
Each pod validates exactly one CSV shard based on its
JOB_COMPLETION_INDEX.
"""

import csv
import json
import os
import re
import socket
import time


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

SHARD_DIR = os.environ.get("SHARD_DIR", "/app/shards")


def is_valid(row):
    return (
        bool(row["user_id"])
        and bool(row["name"].strip())
        and bool(EMAIL_PATTERN.match(row["email"]))
        and bool(row["country"].strip())
    )


def validate_shard(data_path):
    total_rows = 0
    invalid_rows = 0

    with open(data_path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_rows += 1

            if not is_valid(row):
                invalid_rows += 1

    return total_rows, invalid_rows


def main():

    completion_index = int(
        os.environ.get("JOB_COMPLETION_INDEX", "0")
    )

    pod_name = os.environ.get(
        "POD_NAME",
        socket.gethostname()
    )

    node_name = os.environ.get(
        "NODE_NAME",
        "unknown"
    )

    shard_path = os.path.join(
        SHARD_DIR,
        f"shard-{completion_index}.csv"
    )

    print(
        f"[worker {completion_index}] "
        f"pod={pod_name} "
        f"node={node_name} "
        f"shard={shard_path}",
        flush=True
    )

    total_rows, invalid_rows = validate_shard(
        shard_path
    )

    result = {
        "completion_index": completion_index,
        "shard": f"shard-{completion_index}.csv",
        "total_rows": total_rows,
        "invalid_rows": invalid_rows,
        "valid_rows": total_rows - invalid_rows,
        "pod_name": pod_name,
        "node_name": node_name,
    }

    print(
        "RESULT_JSON:" + json.dumps(result),
        flush=True
    )

    # Keep the pod alive briefly so that actual concurrent
    # execution can be observed using kubectl.
    time.sleep(60)


if __name__ == "__main__":
    main()
