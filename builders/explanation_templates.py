"""
Explanation Templates - Pre-formatted explanations for different problem types
"""

CFG_AMBIGUITY_EXPLANATION = """
## Grammar Ambiguity Analysis

A context-free grammar is **ambiguous** if there exists at least one string in the language 
that has two or more distinct parse trees (or equivalently, two or more distinct leftmost/rightmost derivations).

### Method:
1. Generate candidate strings from the grammar
2. For each string, attempt to find multiple derivations
3. If multiple parse trees exist for any string, the grammar is ambiguous

### Result:
{result}
"""

DFA_CONSTRUCTION_EXPLANATION = """
## DFA Construction

A Deterministic Finite Automaton (DFA) consists of:
- A finite set of states
- An input alphabet
- A transition function (each state has exactly one transition per symbol)
- A start state
- A set of accepting (final) states

### Construction Strategy:
{strategy}
"""

NFA_TO_DFA_EXPLANATION = """
## NFA to DFA Conversion (Subset Construction)

The subset construction algorithm converts an NFA to an equivalent DFA:

1. **Initial State**: ε-closure of NFA start state becomes DFA start state
2. **State Creation**: Each DFA state represents a set of NFA states
3. **Transitions**: For each DFA state and input symbol, compute:
   - Move to next NFA states
   - Take ε-closure of those states
   - Result is the next DFA state
4. **Accept States**: DFA state is accepting if it contains any NFA accepting state

### Result:
- Original NFA states: {nfa_states}
- Converted DFA states: {dfa_states}
"""

PDA_CONSTRUCTION_EXPLANATION = """
## Pushdown Automaton (PDA)

A PDA extends finite automata with a stack, allowing recognition of context-free languages.

### Components:
- States
- Input alphabet
- Stack alphabet
- Transition function: (state, input, stack_top) → (new_state, stack_operation)
- Start state and stack symbol
- Acceptance condition (final state or empty stack)

### Operation:
The PDA reads input symbols and manipulates the stack based on transition rules.
"""

TM_CONSTRUCTION_EXPLANATION = """
## Turing Machine

A Turing Machine is a theoretical computing device with:
- A finite set of states
- An infinite tape with cells
- A read/write head
- A transition function: (state, symbol) → (new_state, write_symbol, move_direction)

### Capabilities:
- Can move left or right on the tape
- Can read and write symbols
- Can recognize recursively enumerable languages
- Models the concept of computation
"""

def get_explanation(task_type, **kwargs):
    """Get formatted explanation for a task type"""
    
    templates = {
        'cfg_ambiguity': CFG_AMBIGUITY_EXPLANATION,
        'dfa_construction': DFA_CONSTRUCTION_EXPLANATION,
        'nfa_to_dfa': NFA_TO_DFA_EXPLANATION,
        'pda_construction': PDA_CONSTRUCTION_EXPLANATION,
        'tm_construction': TM_CONSTRUCTION_EXPLANATION
    }
    
    template = templates.get(task_type, "Explanation for {task_type}")
    
    try:
        return template.format(**kwargs)
    except KeyError:
        return template
