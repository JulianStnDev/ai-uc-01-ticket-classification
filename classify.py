import os, json
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
                "description": "billing = Rechnungen/Zahlungen. technical = Bugs, Abstürze, Fehlverhalten der App (nicht login-bezogen). account = Login, Passwort, Zugangsdaten, Konto-Einstellungen — unabhängig davon ob die Ursache ein Update oder ein kaputter Link ist. feature-request = Wünsche für neue Funktionen. other = alles andere."
            },
            "urgency": {
                "type": "string",
                "enum": ["low", "medium", "high"],
                "description": "high = explizite Dringlichkeit/Deadline genannt, oder Totalausfall ohne Workaround. medium = störendes Problem, aber kein genannter Zeitdruck. low = Fragen, Wünsche, kein akutes Problem."
            },
            "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "negative"],
                "description": "positive = Lob/Dank. neutral = sachlicher Bericht ohne emotionale Sprache, auch wenn ein Problem beschrieben wird. negative = explizite Frustration/Ärger in der Formulierung."
            }
        },
        "required": ["category", "urgency", "sentiment"]
    }
}

def classify(ticket_text):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        tools=[CLASSIFY_TOOL],
        tool_choice={"type": "tool", "name": "classify_ticket"},
        messages=[{"role": "user", "content": f"Ticket: {ticket_text}"}]
    )
    tool_call = next(b for b in response.content if b.type == "tool_use")
    return tool_call.input

if __name__ == "__main__":
    with open("sample_tickets.jsonl") as f:
        tickets = [json.loads(line) for line in f]
    for t in tickets:
        result = classify(t["text"])
        print(json.dumps({"text": t["text"], **result}, ensure_ascii=False, indent=2))
