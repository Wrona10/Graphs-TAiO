using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.CompilerServices;
using System.Xml.Schema;

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

        public static long BinomialCoefficient(int n, int k)
        {
            if (k < 0 || k > n)
                return 0;

            k = Math.Max(k, n - k);

            double numerator = 1;
            double denominator = 1;

            for (int i = n; i > k; i--)
                numerator *= i;

            for (int i = n - k; i > 1; i--)
                denominator *= i;

            return (long)(Math.Clamp(numerator / denominator, 0, int.MaxValue));
        }

        // n! / k! * n-k ! -> n * n-1 * n-2 * .. * k+1 / n-k * n-k-1 * ... * 1
    }

    public static class Permutator
    {
        public static IEnumerable<int[]> GetCombinations(int subsetSize, int setSize)
        {
            int[] result = new int[subsetSize];

            for (int i = 0; i < subsetSize; i++)
                result[i] = i;

            yield return result.ToArray();

            while (true)
            {
                if (result[subsetSize - 1] < setSize - 1)
                {
                    result[subsetSize - 1]++;
                    yield return result.ToArray();
                    continue;
                }

                int i = subsetSize - 2;

                while (i >= 0 && result[i] + 1 == result[i + 1])
                    i--;

                if (i < 0)
                    yield break;

                result[i]++;

                for (i++; i < subsetSize; i++)
                    result[i] = result[i - 1] + 1;

                yield return result.ToArray();
            }
        }

        public static IEnumerable<int[]> GetPermutations(int setSize)
        {
            int[] A = new int[setSize];

            for (int i = 0; i < setSize; A[i] = i++) ;

            int[] c = new int[setSize];

            yield return A.ToArray();

            int p = 1;

            while (p < setSize)
            {
                if (c[p] < p)
                {
                    if (p % 2 == 0)
                        (A[0], A[p]) = (A[p], A[0]);
                    else
                        (A[c[p]], A[p]) = (A[p], A[c[p]]);

                    yield return A.ToArray();

                    c[p]++;

                    p = 1;
                }
                else
                {
                    c[p] = 0;
                    p++;
                }
            }
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

        public IEnumerable<int> GetOutgoingVertices(int u)
        {
            for (int v = 0; v < this.numberOfVertices; v++)
            {
                if (adjacencyMatrix[u, v] != 0)
                {
                    yield return v;
                }
            }
        }

        public void AddEdge(int from, int to, int amount)
        {
            adjacencyMatrix[from, to] += amount;
            outgoingEdges[from] += amount;
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

            int maxEdges = 0;

            for (int i = 0; i < numberOfVertices; i++)
            {
                for (int j = 0; j < numberOfVertices; j++)
                {
                    if (adjacencyMatrix[i, j] > maxEdges)
                        maxEdges = adjacencyMatrix[i, j];
                }
            }

            int maxLength = maxEdges.ToString().Length;

            for (int i = 0; i < numberOfVertices; i++)
            {
                StringBuilder line = new StringBuilder(adjacencyMatrix[i, 0].ToString().PadLeft(maxLength));

                for (int j = 1; j < numberOfVertices; j++)
                {
                    line.Append(" " + adjacencyMatrix[i, j].ToString().PadLeft(maxLength));
                }

                sb.AppendLine(line.ToString());
            }

            return sb.ToString();
        }

        public string GetAdditions(Graph compareBase)
        {
            if (numberOfVertices < compareBase.numberOfVertices)
                throw new ArgumentException("Can't show deletions!");

            if (numberOfVertices == 0)
                return "0\n";

            StringBuilder sb = new StringBuilder();

            if (numberOfVertices > compareBase.numberOfVertices)
            {
                sb.AppendLine($"{numberOfVertices} vertices ({compareBase.numberOfVertices} base + {numberOfVertices - compareBase.numberOfVertices} added)");
            }
            else
            {
                sb.AppendLine($"{numberOfVertices} vertices (none added)");
            }

            int maxEdges = 0;

            for (int i = 0; i < compareBase.numberOfVertices; i++)
            {
                for (int j = 0; j < compareBase.numberOfVertices; j++)
                {
                    if (adjacencyMatrix[i, j] - compareBase.adjacencyMatrix[i, j] > maxEdges)
                        maxEdges = adjacencyMatrix[i, j] - compareBase.adjacencyMatrix[i, j];
                }

                for (int j = compareBase.numberOfVertices; j < numberOfVertices; j++)
                {
                    if (adjacencyMatrix[i, j] > maxEdges)
                        maxEdges = adjacencyMatrix[i, j];
                }
            }

            for (int i = compareBase.numberOfVertices; i < numberOfVertices; i++)
            {
                for (int j = 0; j < numberOfVertices; j++)
                {
                    if (adjacencyMatrix[i, j] > maxEdges)
                        maxEdges = adjacencyMatrix[i, j];
                }
            }

            int maxLength = maxEdges.ToString().Length + 1;

            for (int i = 0; i < compareBase.numberOfVertices; i++)
            {
                StringBuilder line = new();

                int t;
                if ((t = adjacencyMatrix[i, 0] - compareBase.adjacencyMatrix[i, 0]) > 0)
                    line.Append(("+" + t.ToString()).PadLeft(maxLength));
                else
                    line.Append("0".PadLeft(maxLength));

                for (int j = 1; j < compareBase.numberOfVertices; j++)
                {
                    if ((t = adjacencyMatrix[i, j] - compareBase.adjacencyMatrix[i, j]) > 0)
                        line.Append(" " + ("+" + t.ToString()).PadLeft(maxLength));
                    else
                        line.Append(" " + "0".PadLeft(maxLength));
                }

                for (int j = compareBase.numberOfVertices; j < numberOfVertices; j++)
                {
                    if ((t = adjacencyMatrix[i, j]) > 0)
                        line.Append(" " + ("+" + t.ToString()).PadLeft(maxLength));
                    else
                        line.Append(" " + "0".PadLeft(maxLength));
                }

                sb.AppendLine(line.ToString());
            }

            for (int i = compareBase.numberOfVertices; i < numberOfVertices; i++)
            {
                StringBuilder line = new();

                int t;
                if ((t = adjacencyMatrix[i, 0]) > 0)
                    line.Append(("+" + t.ToString()).PadLeft(maxLength));
                else
                    line.Append("0".PadLeft(maxLength));

                for (int j = 1; j < numberOfVertices; j++)
                {
                    if ((t = adjacencyMatrix[i, j]) > 0)
                        line.Append(" " + ("+" + t.ToString()).PadLeft(maxLength));
                    else
                        line.Append(" " + "0".PadLeft(maxLength));
                }

                sb.AppendLine(line.ToString());
            }

            return sb.ToString();
        }

        public string ShowSubgraph(Graph subgraph, int[] verticeSelections)
        {
            if (numberOfVertices < subgraph.numberOfVertices)
                throw new ArgumentException("Not a subgraph!");

            if (numberOfVertices == 0 || subgraph.numberOfVertices == 0)
                return "H:\nG:\n0\n";

            StringBuilder sb = new StringBuilder();

            sb.Append("H:");
            for (int i = 0; i < subgraph.numberOfVertices; i++)
                sb.Append($" {i}");
            sb.AppendLine();

            sb.Append("G:");
            for (int i = 0; i < verticeSelections.Length; i++)
                sb.Append($" {verticeSelections[i]}");
            sb.AppendLine();

            sb.AppendLine(numberOfVertices.ToString());

            (int iG, int iH)[] selectedVertices = verticeSelections.Select((int g, int h) => (g, h)).OrderBy(x => x.g).ToArray();

            int[] maxLengthH = new int[subgraph.numberOfVertices];

            for (int j = 0; j < subgraph.numberOfVertices; j++)
            {
                int maxEdges = 0;
                for (int i = 0; i < subgraph.numberOfVertices; i++)
                {
                    if (subgraph.adjacencyMatrix[i, j] > maxEdges)
                        maxEdges = subgraph.adjacencyMatrix[i, j];
                }

                maxLengthH[j] = maxEdges.ToString().Length;
            }

            int[] maxLengthG = new int[subgraph.numberOfVertices];

            for (int j = 0; j < subgraph.numberOfVertices; j++)
            {
                int maxEdges = 0;
                for (int i = 0; i < subgraph.numberOfVertices; i++)
                {
                    if (adjacencyMatrix[selectedVertices[i].iG, selectedVertices[j].iG] > maxEdges)
                        maxEdges = adjacencyMatrix[selectedVertices[i].iG, selectedVertices[j].iG];
                }

                maxLengthG[j] = maxEdges.ToString().Length;
            }

            int ti = 0;
            for (int i = 0; i < numberOfVertices; i++)
            {
                if (ti >= selectedVertices.Length || selectedVertices[ti].iG != i)
                {
                    int tj = 0;
                    for (int j = 0; j < numberOfVertices; j++)
                    {
                        if (tj >= selectedVertices.Length || selectedVertices[tj].iG != j)
                            sb.Append("- ");
                        else
                        {
                            sb.Append("- ".PadLeft(maxLengthH[tj] + maxLengthG[tj] + 2));
                            tj++;
                        }
                    }
                }
                else
                {
                    (int uG, int uH) = selectedVertices[ti];
                    int tj = 0;
                    for (int j = 0; j < numberOfVertices; j++)
                    {
                        if (tj >= selectedVertices.Length || selectedVertices[tj].iG != j)
                            sb.Append("- ");
                        else
                        {
                            (int vG, int vH) = selectedVertices[tj];
                            sb.Append(subgraph.adjacencyMatrix[uH, vH].ToString().PadLeft(maxLengthH[tj])
                                + "/" + adjacencyMatrix[uG, vG].ToString().PadLeft(maxLengthG[tj]) + " ");
                            tj++;
                        }
                    }
                    ti++;
                }

                sb.AppendLine();
            }

            return sb.ToString();
        }
    }
}
