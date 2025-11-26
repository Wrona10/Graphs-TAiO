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

INPUT_DIR = "input"
OUTPUT_DIR = "output"


def parse_n1(filepath):
    """Extract n1 from the first number in the test file."""
    try:
        with open(filepath, "r") as f:
            first_line = f.readline().strip()
            match = re.match(r"(\d+)", first_line)
            return int(match.group(1)) if match else None
    except Exception:
        return None


def run_test(input_file, output_file, mode="exact", use_docker=False):
    """Run single test and return execution time in seconds."""
    if use_docker:
        input_path = os.path.abspath(input_file)
        output_path = os.path.abspath(output_file)
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        cmd = [
            "docker", "run", "--rm",
            "-v", f"{input_path}:/app/input.txt:ro",
            "-v", f"{output_dir}:/app/output",
            "grafy-taio:latest",
        ]
        if mode == "approx":
            cmd.append("-a")
        cmd.extend(["/app/input.txt", f"/app/output/{os.path.basename(output_path)}"])
    else:
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
            print(f"{RED}  FAILED: {input_file.name} - Exit code: {result.returncode}{RESET}")
            if result.stderr:
                print(f"{RED}     Error: {result.stderr[:150]}{RESET}")
            return None

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
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n=== Running {mode.upper()} tests from {test_dir} ===")

    for test_file in sorted(Path(test_dir).glob("*.txt")):
        n1 = parse_n1(test_file)
        if n1 is None:
            continue

        output_file = Path(output_dir) / test_file.name.replace(".txt", "_out.txt")
        elapsed = run_test(test_file, output_file, mode, use_docker)
        if elapsed is not None:
            results[n1].append(elapsed)

    return results


def print_stats(results, label):
    """Print average times per n1."""
    if not results:
        print(f"\n=== {label} - No results ===")
        return

    print(f"\n=== {label} RESULTS ===")
    print(f"{'n1':<6} {'Count':<8} {'Avg Time (s)':<15}")
    print("-" * 30)

    for n1 in sorted(results.keys()):
        times = results[n1]
        avg = sum(times) / len(times)
        print(f"{n1:<6} {len(times):<8} {avg:<15.4f}")


def discover_graph_types(mode):
    """Discover graph type subdirectories for a given mode (exact/approx)."""
    mode_path = Path(INPUT_DIR) / mode
    if not mode_path.exists():
        return []

    return [d.name for d in sorted(mode_path.iterdir()) if d.is_dir() and list(d.glob("*.txt"))]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run graph algorithm tests")
    parser.add_argument("--docker", action="store_true", help="Use Docker instead of direct dotnet")
    parser.add_argument("--mode", type=str, choices=["exact", "approx", "both"], default="both", help="Algorithm mode")
    parser.add_argument("--types", type=str, nargs="+", default=None, help="Graph types to test (default: all)")
    args = parser.parse_args()

    modes = ["exact", "approx"] if args.mode == "both" else [args.mode]

    all_results = {}
    for mode in modes:
        available_types = discover_graph_types(mode)
        if not available_types:
            print(f"No test directories found in {INPUT_DIR}/{mode}/")
            continue

        types_to_run = args.types if args.types else available_types
        types_to_run = [t for t in types_to_run if t in available_types]

        for graph_type in types_to_run:
            input_dir = f"{INPUT_DIR}/{mode}/{graph_type}/"
            output_dir = f"{OUTPUT_DIR}/{mode}/{graph_type}/"

            results = run_all_tests(input_dir, output_dir, mode, args.docker)
            label = f"{graph_type.upper()} ({mode})"
            all_results[label] = results
            print_stats(results, label)

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    for label, results in all_results.items():
        if results:
            total_tests = sum(len(times) for times in results.values())
            total_time = sum(sum(times) for times in results.values())
            print(f"{label}: {total_tests} tests, {total_time:.2f}s total")
