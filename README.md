# Human-in-the-Loop Demo

Ein minimales Python-Skript, das das **Human-in-the-Loop (HITL)**-Konzept für KI-Agenten demonstriert – ohne schweres Framework, nur mit purem Python und der OpenAI-Bibliothek gegen eine lokale **Ollama**-Instanz.

## Konzept

KI-Agenten können über *Function Calling* eigenständig Tools aufrufen – etwa eine Banküberweisung auslösen. Das ist mächtig, aber gefährlich. HITL bedeutet: **Bevor ein kritisches Tool ausgeführt wird, hält das System an und fragt einen Menschen um Erlaubnis.**

```
Nutzer → LLM erkennt Tool-Aufruf → ⚠️ Pause → Mensch genehmigt/lehnt ab → Tool wird ausgeführt oder abgebrochen
```

## Ablauf

1. Der Nutzer schickt: `"Überweise 500 Euro an Max Mustermann"`
2. Das LLM erkennt, dass `execute_bank_transfer` aufgerufen werden muss
3. Das Skript **pausiert** und zeigt die Parameter im Terminal an:
   ```
   ==================================================
   ⚠️  HUMAN-IN-THE-LOOP: Tool-Aufruf erfordert Freigabe
   ==================================================
     Tool:      execute_bank_transfer
     amount       500.0
     recipient    Max Mustermann
   ==================================================
   Möchten Sie diese Aktion freigeben? (ja/nein):
   ```
4. Bei **`ja`**: Tool wird ausgeführt, Ergebnis ans LLM zurückgegeben
5. Bei **`nein`**: LLM erhält `"Aktion vom Administrator abgelehnt"` und informiert den Nutzer

## Voraussetzungen

- [Ollama](https://ollama.com) installiert und gestartet
- [uv](https://docs.astral.sh/uv/) installiert

## Setup & Ausführen

```bash
# Modell herunterladen (einmalig)
ollama pull qwen2.5:7b-instruct

# Abhängigkeiten installieren
uv sync

# Skript starten
uv run python hitl_demo.py
```

## Modell wechseln

In `hitl_demo.py` die Variable `OLLAMA_MODEL` anpassen. Empfohlene Modelle mit Tool-Use-Unterstützung:

| Modell | Größe |
|---|---|
| `qwen2.5:7b-instruct` | 7B (Standard) |
| `llama3.1:8b` | 8B |
| `mistral-nemo` | 12B |
