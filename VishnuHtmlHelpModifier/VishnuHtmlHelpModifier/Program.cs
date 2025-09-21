using HtmlAgilityPack;
using System.Text.RegularExpressions;

namespace VishnuHtmlHelpModifier
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string rootDir = Directory.GetCurrentDirectory();
            if (args.Length > 0)
            {
                string rootDirCandidate = args[0];
                if (!Directory.Exists(rootDirCandidate))
                {
                    throw new ArgumentException($"Directory {rootDirCandidate} doesn't exist.");
                }
                rootDir = rootDirCandidate;
            }
            // keywordIndex = new();
            RecurseSubDirectories(rootDir);
            // SaveIndexToFile(keywordIndex, "index.txt");
        }

        static int RecurseSubDirectories(string rootDirectory, string indention = "")
        {
            Console.WriteLine($"{indention}Working on directory '{rootDirectory}' ...");
            int fileCount = 0;
            foreach (string subDirectory in Directory.GetDirectories(rootDirectory))
            {
                if (!subDirectory.EndsWith(".vs"))
                {
                    fileCount += RecurseSubDirectories(subDirectory, indention + "    ");
                }
            }
            foreach (string file in Directory.GetFiles(rootDirectory))
            {
                if (Path.GetExtension(file) == ".htm")
                {
                    //if (Path.GetFileName(file) == "62ca75a8-ba50-4115-93df-b1e76bf6e5f7.htm")
                    WorkOnFile(file);
                }
            }
            return fileCount;
        }

        private static void WorkOnFile(string file)
        {
            Console.WriteLine($@"\tworking on {file}");
            string allFileText = File.ReadAllText(file);
            string writeText = Regex.Replace(allFileText,
                "\\<div\\s+id=\"PageHeader\".+<button id=\"SearchButton\"\\s+type=\"submit\"></button></form></div>", "");

            File.Move(file, file + ".bak", true);
            File.WriteAllText(file, writeText);

            HtmlDocument doc = new HtmlDocument();
            doc.Load(file);

            // Extrahiere relevante Inhalte aus der HTML-Seite und identifiziere Schlagwörter
            // List<string> keywords = ExtractKeywords(doc);

            // Füge die extrahierten Schlagwörter zum Index hinzu
            // string fileName = Path.GetFileName(file);
            // keywordIndex[fileName] = keywords;
        }

        /* eventuell später mal
        static Dictionary<string, List<string>> keywordIndex;
        private static List<string> _fillWords = new()
        {
              "0"
            , "1"
            , "2"
            , "3"
            , "4"
            , "5"
            , "6"
            , "7"
            , "8"
            , "9"
            , "ein"
            , "eine"
            , "einer"
            , "einen"
            , "dessen"
            , "dieser"
            , "der"
            , "die"
            , "das"
            , "deren"
            , "und"
            , "oder"
            , "einfach"
            , "beispiel"
            , "&lt"
            , "?"
            , "xml"
            , "version"
            , "="
            , "1, 0"
            , "encoding"
            , "utf-8"
            , "?&gt"
            , "&gt"
            , "/"
            , "array"
            , "all"
            , "8"
            , "200"
            , "3"
            , "siehe"
            , "type"
            , "änderung"
            , "auch" };

        static List<string> ExtractKeywords(HtmlDocument doc)
        {
            List<string> keywords = new List<string>();

            foreach (HtmlNode node in doc.DocumentNode.SelectNodes("//strong | //span | //h1 | //h2 | //h3"))
            {
                string text = node.InnerText.Replace("&gt", "").Replace("(", "").Replace(")", "").Replace("\"", "").Replace("/", "");
                string[] strings = text.Split(new char[] { ' ', ',', '.', ':', ';' }, StringSplitOptions.RemoveEmptyEntries);
                foreach (string str in strings)
                {
                    string s = str.ToLower();
                    bool valid = true;
                    foreach (string k in _fillWords)
                    {
                        if (k.Length > 4 && s.Contains(k) || k.Contains(s))
                        {
                            valid = false;
                            break;
                        }
                    }
                    if (valid)
                    {
                        foreach (string k in keywords)
                        {
                            if (k.Contains(s))
                            {
                                valid = false;
                            }
                        }
                    }
                    if (valid)
                    {
                        keywords.Add(s);
                    }
                }
                // keywords.AddRange(strings);
            }
            return keywords;
        }

        static void SaveIndexToFile(Dictionary<string, List<string>> index, string filePath)
        {
            using (StreamWriter writer = new StreamWriter(filePath))
            {
                foreach (var entry in index)
                {
                    writer.WriteLine(entry.Key + ": " + string.Join(", ", entry.Value));
                }
            }
        }
        */ 
    }
}
