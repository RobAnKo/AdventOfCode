namespace AoC25;


class Utils 
{
    internal Utils()
    {
        
    }

    internal int[] IntegerDivisors(int n)
    {
        List<int> output = new();
        for (int i = 1; i <= n/2; i++)
        {
            if (n%i == 0)
            {
                output.Add(i);
            }
            
        }
        return output.ToArray();
    }

    internal char GetLargestDigitInNumberString(string numberString, out int foundIdx)
    {
        foundIdx = 0;
        char candidate = numberString[foundIdx];
        
        int len = numberString.Length;

        for (int i = 1; i < len; i++)
        {
            char newCandidate = numberString[i];
            if (newCandidate - '0' > candidate - '0')
            {
                candidate = newCandidate;
                foundIdx = i;
            }
        }

        return candidate;
    }

    internal int CountOnesAroundPosition(int[,] floor, int xPos, int yPos)
    {
        int output = 0;

        int width = floor.GetLength(0);
        int height = floor.GetLength(1);

        int yStart = yPos == 0 ? 0 : yPos - 1;
        int yEnd = yPos == width - 1 ? width - 1 : yPos + 1; 
    
        int xStart = xPos == 0 ? 0 : xPos - 1;
        int xEnd = xPos == height - 1 ? height - 1 : xPos + 1;

        for (int i = xStart; i <= xEnd; i++)
        {
            for (int j = yStart; j <= yEnd; j++)
            {
                if (!(i == xPos & j == yPos) & floor[i,j] == 1)
                {
                    output++;
                }
            }
        } 
        return output;
    }

    internal int[,] MatrixSubtract(int[,] A, int[,] B)
    {
        int width, height;
        width = A.GetLength(0);
        height = A.GetLength(1);
        for (int i = 0; i < width; i++)
        {
            for (int j = 0; j < height; j++)
            {
                A[i,j] -= B[i,j];
            }
        }
        return A;
        
    }

    internal void PrintMatrix(int[,] A)
    {

        Dictionary<int, char> map = new() {{0,'.'}, {1, '@'}};
        int width, height;
        width = A.GetLength(0);
        height = A.GetLength(1);
        for (int i = 0; i < width; i++)
        {
            for (int j = 0; j < height; j++)
            {
                System.Console.Write(map[A[i,j]]);
            }
            System.Console.WriteLine();
        }
        System.Console.WriteLine();
        System.Console.WriteLine();
        System.Console.WriteLine();
    }

    internal Int128 InclusiveRangeLength((Int128, Int128) referenceRange)
    {
        return referenceRange.Item2 - referenceRange.Item1 + 1;
    }

    internal Int128 Calculate(char symbol, List<Int128> operands)
    {
        Int128 output = symbol == '+' ? 0: 1;

        foreach (Int128 o in operands)
        {
            if (symbol == '+')
            {
                output += o;
            }
            else
            {
                output *= o;
            }
        }
        return output;
    }

    internal double EuclidianDistance(int[] a, int[] b)
    {
        double quadSum = 0;
        for (int i = 0; i < a.Length; i++)
        {
            quadSum += Math.Pow(Math.Abs(a[i] - b[i]), 2);
        }
        return Math.Sqrt(quadSum);
    }

    public Int128 AreasFromCornerCoordinates(int[] coordinates1, int[] coordinates2)
    {
        Int128 product = 1;
        for (int i = 0; i < coordinates1.Length; i++)
        {
            product *= Math.Abs(coordinates1[i] - coordinates2[i]) + 1;
        }
        return product;
    }

}
