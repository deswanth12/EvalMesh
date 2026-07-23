import os
import json
import time
from typing import Dict, Any, List

class GoldenDatasetGenerator:
    """
    Automated Golden Dataset Compilation Engine.
    Ingests verified production prompts and completions to build versioned benchmark datasets.
    """

    def __init__(self, storage_dir: str = "evalmesh_datasets"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def record_pair(self, prompt: str, completion: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Records a verified high-quality prompt-completion pair into the golden dataset buffer.
        """
        entry = {
            "id": f"golden_{int(time.time()*1000)}",
            "timestamp": time.time(),
            "prompt": prompt,
            "completion": completion,
            "metadata": metadata or {}
        }
        
        filename = os.path.join(self.storage_dir, "golden_dataset_latest.jsonl")
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        return entry

    def export_dataset(self, version: str = "v1.0") -> str:
        """
        Exports the current golden dataset buffer to a versioned release file.
        """
        source_file = os.path.join(self.storage_dir, "golden_dataset_latest.jsonl")
        target_file = os.path.join(self.storage_dir, f"golden_dataset_{version}.jsonl")
        
        if os.path.exists(source_file):
            with open(source_file, "r", encoding="utf-8") as sf, open(target_file, "w", encoding="utf-8") as tf:
                tf.write(sf.read())
                
        return target_file
