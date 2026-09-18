# Entscheidungen

## 2026-09-18: Enum-Definitionen für Klassifikations-Schema

Kontext: Erster Testlauf mit reinen Enum-Werten (ohne Beschreibungen) zeigte zwei
Probleme: (1) inhaltlich gleiche Login-Probleme landeten je nach Formulierung in
unterschiedlichen Kategorien (technical vs. account), (2) urgency wurde von
frustriertem Tonfall beeinflusst statt von echtem Zeitdruck/Funktionsausfall
(4 von 6 Tickets "high", obwohl nur 1 eine echte Deadline hatte).

Optionen: (a) Enums ohne Beschreibung lassen und Prompt-Beispiele hinzufügen,
(b) jedem Enum-Wert eine klare Bedingung in der description geben, (c) auf
Few-Shot-Beispiele im Prompt statt Schema-Beschreibungen setzen.

Entscheidung: (b) — description pro Enum-Wert, in zwei Iterationen verschärft.
Erste Runde behob die Kategorie-Inkonsistenz sofort. Urgency blieb ton-verzerrt,
bis die description explizit ausschloss, dass Tonfall zählt.

Begründung: Beschreibungen im Schema sind deterministischer und günstiger als
Few-Shot-Beispiele (weniger Tokens pro Request) und skalieren besser auf neue,
ungesehene Tickets als Einzelfall-Regeln.

## 2026-09-18: Status-Vokabular für meta.json

Kontext: meta.json legt "status": "planned" fest, ohne definierte erlaubte Werte —
das driftet über mehrere Repos auseinander (planned/in-progress/wip/...).

Optionen: (a) einfach: planned → active → done, (b) zusätzlich mit
parked/abandoned für verworfene Use Cases, (c) feiner: research →
building → evaluating → shipped.

Entscheidung: (a) — planned, active, done. Zusätzlich in CLAUDE.md verankert.

Begründung: Bei einem Solo-Portfolio mit meist einem aktiven Repo lohnt sich
keine feinere Staffelung. CLAUDE.md-Verankerung, damit der Agent das Vokabular
bei jedem neuen Repo automatisch mitliest statt dass ich mich erinnern muss.
