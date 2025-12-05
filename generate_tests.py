from generate_graphs import (
    generate_testset,
    default_multi_edge_func,
    chain_edge_func,
    clique_edge_func,
    grid_edge_func,
)
import math

INPUT_DIR = "test_my_input"

# Test configurations: (n1, n2, k) tuples, always n1 >= n2
# Exact: n1 = 1..11, Approx: n1 = 10,20,...,100

def generate_configs(n1_values, n2_values, k_values):
    """Generate (n1, n2, k) configs where n2 = n1 - 1."""
    configs = []
    for n1 in n1_values:
        for n2 in n2_values:
            for k in k_values:
                if n1 >= n2:
                    configs.append((n1, n2, k))
    return configs

EXACT_N1 = [2, 3, 4, 5, 6, 7, 8, 9]  
EXACT_N2 = [2, 3, 4]  
EXACT_K = [1, 2, 3]
APPROX_N1 = [10, 20, 30, 50, 70, 100]  
APPROX_N2 = [5, 15, 25, 50, 75]
APPROX_K = [1, 2, 3, 5, 7, 10]

EXACT_CONFIGS = generate_configs(EXACT_N1, EXACT_N2, EXACT_K)
APPROX_CONFIGS = generate_configs(APPROX_N1, APPROX_N2, APPROX_K)

# Grid needs perfect squares
GRID_EXACT_N1 = [1, 4, 9]
GRID_APPROX_N1 = [16, 25, 36, 49, 64, 81, 100]

#GRID_EXACT_CONFIGS = generate_configs(GRID_EXACT_N1, k_values=[2])
#GRID_APPROX_CONFIGS = generate_configs(GRID_APPROX_N1, k_values=[2])


def generate_for_type(graph_type, edge_func_factory, configs, mode, count):
    """Generate tests for a specific graph type and mode (exact/approx)."""
    output_dir = f"{INPUT_DIR}/{mode}/{graph_type}/"
    for n1, n2, k in configs:
        edge_func = edge_func_factory(max(n1, n2))
        generate_testset(
            output_dir=output_dir,
            count=count,
            n1=n1,
            n2=n2,
            k=k,
            allow_loops=(graph_type == "random"),
            edge_func=edge_func,
        )


def generate_all(types, count):
    """Generate tests for all specified types in both exact and approx modes."""

    type_configs = {
        "random": (lambda n: default_multi_edge_func, EXACT_CONFIGS, APPROX_CONFIGS),
        "chain": (lambda n: chain_edge_func, EXACT_CONFIGS, APPROX_CONFIGS),
        "clique": (lambda n: clique_edge_func(n), EXACT_CONFIGS, APPROX_CONFIGS),
        #"grid": (lambda n: grid_edge_func(int(math.sqrt(n))), GRID_EXACT_CONFIGS, GRID_APPROX_CONFIGS),
    }

    for graph_type in types:
        if graph_type not in type_configs:
            continue

        edge_func_factory, exact_configs, approx_configs = type_configs[graph_type]

        print(f"\n=== Generating {graph_type.upper()} exact tests ===")
        generate_for_type(graph_type, edge_func_factory, exact_configs, "exact", count)

        print(f"\n=== Generating {graph_type.upper()} approx tests ===")
        generate_for_type(graph_type, edge_func_factory, approx_configs, "approx", count)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate tests")
    parser.add_argument(
        "--count", type=int, default=10, help="Number of testcases per config"
    )
    parser.add_argument(
        "--types",
        type=str,
        nargs="+",
        choices=["random", "chain", "clique", "all"],
        default=["all"],
        help="Graph types to generate",
    )

    args = parser.parse_args()

    types = args.types
    if "all" in types:
        types = ["random", "chain", "clique"]

    generate_all(types, args.count)
