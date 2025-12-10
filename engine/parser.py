"""
Input Parser - Parses grammar and automaton specifications
"""
import re

def parse_input(classification, grammar="", automaton=None):
    """
    Parse the input based on classification
    
    Args:
        classification (dict): Result from classifier
        grammar (str): Grammar specification
        automaton (dict): Automaton specification
    
    Returns:
        dict: Parsed input ready for engine processing
    """
    task_type = classification['task_type']
    
    if task_type in ['cfg_construction', 'cfg_ambiguity', 'cfg_derivation', 'cfg_parse_tree', 'cfg_to_cnf', 'cfg_to_pda', 'pda_from_cfg']:
        return parse_grammar(grammar, classification)
    
    elif task_type in ['dfa_construction', 'nfa_to_dfa', 'dfa_minimization']:
        return parse_automaton(automaton, classification)
    
    elif task_type in ['re_to_nfa']:
        return parse_regex(classification.get('regex', ''), classification)
    
    else:
        return classification

def parse_grammar(grammar_str, classification):
    """
    Parse a context-free grammar
    Expected format:
    S → aS | bA
    A → aA | ε
    """
    rules = {}
    start_symbol = None
    
    if not grammar_str:
        # Try to extract from question
        grammar_str = classification.get('grammar', '')
    
    lines = grammar_str.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Split by → or ->
        if '→' in line:
            parts = line.split('→')
        elif '->' in line:
            parts = line.split('->')
        else:
            continue
        
        if len(parts) != 2:
            continue
        
        lhs = parts[0].strip()
        rhs = parts[1].strip()
        
        # First rule defines start symbol
        if start_symbol is None:
            start_symbol = lhs
        
        # Split alternatives by |
        productions = [prod.strip() for prod in rhs.split('|')]
        
        if lhs not in rules:
            rules[lhs] = []
        rules[lhs].extend(productions)
    
    return {
        **classification,
        'grammar': {
            'rules': rules,
            'start_symbol': start_symbol,
            'terminals': extract_terminals(rules),
            'non_terminals': list(rules.keys())
        }
    }

def parse_automaton(automaton_dict, classification):
    """
    Parse automaton specification
    Expected format:
    {
        'states': ['q0', 'q1', 'q2'],
        'alphabet': ['a', 'b'],
        'transitions': {
            'q0': {'a': 'q1', 'b': 'q0'},
            'q1': {'a': 'q2', 'b': 'q0'}
        },
        'start_state': 'q0',
        'accept_states': ['q2']
    }
    """
    if not automaton_dict:
        # Return basic structure
        return {
            **classification,
            'automaton': {
                'states': [],
                'alphabet': [],
                'transitions': {},
                'start_state': None,
                'accept_states': []
            }
        }
    
    return {
        **classification,
        'automaton': automaton_dict
    }

def parse_regex(regex_str, classification):
    """Parse regular expression"""
    return {
        **classification,
        'regex': regex_str,
        'parsed_regex': tokenize_regex(regex_str)
    }

def extract_terminals(rules):
    """Extract terminal symbols from grammar rules"""
    terminals = set()
    
    for productions in rules.values():
        for prod in productions:
            for char in prod:
                if char.islower() or char.isdigit() or char in ['ε', 'epsilon', '+', '*', '(', ')']:
                    terminals.add(char)
    
    terminals.discard('ε')
    terminals.discard('epsilon')
    
    return list(terminals)

def tokenize_regex(regex_str):
    """Tokenize a regular expression"""
    tokens = []
    i = 0
    
    while i < len(regex_str):
        char = regex_str[i]
        
        if char in ['(', ')', '|', '*', '+', '?']:
            tokens.append({'type': 'operator', 'value': char})
        elif char.isalnum():
            tokens.append({'type': 'symbol', 'value': char})
        elif char == ' ':
            i += 1
            continue
        
        i += 1
    
    return tokens
