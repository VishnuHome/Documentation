c:\Program Files (x86)\EWSoftware\Sandcastle Help File Builder\Components\VS2013\styles\branding.css

c:\Program Files (x86)\EWSoftware\Sandcastle Help File Builder\Components\Shared\Content\SharedContent_de-DE.xml

C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.0\de\System.Data.Services.Client.xml
                                                                              v4.6.2
                                                                              v4.6.1
                                                                              v4.6

Sandcastle Tokens (selbst definierbare Text- und Grafik-Bausteine)
	Visual Studio 2019
		Neues Projekt erstellen
			im Suchfenster Sandcastle eingeben
				Sandcastle Help File Builder Project ausw�hlen
		auf Projekt rechte Maustaste
			Hinzuf�gen / Neues Element / Token File
	
	Doppelklick auf <Projektname>.tokens
		Token erstellen, siehe 
			Sandcastle Help File Builder Documentation
				Conceptual and Additional Content
					Conceptual Content
						Token Files
	Token in der Doku einf�gen �ber:
		<token>Token-ID<token>
	Automatisieren:
		Visual Studio 2019
			Erweiterungen
				Erweiterungen verwalten
					Visual Commander downloaden,
					dann Visual Studio beenden und das
					heruntergeladene vsix-file installieren (Doppelklick)
			irgendwo im Text:
				Strg-Umschalt-R (f�r record Macro)
					<token>Token-ID plus drei mal Strg-Rechtspfeil eingeben
						(das </token> wird vom Editor automatisch angef�gt)
				wieder Strg-Umschalt-R (stoppt das Recording)
			Erweiterungen / VCmd / Save Macro as Command
				Name vergeben plus Compile und Save
			Extras / Anpassen / Men� "Erweiterungen" / Tastatur
				VCmd.Command01
					in Feld "Neue Tastenkomb. verwenden in:"
						Global auf Text-Editor �ndern
					Feld "Tastenkombination dr�cken:" ausw�hlen und Tastenkombination eingeben
	Internationalisierern, multilanguage, DE-de, EN-en
		Projekteigenschaften/Help file
			Help file language
		
		https://www.nuget.org/packages/Surviveplus.XmlCommentLocalization/
		...\VishnuHome\Documentation\surviveplus.xmlcommentlocalization.1.0.6.2.nupkg
					
Visual Commander
