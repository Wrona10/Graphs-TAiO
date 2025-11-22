Uwagi pana Homendy:
1. Poprawić dokumentację na kolejny etap z opisem algorytmu znajdowania permutacji (+ ew. inne nieścisłości).
2. Możliwość uruchomienia 4 programów (może być ta sama binarka, tylko z flagą): zwraca rozszerzenie lub odległość (dla każdej opcji dokładny lub aproksyamcyjny).
3. Testy średniego czasu wykonania (dla kazdej z ww. opcji) dla dokładnego n=1,2,...,10, dla aproksymacyjnego n=10,20,...,100

## Test Graph Generator

A Python script for generating test input directed multigraphs with customizable parameters.

### Command Line Usage

```bash
# Basic usage (generates two graphs with 4 and 3 vertices)
python generate_graphs.py

# Custom sizes
python generate_graphs.py --n1 10 --n2 8 --k 2

# Different densities: sparse, default, dense, multi (multigraph)
python generate_graphs.py --n1 5 --n2 5 --density multi

# Allow self-loops
python generate_graphs.py --n1 5 --n2 5 --loops

# Custom output file
python generate_graphs.py --n1 10 --n2 10 -o input/large_test.txt

# Reproducible with seed
python generate_graphs.py --n1 5 --n2 5 --seed 42

# Generate multiple test cases to separate files
python generate_graphs.py --count 10 --n1 5 --n2 5

# Custom directory and prefix
python generate_graphs.py -c 20 -d tests/data -p graph --n1 8 --n2 6
```

### As a Python Module

```python
from generate_graphs import generate_graph, save_test_input, generate_batch, probability_edge_func

# Custom edge function: 70% probability, up to 3 edges
custom_func = probability_edge_func(0.7, max_edges=3)

# Generate and save single test case
save_test_input("input/test.txt", n1=10, n2=8, k=2,
                edge_func1=custom_func, allow_loops=True)

# Generate multiple test cases
generate_batch("input", count=10, n1=5, n2=5, prefix="test")

# Or create your own edge function
def my_edge_func(u, v, n):
    return 2 if (u + v) % 2 == 0 else 0

graph = generate_graph(5, edge_func=my_edge_func, allow_loops=True)
```

### Options

| Option | Description |
|--------|-------------|
| `--n1` | Number of vertices in first graph (default: 4) |
| `--n2` | Number of vertices in second graph (default: 3) |
| `--k` | Optional k parameter |
| `-o, --output` | Output file path (single mode, default: input/generated.txt) |
| `-d, --output-dir` | Output directory (batch mode) |
| `-c, --count` | Number of test cases to generate |
| `-p, --prefix` | Filename prefix for batch mode (default: test) |
| `--density` | Preset: sparse, default, dense, multi |
| `--loops` | Allow self-loops |
| `--seed` | Random seed for reproducibility |

## Running Tests

Use `run_tests.py` to execute all tests and measure performance:

```bash
# Run with Docker
python3 run_tests.py --docker

# Run with dotnet directly
python3 run_tests.py
```

The script will:
- Execute all tests from `input/exact/` and `input/approx/`
- Save results to `output/exact/` and `output/approx/`
- Calculate and display average execution time for each graph size (n1)
