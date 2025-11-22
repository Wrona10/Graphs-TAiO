"""Simple test runner for graph algorithm benchmarking."""

import os
import re
import subprocess
import time
from collections import defaultdict
from pathlib import Path

# ANSI color codes
RED = "\033[91m"
RESET = "\033[0m"


def parse_n1(filename):
    """Extract n1 from filename like test_n1_010_n2_010_k_002_001.txt or test_n110_n210_k02_001.txt"""
    match = re.search(r"n1_(\d+)", filename)
    return int(match.group(1)) if match else None


def run_test(input_file, output_file, mode="exact", use_docker=False):
    """Run single test and return execution time in seconds."""
    if use_docker:
        # Docker command with volume mounts
        input_path = os.path.abspath(input_file)
        output_path = os.path.abspath(output_file)
        output_dir = os.path.dirname(output_path)

        # Ensure output directory exists before mounting
        os.makedirs(output_dir, exist_ok=True)

        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{input_path}:/app/input.txt:ro",
            "-v",
            f"{output_dir}:/app/output",
            "grafy-taio:latest",
        ]
        if mode == "approx":
            cmd.append("-a")
        cmd.extend(["/app/input.txt", f"/app/output/{os.path.basename(output_path)}"])
    else:
        # Direct dotnet command
        cmd = ["dotnet", "run", "--project", "Grafy TAiO/Grafy TAiO.csproj", "--"]
        if mode == "approx":
            cmd.append("-a")
        cmd.append(str(input_file))
        cmd.append(str(output_file))

    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        elapsed = time.time() - start

        if result.returncode != 0:
            print(
                f"{RED}  FAILED: {input_file.name} - Exit code: {result.returncode}{RESET}"
            )
            if result.stderr:
                print(f"{RED}     Error: {result.stderr[:150]}{RESET}")
            return None

        # Check if output file was actually created
        if not os.path.exists(output_file):
            print(f"{RED}  WARNING: Output file not created: {output_file}{RESET}")

        print(f"  {input_file.name} - {elapsed:.3f}s")
        return elapsed
    except subprocess.TimeoutExpired:
        print(f"{RED}  TIMEOUT: {input_file.name} (>300s){RESET}")
        return None
    except FileNotFoundError as e:
        print(f"{RED}  ERROR: {input_file.name} - Command not found: {e}{RESET}")
        return None
    except Exception as e:
        print(f"{RED}  ERROR: {input_file.name} - {e}{RESET}")
        return None


def run_all_tests(test_dir, output_dir, mode="exact", use_docker=False):
    """Run all tests in directory, return dict of n1 -> [times]"""
    results = defaultdict(list)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n=== Running {mode.upper()} tests from {test_dir} ===")

    for test_file in sorted(Path(test_dir).glob("*.txt")):
        n1 = parse_n1(test_file.name)
        if n1 is None:
            continue

        output_file = Path(output_dir) / test_file.name.replace(".txt", "_out.txt")
        elapsed = run_test(test_file, output_file, mode, use_docker)
        if elapsed is not None:
            results[n1].append(elapsed)

    return results


def print_stats(results, mode):
    """Print average times per n1."""
    print(f"\n=== {mode.upper()} RESULTS ===")
    print(f"{'n1':<6} {'Count':<8} {'Avg Time (s)':<15}")
    print("-" * 30)

    for n1 in sorted(results.keys()):
        times = results[n1]
        avg = sum(times) / len(times)
        print(f"{n1:<6} {len(times):<8} {avg:<15.4f}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run graph algorithm tests")
    parser.add_argument(
        "--docker", action="store_true", help="Use Docker instead of direct dotnet"
    )
    args = parser.parse_args()

    # Run exact tests
    exact_results = run_all_tests("input/exact/", "output/exact/", "exact", args.docker)
    print_stats(exact_results, "exact")

    # Run approx tests
    approx_results = run_all_tests(
        "input/approx/", "output/approx/", "approx", args.docker
    )
    print_stats(approx_results, "approx")
