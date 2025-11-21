# Running with Docker

## Quick Start

### 1. Build the Docker image
```bash
docker-compose build
```

### 2. Show usage/help
The program will show usage when run without proper arguments:
```bash
docker-compose up
```

### 3. Run with an input file

First, place your input file in the `input/` directory (e.g., `input/graph.txt`).

Then edit `docker-compose.yml` and uncomment the command line:
```yaml
command: ["/app/input/graph.txt"]
```

Or run directly with docker:
```bash
docker run --rm -v "$(pwd)/input:/app/input" grafy-taio:latest /app/input/graph.txt
```

### 4. Run with input and output files

Edit `docker-compose.yml`:
```yaml
command: ["/app/input/graph.txt", "/app/output/result.txt"]
```

Then run:
```bash
docker-compose up
```

Results will be in `output/result.txt`.

### 5. Run in approximate mode

Edit `docker-compose.yml`:
```yaml
command: ["-a", "/app/input/graph.txt", "/app/output/result.txt"]
```

## Alternative: Direct Docker Commands

```bash
# Build
docker build -t grafy-taio .

# Run with input file (output to console)
docker run --rm -v "$(pwd)/input:/app/input" grafy-taio:latest /app/input/graph.txt

# Run with input and output files
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" grafy-taio:latest /app/input/graph.txt /app/output/result.txt

# Run in approximate mode
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" grafy-taio:latest -a /app/input/graph.txt /app/output/result.txt
```

## Input File Format

Your input file should contain:
1. First graph G
2. Second graph H
3. Optional parameter k

Each graph is specified as:
- First line: number of vertices
- Following lines: adjacency matrix (space-separated)