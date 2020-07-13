[![cronscraper](https://github.com/legal-networks/gesetze-im-internet/workflows/cronscraper/badge.svg?event=schedule)](https://github.com/legal-networks/gesetze-im-internet/actions)

# Gesetze im Internet

Es werden die auf https://www.gesetze-im-internet.de veröffentlichten Gesetze, Rechtsverordnungen, etc. täglich archiviert. 
Das Archiv beschränkt sich auf XML-Dateien nebst Anhänge. (Die inhaltsgleichen PDF-, EPUB- und HTML-Dateien werden nicht geischert.)

Die Daten sind im [Branch 'Data' dieses Repositories](https://github.com/legal-networks/gesetze-im-internet/tree/data) 
abrufbar.

Unter [Releases](https://github.com/legal-networks/gesetze-im-internet/releases) 
kann der Stand zu einem Tag ausgewählt, eingesehen und separat heruntergeladen werden.


## Nutzung

Dieses Archiv enthält die jeweils aktuellen Gesetze seit dem 10. Juni 2019 in strukturiertem Format. 
Dieser historische Datensatz eignet sich insbesondere für die maschinelle Weiterverarbeitung 
und kann beispielsweise für quantitative Analysen des Rechts genutzt werden. 
Daher wird auf eine Weiterverarbeitung der archivierten Daten an dieser Stelle verzichtet.


## Hintergrundinformationen

Das [Log](https://github.com/legal-networks/gesetze-im-internet/blob/data/data/log.md) 
enthält eine Liste aller archivierten Versionen.
Ebenfalls können die Commit-Messages im Branch 'Data' genutzt werden.

Ab Mai 2020 geschieht die Archivierung täglich und transparent mittels 
[Github Actions](https://github.com/legal-networks/gesetze-im-internet/actions).
Das Archiv reicht bis zum 10. Juni 2019 zurück. Für diesen Zeitraum stehen wöchtenliche Versionen bereit.


### Archivierungsprozess

Die Archivierung basiert auf dem Inhaltsverzeichnis von Gesetze im Internet, dass als XML-Datei bereitgestellt wird. 
(Siehe https://www.gesetze-im-internet.de/hinweise.html für nähere Informationen.)
Es werden alle genannten Gesetze heruntergeladen und entpackt. Sofern sich ihr Inhalt geändert hat, 
wird die neue Version zum Repository hinzugefügt.

In seltenen Fällen ist eine im Inhaltsverzeichnis aufgeführte Datei auf dem Server nicht verfügbar. 
Solche eine Datei wird ausgelassen und unter `data/not_found.txt` im jeweiligen Commit dokumentiert. 
Typischerweise ist die Datei leer, da dieser Fehler bei der betreffenden Archivierung nicht aufgetreten ist.

Finden die Betreiber von gesetze-im-internet.de Fehler in den Daten (beispielsweise einen Tippfehler), 
werden diese auf der Webseite nachträglich korrigiert.
Entsprechend wird bei der nächsten Archivierung die Fehlerkorrektur als neue Gesetzesversion in das Archiv übernommen.
Im Archiv wird der Fehler jedoch nicht in bereits archivierten Versionen nachträglich korrigiert. 
Daher kann von einer neuen Dateiversion nicht zwingend auf eine Änderung der Rechtslage geschlossen werden,
ohne die Änderung inhaltlich zu untersuchen.
Neben einer Fehlerkorrektur wird eine neue Version häufig durch eine Aktualisierung des `builddate` 
\[ein Attribut in der XML Datei\] verursacht.
