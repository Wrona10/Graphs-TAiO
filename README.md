Uwagi pana Homendy:
1. Poprawić dokumentację na kolejny etap z opisem algorytmu znajdowania permutacji (+ ew. inne nieścisłości).
2. Możliwość uruchomienia 4 programów (może być ta sama binarka, tylko z flagą): zwraca rozszerzenie lub odległość (dla każdej opcji dokładny lub aproksyamcyjny).
3. Testy średniego czasu wykonania (dla kazdej z ww. opcji) dla dokładnego n=1,2,...,10, dla aproksymacyjnego n=10,20,...,100

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
python run_tests.py --mode approx --docker
```

Results saved to `output/{exact,approx}/{type}/`.
