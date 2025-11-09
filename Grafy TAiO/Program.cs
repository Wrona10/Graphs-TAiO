namespace Grafy_TAiO
{
    internal class Program
    {
        static void Main(string[] args)
        {
            foreach (var list in Permutator.GetPermutations(5, 3))
            {
                Console.WriteLine(string.Join(", ", list));
            }
        }
    }
}
