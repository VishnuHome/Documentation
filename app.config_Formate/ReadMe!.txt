    /// <summary>
    /// Holt Applikationseinstellungen aus verschiedenen Quellen:
    /// Kommandozeile, app.config, ggf. app.config.user, Environment.<br />
    /// Implementiert auch das Lesen der Registry, nutzt dies aber selbst noch nicht.
    /// Wertet unter Umständen zuletzt auch noch öffentliche Properties aus (DumpAppSettings=true).
    /// Macht keine Datenbank-Zugriffe, stellt aber entsprechende Properties bereit.<br />
    /// Die Properties und das Füllen derselben sind nicht zwingend erforderlich, sie dienen
    /// nur der Bequemlichkeit; alternativ kann aus der Applikation auch direkt über die
    /// Schnittstellen IGetStringValue und IGetValue&lt;T&gt; auf die Applikations-/Systemumgebung zugegriffen werden.<br />
    /// Die hier implementierten Applikationseinstellungen sollen allgemeingültig für 
    /// Standalone-Anwendungen sein; Für anwendungsspezifische Einstellungen sollte diese Klasse
    /// abgeleitet werden.
    /// Quellen werden in folgender Reihenfolge ausgewertet (der 1. Treffer gewinnt):<br></br>
    ///     1. Kommandozeilen-Parameter (nicht bei .NetCore-Webanwendungen)<br></br>
    ///     2. Einstellungen in der app.Config (nicht bei .NetCore- Webanwendungen, stattdessen dann appsettings.json)<br></br>
    ///     3. Ggf. Einstellungen in der app.Config.user<br></br>
    ///     4. Environment<br></br>
    ///     5. Registry<br></br>
    ///     6. Unter Umständen öffentliche Properties (DumpAppSettings=true).<br></br>
    /// Zeitkritische Initialisierungen sollten in abgeleiteten AppSettings generell vermieden
    /// werden; die entsprechenden Properties können aber definiert werden und ggf. lazy implementiert werden.<br></br>
    /// Über die Properties "DumpAppSettings" und "DumpLoadedAssemblies" können zu Debug-Zwecken alle Properties mit
    /// ihren Quellen und die FullNames aller zur Laufzeit geladenen Assemblies geloggt werden.



Alle User-Konfigurationen heißen per Default "Vishnu.exe.config.user",
wobei der Teil "Vishnu.exe" je nach Anwendung wechselt (hierbei sind .exe und .dll möglich).

Das Format für .Net-Framework bis Version 4.8 ist Xml:
	<?xml version="1.0"?>
	<configuration>
		<appSettings> (oder auch <userSettings>)
			<!--   Benutzeranwendung und konfigurierte Eigenschafteneinstellungen hier einfuegen.-->
			<!--   Beispiel: <add key="settingName" value="settingValue"/> -->
			<add key="TestEinstellung" value="Test-Einstellung"/>
			<add key="SearchDirectory" value="Test-SearchDirectory"/>
		</appSettings> (oder auch </userSettings>)
	</configuration>

Das Format für alle späteren Versionen ab .Net-Core.1.0 bis heute (.Net 10) ist Json:
	{
	  "TestEinstellung": "Test-Einstellung",
	  "SearchDirectory": "Test-SearchDirectory"
	}

Die Verarbeitung der Vishnu.exe.config.user erfolgt in ...\Framework\UserSettingsAccess.
Alle Values werden als Strings definiert, also auch numerische oder boolesche Werte.
Der Default-Path ist "C:\Users\micro\AppData\Local\Vishnu\Vishnu.exe.config.user"

Eine Anwendungsspezifische "App.config" wird unter .Net-Framework automatisch im
Projektverzeichnis angelegt und mit der Eigenschaft "nicht kopieren" versehen.
Trotzdem wird bei der Umwandlung des Projekts diese App.config automatisch in das
Ausgabeverzeichnis kopiert. Sie wird dabei in <App-Name.{exe|dll}>.config umbenannt.

Eine mögliche Anwendungsspezifische appsettings.json muss im Projektverzeichnis
manuell angelegt werden und mit der Eigenschaft "immer kopieren" versehen sein.
Diese appsettings.json wird dann beim Umwandeln der Anwendung automatisch in das
Verzeichnis der exe oder dll kopiert. Sie behält dabei ihren Namen "appsettings.json"
Beim Laden der Anwendungseinstellungen werden diese Einstellungen dann
in SettingsAccess durch ConfigurationBuilder().AddJsonFile(configPath) eingelesen.

Wenn der Parameter "DumpAppSettings"="true" gesetzt ist, werden alle Einstellungen,
auf die mindestens einmal mit "GetStringValue" oder "GetValue" zugegriffen wurde,
im Logfile ausgegeben.
Das bedeutet auch: wenn man bestimmte Konfigurationseinstellungen testen will,
muss man in der Anwendung auch mindestens einmal darauf zugreifen.
