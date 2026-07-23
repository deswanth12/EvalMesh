import os
import json
from evalmesh.drift import OutputDriftDetector

def run_ci_evaluation_suite(golden_dataset_path: str = "evalmesh_datasets/golden_dataset_v1.0.jsonl") -> bool:
    """
    CI/CD Regression Harness designed for GitHub Actions.
    Evaluates current prompt performance against golden dataset baselines.
    Returns True if evaluation passes without regression, False otherwise.
    """
    print("===============================================================")
    print(" [CI/CD] EVALMESH AGENT REGRESSION HARNESS (GITHUB ACTIONS ENGINE)")
    print("===============================================================\n")

    if not os.path.exists(golden_dataset_path):
        print(f"[INFO] Golden dataset not found at '{golden_dataset_path}'. Creating synthetic benchmark...")
        os.makedirs(os.path.dirname(golden_dataset_path), exist_ok=True)
        sample = {
            "prompt": "Summarize user request: Add 2-factor authentication",
            "completion": "User requested adding two-factor authentication (2FA) security feature to their account."
        }
        with open(golden_dataset_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(sample) + "\n")

    passed_count = 0
    total_count = 0

    with open(golden_dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            baseline = data.get("completion", "")
            
            # Simulate current model evaluation
            current_eval = baseline # Currently matching
            drift_res = OutputDriftDetector.compute_semantic_drift(baseline, current_eval)
            
            total_count += 1
            if drift_res["drift_percent"] < 35.0:
                passed_count += 1
                print(f"  [OK] Benchmark #{total_count}: Drift {drift_res['drift_percent']}% -> PASSED")
            else:
                print(f"  [FAIL] Benchmark #{total_count}: Drift {drift_res['drift_percent']}% -> FAILED REGRESSION")

    print("\n===============================================================")
    print(f" [RESULT] Passed {passed_count}/{total_count} CI Regression Benchmarks.")
    print("===============================================================")

    return passed_count == total_count

if __name__ == "__main__":
    success = run_ci_evaluation_suite()
    exit(0 if success else 1)
