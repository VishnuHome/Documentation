@ECHO OFF
SetLocal EnableDelayedExpansion

del /q translate_all.bat 2>nul
rem FOR /r %%G in ("*.cs") DO (
rem 	IF EXIST "%%G" (
rem 		set origname=%%G
rem 		set newname=!origname:\obj\=\xxx\!
rem 		set newname=!newname:AssemblyInfo.cs=xxx!
rem 		if !newname! == !origname! ECHO CSharpCommentTranslator "!newname!" >> translate_all.bat
rem 	)
rem )
rem FOR /r %%G in ("*.aml") DO (
rem 	IF EXIST "%%G" (
rem 		set origname=%%G
rem 		set newname=!origname:\obj\=\xxx\!
rem 		set newname=!newname:AssemblyInfo.cs=xxx!
rem 		if !newname! == !origname! ECHO MarkDownTranslator "!newname!" >> translate_all.bat
rem 	)
rem )
rem FOR /r %%G in ("*.htm") DO (
rem 	IF EXIST "%%G" (
rem 		set origname=%%G
rem 		set newname=!origname:\obj\=\xxx\!
rem 		set newname=!newname:AssemblyInfo.cs=xxx!
rem 		if !newname! == !origname! ECHO MarkDownTranslator "!newname!" -SourceLanguageCode=de -TargetLanguageCode=en-GB >> translate_all.bat
rem 	)
rem )
FOR %%G in ("*.htm") DO (
	IF EXIST "%%G" (
		set origname=%%G
		set newname=!origname:\obj\=\xxx\!
		set newname=!newname:AssemblyInfo.cs=xxx!
		if !newname! == !origname! ECHO MarkDownTranslator "!newname!" -SourceLanguageCode=de -TargetLanguageCode=en-GB >> translate_all.bat
	)
)
