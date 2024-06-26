...
  /// <summary>
  /// Konvertiert ein übergebenes Datum in das zugehörige Mondalter in Tagen.
  /// </summary>
  /// <remarks>
  /// File: DateToMoonAge.cs
  /// Autor: Erik Nagel, NetEti
  /// Herzlichen Dank an Mostafa Kaisoun für seine Berechnungslogik
  /// https://www.codeproject.com/script/Membership/View.aspx?mid=1961229
  /// 
  /// 04.04.2020 Erik Nagel: erstellt
  /// </remarks>
  public class DateToMoonAge : IValueModifier
  {
      /// <summary>
      /// Konvertiert ein übergebenes Datum in das zugehörige Mondalter in Tagen.
      /// </summary>
      /// <param name="toConvert">Datum als DateTime.</param>
      /// <returns>Mondalter in Tagen.</returns>
      public object ModifyValue(object toConvert)
      {
          if (toConvert is DateTime)
          {
              if (toConvert != null)
              {
                  DateTime inDateTime = (DateTime)toConvert;
                  return new DateToMoonAge_ReturnObject(this.MoonAge(inDateTime.Day, inDateTime.Month, inDateTime.Year));
              }
              else
              {
                  return toConvert;
              }
          }
          else
          {
              throw new ArgumentException(String.Format("{0}: kann {1} nicht konvertieren, erwartet wird DateTime", this.GetType().Name, toConvert.ToString()));
          }
      }
...
    private int MoonAge(int d, int m, int y)
    {
      ...
    }
...
  }
...