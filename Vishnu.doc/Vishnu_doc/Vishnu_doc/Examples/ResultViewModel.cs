		...
    // TODO: Hier müssen die darzustellenden Properties aus UserChecker_ReturnObject hinzugefügt werden:
    /// <summary>
    /// Demo-Property.
    /// Das UserChecker_ReturnObject kann prinzipiell beliebige öffentliche Properties besitzen.
    /// In diesem ViewModel werden nur Properties berücksichtigt, die in den Serialisierungs-
    /// Deserialisierungsroutinen des UserCheckers entsprechend berücksichtigt wurden.
    /// </summary>
    public string DefaultResultProperty
    {
        get
        {
            string prop = this.GetResultProperty<string>(typeof(UserChecker_ReturnObject), "DefaultResultProperty");
            return prop;
        }
    }

		...

    /// <summary>
    /// Wird ausgeführt, wenn sich die Result-Property des ViewModels
    /// des zugehörigen Vishnu-Knotens geändert hat.
    /// </summary>
    public void HandleResultPropertyChanged()
    {
				...
        // TODO: Hier müssen die darzustellenden Properties aus UserChecker_ReturnObject hinzugefügt werden:
        this.RaisePropertyChanged("DefaultResultProperty");

        // TODO: Eventuelle zusätzliche Buttons müssten hier zum Update gezwungen werden,
        // da die Verarbeitung in einem anderen Thread läuft, z.B.:
        // this._btnXYZ...RelayCommand.UpdateCanExecuteState(this.Dispatcher);
    }

		...
