## Running Locally

```bash
dotnet run --project "Grafy TAiO/Grafy TAiO.csproj" -- input.txt output.txt       # exact mode
dotnet run --project "Grafy TAiO/Grafy TAiO.csproj" -- -a input.txt output.txt    # approximate mode
```

## Test Generation & Running

### Generate Tests

```bash
python generate_tests.py                     # all types: random, chain, clique, grid
python generate_tests.py --types chain grid  # specific types
```

Structure: `input/{exact,approx}/{random,chain,clique,grid}/`

### Run Tests

```bash
python run_tests.py                          # both modes, all types
python run_tests.py --mode exact --types random chain
python run_tests.py --mode approx --docker   # use containerized app
```

Results saved to `output/{exact,approx}/{type}/`.
