  ...
  /// <summary>
  /// Loggt Vishnu-Ereignisse in ein Logfile.
  /// </summary>
  public class TextFileLogger : INodeLogger
  {
      /// <summary>
      /// Übernahme von diversen Logging-Informationen und Ausgabe in eine Logdatei.
      /// </summary>
      /// <param name="loggerParameters">Spezifische Aufrufparameter oder null.</param>
      /// <param name="treeParameters">Für den gesamten Tree gültige Parameter oder null.</param>
      /// <param name="treeEvent">Objekt mit Informationen über das Ereignis.</param>
      /// <param name="additionalEventArgs">Enthält z.B. beim Event 'Exception' die zugehörige Exception.</param>
      public void Log(object loggerParameters, TreeParameters treeParameters, TreeEvent treeEvent, object additionalEventArgs)
      {
          // Setzen des Pfades zur Logdatei
          this.SetLogFilePath(loggerParameters, treeEvent);
  
          // Zusammenbauen der zu loggenden Nachricht
          string bigMessage = BuildLogMessage(treeParameters, treeEvent, additionalEventArgs);
  
          this.WriteLog(bigMessage);
      }
  
      ...
      // Übernimmt entweder einen übergebenen, speziellen Pfad zu einer Logdatei
      // oder setzt den Default Pfad. Legt ggf. das Zielverzeichnis an.
      private void SetLogFilePath(object loggerParameters, TreeEvent treeEvent)
      {
          if (loggerParameters != null)
          {
              this._debugFile = loggerParameters.ToString();
          }
          else
          {
              this._debugFile = treeEvent.ReplaceWildcards("%DebugFile%");
          }
          if (!Directory.Exists(Path.GetDirectoryName(this._debugFile)))
          {
              Directory.CreateDirectory(Path.GetDirectoryName(this._debugFile));
          }
      }
  
      // Baut aus den übergebenen Parametern einen einzigen formatierten string zusammen.
      private string BuildLogMessage(TreeParameters treeParameters, TreeEvent treeEvent, object additionalEventArgs)
      {
          string indent = "        ";
          string addInfos = indent;
          if (treeEvent.Name.Contains("Exception"))
          {
              addInfos += (additionalEventArgs as Exception).Message;
          }
          if (treeEvent.Name.Contains("ProgressChanged"))
          {
              addInfos += String.Format("Fortschritt {0:d3}%", Convert.ToInt32(additionalEventArgs));
          }
          string timestamp = System.String.Format(System.Globalization.CultureInfo.CurrentCulture,
              "{0:yyyy.MM.dd HH:mm:ss,ffffff}", new object[] { treeEvent.Timestamp });
          StringBuilder bigMessage = new StringBuilder(timestamp + " Event: " + treeEvent.Name);
          string IdName = treeEvent.NodeName + "|" + treeEvent.SenderId;
          bigMessage.Append(Environment.NewLine + indent + "Knoten: " + IdName);
          bigMessage.Append(", Logical: " + treeEvent.Logical);
          bigMessage.Append(", Quelle: " + treeEvent.SourceId);
          bigMessage.Append(Environment.NewLine + indent + treeEvent.ReplaceWildcards("%MachineName%")
              + ", Thread: " + treeEvent.ThreadId.ToString());
          bigMessage.Append(", Tree: " + treeParameters.ToString());
          if (addInfos.Trim() != "")
          {
              bigMessage.Append(Environment.NewLine + addInfos);
          }
          if (!String.IsNullOrEmpty(treeEvent.NodePath))
          {
              bigMessage.Append(Environment.NewLine + indent + treeEvent.NodePath);
          }
          bigMessage.Append(", Status: " + treeEvent.State.ToString());
          bigMessage.Append(Environment.NewLine + indent + "WorkingDirectory: "
              + treeEvent.ReplaceWildcards("%WorkingDirectory%"));
          return bigMessage.ToString();
      }
  
      // Die Routine versucht, in eine möglicherweise von mehreren Knoten gleichzeitig
      // genutzte Logdatei zu schreiben; wirft im Fehlerfall keine Exception, sondern
      // versucht es wieder, bis ein Zähler abgelaufen ist.
      // Im ungünstigsten Fall kann der Logging-Versuch fehlschlagen.
      private void WriteLog(string message)
      {
          int maxTries = 5;
          StreamWriter streamWriter;
          int i = 0;
          do
          {
              try
              {
                  using (streamWriter = new StreamWriter(new FileStream(this._debugFile,
                      FileMode.Append, FileAccess.Write), Encoding.Default))
                  {
                      streamWriter.WriteLine(message);
                      i = maxTries; // erfolgreich, Loop beenden
                  }
  
              }
              catch (SystemException)
              {
                  Thread.Sleep(10); // 10 tausendstel Sekunden warten
              }
          } while (++i < maxTries);
      }
  ...
 
