import os
import subprocess
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# Path to your executable (using raw string r"" for Windows paths)
EXE_PATH = r".\Grafy TAiO\bin\Release\net8.0\Grafy TAiO.exe"

# Input and Output directories
INPUT_ROOT = r".\complexity_tests"
OUTPUT_ROOT = r".\complexity_tests_results"
LOG_FILE = "execution_times.log"

def format_duration(td):
    """
    Formats a timedelta object into H:MM:SS:ms format
    Example: 0:00:12:453
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = int(td.microseconds / 1000)
    
    return f"{hours}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

def main():
    # Create the log file (or clear it if it exists)
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Execution Log - Started at {datetime.now()}\n")
        f.write("-" * 50 + "\n")

    print(f"Starting tests...")
    print(f"Input: {INPUT_ROOT}")
    print(f"Output: {OUTPUT_ROOT}")

    # Walk through the directory structure
    for root, dirs, files in os.walk(INPUT_ROOT):
        for filename in files:
            # We assume we only want to process text files or specific inputs
            # Remove this check if you want to process ALL files regardless of extension
            if not filename.endswith(".txt"): 
                continue

            input_full_path = os.path.join(root, filename)
            
            # Calculate relative path (e.g., test_k_input\approx\random\file.txt)
            rel_path = os.path.relpath(input_full_path, INPUT_ROOT)
            
            # Construct output path
            output_full_path = os.path.join(OUTPUT_ROOT, rel_path)
            
            # Ensure the directory for the output file exists
            os.makedirs(os.path.dirname(output_full_path), exist_ok=True)

            # Determine mode based on path
            # We look at the path components to see if "approx" is present
            path_parts = rel_path.split(os.sep)
            
            cmd = [EXE_PATH]
            
            if "approx" in path_parts:
                cmd.append("-a")
                
            cmd.append(input_full_path)
            cmd.append(output_full_path)

            print(f"Running: {rel_path}...")

            # Measure execution time
            start_time = datetime.now()
            
            try:
                # Run the subprocess
                subprocess.run(cmd, check=True, capture_output=True, timeout=900)
                
                end_time = datetime.now()
                duration = end_time - start_time
                formatted_duration = format_duration(duration)

                # Format log line: path/to/file: time
                # We replace backslashes with forward slashes for the log format consistency
                log_path = rel_path.replace("\\", "/")
                log_line = f"{log_path}: {formatted_duration}"

                # Append to log file immediately
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(log_line + "\n")

            except subprocess.CalledProcessError as e:
                print(f"Error running {filename}: {e}")
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(f"{rel_path}: ERROR\n")
            except Exception as e:
                print(f"Unexpected error: {e}")

    print("\nProcessing complete. Check execution_times.log.")

if __name__ == "__main__":
    main()