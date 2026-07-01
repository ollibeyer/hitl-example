import json
import openai

# Ollama exposes an OpenAI-compatible API on localhost:11434
OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_MODEL = "qwen2.5:7b-instruct"  # any Ollama model that supports tool use

client = openai.OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

# --- Tool Definition ---

def execute_bank_transfer(amount: float, recipient: str) -> str:
    """Simulated bank transfer tool."""
    print(f"\n💸 [TOOL] Überweisung ausgeführt: {amount} EUR → {recipient}")
    return f"Überweisung von {amount} EUR an {recipient} erfolgreich durchgeführt."


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_bank_transfer",
            "description": "Führt eine Banküberweisung an einen Empfänger aus.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Betrag in Euro",
                    },
                    "recipient": {
                        "type": "string",
                        "description": "Name des Empfängers",
                    },
                },
                "required": ["amount", "recipient"],
            },
        },
    }
]

# --- Human-in-the-Loop Approval ---

def request_human_approval(tool_name: str, arguments: dict) -> bool:
    """Pauses execution and asks the human for explicit approval."""
    print("\n" + "=" * 50)
    print("⚠️  HUMAN-IN-THE-LOOP: Tool-Aufruf erfordert Freigabe")
    print("=" * 50)
    print(f"  Tool:      {tool_name}")
    for key, value in arguments.items():
        print(f"  {key:<12} {value}")
    print("=" * 50)

    answer = input("Möchten Sie diese Aktion freigeben? (ja/nein): ").strip().lower()
    return answer == "ja"


# --- Main Agent Loop ---

def run_agent(user_message: str) -> None:
    messages = [
        {
            "role": "system",
            "content": "Du bist ein hilfreicher Bankassistent. Nutze das Tool execute_bank_transfer, wenn der Nutzer eine Überweisung wünscht.",
        },
        {"role": "user", "content": user_message},
    ]

    print(f"\n🧑 Nutzer: {user_message}\n")

    while True:
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # No tool call → final answer
        if not message.tool_calls:
            print(f"\n🤖 Assistent: {message.content}")
            break

        # Process each tool call
        messages.append(message)  # add assistant message with tool_calls

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            approved = request_human_approval(name, arguments)

            if approved:
                result = execute_bank_transfer(**arguments)
            else:
                result = "Fehler: Aktion vom Administrator abgelehnt."
                print("\n❌ Aktion abgelehnt.")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )


if __name__ == "__main__":
    run_agent("Überweise 500 Euro an Max Mustermann")
