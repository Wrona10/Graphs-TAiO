using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Grafy_TAiO
{
    internal interface ISolver
    {
        public (Graph, int) Solve(Graph G, Graph H, int k);
    }
}
