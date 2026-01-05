using AoC;


System.Console.WriteLine("Which day should we solve?");
string dayNumber = Console.ReadLine();

System.Console.WriteLine("Which part should we solve (1 or 2)?");
string part = Console.ReadLine();


System.Console.WriteLine("Real thing (1) or test (0)?");
bool real = Console.ReadLine() == "1";


Solver solver = new Solver(real, dayNumber, part);
System.Console.WriteLine($"The answer is {solver.Solve()}");