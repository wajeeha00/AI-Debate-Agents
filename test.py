# test.py
from graph.build_graph import build_debate_graph

app = build_debate_graph()

initial_state = {
    "topic": "Should AI replace software engineers?",
    "transcript": [],
    "round_count": 0,
    "max_rounds": 3,
    "verdict": ""
}

result = app.invoke(initial_state)

print("\n=== DEBATE TRANSCRIPT ===\n")
for entry in result["transcript"]:
    print(f"{entry['speaker']}: {entry['message']}\n")

print("=== JUDGE VERDICT ===\n")
print(result["verdict"])