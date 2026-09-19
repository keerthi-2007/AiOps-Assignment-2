
import json
import re
import pandas as pd
from kubernetes import client, config
JOB_NAME = "shard-validator-job"
NAMESPACE = "default"
def main():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(
        namespace=NAMESPACE,
        label_selector=f"job-name={JOB_NAME}"
    )
    results = []
    for pod in pods.items:
        pod_name = pod.metadata.name
        logs = v1.read_namespaced_pod_log(name = pod_name, namespace=NAMESPACE)
        match = re.search(r"RESULT_JSON:(\{.*\})", logs)
        if match:
            result = json.loads(match.group(1))
            results.append(result)
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("completion_index").reset_index(drop = True)
    print("\nResults collected through kubernetes API:\n")
    print(df.to_string(index=False))
    print("\nSummary:")
    print(f"Pods found: {len(pods.items)}")
    print(f"Results collected: {len(results)}")
    if not df.empty:
        print(f"Total rows processed: {df['total_rows'].sum()}")
        print(f"Total invalid rows: {df['invalid_rows'].sum()}")
        print(f"Total valid rows: {df['valid_rows'].sum()}")

if __name__ == "__main__":
    main()
