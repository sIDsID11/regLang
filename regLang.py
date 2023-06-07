from __future__ import annotations
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
                raise ValueError(f"Invalid transition ((q={a}, a={a}), q'={q_}. States or symbol unknown.")

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


class NFA:
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


if __name__ == "__main__":
    Sigma = {"a", "b"}
    Q = {"0", "1"}
    q0 = "0"
    F = {"1"}

    transitions = {
        ("0", "a"): {"0", "1"},
        ("0", "b"): {"1"},
        ("1", "b"): {"1"}
    }

    B = NFA(Sigma, Q, transitions, q0, F)
    A = B.to_DFA()