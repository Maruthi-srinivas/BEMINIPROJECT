"""Illustrative Raft term and log entry checks (not a full implementation)."""
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LogEntry:
    term: int
    command: str

@dataclass
class Server:
    current_term: int = 0
    voted_for: Optional[int] = None
    log: List[LogEntry] = field(default_factory=list)

    def last_log_index(self) -> int:
        return len(self.log)

    def last_log_term(self) -> int:
        return self.log[-1].term if self.log else 0

    def can_vote_for(self, candidate_id: int, candidate_term: int, candidate_last_index: int, candidate_last_term: int) -> bool:
        if candidate_term < self.current_term:
            return False
        if self.voted_for not in (None, candidate_id):
            return False
        # Up-to-date: higher term in last entry, or same term with longer log.
        up_to_date = (candidate_last_term, candidate_last_index) >= (self.last_log_term(), self.last_log_index())
        return up_to_date

if __name__ == "__main__":
    s = Server(log=[LogEntry(1, "set x=1")])
    assert s.can_vote_for(2, 2, 1, 1)
    print("ok", s.last_log_index())