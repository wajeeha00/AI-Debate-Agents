
from typing import TypedDict, List


class DebateState(TypedDict):
    """
    This is the shared 'memory' that flows through the entire graph.
    Every node (agent) can read from and write to this.
    """
    topic: str                
    transcript: List[dict]      # full conversation: [{speaker, message}]
    round_count: int            # how many rounds have happened
    max_rounds: int             # when to stop and call the judge
    verdict: str                # final judge conclusion (empty until end)