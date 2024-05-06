  ...
  class Program
  {
      public static void Main(string[] args)
      {
          TimerTrigger.TimerTrigger trigger = new TimerTrigger.TimerTrigger();
          trigger.Start(null, @"S:5|S:3", trigger_TriggerIt);
          Console.WriteLine("Stopp Trigger mit Enter");
          Console.WriteLine();
          Console.ReadLine();
          trigger.Stop(null, trigger_TriggerIt);
          Console.WriteLine("Trigger gestoppt");
          Console.ReadLine();
      }

      static void trigger_TriggerIt(TreeEvent source)
      {
          Console.WriteLine($"{source.Name} feuert ({source.SourceId} {source.SenderId}).");
      }
  }
