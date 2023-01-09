		...
    private bool? Work(TreeEvent source)
    {
        // Beispielhaft wird hier über das übergebene TreeEvent ein Zusatzparameter
        // aus dem Result eines angenommenen Vorgänger-Checkers weiterverarbeitet.
        // Bei den meisten Checkern ist dieser Teil allerdings nicht erforderlich.
        string demoInterestingPredecessorHello = null;
        if (source?.Results?.ContainsKey("Predecessor") == true)
        {
            object returnObject = source.Results["Predecessor"].ReturnObject;
            demoInterestingPredecessorHello = GenericPropertyGetter.GetProperty<string>(
                returnObject, "DefaultResultProperty");
        }
        else
        {
            if (source?.Environment?.ContainsKey("Predecessor") == true)
            {
                object returnObject = source.Environment["Predecessor"].ReturnObject;
                demoInterestingPredecessorHello = GenericPropertyGetter.GetProperty<string>(
                    returnObject, "DefaultResultProperty");
            }
            // Je nach Anforderungen kann hier eine Exception geworfen werden.
            //else
            //{
            //    throw new ApplicationException(
            //    "UserChecker: DemoInterestingPredecessor wurde nicht gefunden!");
            //}
        }

        // Hier folgt die eigentliche Checker-Verarbeitung, die einen erweiterten boolean als Rückgabe
        // dieses Checkers ermittelt und ggf. auch ein Return-Objekt mit zusätzlichen Informationen füllt.
        // Die Rückgabe kann völlig unabhängig von Results oder Environment sein; ist hier nur für
        // die Demo abhängig kodiert.
        // TODO: hier können Sie Ihre eigene Verarbeitung implementieren.
        if (!String.IsNullOrEmpty(demoInterestingPredecessorHello))
        {
            this._returnObject = demoInterestingPredecessorHello;
            return true;
        }
        else
        {
            this._returnObject = "no Predecessor-Result found!";
            return false;
        }
    }
		...
				