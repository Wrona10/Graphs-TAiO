namespace Grafy_TAiO
{
    internal class Program
    {
        static void Main(string[] args)
        {
#if RELEASE
            if(args.Length < 1 || args.Length > 3)
            {
                Usage();
                return;
            }

            bool approximate = false;
            string source;
            string? destination = null;

            if(args[0] == "-a")
                approximate = true;
            
            source = args[approximate ? 1 : 0];

            if(args.Length == (approximate ? 3 : 2))
                destination = args[approximate ? 2 : 1];

            if(args.Length == 3 && !approximate || !Path.Exists(source) || (destination == null || !Path.Exists(destination)))
            {
                Usage();
                return;
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

            ISolver solver = approximate ? new ApproximateSolver() : new ExactSolver();

            (Graph result, int edits) = solver.Solve(G, H, k);

            if(destination != null)
            {
                using(StreamWriter sw =  new StreamWriter(destination))
                {
                    sw.Write(result.ToString());
                    sw.WriteLine($"{edits}");
                }
            }
            else
            {
                Console.WriteLine($"Solutions found with {edits} editions:");
                Console.Write(result.ToString());
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

                if(line != null)
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
