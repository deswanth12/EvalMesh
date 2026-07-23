#!/usr/bin/env python3
"""
EvalMesh Quickstart Launcher
Run: python evalmesh_start.py
"""
import sys
import subprocess

def start_evalmesh():
    print("===============================================================")
    print(" 🚀 LAUNCHING EVALMESH AI AGENT CONTROL PLANE")
    print("===============================================================")
    print(" ► Web Dashboard : http://localhost:8000")
    print(" ► API Docs UI   : http://localhost:8000/docs")
    print(" ► Proxy Gateway : http://localhost:8000/v1/chat/completions")
    print("===============================================================\n")

    cmd = [sys.executable, "-m", "evalmesh.cli", "--port", "8000"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[INFO] EvalMesh Proxy Server stopped safely.")

if __name__ == "__main__":
    start_evalmesh()
