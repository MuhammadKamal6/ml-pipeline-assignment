from pathlib import Path
import sys
import os
import mlflow

THRESHOLD = 0.99

tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "file:./mlruns")
mlflow.set_tracking_uri(tracking_uri)

run_id = Path("model_info.txt").read_text().strip()
if not run_id:
    raise RuntimeError("model_info.txt is empty")

client = mlflow.tracking.MlflowClient()
run = client.get_run(run_id)

accuracy = run.data.metrics.get("val_accuracy")
if accuracy is None:
    raise RuntimeError("val_accuracy not found")

print("Run ID:", run_id)
print("Validation accuracy:", accuracy)

if accuracy < THRESHOLD:
    print(f"Threshold check failed: {accuracy:.4f} < {THRESHOLD}")
    sys.exit(1)

print(f"Threshold check passed: {accuracy:.4f} >= {THRESHOLD}")
