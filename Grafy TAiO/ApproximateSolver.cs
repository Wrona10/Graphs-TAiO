using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Grafy_TAiO
{
    internal class ApproximateSolver : ISolver
    {
        public (Graph, int) Solve(Graph G, Graph H, int k)
        {
            int missingVertices = 0;
            while (Helpers.BinomialCoefficient(G.GetNumberOfVertices() + missingVertices, H.GetNumberOfVertices()) < k)
            {
                missingVertices++;
            }

            G = new Graph(G, G.GetNumberOfVertices() + missingVertices);

            int operationsCount = missingVertices;

            int[] tG = GetSortedIndices(G);
            int[] tH = GetSortedIndices(H);

            int i = 0;

            foreach (var P in Permutator.GetCombinations(H.GetNumberOfVertices(), G.GetNumberOfVertices()))
            {
                if (i++ >= k)
                    break;

                for (int u = 0; u < H.GetNumberOfVertices(); u++)
                {
                    for (int v = 0; v < H.GetNumberOfVertices(); v++)
                    {
                        int d = H.GetEdge(tH[u], tH[v]) - G.GetEdge(tG[P[u]], tG[P[v]]);
                        if (d > 0)
                        {
                            G.AddEdge(tG[P[u]], tG[P[v]], d);
                            operationsCount += d;
                        }
                    }
                }
            }

            return (G, operationsCount);
        }

        private int[] GetSortedIndices(Graph G)
        {
            int[] tG = new int[G.GetNumberOfVertices()];
            for (int i = 0; i < G.GetNumberOfVertices(); i++)
            {
                tG[i] = i;
            }

            int[] tGSorted = tG.OrderByDescending(ind => G.GetOutgoingEdges(ind)).ToArray();
            return tGSorted;
        }
    }
}
