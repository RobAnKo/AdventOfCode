using FileReader;

namespace AoC
{
    public class Solver
    {


        bool _real;
        string _dayNumber;
        string _part = "1";
        string _basePath = "/home/karlchen/Documents/AdventOfCode/AoC25/";
        string _inputFilePath = "";

        Reader _fileReader;
        Utils _utils;

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
                int distance;

                distance = move.StartsWith("R") ? 100 - position : position;
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


                    ///iterate over plausible sequence lengths
                    foreach (int leadLength in plausibleLengths)
                    {
                        string leadSequence = number.Substring(0, leadLength);
                        bool hit = true;

                        ///iterate over chunks of length
                        for (int startIndex = leadLength; startIndex + leadLength <= numberLength; startIndex += leadLength)
                        {
                            string compareSequence = number.Substring(startIndex, leadLength);
                            if (leadSequence != compareSequence)
                            {
                                hit = false;
                                break;
                            }
                        }

                        ///only invalid if all chunks are repetitions of the lead sequence
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
                    if (_utils.CountOnesAroundPosition(floor, xPos, yPos) < 4)
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
            int position = 50;
            string[] moves = _fileReader.StringsFromLines(_inputFilePath);

            foreach (string move in moves)
            {
                int clicks = Int32.Parse(move.Substring(1));
                int distance;

                distance = move.StartsWith("R") ? 100 - position : position;
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


    }
}