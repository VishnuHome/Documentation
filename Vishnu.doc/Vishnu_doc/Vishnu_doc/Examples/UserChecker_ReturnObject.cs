		...
    /// <summary>
    /// Deserialisierungs-Konstruktor.
    /// </summary>
    /// <param name="info">Property-Container.</param>
    /// <param name="context">Übertragungs-Kontext.</param>
    protected UserChecker_ReturnObject(SerializationInfo info, StreamingContext context)
    {
        this.DefaultResultProperty = info.GetString("DefaultResultProperty");
    }

    /// <summary>
    /// Serialisierungs-Hilfsroutine: holt die Objekt-Properties in den Property-Container.
    /// </summary>
    /// <param name="info">Property-Container.</param>
    /// <param name="context">Serialisierungs-Kontext.</param>
    public virtual void GetObjectData(SerializationInfo info, StreamingContext context)
    {
        info.AddValue("DefaultResultProperty", this.DefaultResultProperty);
    }

    /// <summary>
    /// Überschriebene ToString()-Methode - stellt alle öffentlichen Properties
    /// als einen aufbereiteten String zur Verfügung.
    /// </summary>
    /// <returns>Alle öffentlichen Properties als ein String aufbereitet.</returns>
    public override string ToString()
    {
        StringBuilder str = new StringBuilder(this.DefaultResultProperty);
        // str.Append(...);
        return str.ToString();
    }

    /// <summary>
    /// Überschriebene Vergleichsmethode - vergleicht dieses Result mit
    /// einem übergebenen Result nach Inhalt.
    /// </summary>
    /// <param name="obj">Das zu vergleichende Result.</param>
    /// <returns>True, wenn das übergebene Result inhaltlich gleich diesem Result ist.</returns>
    public override bool Equals(object obj)
    {
        if (obj == null || this.GetType() != obj.GetType())
        {
            return false;
        }
        if (Object.ReferenceEquals(this, obj))
        {
            return true;
        }
        if (this.ToString() != obj.ToString())
        {
            return false;
        }
        return true;
    }

    /// <summary>
    /// Überschriebene Hashcode Erzeugungsroutine - Erzeugt einen
    /// eindeutigen Hashcode für dieses Result.
    /// </summary>
    /// <returns>Hashcode (int).</returns>
    public override int GetHashCode()
    {
        return (this.ToString()).GetHashCode();
    }
		...