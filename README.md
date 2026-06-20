# ⚔️ AI Debate Arena

Two AI agents argue opposite sides of any topic in real time — a third AI judges the debate and delivers a verdict. Built with **LangGraph** to demonstrate stateful, cyclical multi-agent orchestration.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)

---

## ✨ Features
- 🟢 **Optimist agent** — argues FOR the topic
- 🔴 **Skeptic agent** — argues AGAINST the topic
- ⚖️ **Judge agent** — reads the full debate, gives a balanced verdict
- 🔁 Configurable number of rounds (1–5)
- 💬 Live chat-style UI — watch the debate unfold turn by turn

---

## 🏗️ Project Structure
```
ai-debate-agents/
├── graph/
│   ├── state.py        # Shared state (TypedDict) across all nodes
│   ├── nodes.py         # Optimist, Skeptic, and Judge agent logic
│   └── build_graph.py   # Wires nodes into a LangGraph StateGraph
├── app.py                # Streamlit chat UI
├── requirements.txt
└── .env                  # API keys (never commit!)
```

---

## 🧠 Why LangGraph (not just LangChain)

LangChain chains run linearly: `A → B → C`. This project needed **agents that loop and argue back and forth** until a condition is met — that requires a graph with cycles and conditional routing, which is exactly what LangGraph is built for.

```
START → Optimist → Skeptic → (continue debating? loop back : go to Judge) → END
```

| LangGraph Concept | Used For |
|---|---|
| `StateGraph` | Shared state (topic, transcript, round count) across all agents |
| `add_node` | Each agent (Optimist, Skeptic, Judge) is a graph node |
| `add_conditional_edges` | Decides whether to keep debating or call the judge |
| `app.stream()` | Streams each agent's turn live to the UI, instead of waiting for the full result |

---

## 🚀 Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/ai-debate-agents.git
cd ai-debate-agents
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Add your key to `.env`:
```
GROQ_API_KEY=your_key_here
```

Run:
```bash
streamlit run app.py
```

Get a free Groq API key: [console.groq.com](https://console.groq.com)

---

## ⚠️ Limitations
- Agents argue from reasoning only — no web search, so claims aren't fact-checked
- Very high round counts can make agents repeat similar points

---

*Built with LangGraph · Groq · Streamlit*
