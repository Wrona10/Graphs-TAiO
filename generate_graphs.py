import random
from typing import Callable, Optional


def dense_edge_func(u: int, v: int, n: int) -> int:
    """Dense graph: 80% chance of 1-2 edges."""
    if random.random() < 0.8:
        return random.randint(1, 2)
    return 0


def chain_edge_func(u: int, v: int, n: int) -> int:
    """Chain: 0→1→2→3→... (like train cars)"""
    return 1 if v == u + 1 else 0


def clique_edge_func(clique_size: int):
    """Factory: first clique_size nodes fully connected, rest isolated."""

    def edge_func(u: int, v: int, n: int) -> int:
        if u < clique_size and v < clique_size and u != v:
            return 1
        return 0

    return edge_func


def grid_edge_func(width: int):
    """Factory: grid graph with given width. Nodes arranged in rows."""

    def edge_func(u: int, v: int, n: int) -> int:
        row_u, col_u = u // width, u % width
        row_v, col_v = v // width, v % width
        # connect to right neighbor
        if row_u == row_v and col_v == col_u + 1:
            return 1
        # connect to bottom neighbor
        if col_u == col_v and row_v == row_u + 1:
            return 1
        return 0

    return edge_func


def sparse_edge_func(u: int, v: int, n: int) -> int:
    """Sparse graph: 20% chance of 1 edge."""
    return 1 if random.random() < 0.2 else 0


def default_multi_edge_func(u: int, v: int, n: int) -> int:
    """Multigraph: random 0-3 edges."""
    return random.randint(0, 3)


def generate_graph(
    n: int,
    edge_func: Callable[[int, int, int], int] = default_multi_edge_func,
    allow_loops: bool = False,
) -> list[list[int]]:
    """Generate a directed multigraph as an adjacency matrix."""
    matrix = [[0] * n for _ in range(n)]

    for u in range(n):
        for v in range(n):
            if u == v and not allow_loops:
                continue

            edge_count = edge_func(u, v, n)
            matrix[u][v] = edge_count

    return matrix


def matrix_to_string(matrix: list[list[int]]) -> str:
    n = len(matrix)
    lines = [str(n)]
    for row in matrix:
        lines.append(" ".join(map(str, row)))
    return "\n".join(lines)


def generate_test_input(
    n1: int,
    n2: int,
    k: Optional[int] = None,
    edge_func1: Callable[[int, int, int], int] = default_multi_edge_func,
    edge_func2: Callable[[int, int, int], int] = default_multi_edge_func,
    allow_loops: bool = False,
) -> str:
    """
    Generate a complete test input file with two directed multigraphs and k parameter.
    If k is not provided its value is random.
    """
    graph1 = generate_graph(n1, edge_func1, allow_loops)
    graph2 = generate_graph(n2, edge_func2, allow_loops)

    if k is None:
        k = random.randint(1, max(n1, n2))

    result = matrix_to_string(graph1) + "\n" + matrix_to_string(graph2)
    result += f"\n{k}"

    return result


def save_test_input(
    filename: str,
    n1: int,
    n2: int,
    k: Optional[int] = None,
    edge_func1: Callable[[int, int, int], int] = default_multi_edge_func,
    edge_func2: Callable[[int, int, int], int] = default_multi_edge_func,
    allow_loops: bool = False,
) -> None:
    """Generate and save test input to a file."""
    content = generate_test_input(n1, n2, k, edge_func1, edge_func2, allow_loops)
    with open(filename, "w") as f:
        f.write(content)
    print(f"Generated test input saved to {filename}")


def generate_testset(
    output_dir: str,
    count: int,
    n1: int,
    n2: int,
    k: Optional[int],
    allow_loops: bool = False,
    edge_func: Callable[[int, int, int], int] = default_multi_edge_func,
    prefix: str = "test",
) -> list[str]:
    """Generate multiple test cases, each saved to a separate file."""
    import os

    os.makedirs(output_dir, exist_ok=True)

    files = []
    for i in range(1, count + 1):
        filename = os.path.join(
            output_dir, f"{prefix}_n1_{n1:06d}_n2_{n2:06d}_k_{k:03d}_{i:03d}.txt"
        )
        save_test_input(filename, n1, n2, k, edge_func, edge_func, allow_loops)
        files.append(filename)

    print(f"\nGenerated {count} test cases in {output_dir}/")
    return files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate test graphs")
    parser.add_argument(
        "--n1", type=int, default=4, help="Vertices number in the first graph"
    )
    parser.add_argument(
        "--n2", type=int, default=3, help="Vertices number in the second graph"
    )
    parser.add_argument(
        "--k", type=int, default=None, help="Parameter k (random if not specified)"
    )
    parser.add_argument(
        "--output-dir", "-d", type=str, default="input/", help="Output directory"
    )
    parser.add_argument(
        "--count", "-c", type=int, default=10, help="Number of test cases to generate"
    )
    parser.add_argument(
        "--prefix",
        "-p",
        type=str,
        default="test",
        help="Filename prefix for batch mode",
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["sparse", "default", "dense", "chain", "clique", "grid"],
        default="default",
        help="Graph type preset",
    )
    parser.add_argument(
        "--clique-size",
        type=int,
        default=None,
        help="Size of clique for --type=clique (defaults to n)",
    )
    parser.add_argument(
        "--grid-width",
        type=int,
        default=None,
        help="Width of grid for --type=grid (defaults to sqrt(n))",
    )
    parser.add_argument("--loops", action="store_true", help="Allow self-loops")
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    import math

    edge_funcs = {
        "sparse": sparse_edge_func,
        "default": default_multi_edge_func,
        "dense": dense_edge_func,
        "chain": chain_edge_func,
        "clique": clique_edge_func(args.clique_size or args.n1),
        "grid": grid_edge_func(args.grid_width or int(math.sqrt(args.n1))),
    }

    generate_testset(
        output_dir=args.output_dir,
        count=args.count,
        n1=args.n1,
        n2=args.n2,
        k=args.k,
        edge_func=edge_funcs[args.type],
        allow_loops=args.loops,
        prefix=args.prefix,
    )
