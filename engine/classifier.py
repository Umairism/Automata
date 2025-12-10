"""
Query Classifier - Determines the type of automata problem from user input
"""
import re

def classify_query(question, grammar="", automaton=None):
    """
    Classify the type of problem based on keywords in the question
    
    Args:
        question (str): User's question
        grammar (str): Optional grammar specification
        automaton (dict): Optional automaton specification
    
    Returns:
        dict: Classification result with task_type and metadata
    """
    question_lower = question.lower()
    
    # Moore Machine patterns
    if any(keyword in question_lower for keyword in ['moore machine', 'moore model', 'construct moore']):
        return {
            'task_type': 'moore_machine',
            'question': question,
            'automaton': automaton,
            'constraints': {}
        }
    
    # Mealy Machine patterns
    if any(keyword in question_lower for keyword in ['mealy machine', 'mealy model', 'construct mealy']):
        return {
            'task_type': 'mealy_machine',
            'question': question,
            'automaton': automaton,
            'constraints': {}
        }
    
    # Moore to Mealy or vice versa
    if any(keyword in question_lower for keyword in ['moore to mealy', 'convert moore', 'mealy to moore', 'convert mealy']):
        if 'moore to mealy' in question_lower or 'convert moore' in question_lower:
            return {
                'task_type': 'moore_to_mealy',
                'question': question,
                'automaton': automaton,
                'constraints': {}
            }
        else:
            return {
                'task_type': 'mealy_to_moore',
                'question': question,
                'automaton': automaton,
                'constraints': {}
            }
    
    # Pumping Lemma patterns
    if any(keyword in question_lower for keyword in ['pumping lemma', 'pumping theorem']):
        if any(keyword in question_lower for keyword in ['context-free', 'cfl', 'cfg']):
            return {
                'task_type': 'pumping_lemma_cfl',
                'question': question,
                'grammar': grammar,
                'constraints': {}
            }
        else:
            return {
                'task_type': 'pumping_lemma_regular',
                'question': question,
                'constraints': {}
            }
    
    # Closure Properties patterns
    if any(keyword in question_lower for keyword in ['closure property', 'closure properties', 'closed under']):
        if any(keyword in question_lower for keyword in ['regular', 'regular language', 'regular expression']):
            return {
                'task_type': 'closure_regular',
                'question': question,
                'constraints': {}
            }
        elif any(keyword in question_lower for keyword in ['context-free', 'cfl', 'cfg']):
            return {
                'task_type': 'closure_cfl',
                'question': question,
                'constraints': {}
            }
    
    # Derivation Tree (Parse Tree)
    if any(keyword in question_lower for keyword in ['derivation tree', 'parse tree', 'syntax tree']):
        return {
            'task_type': 'cfg_parse_tree',
            'question': question,
            'grammar': grammar,
            'constraints': {}
        }
    
    # Leftmost/Rightmost Derivation
    if any(keyword in question_lower for keyword in ['leftmost derivation', 'rightmost derivation']):
        return {
            'task_type': 'cfg_derivation',
            'question': question,
            'grammar': grammar,
            'derivation_type': 'leftmost' if 'leftmost' in question_lower else 'rightmost',
            'constraints': {}
        }
    
    # CFG Construction patterns
    if any(keyword in question_lower for keyword in ['construct cfg', 'construct a cfg', 'build cfg', 'build a cfg', 'create cfg', 'cfg for']) and not grammar:
        return {
            'task_type': 'cfg_construction',
            'question': question,
            'constraints': extract_language_constraints(question)
        }
    
    # CFG-related patterns
    if any(keyword in question_lower for keyword in ['ambiguous', 'ambiguity']):
        return {
            'task_type': 'cfg_ambiguity',
            'question': question,
            'grammar': grammar,
            'constraints': {}
        }
    
    if any(keyword in question_lower for keyword in ['derive', 'derivation']) and grammar:
        return {
            'task_type': 'cfg_derivation',
            'question': question,
            'grammar': grammar,
            'derivation_type': 'leftmost' if 'leftmost' in question_lower else 'rightmost',
            'constraints': {}
        }
    
    if any(keyword in question_lower for keyword in ['cnf', 'chomsky normal form']):
        return {
            'task_type': 'cfg_to_cnf',
            'question': question,
            'grammar': grammar,
            'constraints': {}
        }
    
    # LBA (Linear Bounded Automaton) patterns
    if any(keyword in question_lower for keyword in ['lba', 'linear bounded automaton', 'linear bounded automata']):
        return {
            'task_type': 'lba_construction',
            'question': question,
            'constraints': extract_language_constraints(question)
        }
    
    # PDA Transition Function
    if any(keyword in question_lower for keyword in ['transition function', 'transition table']) and 'pda' in question_lower:
        return {
            'task_type': 'pda_transitions',
            'question': question,
            'automaton': automaton,
            'constraints': {}
        }
    
    # DFA/NFA patterns
    if any(keyword in question_lower for keyword in ['construct dfa', 'construct a dfa', 'build dfa', 'build a dfa', 'create dfa', 'create a dfa', 'design dfa', 'design a dfa', 'dfa with', 'dfa that']):
        return {
            'task_type': 'dfa_construction',
            'question': question,
            'constraints': extract_language_constraints(question)
        }
    
    if any(keyword in question_lower for keyword in ['nfa to dfa', 'convert nfa', 'determinize']):
        return {
            'task_type': 'nfa_to_dfa',
            'question': question,
            'automaton': automaton,
            'constraints': {}
        }
    
    if any(keyword in question_lower for keyword in ['minimize', 'minimization', 'minimum dfa']):
        return {
            'task_type': 'dfa_minimization',
            'question': question,
            'automaton': automaton,
            'constraints': {}
        }
    
    if any(keyword in question_lower for keyword in ['regular expression', 're to nfa', 'regex to nfa']):
        return {
            'task_type': 're_to_nfa',
            'question': question,
            'regex': extract_regex(question),
            'constraints': {}
        }
    
    # Palindrome patterns - context-free, needs PDA
    if any(keyword in question_lower for keyword in ['palindrome', 'palindromes', 'reads the same backward', 'same forward and backward']):
        # Check if explicitly asking for TM
        if any(keyword in question_lower for keyword in ['turing machine', 'tm', 'build tm', 'construct tm']):
            return {
                'task_type': 'tm_construction',
                'question': question,
                'constraints': extract_language_constraints(question)
            }
        # Default to PDA for palindromes (context-free language)
        else:
            return {
                'task_type': 'pda_construction',
                'question': question,
                'constraints': extract_language_constraints(question)
            }
    
    # PDA patterns
    if any(keyword in question_lower for keyword in ['pda', 'pushdown automaton', 'pushdown automata']):
        if 'cfg' in question_lower or 'grammar' in question_lower:
            return {
                'task_type': 'pda_from_cfg',
                'question': question,
                'grammar': grammar,
                'constraints': {}
            }
        else:
            return {
                'task_type': 'pda_construction',
                'question': question,
                'constraints': extract_language_constraints(question)
            }
    
    # Turing Machine patterns
    if any(keyword in question_lower for keyword in ['turing machine', 'tm construction', 'build tm']):
        return {
            'task_type': 'tm_construction',
            'question': question,
            'constraints': extract_language_constraints(question)
        }
    
    if any(keyword in question_lower for keyword in ['tm trace', 'turing machine trace', 'configuration']):
        return {
            'task_type': 'tm_trace',
            'question': question,
            'automaton': automaton,
            'constraints': {}
        }
    
    # Membership testing
    if any(keyword in question_lower for keyword in ['belongs', 'accept', 'membership', 'recognize']):
        if 'dfa' in question_lower or 'nfa' in question_lower:
            return {
                'task_type': 'dfa_membership',
                'question': question,
                'automaton': automaton,
                'constraints': {}
            }
        elif 'pda' in question_lower:
            return {
                'task_type': 'pda_membership',
                'question': question,
                'automaton': automaton,
                'constraints': {}
            }
        elif 'tm' in question_lower or 'turing' in question_lower:
            return {
                'task_type': 'tm_membership',
                'question': question,
                'automaton': automaton,
                'constraints': {}
            }
    
    # Default: Try to infer from grammar or automaton presence
    if grammar:
        return {
            'task_type': 'cfg_ambiguity',
            'question': question,
            'grammar': grammar,
            'constraints': {}
        }
    
    # Fallback
    return {
        'task_type': 'unknown',
        'question': question,
        'error': 'Could not classify query. Please be more specific.',
        'constraints': {}
    }

def extract_language_constraints(question):
    """Extract language patterns from the question"""
    constraints = {}
    
    # Palindrome patterns
    if 'palindrome' in question.lower():
        constraints['pattern'] = 'palindrome'
        if 'even' in question.lower():
            constraints['palindrome_type'] = 'even'
        elif 'odd' in question.lower():
            constraints['palindrome_type'] = 'odd'
        else:
            constraints['palindrome_type'] = 'any'
    
    # Common patterns
    if re.search(r'strings with (\d+)', question):
        match = re.search(r'strings with (\d+)', question)
        constraints['count'] = match.group(1)
    
    if 'even' in question.lower() and 'palindrome' not in question.lower():
        constraints['parity'] = 'even'
    elif 'odd' in question.lower() and 'palindrome' not in question.lower():
        constraints['parity'] = 'odd'
    
    if re.search(r'a+b+', question) or re.search(r'a\*b\*', question):
        constraints['pattern'] = 'concatenation'
    
    return constraints

def extract_regex(question):
    """Extract regular expression from question"""
    # Look for patterns like (a|b)*, a+b*, etc.
    regex_pattern = r'[\(]?[a-z\|\*\+\(\)]+[\)]?[\*\+]?'
    matches = re.findall(regex_pattern, question)
    return matches[0] if matches else ''
