# Bundeshaushaltsanalyse

*Find an English summary below*

Mit dem Projekt verfolgte ich zwei Zwecke: 
<ol>
  <li>Mich tiefgehend mit dem Bundeshaushalt auseinandersetzen</li>
  <li>Die Entwicklung des Bundeshaushalts über ein Jahrzehnt visualisieren</li>
</ol>

Zum deutschen Bundeshaushalt gibt es auch eine eigene Plattform, die wirklich schön alle Punkte aufschlüsselt. Die Plattform findet ihr [hier](https://www.bundeshaushalt.de/DE/Bundeshaushalt-digital/bundeshaushalt-digital.html). Für mich war es allerdings nicht ausreichend, die aggregierten Daten präsentiert zu bekommen, ich wollte sie selbst analyisieren. Die Analyse kann ich somit auch selbständig die nächsten Jahre fortführen und nach Lust und Laune um weitere Forschungsfragen vertiefen. 

## Datenquelle

Der Bund stellt die Daten über das bereits genannte [Portal](https://www.bundeshaushalt.de/DE/Download-Portal/download-portal.html) zum digitalen Bundeshaushalt verfügbar. Die zur Verfügung gestellten Daten reichen bis ins Jahr 2005 zurück. Richtig bearbeitet werden können aber nur die Datein ab 2014, weshalb ich mich dazu entschieden hatte, mich bei der Analyse auf die vergangenen zehn Jahre zu konzentrieren. Dateiformate zu den früheren Bundeshaushalten sind teilweise nicht uniform zu den neueren Dateiformaten. Zur Verarbeitung bzw. zum Vergleich, mussten diese nachbereinigt werden. 

Beim sporadischen Abgleich mit den Grafiken auf dem Portal zum digitalen Bundeshaushalt sind mir Unstimmigkeiten für das Jahr 2023 aufgefallen. Die Ursache der Unstimmigkeit konnte ich identifizieren, mir aber nicht erklären. Meiner Vermutung nach veranlasst dabei einer finanzieller Sonderfall eine abweichende Berechnung, die sich für mich ohne Fachkenntnisse nicht nachvollziehen lässt. 

## Ergebnisse

![Entwicklung als Balkendiagramm](/output_data/visualisierungen/complete_bar.svg)

An dieser Stelle erhält man einen guten ersten Überblick. Schnell ersichtlich ist, dass der größte Kostenpunkt "Soziales" ist. Mit großem Abstand folgt der Punkt "Allgemeine Dienste", der auch unsere Verteidigungsausgaben beinhaltet.

![Logarithmische Skala zur Entwicklung des Bundeshaushalts](/output_data/visualisierungen/complete_logarithmic.svg)

Die Entwicklung der Kostenpunkte ist auf einer logarithmischen Skala deutlich besser erkennbar.

![Steigung der Entwickung des Bundeshaushalts](/output_data/visualisierungen/slope.svg)

Ein wahrhaft interessantes Bild ist die Entwicklung des Bundeshaushalts als Graphen, der die Haushaltsausgaben im Vergleich zu den Haushaltsausgaben im Vorjahr setzt. Die Steigung der Ausgaben nach Kostenpunkt also so zu sagen.

![Nachtragshaushalte](/output_data/visualisierungen/integrated_supp.svg)

Auch die Nachtragshaushalte lassen sich in den Vergleich zu den sonstigen Haushaltsausgaben setzen. Hierbei spiegeln sie gesellschaftliche Entwicklungen und Vorkommnisse wieder. Wie auch schon die anderen Diagramme zeigten, wird hier die Flüchtlingskrise 2015 und die Corona-Pandemie 2020-2023 im Diagramm einordenbar.

![Nachtragshaushalte isoliert](/output_data/visualisierungen/supp_individual.svg)

Zuletzt hier noch einmal die Nachtragshaushalte isoliert im Vergleich. 

Nun nochmal eine kurze Zusammenfassung auf Englisch:

# English summary

I had two purposes for the project:
<ol>
  <li>Deal in depth with the federal budget</li>
  <li>Visualize the development of the federal budget over a decade</li>
</ol>

There is also a separate platform for the German federal budget that really breaks down all the points. You can find the platform [here](https://www.bundeshaushalt.de/DE/Bundeshaushalt-digital/bundeshaushalt-digital.html). However, for me it was not enough to be presented with the aggregated data; I wanted to analyze it myself. I can therefore continue the analysis independently over the next few years and expand on further research questions as I wish.

## Data Source

The federal government makes the data available via the aforementioned [portal](https://www.bundeshaushalt.de/DE/Download-Portal/download-portal.html) for the digital federal budget. The data provided goes back to 2005. However, only the files from 2014 onwards can be edited properly, which is why I decided to concentrate on the past ten years in the analysis. File formats for the previous federal budgets are sometimes not uniform to the newer file formats. These had to be readjusted for processing or comparison.

When I sporadically compared the graphics on the digital federal budget portal, I noticed discrepancies for the year 2023. I was able to identify the cause of the discrepancy, but I couldn't explain it. My guess is that a special financial case causes a different calculation, which I cannot understand without specialist knowledge.

## Results

Find the diagrams above.

Diagram content:
<ol>
  <li>Complete bar chart of the budget plans</li>
  <li>Logarithmic visualization of the budget plans</li>
  <li>Slope visualizations - calculated how much the budget changes from one year to the next</li>
  <li>First visualization of the supplementary budgets</li>
  <li>Second visualization of the supplementary budgets</li>
</ol>