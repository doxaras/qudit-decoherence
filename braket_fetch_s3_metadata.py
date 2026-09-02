"""Re-fetch the Braket task result objects from S3 (free; no resubmission).

Retrieves the full per-shot measurement records, the measuredQubits
ordering, and IQM's compiled (routed) program for the two Garnet tasks,
writing results/braket_s3_<label>_results.json. This is the provenance
behind Sec. IX's resolution of the m=5 control-qubit inversion:

  * the committed histogram counts match the per-shot records exactly;
  * the measure map is explicit (c[0] = measure $10 in BOTH tasks), so
    the analysis bit order is what the device returned;
  * the two tasks were created within one second of each other
    (07:04:25.6 / 07:04:26.1 UTC, 2026-08-11), and the same qubit reads
    inverted at m=5 but normal at m=7 -- excluding a readout-assignment
    inversion (static on that timescale, shared between tasks) and
    leaving a spurious pi accumulated in the m=5 routed sequence.

Requires AWS credentials with read access to the task bucket.
Run: python3 braket_fetch_s3_metadata.py
"""

import json
import os

import boto3

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
REGION = "eu-north-1"
TASKS = {
    "garnet_m5": "arn:aws:braket:eu-north-1:081731914950:quantum-task/"
                 "f38e3137-a394-4f4e-8153-ed2bdf2b6880",
    "garnet_m7": "arn:aws:braket:eu-north-1:081731914950:quantum-task/"
                 "08f87bf6-307e-4558-a4c8-7d6830b639c7",
}


def main():
    bk = boto3.client("braket", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)
    for label, arn in TASKS.items():
        t = bk.get_quantum_task(quantumTaskArn=arn)
        key = f"{t['outputS3Directory']}/results.json"
        obj = json.loads(s3.get_object(Bucket=t["outputS3Bucket"],
                                       Key=key)["Body"].read())
        path = os.path.join(RESULTS, f"braket_s3_{label}_results.json")
        with open(path, "w") as fh:
            json.dump(obj, fh)
        prog = obj["additionalMetadata"]["iqmMetadata"]["compiledProgram"]
        measures = [l for l in prog.splitlines() if "measure" in l]
        tm = obj["taskMetadata"]
        print(f"{label}: {tm['createdAt']}  shots={tm['shots']}")
        print(f"  measuredQubits={obj['measuredQubits']}")
        for line in sorted(measures):
            print(f"  {line}")


if __name__ == "__main__":
    main()
