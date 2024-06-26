...
  /// <summary>
  /// ReturnObject für das Ergebnis des DateToMoonAge ValueModifiers.
  /// </summary>
  /// <remarks>
  /// Autor: Erik Nagel, NetEti
  ///
  /// 04.04.2020 Erik Nagel: erstellt
  /// </remarks>
  [DataContract] //[Serializable()]
  public class DateToMoonAge_ReturnObject
  {
      /// <summary>
      /// Mondalter in Tagen.
      /// </summary>
      [DataMember]
      public int MoonAge { get; set; }
...
      /// <summary>
      /// Konstruktor - übernimmt einen String-Wert für die DefaultResultProperty.
      /// </summary>
      /// <param name="resultProperty">Int-Wert für die MoonAgeProperty</param>
      public DateToMoonAge_ReturnObject(int resultProperty)
      {
          this.MoonAge = resultProperty;
      }
      
      // Es folgen Serialisierungs- und De-Serialisierung-Routinen
      ...
  }
...
