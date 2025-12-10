"""
Utility functions for automata engines
"""
import string
import random

def generate_unique_id(prefix=''):
    """Generate a unique identifier"""
    return f"{prefix}_{random.randint(1000, 9999)}"

def epsilon_closure(state, transitions):
    """Compute epsilon closure for NFA states"""
    closure = {state}
    stack = [state]
    
    while stack:
        current = stack.pop()
        
        if current in transitions and 'ε' in transitions[current]:
            epsilon_states = transitions[current]['ε']
            if isinstance(epsilon_states, str):
                epsilon_states = [epsilon_states]
            
            for next_state in epsilon_states:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    
    return closure

def move(states, symbol, transitions):
    """Compute move operation for a set of states"""
    result = set()
    
    for state in states:
        if state in transitions and symbol in transitions[state]:
            next_states = transitions[state][symbol]
            if isinstance(next_states, str):
                next_states = [next_states]
            result.update(next_states)
    
    return result

def is_accepting_state(state, accept_states):
    """Check if a state is an accepting state"""
    return state in accept_states

def format_state_name(states):
    """Format a set of states as a string"""
    if isinstance(states, set):
        return '{' + ','.join(sorted(states)) + '}'
    return str(states)

def validate_grammar(grammar):
    """Validate a context-free grammar"""
    if not grammar or 'rules' not in grammar:
        return False, "Grammar is missing or invalid"
    
    if not grammar.get('start_symbol'):
        return False, "No start symbol defined"
    
    rules = grammar['rules']
    if not rules:
        return False, "No production rules defined"
    
    return True, "Valid grammar"

def normalize_production(production):
    """Normalize a production rule"""
    # Replace epsilon variants
    production = production.replace('epsilon', 'ε')
    production = production.replace('EPSILON', 'ε')
    production = production.strip()
    
    return production
