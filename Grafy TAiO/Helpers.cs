using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.CompilerServices;

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
        public static IEnumerable<int[]> GetCombinations(int length, int setSize)
        {
            int[] result = new int[length];

            for (int i = 0; i < length; i++)
                result[i] = i;

            yield return result.ToArray();

            while (true)
            {
                if (result[length - 1] < setSize - 1)
                {
                    result[length - 1]++;
                    yield return result.ToArray();
                    continue;
                }

                int i = length - 2;

                while (i >= 0 && result[i] + 1 == result[i + 1])
                    i--;

                if (i < 0)
                    yield break;

                result[i]++;

                for (i++; i < length; i++)
                    result[i] = result[i - 1] + 1;

                yield return result.ToArray();
            }
        }

        public static IEnumerable<int[]> GetPermutations(int setSize)
        {
            throw new NotImplementedException();
        }

        public static IEnumerable<int[]> GetWords(int length, int alphabetSize)
        {
            int[] result = new int[length];

            yield return result.ToArray();

            while (true)
            {
                int i = 0;

                while (i < length && result[i] == alphabetSize - 1)
                    result[i++] = 0;

                if (i == length)
                    yield break;

                result[i]++;

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

        public void AddEdge(int from, int to, int amount)
        {
            adjacencyMatrix[from, to]+=amount;
            outgoingEdges[from]+=amount;
        }

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public int GetEdge(int from, int to) => this.adjacencyMatrix[from, to];

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public int GetOutgoingEdges(int from) => this.outgoingEdges[from];

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        public int GetNumberOfVertices() => this.numberOfVertices;

        public override string ToString()
        {
            if (numberOfVertices == 0)
                return "0\n";

            StringBuilder sb = new StringBuilder();

            sb.AppendLine(numberOfVertices.ToString());

            for(int i=0; i<numberOfVertices; i++)
            {
                StringBuilder line = new StringBuilder($"{adjacencyMatrix[i, 0]}");

                for(int j=1; j<numberOfVertices; j++)
                {
                    line.Append($" {adjacencyMatrix[i, j]}");
                }

                sb.AppendLine(line.ToString());
            }

            return sb.ToString();
        }
    }
}
