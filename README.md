upapap: Universität PAssau PrüfungsAusschussParser
==================================================

Dieses Skript generiert eine machinen- und einfacher menschenlesbare Übersicht
der Links auf den vier studienrelevanten Informationsseiten der Fakultät für
Informatik und Mathematik der Universität Passau:

- [Modulkataloge](https://www.fim.uni-passau.de/studium/modulkataloge/)
- [Anrechenbarkeiten](https://www.fim.uni-passau.de/index.php?id=17010)
- [Beschlüsse des Prüfungsausschusses](https://www.fim.uni-passau.de/ueber-die-fakultaet/ausschuesse/pruefungsausschuss/)
- [Prüfungsordnungen](https://www.fim.uni-passau.de/studium/pruefungsordnungen/)

Die Inhalte werden direkt von der Uni-Website abgerufen und bei `upapap-cgi`
für 15 Minuten lokal gecached.

## Ausgabeformate

`upapap` und `upapap-cgi` produzieren standardmäßig Markdown-ähnlichen Text.  
Dieser eignet sich unter anderem, um per `diff`, `urlwatch`, o.ä. automatisch
nach Änderungen zu suchen und diese übersichtlich darzustellen.

Wenn `upapap-cgi` über die `SCRIPT_NAME`-Umgebungsvariable feststellt, dass es
über eine URL mit der Endung `.html` aufgerufen wurde, produziert es statt
Markdown eine nach HTML konvertierte Fassung der selben Inhalte.

## Voraussetzungen

Für `upapap` und `upapap-cgi`:

- beautifulsoup4
- requests

Für `upapap-cgi` außerdem:

- requests-cache

`upapap-cgi` nutzt aus Kompatibilitätsgründen Python2.

## Einrichtung

`upapap` kann direkt auf der Kommandozeile ausgeführt werden.  
Es gibt kein Caching, also besser sparsam benutzen.

`upapap-cgi` kann als CGI-Skript von einem geeigneten Webserver aufgerufen werden, z.B. über folgenden Eintrag in der Apache-Konfiguration:

```
ScriptAlias /upapap /var/www/cgi-bin/upapap-cgi
ScriptAlias /upapap.html /var/www/cgi-bin/upapap-cgi
```
