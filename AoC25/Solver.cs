using FileReader;

namespace AoC25;

public class Solver
{
    private readonly bool _real;
    private readonly string _dayNumber;
    private readonly string _part;
    private readonly string _basePath = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", ".."));
    private string _inputFilePath = "";

    readonly Reader _fileReader;
    readonly Utils _utils;

    public Solver(bool real, string dayNumber, string part)
    {
        _real = real;
        _dayNumber = dayNumber;
        _part = part;
        _fileReader = new Reader();
        _utils = new Utils();
    }

    public Int128 Solve()
    {

        string inputFileName = _real ? "input" + _dayNumber + ".txt" : "input" + _dayNumber + "_test.txt";
        _inputFilePath = Path.Combine([_basePath, inputFileName]);
        switch (int.Parse(_dayNumber))
        {
            case 1:
                {
                    if (_part == "1")
                        return Solve1_1();
                    else
                        return Solve1_2();
                }
            case 2:
                {
                    if (_part == "1")
                        return Solve2_1();
                    else
                        return Solve2_2();
                }
            case 3:
                {
                    if (_part == "1")
                        return Solve3_1(2);
                    else
                        return Solve3_1(12);
                }
            case 4:
                {
                    if (_part == "1")
                        return Solve4_1();
                    else
                        return Solve4_2();
                }
            case 5:
                {
                    if (_part == "1")
                        return Solve5_1();
                    else
                        return Solve5_2();
                }
            case 6:
                {
                    if (_part == "1")
                        return Solve6_1();
                    else
                        return Solve6_2();
                }
            case 7:
                {
                    if (_part == "1")
                        return Solve7_1();
                    else
                        return Solve7_2();
                }
            case 8:
            {
                if (_part == "1")
                    return Solve8_1();
                else
                    return Solve8_2();
            }
            case 9:
            {
                if (_part == "1")
                    return Solve9_1();
                else
                    return Solve9_2();
            }
            default:
                return 0;
        }

    }

    private int Solve1_1()
    {
        int output = 0;
        int position = 50;
        string[] moves = _fileReader.StringsFromLines(_inputFilePath);

        foreach (string move in moves)
        {
            int clicks;
            if (move.StartsWith("R"))
                clicks = Int32.Parse(move.Substring(1));
            else
                clicks = -Int32.Parse(move.Substring(1));

            position += clicks;
            position = position % 100;
            if (position == 0)
                output += 1;
        }
        return output;
    }

    private int Solve1_2()
    {
        int output = 0;
        int position = 50;
        string[] moves = _fileReader.StringsFromLines(_inputFilePath);

        foreach (string move in moves)
        {
            int clicks = Int32.Parse(move.Substring(1));
            int distance = move.StartsWith("R") ? 100 - position : position;
            
            if (distance == 0)
                distance = position = 100;

            while (clicks >= distance)
            {
                output++;
                clicks -= distance;
                distance = 100;
                position = 100;
            }

            position = move.StartsWith("R")
            ? (position + clicks) % 100
            : (position - clicks) % 100;
        }

        return output;
    }

    private Int128 Solve2_1()
    {
        Int128 output = 0;
        List<(Int128, Int128)> boundaries = _fileReader.RangesFromCommaSeparated(_inputFilePath);

        foreach ((Int128, Int128) boundary in boundaries)
        {
            Int128 start = boundary.Item1;
            Int128 end = boundary.Item2;

            while (start <= end)
            {
                string number = start.ToString();
                int len = number.Length;

                if (len % 2 == 0)
                {
                    string firstHalf = number.Substring(0, len / 2);
                    string secondHalf = number.Substring(len / 2);
                    if (firstHalf == secondHalf)
                        output += start;
                }
                start++;
            }
        }
        return output;
    }

    private Int128 Solve2_2()
    {
        Int128 output = 0;
        List<(Int128, Int128)> boundaries = _fileReader.RangesFromCommaSeparated(_inputFilePath);

        foreach ((Int128, Int128) boundary in boundaries)
        {
            Int128 startNumber = boundary.Item1;
            Int128 endNumber = boundary.Item2;

            while (startNumber <= endNumber)
            {
                string number = startNumber.ToString();
                int numberLength = number.Length;

                int[] plausibleLengths = _utils.IntegerDivisors(numberLength);


                //iterate over plausible sequence lengths
                foreach (int leadLength in plausibleLengths)
                {
                    string leadSequence = number.Substring(0, leadLength);
                    bool hit = true;

                    //iterate over chunks of length
                    for (int startIndex = leadLength; startIndex + leadLength <= numberLength; startIndex += leadLength)
                    {
                        string compareSequence = number.Substring(startIndex, leadLength);
                        if (leadSequence != compareSequence)
                        {
                            hit = false;
                            break;
                        }
                    }

                    //only invalid if all chunks are repetitions of the lead sequence
                    if (hit)
                    {
                        output += startNumber;
                        break;
                    }
                }

                startNumber++;
            }
        }
        return output;
    }

    private Int128 Solve3_1(int numberOfBatteries)
    {
        Int128 output = 0;
        string[] banks = _fileReader.StringsFromLines(_inputFilePath);

        foreach (string bank in banks)
        {
            string bankOutput = "";

            int bankSize = bank.Length;

            int searchStartIdx = 0;
            int subStringMaxIdx = 0;

            for (int outputIdx = 0; outputIdx < numberOfBatteries; outputIdx++)
            {

                if (outputIdx != 0)
                {
                    searchStartIdx = searchStartIdx + subStringMaxIdx + 1;
                }


                int searchLength = bankSize - searchStartIdx - (numberOfBatteries - outputIdx - 1);

                string subStringToSearch = bank.Substring(searchStartIdx, searchLength);

                bankOutput += _utils.GetLargestDigitInNumberString(subStringToSearch, out subStringMaxIdx);
            }

            output += Int128.Parse(bankOutput);

        }
        return output;
    }

    private int Solve4_1()
    {
        int output = 0;
        int[,] floor = _fileReader.MatrixFromLines(_inputFilePath);

        for (int xPos = 0; xPos < floor.GetLength(0); xPos++)
        {
            for (int yPos = 0; yPos < floor.GetLength(1); yPos++)
            {
                if (floor[xPos, yPos] == 1 && _utils.CountOnesAroundPosition(floor, xPos, yPos) < 4)
                {
                    output++;
                }
            }
        }
        return output;
    }

    private int Solve4_2()
    {
        int output = 0;
        int[,] floor = _fileReader.MatrixFromLines(_inputFilePath);

        _utils.PrintMatrix(floor);          

        bool changed = true;

        while (changed)
        {
            int[,] floorChanges = new int[floor.GetLength(0), floor.GetLength(1)];

            changed = false;

            for (int xPos = 0; xPos < floor.GetLength(0); xPos++)
            {
                for (int yPos = 0; yPos < floor.GetLength(1); yPos++)
                {
                    if (floor[xPos, yPos] == 1 && _utils.CountOnesAroundPosition(floor, xPos, yPos) < 4)
                    {
                        output++;
                        floorChanges[xPos, yPos] = 1;
                        changed = true;
                    }
                }
            }
            floor =_utils.MatrixSubtract(floor, floorChanges);
            _utils.PrintMatrix(floor);
        }

        

        return output;
    }

    private int Solve5_1()
    {
        int output = 0;
        
        ((Int128, Int128)[], Int128[]) rangesAndIDs = _fileReader.ArrayListFromSplitLines(_inputFilePath);

        (Int128, Int128)[] ranges = rangesAndIDs.Item1;
        Int128[] ids = rangesAndIDs.Item2;


        foreach (Int128 id in ids)
        {
            foreach((Int128, Int128) range in ranges)
            {
                if (id >= range.Item1 && id <= range.Item2) 
                {
                    output++;
                    break;
                }
            }
        }
        return output;
    }

    private Int128 Solve5_2()
    {
        Int128 output = 0;
        
        ((Int128, Int128)[], Int128[]) rangesAndIDs = _fileReader.ArrayListFromSplitLines(_inputFilePath);

        (Int128, Int128)[] ranges = rangesAndIDs.Item1;

        (Int128, Int128) referenceRange = ranges[0];

        foreach ((Int128, Int128) compareRange in ranges.Skip(1))
        {
            //Containment
            if (!(compareRange.Item2 > referenceRange.Item2))
            {
                continue;
            }
            //Extension -> update upper boundary of reference range

            if (!(compareRange.Item1 > referenceRange.Item2 + 1))
            {
                referenceRange.Item2 = compareRange.Item2;
            }
            //Exclusive -> change reference to new range and add former reference to output
            else
            {
                output += _utils.InclusiveRangeLength(referenceRange);
                referenceRange = compareRange;
            }
        }

        output += _utils.InclusiveRangeLength(referenceRange);

        return output;
    }

    private Int128 Solve6_1()
    {
        Int128 output = 0;
        string[,] sheet = _fileReader.ArrayFromSpaceSeparated(_inputFilePath);

        for (int xPos = 0; xPos < sheet.GetLength(1); xPos++)
        {
            Int128 intermediateOutput = 0;
            string operation = "";
            for (int yPos = sheet.GetLength(0) - 1; yPos >= 0; yPos--)
            {
                if (yPos == sheet.GetLength(0) - 1)
                {
                    operation = sheet[yPos, xPos];
                    intermediateOutput = (operation == "+") ? 0 : 1;
                }
                else if (operation == "+") intermediateOutput += Int128.Parse(sheet[yPos, xPos]);
                else if (operation == "*") intermediateOutput *= Int128.Parse(sheet[yPos, xPos]);
                    
            }
            output += intermediateOutput;
        }    
        return output;
    }

    private Int128 Solve6_2()
    {
        Int128 output = 0;
        char[,] sheet = _fileReader.CharMatrixFromLines(_inputFilePath);

        List<Int128> operands = new();
        //go from upper right downwards until end up lower left
        for (int xPos = sheet.GetLength(1) - 1; xPos >= 0 ; xPos--)
        {   
            string intermediateString = "";
            bool calculate = false;
            char symbol = ' ';
            //down
            for (int yPos = 0; yPos < sheet.GetLength(0); yPos++)
            {
                symbol = sheet[yPos,xPos];
                switch (symbol)
                {
                    case ' ':
                        continue;
                    case '+':
                    case '*':
                        calculate = true;
                        break;
                    default:
                        intermediateString += symbol;
                        break;
                }
            }
            if (intermediateString == "")
            {
                continue;
            }
            else
            {
                operands.Add(Int128.Parse(intermediateString));
            }
            
            if (calculate)
            {
                output += _utils.Calculate(symbol, operands);
                operands = new();
            }
        }
        return output;
    }

    private int Solve7_1()
    {
        int output = 0;
        int sourceIdx = _fileReader.StringsFromLines(_inputFilePath)[0].IndexOf('S');
        int[,] splitterMap = _fileReader.MatrixFromLines(_inputFilePath, '^');

        HashSet<int> currentBeams = [sourceIdx];

        for (int level = 0; level < splitterMap.GetLength(1); level++)
        {
            HashSet<int> newBeams = [];
            foreach (int xIdx in currentBeams)
            {
                if (splitterMap[xIdx, level] == 1)
                {
                    output++;
                    newBeams.UnionWith([xIdx-1, xIdx+1]);
                }
                else newBeams.Add(xIdx);
            }
            currentBeams = newBeams;
        }
        return output;
    }


    private Int128 Solve7_2()
    {
        int sourceIdx = _fileReader.StringsFromLines(_inputFilePath)[0].IndexOf('S');
        int[,] splitterMap = _fileReader.MatrixFromLines(_inputFilePath, '^');
        int height = splitterMap.GetLength(1);
        int width = splitterMap.GetLength(0);

        Int128[] currentBeams = new Int128[width];
        currentBeams[sourceIdx] = 1;
        Console.WriteLine(string.Join(" ", currentBeams));
        for (int level = 0; level < height; level++)
        {
            
            Int128[] newBeams = new Int128[width];
            for (int xIdx = 0; xIdx < width; xIdx++)
            {
                if (currentBeams[xIdx] == 0) continue;
                //splitter found
                if (splitterMap[xIdx, level] != 0)
                {
                    Int128 bundle = currentBeams[xIdx];
                    newBeams[xIdx - 1] += bundle;
                    newBeams[xIdx + 1] += bundle;
                }
                else
                {
                    newBeams[xIdx] += currentBeams[xIdx];
                }
            }
            currentBeams = newBeams;
            Console.WriteLine(string.Join(" ", currentBeams));
        }

        Int128 output = 0;
        foreach (Int128 i in currentBeams)
        {
            output+=i;
        }

        return output;
    }

    private int Solve8_1()
    {

        int nConnections = _real ? 1000 : 10;
        
        int[][] coordinates = _fileReader.CoordinatesFromLines(_inputFilePath);


        //distances
        Dictionary<(int,int), double> distances = new();
        
        for (int i = 0; i < coordinates.Length-1; i++)
        {
            var coordinates1 = coordinates[i];
            for (int j = i+1; j < coordinates.Length; j++)
            {
                var coordinates2 = coordinates[j];
                distances[(i, j)] = _utils.EuclidianDistance(coordinates1, coordinates2);
            }
        }
        
        //sort by distance
        var sortedPairs = distances.OrderBy(item => item.Value)
            .Select(item => item.Key);



        //clustering by distance
        
        Dictionary<int, HashSet<int>> clusterMemberDict = new();
        Dictionary<int, int> nodeClusterDict = new();

        int currentCluster = 0;

        foreach (var keyPair in sortedPairs.Take(nConnections))
        {
            int one = keyPair.Item1;
            int two = keyPair.Item2;

            int oneCluster = nodeClusterDict.GetValueOrDefault(one, -1);
            int twoCluster = nodeClusterDict.GetValueOrDefault(two, -1);

            bool sameState = oneCluster == twoCluster;
            bool clusteredYet = oneCluster > -1 && twoCluster > -1;

            //same cluster or no cluster yet
            if (sameState)
            {
                //new cluster with both nodes
                if (!clusteredYet)
                {
                    clusterMemberDict[currentCluster] = new HashSet<int>([one, two]);
                    nodeClusterDict[one] = currentCluster;
                    nodeClusterDict[two] = currentCluster;
                    currentCluster++;
                }
                //already in same cluster, do nothing
                continue;
            }

            //different clusters
            
            //both clustered, need to merge
            if (clusteredYet)
            {
                int targetCluster = nodeClusterDict[one];
                int sourceCluster = nodeClusterDict[two];
                foreach (int member in clusterMemberDict[sourceCluster])
                {
                    nodeClusterDict[member] = targetCluster;
                }
                clusterMemberDict[targetCluster].UnionWith(clusterMemberDict[sourceCluster]);
                clusterMemberDict.Remove(sourceCluster);

            }
            //only one clustered, add the other to that cluster
            else
            {
                if (oneCluster > -1)
                {
                    clusterMemberDict[oneCluster].Add(two);
                    nodeClusterDict[two] = oneCluster;
                }
                else
                {
                    clusterMemberDict[twoCluster].Add(one);
                    nodeClusterDict[one] = twoCluster;
                }
            }
        }

        //sort by size

        //var sortedClusters = clusterMemberDict.OrderByDescending(cluster => cluster.Value.Count);
        var sortedCounts = clusterMemberDict.Values.OrderByDescending(cluster => cluster.Count).Select(value => value.Count).ToArray();
        
        //calculate result

        int output = 1;
        int idx = 0;
        while (idx < 3)
        {
            output *= sortedCounts[idx];
            idx++;
        }

        return output;
    }


    private Int128 Solve8_2()
    {
        int[][] coordinates = _fileReader.CoordinatesFromLines(_inputFilePath);


        //distances
        Dictionary<(int, int), double> distances = new();

        for (int i = 0; i < coordinates.Length - 1; i++)
        {
            var coordinates1 = coordinates[i];
            for (int j = i + 1; j < coordinates.Length; j++)
            {
                var coordinates2 = coordinates[j];
                distances[(i, j)] = _utils.EuclidianDistance(coordinates1, coordinates2);
            }
        }

        //sort by distance
        var sortedPairs = distances.OrderBy(item => item.Value)
            .Select(item => item.Key);



        //clustering by distance

        Dictionary<int, HashSet<int>> clusterMemberDict = new();
        Dictionary<int, int> nodeClusterDict = new();

        int currentCluster = 0;

        foreach (var keyPair in sortedPairs)
        {
            int one = keyPair.Item1;
            int two = keyPair.Item2;

            int oneCluster = nodeClusterDict.GetValueOrDefault(one, -1);
            int twoCluster = nodeClusterDict.GetValueOrDefault(two, -1);

            bool sameState = oneCluster == twoCluster;
            bool clusteredYet = oneCluster > -1 && twoCluster > -1;

            //same cluster or no cluster yet
            if (sameState)
            {
                //new cluster with both nodes
                if (!clusteredYet)
                {
                    clusterMemberDict[currentCluster] = new HashSet<int>([one, two]);
                    nodeClusterDict[one] = currentCluster;
                    nodeClusterDict[two] = currentCluster;
                    currentCluster++;
                }
                //already in same cluster, do nothing
                continue;
            }

            //different clusters

            //both clustered, need to merge
            if (clusteredYet)
            {
                int targetCluster = nodeClusterDict[one];
                int sourceCluster = nodeClusterDict[two];
                foreach (int member in clusterMemberDict[sourceCluster])
                {
                    nodeClusterDict[member] = targetCluster;
                }
                clusterMemberDict[targetCluster].UnionWith(clusterMemberDict[sourceCluster]);
                clusterMemberDict.Remove(sourceCluster);

            }
            //only one clustered, add the other to that cluster
            else
            {
                if (oneCluster > -1)
                {
                    clusterMemberDict[oneCluster].Add(two);
                    nodeClusterDict[two] = oneCluster;
                }
                else
                {
                    clusterMemberDict[twoCluster].Add(one);
                    nodeClusterDict[one] = twoCluster;
                }
            }

            //stop if all nodes are in one cluster
            if (nodeClusterDict.Count == coordinates.Length && clusterMemberDict.Count == 1)
            {
                return coordinates[one][0] * coordinates[two][0];
            }
        }

        return default;
    }

    private int Solve9_1()
    {
        int output = 0;
        return output;
    }


    private int Solve9_2()
    {
        int output = 0;
        return output;
    }

}