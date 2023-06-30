# regLang

Python implementation for finate automatoms (FAs) to represent regulare languages.

Currently the following is implemented:

- Deterministic FA (DFA)
- Non-deterministic FA (NFA)
- NFA with spontanious transitions (epsilon-NFA)

## Code

### DFA class

#### properties

- `Sigma: str`: Alphabet
- `Q: set[str]`: States
- `transitions: dict[tuple[str, str], str]`: Transition function. It maps a (state, symbol) pair to the next state. Must be deterministic.
- `q0: str`: Starting state. Must be in `Q`.
- `F: set[str]`: Terminating states. Must be a subset of `Q`

#### methods

- `simulate(state: str, word: str) -> state: str` Simulates a few steps in the DFA and get the resulting state. Primarily usage is for visualization / understanding.
- `accepts(word: str) -> bool` Tests wether a given word is in the language of the DFA.
- `to_NFA()` Transforms DFA to NFA
- `to_E_NFA()` Transforms DFA to epsilon-NFA
- `renameStates(Q: set[str], inplace: bool = False) -> Optional[DFA]` Renames the states of the DFA. Must be same number than previous states. Renaming can be inplace if wished.
- `union(other: DFA) -> E_NFA` Creates a epsilon-FA that accepts the union language of both DFAs. States are renamed.

### NFA class

#### properties

- `Sigma: str`: Alphabet
- `Q: set[str]`: States
- `transitions: dict[tuple[str, str], set[str]]`: Transition function. It maps a (state, symbol) pair to the set of next states.
- `q0: str`: Starting state. Must be in `Q`.
- `F: set[str]`: Terminating states. Must be a subset of `Q`

#### methods

- `simulate(state: str, word: str) -> state: str` Simulates a few steps in the NFA and returns all possible resulting states. Primarily usage is for visualization / understanding.
- `accepts(word: str) -> bool` Tests wether a given word is in the language of the NFA.
- `to_DFA()` Transforms NFA to DFA. Uses the powerset construction.
- `to_E_NFA()` Transforms NFA to epsilon-NFA
- `renameStates(Q: set[str], inplace: bool = False) -> Optional[NFA]` Renames the states of the NFA. Must be same number than previous states. Renaming can be inplace if wished.
- `union(other: NFA) -> E_NFA` Creates a epsilon-FA that accepts the union language of both NFAs. States are renamed.

### E_NFA class

#### properties

- `Sigma: str`: Alphabet
- `Q: set[str]`: States
- `transitions: dict[tuple[str, str], set[str]]`: Transition function. It maps a (state, symbol) pair to the set of next states. Epsilon transitions are represented with the empty string `""`
- `q0: str`: Starting state. Must be in `Q`.
- `F: set[str]`: Terminating states. Must be a subset of `Q`

#### methods

- `simulate(state: str, word: str) -> state: str` Simulates a few steps in the E_NFA and returns all possible resulting states. Primarily usage is for visualization / understanding.
- `accepts(word: str) -> bool` Tests wether a given word is in the language of the E_NFA.
- `to_DFA()` Transforms epsilon-NFA to DFA. Uses the powerset construction.
- `to_NFA()` Transforms epsilon-NFA to NFA by removing the epsilon transitions.
- `renameStates(Q: set[str], inplace: bool = False) -> Optional[E_NFA]` Renames the states of the E_NFA. Must be same number than previous states. Renaming can be inplace if wished.
- `union(other: E_NFA) -> E_NFA` Creates a epsilon-FA that accepts the union language of both epsilon-NFAs. States are renamed.

## Installation

You install this project by running the following command in the terminal:

```bash
pip install git+https://github.com/sIDsID11/regLang
```
