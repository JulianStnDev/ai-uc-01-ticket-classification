# Ticket-Klassifikation (Structured Output)

## Problem
Support-Teams bekommen Tickets als Freitext. Ohne Struktur lässt sich weder
priorisieren noch auswerten, welche Kategorien/Dringlichkeiten überwiegen.
Ziel: Freitext zuverlässig in ein festes JSON-Format bringen (Kategorie,
Dringlichkeit, Stimmung).

## PM-Entscheidung
Erste Version nutzte reine Enum-Werte ohne Definition — das Modell kategorisierte
inhaltlich identische Login-Probleme uneinheitlich und stufte fast alles als
"high" ein, sobald der Ton frustriert klang. Statt mit Few-Shot-Beispielen zu
arbeiten (mehr Tokens, weniger generalisierbar), habe ich jedem Enum-Wert eine
explizite Bedingung im Tool-Schema gegeben — inklusive der Einschränkung, dass
Tonfall keine Rolle für die Dringlichkeit spielen darf. Details: docs/decisions.md.

## Architekturskizze
Freitext-Ticket → Claude Haiku 4.5 mit erzwungenem Tool-Call (tool_choice) →
validiertes JSON (category, urgency, sentiment). Kein Framework, direkte
Nutzung des anthropic-Python-Pakets.

## Evaluationsergebnisse
6 synthetische Test-Tickets, 3 Iterationen:
1. Enums ohne Beschreibung: Kategorie-Inkonsistenz bei Login-Themen, Urgency-Inflation (4/6 "high")
2. + Enum-Beschreibungen: Kategorien konsistent, Urgency noch ton-verzerrt
3. + ton-unabhängige Urgency-Definition: alle 6 Klassifikationen plausibel

## Kosten & Latenz
- Kosten pro 1000 Requests: $1.37 (Haiku 4.5, $1/$5 pro Mio Tokens, Stand Sept 2026)
- Ø Latenz: 0.88s, p95: 0.96s (nur indikativ, n=6)
- Ø Input-Tokens: 1030, Ø Output-Tokens: 68

## Learnings
Enum-Werte allein reichen nicht — ohne Definition interpretiert das Modell sie
uneinheitlich. Der größte Hebel war nicht ein anderes Modell oder ein längerer
Prompt, sondern präzise Bedingungen direkt im Tool-Schema. Ton und Dringlichkeit
lassen sich leicht verwechseln, wenn man es nicht explizit ausschließt.

## Was ich anders machen würde
Mit nur 6 Testfällen lässt sich Kalibrierung nicht wirklich absichern — das
gehört strukturell in UC2 (Evaluation Harness) mit einem größeren Goldset statt
Stichproben-Eyeballing.
