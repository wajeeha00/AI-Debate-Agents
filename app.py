import streamlit as st
from graph.build_graph import build_debate_graph

st.set_page_config(
    page_title="AI Debate Arena",
    page_icon="⚔️",
    layout="centered"
)

st.title("⚔️ AI Debate Arena")
st.markdown("*Two AI agents argue. A third AI judges. Built with LangGraph.*")
st.divider()

# --- Sidebar settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    max_rounds = st.slider("Number of rounds", min_value=1, max_value=5, value=3)
    st.markdown("---")
    st.markdown("**Agents:**")
    st.markdown("🟢 Optimist — argues FOR")
    st.markdown("🔴 Skeptic — argues AGAINST")
    st.markdown("⚖️ Judge — final verdict")

# --- Topic input ---
topic = st.text_input(
    "Enter a debate topic:",
    placeholder="e.g. Should AI replace software engineers?"
)

start_button = st.button("🚀 Start Debate", type="primary", use_container_width=True)

# --- Run debate ---
if start_button:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        app = build_debate_graph()

        initial_state = {
            "topic": topic,
            "transcript": [],
            "round_count": 0,
            "max_rounds": max_rounds,
            "verdict": ""
        }

        st.subheader(f"📋 Topic: {topic}")
        st.markdown("---")

        chat_container = st.container()
        verdict_text = ""

        with st.spinner("Agents are debating..."):
            # app.stream() runs the graph node-by-node, yielding state
            # updates as each node finishes. This lets us render messages
            # live instead of waiting for the entire graph to finish.
            for step in app.stream(initial_state):
                node_name = list(step.keys())[0]
                node_output = step[node_name]

                # Show new debate messages as they arrive
                if node_output.get("transcript"):
                    latest_message = node_output["transcript"][-1]

                    with chat_container:
                        role = "assistant" if "Optimist" in latest_message["speaker"] else "user"
                        with st.chat_message(role):
                            st.markdown(f"**{latest_message['speaker']}**")
                            st.markdown(latest_message["message"])

                # Capture verdict when judge node runs
                if node_output.get("verdict"):
                    verdict_text = node_output["verdict"]

        st.markdown("---")
        st.subheader("⚖️ Final Verdict")
        st.info(verdict_text)
        st.success("Debate complete!")