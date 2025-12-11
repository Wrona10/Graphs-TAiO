"""Simple test runner for graph algorithm benchmarking."""

import atexit
import os
import re
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

# ANSI color codes
RED = "\033[91m"
RESET = "\033[0m"

INPUT_DIR = "input"
OUTPUT_DIR = "output"
CONTAINER_NAME = "taio-test-runner"
_container_started = False


def start_docker_container():
    """Start a persistent Docker container for running tests."""
    global _container_started
    if _container_started:
        return True
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], capture_output=True)
    input_abs, output_abs = os.path.abspath(INPUT_DIR), os.path.abspath(OUTPUT_DIR)
    os.makedirs(output_abs, exist_ok=True)
    result = subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "--name",
            CONTAINER_NAME,
            "-v",
            f"{input_abs}:/app/input:ro",
            "-v",
            f"{output_abs}:/app/output",
            "--entrypoint",
            "tail",
            "grafy-taio:latest",
            "-f",
            "/dev/null",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"{RED}Failed to start Docker container: {result.stderr}{RESET}")
        return False
    _container_started = True
    atexit.register(stop_docker_container)
    print("Docker container started.")
    return True


def stop_docker_container():
    """Stop and remove the Docker container."""
    global _container_started
    if _container_started:
        subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], capture_output=True)
        _container_started = False
        print("\nDocker container stopped.")


def parse_n1_n2_k(filepath):
    """Extract n1, n2, k from filename like test_n1_000010_n2_010000_k_003_002.txt"""
    filename = Path(filepath).stem
    match = re.search(r"n1_(\d+)_n2_(\d+)_k_(\d+)", filename)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    return None, None, None


def run_test(input_file, output_file, mode="exact", use_docker=False):
    """Run single test and return execution time in seconds."""
    if use_docker:
        input_rel = os.path.relpath(input_file, INPUT_DIR)
        output_rel = os.path.relpath(output_file, OUTPUT_DIR)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        cmd = ["docker", "exec", CONTAINER_NAME, "dotnet", "Grafy TAiO.dll"]
        if mode == "approx":
            cmd.append("-a")
        cmd.extend([f"/app/input/{input_rel}", f"/app/output/{output_rel}"])
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
            print(
                f"{RED}  FAILED: {input_file.name} - Exit code: {result.returncode}{RESET}"
            )
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
        n1, n2, k = parse_n1_n2_k(test_file)

        if n2 > 10000:
            print("too big n2", file=sys.stderr)
            continue

        output_file = Path(output_dir) / test_file.name.replace(".txt", "_out.txt")
        elapsed = run_test(test_file, output_file, mode, use_docker)
        if elapsed is not None:
            results[(n1, n2, k)].append(elapsed)

    return results


def print_stats(results, label):
    """Print average times per (n1, n2, k)."""
    if not results:
        print(f"\n=== {label} - No results ===")
        return

    print(f"\n=== {label} RESULTS ===")
    print(f"{'n1':<8} {'n2':<8} {'k':<6} {'Count':<8} {'Avg Time (s)':<15}")
    print("-" * 50)

    for n1, n2, k in sorted(results.keys()):
        times = results[(n1, n2, k)]
        avg = sum(times) / len(times)
        print(f"{n1:<8} {n2:<8} {k:<6} {len(times):<8} {avg:<15.4f}")


def discover_graph_types(mode):
    """Discover graph type subdirectories for a given mode (exact/approx)."""
    mode_path = Path(INPUT_DIR) / mode
    if not mode_path.exists():
        return []

    return [
        d.name
        for d in sorted(mode_path.iterdir())
        if d.is_dir() and list(d.glob("*.txt"))
    ]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run graph algorithm tests")
    parser.add_argument(
        "--docker", action="store_true", help="Use Docker instead of direct dotnet"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["exact", "approx", "both"],
        default="both",
        help="Algorithm mode",
    )
    parser.add_argument(
        "--types",
        type=str,
        nargs="+",
        default=None,
        help="Graph types to test (default: all)",
    )
    args = parser.parse_args()

    modes = ["exact", "approx"] if args.mode == "both" else [args.mode]

    if args.docker and not start_docker_container():
        exit(1)

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
