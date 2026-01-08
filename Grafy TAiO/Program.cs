namespace Grafy_TAiO
{
    internal class Program
    {
        static void Main(string[] args)
        {
#if RELEASE
            if (args.Length < 1 || args.Length > 3)
            {
                Usage();
                return;
            }

            int currentIndex = 0;
            bool approximate = false;

            if (args[currentIndex] == "-a")
            {
                approximate = true;
                currentIndex++;
            }

            if (currentIndex >= args.Length)
            {
                Usage();
                return;
            }

            string source = args[currentIndex];
            currentIndex++;

            if (!File.Exists(source))
            {
                Console.WriteLine($"Error: Source file '{source}' does not exist.");
                Usage();
                return;
            }

            string? destination = null;
            if (currentIndex < args.Length)
            {
                destination = args[currentIndex];
                currentIndex++;
            }

            if (currentIndex < args.Length)
            {
                Usage();
                return;
            }

            if (destination != null)
            {
                string? destDir = Path.GetDirectoryName(destination);
                if (!string.IsNullOrEmpty(destDir) && !Directory.Exists(destDir))
                {
                    Console.WriteLine($"Error: Destination directory '{destDir}' does not exist.");
                    return;
                }
            }
#endif
#if DEBUG
            bool approximate = false;
            string source = @"C:\MY\PATH\TO\SRC";
            string? destination = null;
#endif

            Graph G, H;
            int k;

            try
            {
                (G, H, k) = ReadFile(source);
            }
            catch (Exception e)
            {
                Console.WriteLine("Failure while reading source file!");
                Usage();
                return;
            }

            if (H.GetNumberOfVertices() == 0)
            {
                Console.WriteLine("Please provide a non-empty graph H!");
                Usage();
                return;
            }

            ISolver solver = approximate ? new ApproximateSolver() : new ExactSolver();

            (Graph result, int edits, int[][] verticeSelections) = solver.Solve(G, H, k);

            if (destination != null)
            {
                using (StreamWriter sw = new StreamWriter(destination))
                {
                    sw.WriteLine("Graphs are displayed as adjacency matrixes preceded by a number of vertices.");
                    sw.WriteLine("'m[i][j] = x' means there are 'x' edges between vertex 'i' and vertex 'j'");
                    sw.WriteLine();
                    sw.WriteLine("Given the graph G:");
                    sw.WriteLine(G.ToString());
                    sw.WriteLine("Given the graph H to find in the extended G:");
                    sw.WriteLine(H.ToString());
                    sw.WriteLine();
                    sw.WriteLine($"And given the number of copies to find k is {k}");
                    sw.WriteLine();
                    sw.WriteLine($"Solution (the extended G) found with {edits} editions:");
                    sw.Write(result.ToString());
                    sw.WriteLine();
                    sw.WriteLine("The difference between the base graph G and the solution is:");
                    sw.Write(result.GetAdditions(G));
                    sw.WriteLine();
                    sw.WriteLine("Copies of H found in the extended G are as follows:");
                    for (int i = 0; i < k; i++)
                    {
                        sw.WriteLine();
                        sw.Write(result.ShowSubgraph(H, verticeSelections[i]));
                    }
                }
            }
            else
            {
                Console.WriteLine("Graphs are displayed as adjacency matrixes.");
                Console.WriteLine("'m[i][j] = x' means there are 'x' edges between vertex 'i' and vertex 'j'");
                Console.WriteLine();
                
                Console.WriteLine("Given the graph G:");
                Console.WriteLine(G.ToString());

                Console.WriteLine("Given the graph H to find in the extended G:");
                Console.WriteLine(H.ToString());

                Console.WriteLine($"And given the number of copies to find k is {k}");
                Console.WriteLine();

                Console.WriteLine($"Solution (the extended G) found with {edits} editions:");
                Console.Write(result.ToString());
                Console.WriteLine();

                Console.WriteLine("The difference between the base graph G and the solution is:");
                Console.Write(result.GetAdditions(G));
                Console.WriteLine();

                Console.WriteLine("Copies of H found in the extended G are as follows:");
                for (int i = 0; i < k; i++)
                {
                    Console.WriteLine();
                    Console.WriteLine($"Nr {i + 1}:");
                    Console.Write(result.ShowSubgraph(H, verticeSelections[i]));
                }
            }
        }

        static void Usage()
        {
            Console.WriteLine("Usage:\n" +
                "program [-a] src [dst]\n" +
                "\n" +
                "-a - calculate approximation\n" +
                "src - source file path containing both graph descriptions and optional number k\n" +
                "dst - optional destination file path to write minimal extension and number of additions\n");
        }


        static (Graph G, Graph H, int k) ReadFile(string path)
        {
            Graph G = new(0), H = new(0);
            int k = 1;

            if (!File.Exists(path))
                throw new FileNotFoundException();

            using (StreamReader sr = new StreamReader(path))
            {
                G = ReadGraph(sr);

                H = ReadGraph(sr);

                string? line = sr.ReadLine();

                if (line != null)
                {
                    if (line.Trim().Split().Length > 1)
                        throw new ArgumentException();

                    k = int.Parse(line.Trim());
                }
            }

            return (G, H, k);

            static Graph ReadGraph(StreamReader sr)
            {
                string? line = sr.ReadLine();

                Graph G = new Graph(int.Parse(line));

                for (int i = 0; i < G.GetNumberOfVertices(); i++)
                {
                    line = sr.ReadLine();

                    if (line.Trim().Split().Length != G.GetNumberOfVertices())
                        throw new ArgumentException();

                    var nums = line.Trim().Split();

                    for (int j = 0; j < G.GetNumberOfVertices(); j++)
                    {
                        G.AddEdge(i, j, int.Parse(nums[j]));
                    }
                }

                return G;
            }
        }
    }
}
