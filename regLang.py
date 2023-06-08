from __future__ import annotations
from functools import reduce
from utils import powerset


class DFA:
    def __init__(self, Sigma: set[str], Q: set[str], transitions: dict[tuple[str, str], str], q0: str, F: set[str]):
        self.__Sigma = Sigma
        self.__Q = Q
        self.__transitions = transitions
        self.__q0 = q0
        self.__F = F
        self.__validate()

    def __validate(self):
        # valid stating state
        if self.__q0 not in self.__Q:
            raise ValueError(f"Starting state q0={self.__q0} must be in states Q={self.__Q}.")

        # valid accepting states
        if not (self.__F).issubset(self.__Q):
            raise ValueError(f"Accepting states F={self.__F} must be a subset of states Q={self.__Q}.")

        # no undefined transitions
        for q in self.__Q:
            for a in self.__Sigma:
                if (q, a) not in self.__transitions.keys():
                    raise ValueError(f"Transition for q={q} and a={a} is undefined.")

        # No invalid transition
        for ((q, a), q_) in self.__transitions.items():
            if (a not in self.__Sigma) or (q not in self.__Q) or (q_ not in self.__Q):
                raise ValueError(f"Invalid transition ((q={a}, a={a}), q'={q_}). States or symbol unknown.")

    def simulate(self, q: str, w: str) -> str:
        if not set(w).issubset(self.__Sigma):
            raise ValueError(f"Word w={w} contains symbols that are not in alphabet Sigma={self.__Sigma}.")
        for a in w:
            q = self.__transitions[(q, a)]
        return q

    def accepts(self, w: str) -> bool:
        q = self.simulate(self.__q0, w)
        return q in self.__F

    def to_NFA(self) -> NFA:
        Sigma = self.__Sigma
        Q = self.__Q
        transitions = dict(((q1, a), {q2}) for ((q1, a), q2) in self.__transitions.items())
        q0 = self.__q0
        F = self.__F
        return NFA(Sigma, Q, transitions, q0, F)

    def to_E_NFA(self) -> E_NFA:
        nfa = self.to_NFA()
        e_nfa = nfa.to_E_NFA()
        return e_nfa


class NFA:
    def __init__(self, Sigma: set[str], Q: set[str], transitions: dict[tuple[str, str], set(str)], q0: str, F: set[str]):
        self.__Sigma = Sigma
        self.__Q = Q
        self.__transitions = transitions
        self.__q0 = q0
        self.__F = F
        self.__validate()

    def __validate(self):
        # valid stating state
        if self.__q0 not in self.__Q:
            raise ValueError(f"Starting state q0={self.__q0} must be in states Q={self.__Q}.")

        # valid accepting states
        if not (self.__F).issubset(self.__Q):
            raise ValueError(f"Accepting states F={self.__F} must be a subset of states Q={self.__Q}.")

        # No invalid transition
        for ((q, a), q_) in self.__transitions.items():
            if (a not in self.__Sigma) or (q not in self.__Q) or (len(q_ - self.__Q) >= 1):
                raise ValueError(f"Invalid transition ((q={a}, a={a}), q'={q_}. States or symbol unknown.")

    def simulate(self, qs: set[str], w: str) -> set[str]:
        if not set(w).issubset(self.__Sigma):
            raise ValueError(f"w = {w} contains symbols that are not in alphabet {self.__Sigma}.")
        if not w:
            return qs
        for a in w:
            next_qs = set()
            for q in qs:
                if (q, a) not in self.__transitions.keys():
                    continue
                next_qs.update(self.__transitions[(q, a)])
            qs = next_qs.copy()
        return qs

    def accepts(self, w: str) -> bool:
        qs = self.simulate({self.__q0}, w)
        return len(qs & self.__F) >= 1

    def to_DFA(self) -> DFA:
        Sigma = self.__Sigma
        Q = powerset(self.__Q)
        transitions = dict()
        for q in Q:
            for a in Sigma:
                transitions[(q, a)] = frozenset()
                for q_ in q:
                    qs = self.__transitions.get((q_, a))
                    transitions[(q, a)] |= frozenset(qs) if qs else frozenset()

        q0 = frozenset(self.__q0)
        F = set(q for q in Q if len(q & self.__F) >= 1)
        return DFA(Sigma, Q, transitions, q0, F)

    def to_E_NFA(self) -> E_NFA:
        Sigma = self.__Sigma
        Q = self.__Q
        transitions = self.__transitions
        q0 = self.__q0
        F = self.__F
        return E_NFA(Sigma, Q, transitions, q0, F)


class E_NFA:
    def __init__(self, Sigma: set[str], Q: set[str], transitions: dict[tuple[str, str], set(str)], q0: str, F: set[str]):
        self.__Sigma = Sigma
        self.__Q = Q
        self.__transitions = transitions
        self.__q0 = q0
        self.__F = F
        self.__epsilon_reachable = self.__get_epsilon_reachable()
        self.__epsilon_reachable_reversed = dict((q, set(q_ for (q_, qs) in self.__epsilon_reachable.items() if q in qs)) for q in self.__Q)
        self.__validate()

    def __validate(self):
        # valid stating state
        if self.__q0 not in self.__Q:
            raise ValueError(f"Starting state q0={self.__q0} must be in states Q={self.__Q}.")

        # valid accepting states
        if not (self.__F).issubset(self.__Q):
            raise ValueError(f"Accepting states F={self.__F} must be a subset of states Q={self.__Q}.")

        # No invalid transition
        for ((q, a), q_) in self.__transitions.items():
            if (a not in (self.__Sigma | {""})) or (q not in self.__Q) or (len(q_ - self.__Q) >= 1):
                raise ValueError(f"Invalid transition ((q={a}, a={a}), q'={q_}. States or symbol unknown.")

    def __get_epsilon_reachable(self) -> dict[str, str]:
        e_reachable = dict((q, {q}) for q in self.__Q)

        changes = True
        while changes:
            changes = False
            for q in Q:
                for q_eps_reachable in e_reachable[q].copy():
                    q_eps_reachable_new = self.__transitions.get((q_eps_reachable, ""))
                    if q_eps_reachable_new and len(q_eps_reachable_new - e_reachable[q]) >= 1:
                        e_reachable[q] |= q_eps_reachable_new
                        changes = True
        return e_reachable

    def simulate(self, qs: set[str], w: str) -> set[str]:
        if not set(w).issubset(self.__Sigma):
            raise ValueError(f"w = {w} contains symbols that are not in alphabet {self.__Sigma}.")
        if not w:
            qs = reduce(lambda x, y: x | y, (self.__epsilon_reachable[q] for q in qs))
            return qs

        for a in w:
            qs = reduce(lambda x, y: x | y, (self.__epsilon_reachable[q] for q in qs))
            new_qs = set()
            for q in qs:
                if (q, a) not in self.__transitions.keys():
                    continue
                new_qs |= self.__transitions[(q, a)]
            qs = reduce(lambda x, y: x | y, (self.__epsilon_reachable[q] for q in new_qs))
        return qs

    def accepts(self, w: str) -> bool:
        qs = self.simulate({self.__q0}, w)
        return len(qs & self.__F) >= 1

    def to_NFA(self) -> NFA:
        Sigma = self.__Sigma
        Q = self.__Q
        transitions = dict()
        for ((q, a), qs) in self.__transitions.items():
            if a == "":
                continue
            start_qs = self.__epsilon_reachable_reversed[q].copy()
            end_qs = reduce(lambda x, y: x | y, (self.__epsilon_reachable[q] for q in qs))
            for q1 in start_qs:
                for q2 in end_qs:
                    if (q1, a) not in transitions.keys():
                        transitions[(q1, a)] = set()
                    transitions[(q1, a)] |= {q2}
        q0 = self.__q0
        F = set(q for q in Q if len(self.__epsilon_reachable[q] & self.__F) >= 1)
        return NFA(Sigma, Q, transitions, q0, F)
    
    def to_DFA(self) -> DFA:
        nfa = self.to_NFA()
        dfa = nfa.to_DFA()
        return nfa


if __name__ == "__main__":
    Sigma = {"a", "b"}
    Q = {"0", "1"}
    q0 = "0"
    F = {"1"}

    transitions = {
        ("0", "a"): "0",
        ("0", "b"): "0",
        ("1", "a"): "1",
        ("1", "b"): "1"
    }

    A = DFA(Sigma, Q, transitions, q0, F)
    B = A.to_E_NFA()