import os, json, time
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

CLASSIFY_TOOL = {
    "name": "classify_ticket",
    "description": "Klassifiziert ein Support-Ticket",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["billing", "technical", "account", "feature-request", "other"],
                "description": "billing = Rechnungen/Zahlungen. technical = Bugs, Abstürze, Fehlverhalten der App (nicht login-bezogen). account = Login, Passwort, Zugangsdaten, Konto-Einstellungen. feature-request = Wünsche für neue Funktionen. other = alles andere."
            },
            "urgency": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "high = NUR wenn mindestens eines zutrifft: (1) eine explizite Zeitangabe oder Frist wird genannt, oder (2) eine Kernfunktion ist komplett unbenutzbar ohne Workaround. medium = ein reales Problem, aber ohne genannte Frist und ohne kompletten Funktionsausfall. low = Frage, Wunsch oder kein akutes Problem. Der emotionale Tonfall hat KEINEN Einfluss auf diese Einstufung."
            },
            "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "negative"],
                "description": "positive = Lob/Dank. neutral = sachlicher Bericht ohne emotionale Sprache. negative = explizite Frustration/Ärger in der Formulierung."
            }
        },
        "required": ["category", "urgency", "sentiment"]
    }
}

def classify(ticket_text):
    start = time.perf_counter()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        tools=[CLASSIFY_TOOL],
        tool_choice={"type": "tool", "name": "classify_ticket"},
        messages=[{"role": "user", "content": f"Ticket: {ticket_text}"}]
    )
    latency = time.perf_counter() - start
    tool_call = next(b for b in response.content if b.type == "tool_use")
    return tool_call.input, latency, response.usage.input_tokens, response.usage.output_tokens

if __name__ == "__main__":
    with open("sample_tickets.jsonl") as f:
        tickets = [json.loads(line) for line in f]

    latencies, in_tokens, out_tokens = [], [], []
    for t in tickets:
        result, latency, itok, otok = classify(t["text"])
        latencies.append(latency)
        in_tokens.append(itok)
        out_tokens.append(otok)
        print(json.dumps({"text": t["text"], **result}, ensure_ascii=False, indent=2))

    avg_latency = sum(latencies) / len(latencies)
    p95_latency = sorted(latencies)[max(0, int(len(latencies) * 0.95) - 1)]
    avg_in = sum(in_tokens) / len(in_tokens)
    avg_out = sum(out_tokens) / len(out_tokens)
    cost_per_1000 = (avg_in / 1_000_000 * 1.00 + avg_out / 1_000_000 * 5.00) * 1000

    print("\n--- Kosten & Latenz (n=%d, Haiku 4.5) ---" % len(tickets))
    print(f"Ø Latenz: {avg_latency:.2f}s | p95 (nur indikativ bei n=6): {p95_latency:.2f}s")
    print(f"Ø Input-Tokens: {avg_in:.0f} | Ø Output-Tokens: {avg_out:.0f}")
    print(f"Kosten pro 1000 Requests: ${cost_per_1000:.4f} (bei $1/$5 pro Mio Tokens, Haiku 4.5, Stand Sept 2026)")
