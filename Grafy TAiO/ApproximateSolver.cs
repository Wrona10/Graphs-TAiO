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

            int[][] P = Permutator.GetCombinations(k, H.GetNumberOfVertices()).ToArray();

            for (int i = 0; i < k; i++)
            {
                for (int u = 0; u < H.GetNumberOfVertices(); u++)
                {
                    foreach (int v in H.GetOutgoingVertices(u))
                    {
                        int d = H.GetEdge(P[i][tH[u]], P[i][tH[v]]) - G.GetEdge(P[i][tG[u]], P[i][tG[v]]);
                        if (d > 0)
                        {
                            G.AddEdge(P[i][tG[u]], P[i][tG[v]], d);
                            operationsCount++;
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
