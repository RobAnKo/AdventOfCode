using System.Xml;

namespace AoC
{

    class Utils 
    {
        public Utils()
        {
            
        }
 
        public int[] IntegerDivisors(int n)
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

        public char GetLargestDigitInNumberString(string numberString, out int foundIdx)
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
            int yEnd = yPos == width ? width : yPos + 1; 
        
            int xStart = xPos == 0 ? 0 : xPos - 1;
            int xEnd = xPos == height ? height : xPos + 1;

            for (int i = xStart; i <= xEnd; i++)
            {
                for (int j = yStart; i <= yEnd; j++)
                {
                    if (floor[i])
                }
            } 


        }
    }
    
}