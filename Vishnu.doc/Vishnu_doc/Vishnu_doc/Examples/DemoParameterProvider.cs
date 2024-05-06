  ...
  public class DemoParameterProvider : IParameterReader
  {
      #region IParameterReader Implementation

      /// <summary>
      /// Event, das ausgelöst wird, wenn die Parameter neu geladen wurden.
      /// </summary>
      public event EventHandler ParametersReloaded;

      /// <summary>
      /// Liefert zu einem String-Parameter einen String-Wert.
      /// </summary>
      /// <param name="parameterName">Parameter-Name.</param>
      /// <returns>Parameter-Value.</returns>
      public string ReadParameter(string parameterName)
      {
          if (parameterName == "GesuchterParameter")
          {
              return "Gefunden!";
          }
          else
          {
              if (parameterName == "UebergebenerParameter")
              {
                  string timeString = this._lastTimerStart == DateTime.MinValue ? " - "
                      : this._lastTimerStart.ToString("hh:mm:ss.ms");
                  return String.Format($"{this._initParameter} - letzter Refresh: {timeString}");
              }
              else
              {
                  return null;
              }
          }
      }

      /// <summary>
      /// Einrichtungsroutine - übernimmt Parameter, holt alle Infos
      /// und stellt sie als Properties zur Verfügung.
      /// Startet ggf. einen Timer für den Parameter-Refresh.
      /// </summary>
      /// <param name="parameters">Ein Objekt zur Parameterübergabe; dieser ParameterProvider
      /// erwartet einen String mit einem übergebenem Testwert plus optional
      /// einen Timer-Parameter für regelmäßige Reloads durch Pipe-Symbol '|' abgetrennt.</param>
      public void Init(object parameters)
      {
          this._publisher = InfoController.GetInfoController();
          this.EvaluateParameters(parameters.ToString());

          this.ReloadApplicationParameters();

          if (this._eventTimer != null)
          {
              this._lastTimerStart = DateTime.Now;
              this._nextTimerStart = this._lastTimerStart.AddMilliseconds(this._timerInterval);
              this._eventTimer.Start();
          }
      }

      #endregion IParameterReader Implementation
      ...
      private void ReloadApplicationParameters()
      {
          try
          {
              this._publisher.Publish("Lade aufwändige Parameter...");
              Thread.Sleep(2000);
          }
          catch (Exception ex)
          {
              this._publisher.Publish(this, ex.Message);
              throw;
          }
          this.OnParametersReloaded();
      }
      ...
      private void eventTimer_Elapsed(object sender, ElapsedEventArgs e)
      {
          ...
          this.ReloadApplicationParameters();
          ...
      }
      ...
