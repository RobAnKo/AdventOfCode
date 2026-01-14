using System.Collections;

namespace FileReader;


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
                output[x,y] = lines[y][x] == one ? 1 : 0;
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

    internal ((Int128, Int128)[], Int128[]) ArrayListFromSplitLines(string inputFilePath)
    {
        ((Int128, Int128)[], Int128[]) output = new();
        
        string[] lines = StringsFromLines(inputFilePath);

        int aLIdx = 0;
        List<(Int128, Int128)> ranges = new();
        List<Int128> IDs = new ();

        bool rangeFlag = true;

        foreach (string line in lines)
        {
            if (line == "") 
            {
                rangeFlag = false;
                continue;
            }
            
            if (rangeFlag)
            {
                string[] lineParts = line.Split('-');
                ranges.Add((Int128.Parse(lineParts[0]),Int128.Parse(lineParts[1])));
            }
            else
            {
                IDs.Add(Int128.Parse(line));
            }
        }
        output.Item1 = ranges.OrderBy(x => x.Item1).ToArray();
        output.Item2 = IDs.ToArray();

        return output;

    }


    public string[,] ArrayFromSpaceSeparated(string inputFilePath)
    {
        string[] lines = StringsFromLines(inputFilePath);
        int height = lines.Length;
        int width = lines[0].Split(" ", StringSplitOptions.RemoveEmptyEntries).Length;

        string[,] output = new string[height, width];

        int yIdx = 0;

        foreach (string line in lines)
        {
            string[] splitLine = line.Split(" ", StringSplitOptions.RemoveEmptyEntries);
            int xIdx = 0;

            foreach (string entry in splitLine)
            {
                output[yIdx, xIdx] = entry;
                xIdx++;
            }
            yIdx++;

        }

        return output;
    }

    internal char[,] CharMatrixFromLines(string inputFilePath)
    {
        string[] lines = StringsFromLines(inputFilePath);
        int height = lines.Length;
        int width = lines[0].Length;

        char[,] output = new char[height, width];

        int yIdx = 0;

        foreach (string line in lines)
        {
            int xIdx = 0;

            foreach (char symbol in line)
            {
                output[yIdx, xIdx] = symbol;
                xIdx++;
            }
            yIdx++;

        }
        return output;
    }

    internal int[][] CoordinatesFromLines(string inputFilePath)
    {
        List<int[]> coordinates = new();
        string[] lines = StringsFromLines(inputFilePath);
        foreach (string line in lines)
        {
            string[] parts = line.Split(',', StringSplitOptions.RemoveEmptyEntries);
            int x = int.Parse(parts[0]);
            int y = int.Parse(parts[1]);
            int z = int.Parse(parts[2]);
            coordinates.Add([x,y,z]);
        }
        return coordinates.ToArray();
    }


}