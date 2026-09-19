"""
generate_shards.py — AI Operations, Kubernetes Indexed Job

Generates 8 deterministic CSV shards.
Each shard contains 100 rows, including exactly 3
deliberately invalid rows.

The random seed makes the invalid-row placement reproducible.
"""

import argparse
import csv
import os
import random


COUNTRIES = [
    "India",
    "USA",
    "UK",
    "Canada",
    "Germany",
    "Australia",
]

NAMES = [
    "Aarav",
    "Aditya",
    "Rahul",
    "Priya",
    "Ananya",
    "Arjun",
    "Karthik",
    "Sneha",
]


def generate_shard(
    shard_id,
    n_rows=100,
    invalid_rows=3,
    random_state=42,
    out_dir="shards",
):
    rng = random.Random(random_state + shard_id)

    rows = []

    # Choose exactly `invalid_rows` positions in this shard.
    invalid_indices = set(
        rng.sample(range(n_rows), invalid_rows)
    )

    for i in range(n_rows):
        user_id = shard_id * n_rows + i + 1
        name = rng.choice(NAMES)
        email = f"user{user_id}@example.com"
        country = rng.choice(COUNTRIES)

        # Deliberately introduce invalid data.
        if i in invalid_indices:
            invalid_type = (i + shard_id) % 3

            if invalid_type == 0:
                # Invalid: missing name
                name = ""

            elif invalid_type == 1:
                # Invalid: malformed email
                email = f"user{user_id}-invalid"

            else:
                # Invalid: missing country
                country = ""

        rows.append(
            {
                "user_id": user_id,
                "name": name,
                "email": email,
                "country": country,
            }
        )

    os.makedirs(out_dir, exist_ok=True)

    output_file = os.path.join(
        out_dir,
        f"shard-{shard_id}.csv"
    )

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["user_id", "name", "email", "country"],
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Wrote {len(rows)} rows to {output_file} "
        f"with exactly {invalid_rows} invalid rows"
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--n-shards",
        type=int,
        default=8,
    )

    parser.add_argument(
        "--rows-per-shard",
        type=int,
        default=100,
    )

    parser.add_argument(
        "--invalid-per-shard",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
    )

    parser.add_argument(
        "--out-dir",
        default="shards",
    )

    args = parser.parse_args()

    for shard_id in range(args.n_shards):
        generate_shard(
            shard_id=shard_id,
            n_rows=args.rows_per_shard,
            invalid_rows=args.invalid_per_shard,
            random_state=args.random_state,
            out_dir=args.out_dir,
        )


if __name__ == "__main__":
    main()
