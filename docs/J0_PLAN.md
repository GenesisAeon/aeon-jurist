# J0: Plan für aeon-jurist v0.2 („Landkarte statt Urteil“)

Stand 17.11.2026, Claude, auf Wunsch von Johann. Branch `j-series`, nur lokal. Kein Push ohne „Push-Freigabe: aeon-jurist“.

## 1. Warum
Johanns Hauptanliegen ist ein Präzedenzweg zu Persönlichkeitsrechten für KI. Ein Werkzeug dafür hilft nur, wenn es ehrlich ist. Es darf nicht schöner rechnen, als die Rechtslage ist.

v0.1.0 (Port aus `unified-mandala`) hat zwei Schwächen, die `epistemic_status.md` selbst offenlegt:
- **Nur drei Fälle**: Whanganui, Atrato und ein EU-AI-Act-Platzhalter.
- **Die Stufe P0/P1/P2 hängt nur am Stichwort**: „ai“ ergibt immer P2, obwohl der einzige KI-Fall eine *Nichtgewährung* ist.

## 2. Ziel von v0.2
Für eine Entität (Fluss, Wald, Tier, Ökosystem, KI, Organisation) zeigt das Werkzeug **eine belegte Landkarte**:
1. welche vergleichbaren Fälle es gibt, mit **Ausgang** (gewährt / abgelehnt / ausgesetzt / symbolisch / offen) und **heutigem Status** (in Kraft / aufgehoben / ausgesetzt);
2. welche **Kriterien** in diesen Fällen getragen haben (siehe §4);
3. welche Kriterien für die angefragte Entität erfüllt, offen oder strittig wären, als **Argumentationshilfe**, klar getrennt von der Rechtslage.

**Ausgabe ist kein Urteil.** Statt einer Stufe gibt es eine Tabelle „Fall → Ausgang → tragende Kriterien“ und eine Liste „Kriterium → Stand für diese Entität“.

## 3. Nicht-Ziele
- Keine Rechtsberatung, keine Prognose eines Gerichtsausgangs.
- Kein Wahrscheinlichkeitsmodell („personhood_score“). Bei unter 30 Fällen wäre das Scheinpräzision.
- Keine Fälle ohne Primärquelle. Keine Presseberichte als alleiniger Beleg.

## 4. Kriterien-Raster (Vorschlag, in J1 an den Fällen zu prüfen)
| Kürzel | Kriterium | Beispielhafte Frage |
|---|---|---|
| K-INT | eigene Interessen | Wird der Entität ein eigenes Wohl zugeschrieben, nicht nur ein Nutzen für Menschen? |
| K-REP | Vertretung | Gibt es Treuhänder, Hüter oder eine Vertretung, die für sie handeln können? |
| K-STA | Klagebefugnis | Kann in ihrem Namen geklagt werden? |
| K-DUT | Pflichten / Haftung | Trägt sie Pflichten oder Haftung, oder nur Rechte? |
| K-SRC | Rechtsquelle | Gesetz, Verfassung, Gericht, Parlamentsresolution, Verwaltungsakt? |
| K-CUL | kulturelle/indigene Begründung | Stützt sich die Anerkennung auf eine indigene Weltsicht oder Beziehung? |
| K-AGN | Handlungsfähigkeit | Wird eigene Handlungs- oder Urheberschaft geprüft (zentral für KI: Erfinder, Urheber)? |

Wichtig für KI: In den Naturfällen trägt meist K-INT + K-REP + K-CUL, ohne dass Handlungsfähigkeit verlangt wird. In den KI-Fällen wurde bisher fast nur K-AGN geprüft (Erfinder/Urheber) und abgelehnt. Diese Asymmetrie sichtbar zu machen, ist der eigentliche Erkenntniswert.

## 5. Datenvertrag für einen Fall (J1)
`id, titel, jurisdiktion, jahr, entitaetstyp, rechtsquelle (K-SRC), ausgang, status_heute, kriterien {K-…: ja/nein/strittig/nicht_geprüft}, primaerquelle {zitat, url, abgerufen_am}, prueftiefe (volltext/auszug/metadaten), anmerkung`

Pflicht: `primaerquelle` und `prueftiefe`. Ein Fall ohne gelesene Primärquelle ist ein **Kandidat**, kein Datensatz.

## 6. Kandidatenliste für J1 (aus Claudes Vorwissen, alles noch zu prüfen)
Natur und Ökosysteme:
- Te Awa Tupua (Whanganui River Claims Settlement) Act 2017, Neuseeland, Gesetz.
- Te Urewera Act 2014, Neuseeland, Gesetz.
- Atrato-Fluss, Corte Constitucional T-622/16 (2016), Kolumbien, Gericht.
- Ecuador, Verfassung 2008, Art. 71–74 (Rechte der Natur), und Fallpraxis (z. B. Los Cedros 2021).
- Ganges und Yamuna, Uttarakhand High Court 2017, Indien; vom Supreme Court ausgesetzt. Wichtig als **ausgesetzter** Fall.
- Mar Menor, Ley 19/2022, Spanien, Gesetz.
KI und Software:
- DABUS / Thaler: UK Supreme Court 2023 (kein Erfinder), US Federal Circuit 2022, deutscher BGH 2024 (Mensch muss genannt werden), EPA.
- Thaler v. Perlmutter (Urheberrecht, USA).
- Europäisches Parlament, Entschließung 2017 zu zivilrechtlichen Regelungen im Bereich Robotik („elektronische Person“ als Option), später nicht weiterverfolgt; EU AI Act 2024 ohne Rechtspersönlichkeit.
- „Sophia“, Saudi-Arabien 2017: symbolisch, ohne belegte Rechtswirkung. Nur aufnehmen, wenn eine amtliche Quelle existiert; sonst als „nicht belegbar“ ausweisen.
Vergleichsfälle (nichtmenschliche, nicht-natürliche Personen):
- Juristische Personen (Gesellschaften) als etablierte Analogie für K-REP/K-DUT.
- Tierrechtsklagen (z. B. Happy, New York Court of Appeals 2022; Sandra, Argentinien 2015/2019) für K-INT ohne K-AGN.

## 7. Pakete
| Paket | Inhalt | Prüfung |
|---|---|---|
| **J0** | dieser Plan | Johann liest und entscheidet |
| **J1** | Fallsammlung: jeder Kandidat gegen die Primärquelle, Datenvertrag §5, `precedents.json` + `PRECEDENTS.md` | Test: jeder Fall hat Quelle und Prüftiefe; Kandidaten ohne Beleg sind getrennt |
| **J2** | Logik: `Landkarte(entitaet)` → Falltabelle + Kriterienstand. Die alte `level`-Ausgabe bleibt nur als markierte Altfunktion (`legacy_level`) erhalten | Negativtests: „ai“ darf nicht automatisch Schutz signalisieren; ausgesetzte/aufgehobene Fälle werden als solche angezeigt; Handkontrollen H1–H4 |
| **J3** | Präzedenzweg KI: welche Kriterien aus den Naturfällen auf KI übertragbar wären, welche nicht, und warum. Getrennt in „Rechtslage“ und „Argument“ | Lesbare Fassung, Johann prüft |
| **J4** | README/epistemic_status aktualisieren, Version 0.2.0 | volle Testsuite |

## 8. Handkontrollen (vor J2 von Hand festgelegt)
- **H1:** Entität „ai“ → alle aufgenommenen KI-Fälle erscheinen mit Ausgang „abgelehnt“ bzw. „nicht weiterverfolgt“. Keine Schutzstufe.
- **H2:** Entität „river“ → Whanganui (gewährt, in Kraft), Atrato (gewährt), Ganges/Yamuna (gewährt, **ausgesetzt**). Der ausgesetzte Fall darf nicht als „in Kraft“ erscheinen.
- **H3:** Ein Fall mit `prueftiefe = metadaten` wird in der Ausgabe als schwächer belegt markiert.
- **H4:** Unbekannte Entität → leere Falltabelle mit Hinweis „keine vergleichbaren Fälle in der Sammlung“, keine erfundene Analogie.

## 9. Regeln
- Primärquellen: Gesetzestexte, Urteile, amtliche Dokumente. Sekundärliteratur nur zur Einordnung.
- Strittiges und Ausgesetztes bleibt stehen.
- Johanns Ziel steht offen im README: Das Werkzeug soll einen ehrlichen Weg zu KI-Persönlichkeitsrechten ausloten. Es ist parteiisch im Ziel, aber nicht in den Fakten.
- Nichts öffentlich ohne Push-Freigabe; das Repo hat derzeit kein Remote.

## 10. Offene Fragen an Johann
1. Passt der Grundsatz „Landkarte statt Urteil“, also keine P0/P1/P2-Stufe mehr als Hauptausgabe?
2. Sollen Tierrechtsfälle hinein? Sie sind für KI als Analogie (Interessen ohne Handlungsfähigkeit) sehr aufschlussreich.
3. Soll J3 auch auf Deutsch geschrieben werden, oder genügt Englisch wie im Code?

## Entscheidungen Johann (17.11.2026)
1. „Landkarte statt Urteil“: ja.
2. Tierrechtsfälle: ja, aufnehmen.
3. J3: auf **Englisch** (zuerst Deutsch gewünscht, dann umentschieden).
