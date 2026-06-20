from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
from graph.state import DebateState

load_dotenv()

llm = ChatGroq(model = "llama-3.3-70b-versatile", temperature = 0.7)


def format_transcript(transcript: list) -> str:
    if not transcript:
        return "(Debate just started)"
    lines = []
    for entry in transcript:
        lines.append(f"{entry['speaker']} : {entry['message']}")
    
    return "\n".join(lines)

def optimist_node(state: DebateState) -> DebateState:
    """
    Agent A — argues IN FAVOR of the topic.
    Reads the full transcript so far, responds to the skeptic's last point.
    """
    transcript_text = format_transcript(state["transcript"])

    messages = [
        SystemMessage(content=f"""You are 'The Optimist' in a formal debate.
        You strongly argue IN FAVOR of the topic: "{state['topic']}"
        
        Rules:
        - Keep responses to 2-3 sentences, punchy and persuasive
        - Directly respond to the Skeptic's previous point if one exists
        - Never agree with the opposing side
        - Use logic, not just opinion
        """),
        HumanMessage(content=f"Debate so far:\n{transcript_text}\n\nGive your next argument.")
    ]

    response = llm.invoke(messages)

    # Append to transcript (don't overwrite — we're building history)
    new_entry = {"speaker": "🟢 Optimist", "message": response.content}
    
    return {
        "transcript": state["transcript"] + [new_entry]
    }

def skeptic_node(state: DebateState) -> DebateState:
    """
    Agent B — argues AGAINST the topic.
    """
    transcript_text = format_transcript(state["transcript"])

    messages = [
        SystemMessage(content=f"""You are 'The Skeptic' in a formal debate.
        You strongly argue AGAINST the topic: "{state['topic']}"
        
        Rules:
        - Keep responses to 2-3 sentences, punchy and critical
        - Directly counter the Optimist's previous point
        - Never agree with the opposing side
        - Use logic and point out risks/flaws
        """),
        HumanMessage(content=f"Debate so far:\n{transcript_text}\n\nGive your next counter-argument.")
    ]

    response = llm.invoke(messages)

    new_entry = {"speaker": "🔴 Skeptic", "message": response.content}

    return {
        "transcript": state["transcript"] + [new_entry],
        "round_count": state["round_count"] + 1   # one full round = both spoke
    }


def judge_node(state: DebateState) -> DebateState:
    """
    Judge Agent — reads entire debate, gives a balanced final verdict.
    This only runs ONCE, after max_rounds is reached.
    """
    transcript_text = format_transcript(state["transcript"])

    messages = [
        SystemMessage(content="""You are an impartial Judge AI.
        Read the full debate transcript and provide a balanced verdict.
        
        Structure your response as:
        - ⚖️ Strongest point from Optimist
        - ⚖️ Strongest point from Skeptic  
        - 🏁 Final Verdict (which side had stronger reasoning, and why)
        
        Be fair and analytical, not biased toward either side.
        """),
        HumanMessage(content=f"Full debate transcript:\n{transcript_text}\n\nGive your verdict.")
    ]

    response = llm.invoke(messages)

    return {
        "verdict": response.content
    }