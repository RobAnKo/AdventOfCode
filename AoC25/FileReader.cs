namespace FileReader
{
    
public class Reader
{
    public string[] StringsFromLines(string inputFile)
    {
        return File.ReadAllLines(inputFile);
    }

    public List<(Int128, Int128)> RangesFromCommaSeparated(string inputFile)
    {
        List<(Int128, Int128)> output = new();
        string[] boundaries = StringsFromCommaSeparated(inputFile);

        foreach (string bd in boundaries)
        {
            string[] bds = bd.Split('-');
            output.Add((Int128.Parse(bds[0]),Int128.Parse(bds[1])));
        }
        return output;    
    }

    public int[,] MatrixFromLines(string inputFile, char one = '@', char zero = '.')
        {
            string[] lines = StringsFromLines(inputFile);
            int height = lines.Length;
            int width = lines[0].Length;

            int[,] output = new int[width, height];

            for (int x = 0; x < width; x++)
            {
                for(int y = 0; y < height; y++)
                {
                    output[x,y] = lines[x][y] == one ? 1 : 0;
                }
            }
            return output;
        }




    public List<int> NumbersFromLines(string inputFile)
    {
        List<int> output = new();
        return output;
    }


    private string[] StringsFromCommaSeparated(string inputFile)
    {
        string line = File.ReadLines(inputFile).First();
        return line.Split(',');
    }
}
}