import re
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# 1. HELPER FUNCTIONS
# ---------------------------------------------------------

def parse_time_to_ms(time_str):
    """
    Parses string 'H:M:S:ms' (e.g., '0:00:00:096') to milliseconds (float).
    """
    try:
        parts = time_str.strip().split(':')
        if len(parts) == 4:
            h, m, s, ms = map(int, parts)
            return (h * 3600000) + (m * 60000) + (s * 1000) + ms
        elif len(parts) == 3: # Fallback for H:M:S
            h, m, s = map(int, parts)
            return (h * 3600000) + (m * 60000) + (s * 1000)
    except ValueError:
        return None
    return None

def parse_log_file(filename):
    """
    Reads the log file line by line and extracts parameters using Regex.
    Returns a Pandas DataFrame.
    """
    data = []
    
    # Regex Explanation:
    # 1. test_(?P<exp_type>[a-z0-9]+)_input  -> Captures 'k', 'n1', or 'n2' from folder name
    # 2. /(?P<algo>approx|exact)/            -> Captures algorithm type
    # 3. n1_(?P<n1>\d+)_n2_(?P<n2>\d+)_k_(?P<k>\d+) -> Captures parameters
    # 4. :\s+(?P<time>[\d:]+)                -> Captures time string
    pattern = re.compile(
        r"test_(?P<exp_type>\w+)_input/"
        r"(?P<algo>approx|exact)/.*?/"
        r"test_n1_(?P<n1>\d+)_n2_(?P<n2>\d+)_k_(?P<k>\d+)_\d+\.txt:\s+"
        r"(?P<time>[\d:]+)"
    )

    print(f"Reading {filename}...")
    
    with open(filename, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                entry = match.groupdict()
                
                # Convert types
                row = {
                    'exp_type': entry['exp_type'], # e.g., 'k', 'n1', 'n2'
                    'algo': entry['algo'],
                    'n1': int(entry['n1']),
                    'n2': int(entry['n2']),
                    'k': int(entry['k']),
                    'time_ms': parse_time_to_ms(entry['time'])
                }
                data.append(row)

    if not data:
        print("No valid data found matching the pattern.")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    return df

# ---------------------------------------------------------
# 2. PLOTTING LOGIC
# ---------------------------------------------------------

def generate_plots(df):
    """
    Groups data and generates plots for each experiment type.
    """
    df_avg = df.groupby(['exp_type', 'algo', 'n1', 'n2', 'k'])['time_ms'].mean().reset_index()

    # Get unique experiment types (e.g., 'k', 'n1', 'n2') found in the file
    experiments = df_avg['exp_type'].unique()

    for exp in experiments:
        # Filter data for this experiment category
        exp_data = df_avg[df_avg['exp_type'] == exp]
        
        # Determine which column is the X-axis
        x_col = exp  # e.g., 'k', 'n1', or 'n2'
        
        # Determine fixed columns (the other two)
        param_cols = {'n1', 'n2', 'k'}
        fixed_cols = list(param_cols - {x_col})
        
        grouped_scenarios = exp_data.groupby(fixed_cols)

        for fixed_vals, scenario_df in grouped_scenarios:
            # Create a label for the fixed parameters
            title_suffix = ", ".join([f"{col}={val}" for col, val in zip(fixed_cols, fixed_vals)])
            
            # Iterate through available algorithms to plot them separately
            unique_algos = scenario_df['algo'].unique()
            
            for algo in unique_algos:
                plt.figure(figsize=(10, 6))
                
                # Filter data for specific algorithm
                algo_data = scenario_df[scenario_df['algo'] == algo].sort_values(by=x_col)
                
                # Style settings
                color = 'blue' if algo == 'approx' else 'red'
                marker = 'o' if algo == 'approx' else 's'
                
                plt.plot(algo_data[x_col], algo_data['time_ms'], marker=marker, label=algo.capitalize(), linestyle='-', color=color)

                plt.title(f"{algo.capitalize()} Avg Execution Time vs {x_col.upper()}\n(Fixed: {title_suffix})")
                plt.xlabel(f"{x_col} value")
                plt.ylabel("Time [ms]")
                plt.legend()
                plt.grid(True, which='both', linestyle='--', linewidth=0.5)
                
                # Save with distinct filename per algorithm
                filename_safe_title = f"plot_{algo}_var_{x_col}_{title_suffix.replace(', ', '_').replace('=', '')}.png"
                plt.savefig(os.path.join("fig", filename_safe_title))
                print(f"Generated plot: {filename_safe_title}")
                plt.close() # Close to free memory

# ---------------------------------------------------------
# 3. MAIN EXECUTION (With Dummy Data Generator)
# ---------------------------------------------------------

def create_dummy_log(filename):
    """Creates a sample log file for demonstration purposes."""
    lines = []
    import random
    
    # Scene 1: Varying K, fixed n1=50, n2=25
    n1, n2 = 50, 25
    for k in range(5, 55, 5): # k = 5, 10, ... 50
        for i in range(1, 11): # 10 tests
            # Exact takes longer as K grows
            t_exact = 80 + (k * 2) + random.randint(-5, 5) 
            # Approx is faster and constant-ish
            t_approx = 40 + (k * 0.5) + random.randint(-5, 5)
            
            # Format: H:M:S:ms
            lines.append(f"test_k_input/exact/random/test_n1_{n1:03d}_n2_{n2:03d}_k_{k:03d}_{i:03d}.txt: 0:00:00:{t_exact:03d}")
            lines.append(f"test_k_input/approx/random/test_n1_{n1:03d}_n2_{n2:03d}_k_{k:03d}_{i:03d}.txt: 0:00:00:{t_approx:03d}")

    # Scene 2: Varying N1, fixed n2=25, k=10
    n2, k = 25, 10
    for n1 in range(50, 550, 50):
        for i in range(1, 11):
            t_exact = 100 + (n1 * 0.8) + random.randint(-10, 10)
            t_approx = 50 + (n1 * 0.1) + random.randint(-5, 5)
            
            lines.append(f"test_n1_input/exact/random/test_n1_{n1:03d}_n2_{n2:03d}_k_{k:03d}_{i:03d}.txt: 0:00:00:{t_exact:03d}")
            lines.append(f"test_n1_input/approx/random/test_n1_{n1:03d}_n2_{n2:03d}_k_{k:03d}_{i:03d}.txt: 0:00:00:{t_approx:03d}")

    with open(filename, 'w') as f:
        f.write('\n'.join(lines))
    print("Dummy log file created.")

if __name__ == "__main__":
    LOG_FILE = "C:/Users/kegor/Downloads/execution_times.log"
    
    # Check if file exists, if not create dummy data
    if not os.path.exists(LOG_FILE):
        print(f"'{LOG_FILE}' not found. Creating dummy data for demonstration...")
        create_dummy_log(LOG_FILE)
    
    # 1. Parse
    df = parse_log_file(LOG_FILE)
    
    # 2. Plot
    if not df.empty:
        generate_plots(df)
        print("Done! Check the directory for .png files.")
    else:
        print("Dataset is empty. Check your log file format.")