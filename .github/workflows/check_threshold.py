from pathlib import Path
import sys
import mlflow

THRESHOLD = 0.85

run_id = Path("model_info.txt").read_text().strip()
client = mlflow.tracking.MlflowClient()
run = client.get_run(run_id)

accuracy = run.data.metrics.get("val_accuracy")
if accuracy is None:
    raise RuntimeError("val_accuracy not found")

print("Run ID:", run_id)
print("Validation accuracy:", accuracy)

if accuracy < THRESHOLD:
    print("Threshold check failed")
    sys.exit(1)

print("Threshold check passed")
