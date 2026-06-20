from langgraph.graph import StateGraph, END
from graph.state import DebateState
from graph.nodes import optimist_node, skeptic_node, judge_node


def should_continue_debate(state: DebateState) -> str:
    """
    This is a CONDITIONAL EDGE function.
    LangGraph calls this after the skeptic speaks to decide:
    'loop back to optimist' OR 'go to judge'
    
    This is the core power of LangGraph — dynamic routing based on state.
    """
    if state["round_count"] >= state["max_rounds"]:
        return "judge"
    else:
        return "continue"


def build_debate_graph():
    """
    Builds and compiles the LangGraph state machine.
    """
    # 1. Create the graph, tell it what State shape it manages
    workflow = StateGraph(DebateState)

    # 2. Add nodes — each node is a function we wrote in nodes.py
    workflow.add_node("optimist", optimist_node)
    workflow.add_node("skeptic", skeptic_node)
    workflow.add_node("judge", judge_node)

    # 3. Set entry point — where the graph starts
    workflow.set_entry_point("optimist")

    # 4. Simple edge: after optimist speaks, skeptic always speaks next
    workflow.add_edge("optimist", "skeptic")

    # 5. CONDITIONAL edge: after skeptic speaks, decide what's next
    workflow.add_conditional_edges(
        "skeptic",                    # from this node
        should_continue_debate,       # call this function to decide
        {
            "continue": "optimist",   # loop back — debate continues
            "judge": "judge"          # enough rounds — go to judge
        }
    )

    # 6. After judge gives verdict, graph ends
    workflow.add_edge("judge", END)

    # 7. Compile into a runnable graph
    app = workflow.compile()

    return app