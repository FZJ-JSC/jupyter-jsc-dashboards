------------------------
### Fragen & Antworten
##### Bayessches räumlich-zeitliches Interaktionsmodell für Covid-19                   
------------------------

#### Was ist ein Nowcast?
Aufgrund von verschiedenen Verzögerungen in der Erfassung von Infektionen entsprechen die aktuellen Meldezahlen nicht den tatsächlichen des heutigen Tages.
Das Nowcasting schätzt wie viele Fälle noch nicht berücksichtigt wurden und korrigiert Zahlen so, dass sie möglichst nah an den echten Zahlen sind.
Für weitere Informationen siehe das [FAQ des Robert Koch-Instituts](https://www.rki.de/SharedDocs/FAQ/NCOV2019/gesamt.html) und den [Erklärfilm](https://youtu.be/8-AfYeosBW8) .

------------------------

#### Woher kommen die Daten?
Die Zahlen der Positiv-Tests beziehen wir vom offiziellen [Dashboard des RKIs](https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4), bzw. dem dahinterliegenden ArcGIS-System.
Eine Zusammenfassung dieser Zahlen wird auch im [Wochenbericht des RKI](https://ars.rki.de/Content/COVID19/Main.aspx) veröffentlicht. 

------------------------

#### Worin unterscheidet sich diese Analyse von anderen Vorhersagen?
Dieses Modell modelliert nicht nur den wahrscheinlichsten Verlauf, sondern zeigt eine Vielzahl von mit den Daten kompatiblen Verläufen und berechnet deren Wahrscheinlichkeit (Bayesian Analyse, siehe auch [Konfidenzintervall](https://de.wikipedia.org/wiki/Konfidenzintervall)).
Dies erlaubt es die Wahrscheinlichkeit für eine Zu- oder Abnahme zu bestimmen, und zudem auch seltene aber eventuell extreme Vorhersagen in die Bewertung einfließen zu lassen.

------------------------

#### Was ist ein Konfidenzintervall?
Ein Konfidenzintervall gibt an wie groß der Bereich der Modell-Entwicklung ist, der mit einer bestimmten Wahrscheinlichkeit vorhergesagt wird.
In unserem Fall haben wir für die Vorhersage zwei Konfidenzintervalle genutzt, die wie folgt interpretiert werden können. 
- 25%-75% Quantil: Dieses dunkelgrüne/-orange Intervall beinhaltet 50% der Vorhersagen.
    Das heißt man kann erwarten, dass für eine Vorhersage die echten zukünftigen Daten mit einer Wahrscheinlichkeit von 50% in dem dunkelgrünen/-orangen Intervall liegen. 
- 5%-95% Quantil: Dieses hellgrüne/-orange Intervall beinhaltet 90% der Vorhersagen.
    Das heißt man kann erwarten, dass für eine Vorhersage die echten zukünftigen Daten mit einer Wahrscheinlichkeit von 90 % in dem hellgrünen/-orangen Intervall liegen. 

------------------------

#### Was ist der Interaktionskernel?
Der Interaktionskernel schätzt ab um wie stark eine gemeldete Infektion eine Neuansteckung in den nächsten Tagen in einem Umkreis von bis zu 50km beeinflusst.
Diese Interaktion ist ein zusätzlicher Faktor der den Trend in einem Landkreis verstärkt oder abschwächt.
Eine warme Farbe indiziert, dass eine Covid-19 Meldung eine erhöhte Wahrscheinlichkeit einer Neuinfektion im Verhältnis zum Trend zur Folge hat.
Eine starke Farben in der Nähe kleiner Radien bedeutet, dass das Infektionsgeschehen vor allem Auswirkungen in der direkten Nähe der gemeldeten Fälle zur Folge hat.
Die Interaktion basiert auf einer Schätzung der Bevölkerungsdichte und der Form der Landkreise.
Daten zu den Wohnorten der Infizierten werden in dem Model nicht genutzt.
Alle hier genutzten Daten sind vollständig anonymisiert (siehe Erklärvideo).
Bei der Interpretation der Interaktionskernel ist dies zu berücksichtigen, und wir weisen darauf hin, dass dies nur eine Schätzung ist die von der Realität abweichen kann.

------------------------

#### Nach welchen Regeln werden die Farben des Interaktionskernels gewählt?
Die Farben des Interaktionskernel geben die Stärke des lokalen und zeitlichen Einflusses der Umgebung an.
Die Farben wurden so gewählt, dass starke Farben den größten Effekten seit dem Beginn der Analyse entsprechen.
Schwache Farben indizieren, dass der Effekt deutlich kleiner ist. 

------------------------

#### Welche Schwächen hat die Methode?
Alle hier präsentierten Ergebnisse basieren auf statistischen Methoden und bilden damit nicht das tatsächliche Geschehen ab, sondern Schätzungen, die von der wirklichen Situation abweichen können.
Dies ist bei der Interpretation der Ergebnisse zu berücksichtigen.
Die hier präsentierten Forschungsergebnisse basieren auf einer neuen Methodik, die bisher nicht für COVID-19 sondern für Campylobacteriosis-, Rotavirus- und Borreliose-Infektionen eingesetzt wurde (siehe Veröffentlichung).
Die Validierung der Ergebnisse für COVID-19 wird mit der wachsenden Menge an Daten in den kommenden Monaten fortgeführt. 

------------------------

#### Was ist das geglättete und ungeglättete Modell?
Die Daten des RKI zeigen eine Modulation im Wochenrhythmus, mit einer typischerweise niedrigeren Rate an Neuinfektionen am Wochenende.
Die Modulation lässt sich durch systematische Verzögerungen im Meldeprozess erklären.
Um die wirklichen Fallzahlen zu schätzen, nutzen wir ein Modell, welches diese Modulation im Wochenrhythmus korrigiert.
Diese korrigierte Version entspricht den geglätteten Daten und dem wahrscheinlichsten wirklichen Infektionsgeschehen. 
Um die Modulation zu korrigieren, verfolgen wir den Ansatz, den Wochenrhythmus zunächst im Modell zu beschreiben und anschließend diesen Teil aus dem Modell zur Vorhersage zu entfernen.
Eine Alternative zu unserem Verfahren wäre es, die Daten zunächst zu filtern.
Im Vergleich bietet das von uns eingesetzte Model die Möglichkeit, die Güte der Beschreibung der Daten sowohl für die geglätteten als auch ungeglätteten Daten durchzuführen und so auch die Qualität der Glättung selbst zu bestimmen. 

------------------------

#### Wer hat zu diesem Modell beigetragen?
- Luke Effenberger (Uni Osnabrück) (Umsetzung, Daten Analyse und Konzeption, Darstellung der Ergebnisse)
- [Jens Henrik Göbbert](https://www.fz-juelich.de/SharedDocs/Personen/IAS/JSC/EN/staff/goebbert_j_h.html) (Jülich Supercomputing Centre) (Umsetzung und Konzeption der Webapplikation sowie des wissenschaftlichen Rechnens)
- [Alice Grosch](https://www.fz-juelich.de/SharedDocs/Personen/IAS/JSC/EN/staff/grosch_a.html) (Jülich Supercomputing Centre) (Umsetzung und Konzeption der Webapplikation)
- [Dr. Kai Krajsek](https://www.fz-juelich.de/SharedDocs/Personen/IAS/JSC/EN/staff/krajsek_k.html) (Jülich Supercomputing Centre) (Performance-Analyse und -Optimierung durch Nutzung von GPU) 
- [Tim Kreuzer](https://www.fz-juelich.de/SharedDocs/Personen/IAS/JSC/EN/staff/kreuzer_t.html) (Jülich Supercomputing Centre) (Infrastruktur für das wissenschaftliche Rechens, Webapplikation, Automatisierung der Rechnungen) 
- [Prof. Dr. Gordon Pipa](https://www.ikw.uni-osnabrueck.de/en/research_groups/neuroinformatics/people/prof_dr_gordon_pipa.html) (Uni Osnabrück) (Konzeption und wissenschaftliche Leitung)
- [Pascal Nieters](https://www.ikw.uni-osnabrueck.de/en/research_groups/neuroinformatics/people/msc_pascal_nieters.html) (Uni Osnabrück) (Umsetzung, Daten Analyse und Konzeption, Darstellung der Ergebnisse)
- Dr. Daniel Rohe (Jülich Supercomputing Centre) (Organisation und Diskussion)