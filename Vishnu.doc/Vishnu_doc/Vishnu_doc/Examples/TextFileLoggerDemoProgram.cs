using System;
using Vishnu.Interchange;

namespace TextFileLogger
{
    class Program
    {
        static void Main(string[] args)
        {
            TextFileLogger myLogger = new TextFileLogger();
            myLogger.Log(null, new TreeParameters("Test-Tree", null),
              new TreeEvent("Ereignis auf Standard-LogPath", "4711", "0815", "ein Knoten", "",
                            false, NodeLogicalState.Done, null, null), null);
            myLogger.Log(@"sub1\TextFileLoggerDemo.log", new TreeParameters("Test-Tree", null),
              new TreeEvent("Ereignis auf speziellem LogPath", "4711", "0815", "ein Knoten", "",
                            false, NodeLogicalState.Done, null, null), null);
            Console.WriteLine("Ende mit Enter");
            Console.ReadLine();
        }
    }
}
