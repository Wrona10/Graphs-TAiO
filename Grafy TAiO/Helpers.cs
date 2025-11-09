using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace Grafy_TAiO
{
    public static class Helpers
    {
        public static int Factorial(int n)
        {
            if (n == 0 || n == 1)
                return 1;
            int result = 1;
            for (int i = 2; i <= n; i++)
            {
                result *= i;
            }
            return result;
        }

        public static int BinomialCoefficient(int n, int k)
        {
            if (k < 0 || k > n)
                return 0;

            k = Math.Max(k, n - k);

            int numerator = 1;
            int denominator = 1;

            for (int i = n; i > k; i--)
                numerator *= i;

            for (int i = n - k; i > 1; i--)
                denominator *= i;

            return numerator / denominator;
        }
    }

    public static class Permutator
    {
        public static IEnumerable<int[]> GetPermutations(int n, int m)
        {
            int[] result = new int[m];

            for (int i = 0; i < m; i++)
                result[i] = i;

            yield return result.ToArray();

            while (true)
            {
                if (result[m - 1] < n - 1)
                {
                    result[m - 1]++;
                    yield return result.ToArray();
                    continue;
                }

                int i = m - 2;

                while(i >= 0 && result[i] + 1 == result[i + 1])
                    i--;

                if (i < 0)
                    yield break;

                result[i]++;
                
                for (i++; i < m; i++)
                    result[i] = result [i - 1] + 1;

                yield return result.ToArray();
            }
        }
    }

    public class Graph
    {
        int[,] adjacencyMatrix;
        int[] outgoingEdges;
        int numberOfVertices;

        public Graph(int numberOfVertices)
        {
            this.numberOfVertices = numberOfVertices;
            adjacencyMatrix = new int[numberOfVertices, numberOfVertices];
            outgoingEdges = new int[numberOfVertices];
        }

        public Graph(Graph other)
        {
            this.numberOfVertices = other.numberOfVertices;
            adjacencyMatrix = new int[numberOfVertices, numberOfVertices];
            outgoingEdges = new int[numberOfVertices];
            Array.Copy(other.adjacencyMatrix, this.adjacencyMatrix, other.adjacencyMatrix.Length);
            Array.Copy(other.outgoingEdges, this.outgoingEdges, other.outgoingEdges.Length);
        }

        public Graph(Graph other, int numberOfVertices)
        {
            this.numberOfVertices = numberOfVertices;
            adjacencyMatrix = new int[numberOfVertices, numberOfVertices];
            outgoingEdges = new int[numberOfVertices];
            Array.Copy(other.outgoingEdges, this.outgoingEdges, Math.Min(other.outgoingEdges.Length, this.outgoingEdges.Length));

            for (int i = 0; i < Math.Min(other.numberOfVertices, this.numberOfVertices); i++)
            {
                for (int j = 0; j < Math.Min(other.numberOfVertices, this.numberOfVertices); j++)
                {
                    this.adjacencyMatrix[i, j] = other.adjacencyMatrix[i, j];
                }
            }
        }

        public void AddEdge(int from, int to)
        {
            adjacencyMatrix[from, to]++;
            outgoingEdges[from]++;
        }
    }
}
