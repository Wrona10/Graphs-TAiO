from generate_graphs import (
    generate_testset,
)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate tests")
    parser.add_argument("--k", type=int, default=2, help="Numer of copies")
    parser.add_argument(
        "--count", type=int, default=10, help="Number of testcases per one graph size"
    )

    args = parser.parse_args()

    # tests for exact
    exact_dir = "input/exact/"
    exact_min_size = 1
    exact_max_size = 10
    exact_step = 1
    for exact_n in range(exact_min_size, exact_max_size + 1, exact_step):
        generate_testset(
            output_dir=exact_dir,
            count=args.count,
            n1=exact_n,
            n2=exact_n,
            k=args.k,
            allow_loops=True,
        )

    # tests for approximation
    approx_dir = "input/approx/"
    approx_min_size = 10
    approx_max_size = 100
    approx_step = 10
    for approx_n in range(approx_min_size, approx_max_size + 1, approx_step):
        generate_testset(
            output_dir=approx_dir,
            count=args.count,
            n1=approx_n,
            n2=approx_n,
            k=args.k,
            allow_loops=True,
        )
