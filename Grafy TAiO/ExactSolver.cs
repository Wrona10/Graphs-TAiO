using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Grafy_TAiO
{
    internal class ExactSolver : ISolver
    {
        public (Graph, int) Solve(Graph G, Graph H, int k)
        {
            int missingVertices = 0;
            while (Helpers.BinomialCoefficient(G.GetNumberOfVertices() + missingVertices, H.GetNumberOfVertices()) < k)
            {
                missingVertices++;
            }

            G = new Graph(G, G.GetNumberOfVertices() + missingVertices);

            int minimalEdgeAdditions = int.MaxValue;
            Graph minimalExtension = new Graph(0);

            int[][] subsets = Permutator.GetCombinations(H.GetNumberOfVertices(), G.GetNumberOfVertices()).ToArray();
            int[][] permutations = Permutator.GetPermutations(H.GetNumberOfVertices()).ToArray();

            foreach (var selection in Permutator.GetCombinations(k, subsets.Length))
            {
                foreach (int[] permutationSelection in Permutator.GetWords(k, permutations.Length))
                {
                    Graph copy = new Graph(G);
                    int currentEdgeAdditions = 0;

                    for (int i = 0; i < k; i++)
                    {
                        for (int u = 0; u < H.GetNumberOfVertices(); u++)
                        {
                            int gu = subsets[selection[i]][permutations[permutationSelection[i]][u]];
                            for (int v = 0; v < H.GetNumberOfVertices(); v++)
                            {
                                int gv = subsets[selection[i]][permutations[permutationSelection[i]][v]];

                                int d = H.GetEdge(u, v) - copy.GetEdge(gu, gv);

                                if (d > 0)
                                {
                                    copy.AddEdge(gu, gv, d);
                                    currentEdgeAdditions += d;

                                    if (currentEdgeAdditions >= minimalEdgeAdditions)
                                        goto skip;
                                }
                            }
                        }
                    }

                    if (currentEdgeAdditions < minimalEdgeAdditions)
                    {
                        minimalEdgeAdditions = currentEdgeAdditions;
                        minimalExtension = copy;
                    }

                skip:;
                }
            }

            return (minimalExtension, missingVertices + minimalEdgeAdditions);
        }
    }
}
