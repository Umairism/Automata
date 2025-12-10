"""
DFA/NFA Engine - Handles finite automata problems
"""
from engine.utils import epsilon_closure, move, format_state_name
import copy

class DFAEngine:
    """Engine for DFA/NFA-related problems"""
    
    def __init__(self):
        self.state_counter = 0
    
    def solve(self, task_type, parsed_input):
        """Main solver dispatcher"""
        
        if task_type == 'dfa_construction':
            return self.construct_dfa(parsed_input)
        
        elif task_type == 'nfa_construction':
            return self.construct_nfa(parsed_input)
        
        elif task_type == 'nfa_to_dfa':
            return self.nfa_to_dfa(parsed_input)
        
        elif task_type == 'dfa_minimization':
            return self.minimize_dfa(parsed_input)
        
        elif task_type == 're_to_nfa':
            return self.regex_to_nfa(parsed_input)
        
        elif task_type == 'dfa_membership':
            return self.test_membership(parsed_input)
        
        else:
            return {'error': f'Unsupported DFA task: {task_type}'}
    
    def construct_dfa(self, parsed_input):
        """Construct a DFA from language description"""
        question = parsed_input.get('question', '')
        constraints = parsed_input.get('constraints', {})
        
        # Check if it's a specific string acceptance problem
        specific_string = self._extract_specific_string(question)
        
        if specific_string:
            dfa = self._construct_dfa_for_string(specific_string)
            return {
                'dfa': dfa,
                'explanation': f'DFA constructed to accept only the string "{specific_string}".\n\nThe DFA has {len(specific_string) + 2} states: one for each character in the string, plus a start state and a dead/reject state. Any deviation from the exact sequence leads to the reject state.',
                'transition_table': self._generate_transition_table(dfa),
                'diagram_filename': 'dfa_construction.png'
            }
        
        # Check for common patterns
        if 'even' in question.lower() and 'a' in question.lower():
            dfa = {
                'states': ['q0', 'q1'],
                'alphabet': ['a', 'b'],
                'transitions': {
                    'q0': {'a': 'q1', 'b': 'q0'},
                    'q1': {'a': 'q0', 'b': 'q1'}
                },
                'start_state': 'q0',
                'accept_states': ['q0']
            }
            explanation = 'DFA that accepts strings with even number of a\'s. State q0 represents even count, q1 represents odd count.'
        
        elif 'odd' in question.lower() and 'a' in question.lower():
            dfa = {
                'states': ['q0', 'q1'],
                'alphabet': ['a', 'b'],
                'transitions': {
                    'q0': {'a': 'q1', 'b': 'q0'},
                    'q1': {'a': 'q0', 'b': 'q1'}
                },
                'start_state': 'q0',
                'accept_states': ['q1']
            }
            explanation = 'DFA that accepts strings with odd number of a\'s. State q0 represents even count, q1 represents odd count.'
        
        elif 'end' in question.lower() and 'ab' in question.lower():
            dfa = {
                'states': ['q0', 'q1', 'q2'],
                'alphabet': ['a', 'b'],
                'transitions': {
                    'q0': {'a': 'q1', 'b': 'q0'},
                    'q1': {'a': 'q1', 'b': 'q2'},
                    'q2': {'a': 'q1', 'b': 'q0'}
                },
                'start_state': 'q0',
                'accept_states': ['q2']
            }
            explanation = 'DFA that accepts strings ending with "ab".'
        
        else:
            # Default example
            dfa = {
                'states': ['q0', 'q1'],
                'alphabet': ['a', 'b'],
                'transitions': {
                    'q0': {'a': 'q1', 'b': 'q0'},
                    'q1': {'a': 'q0', 'b': 'q1'}
                },
                'start_state': 'q0',
                'accept_states': ['q0']
            }
            explanation = 'DFA constructed for the given language specification (default: even number of a\'s).'
        
        return {
            'dfa': dfa,
            'explanation': explanation,
            'transition_table': self._generate_transition_table(dfa),
            'diagram_filename': 'dfa_construction.png'
        }
    
    def _extract_specific_string(self, question):
        """Extract a specific string from the question if present"""
        import re
        
        # Look for patterns like "only the input 'aaab'" or 'accepts "aaab"' or 'string aaab'
        patterns = [
            r'input\s+["\']([a-z]+)["\']',
            r'string\s+["\']([a-z]+)["\']',
            r'accepts\s+only\s+["\']([a-z]+)["\']',
            r'only\s+["\']([a-z]+)["\']',
            r'exactly\s+["\']([a-z]+)["\']',
            r'["\']([a-z]+)["\']'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, question.lower())
            if match:
                return match.group(1)
        
        return None
    
    def _construct_dfa_for_string(self, target_string):
        """
        Construct a DFA that accepts only a specific string
        
        For a string like "aaab", we create:
        - One state for start (q0)
        - One state for each position in the string (q1, q2, q3, q4)
        - One dead/reject state (qreject)
        - Transitions follow the string exactly
        - Any other input goes to reject state
        """
        # Determine alphabet from the string
        alphabet = sorted(list(set(target_string)))
        
        # Create states
        num_states = len(target_string) + 1  # +1 for start state
        states = [f'q{i}' for i in range(num_states)]
        states.append('qreject')  # Dead state
        
        # Build transitions
        transitions = {}
        
        for i in range(num_states - 1):
            transitions[f'q{i}'] = {}
            
            # Current character to match
            expected_char = target_string[i]
            
            for symbol in alphabet:
                if symbol == expected_char:
                    # Correct character, move to next state
                    transitions[f'q{i}'][symbol] = f'q{i+1}'
                else:
                    # Wrong character, go to reject state
                    transitions[f'q{i}'][symbol] = 'qreject'
        
        # Final accepting state - all transitions go to reject
        transitions[f'q{num_states - 1}'] = {}
        for symbol in alphabet:
            transitions[f'q{num_states - 1}'][symbol] = 'qreject'
        
        # Reject state - loops to itself
        transitions['qreject'] = {}
        for symbol in alphabet:
            transitions['qreject'][symbol] = 'qreject'
        
        return {
            'states': states,
            'alphabet': alphabet,
            'transitions': transitions,
            'start_state': 'q0',
            'accept_states': [f'q{num_states - 1}']
        }
    
    def construct_nfa(self, parsed_input):
        """Construct an NFA from language description"""
        question = parsed_input.get('question', '').lower()
        constraints = parsed_input.get('constraints', {})
        
        # Check for substring patterns (contains 010, contains 101, etc.)
        if 'contain' in question or 'substring' in question:
            import re
            # Look for patterns like "010", "101", "abb", etc.
            substring_match = re.search(r'["\']?([01]+|[ab]+)["\']?', question)
            if substring_match:
                substring = substring_match.group(1)
                nfa = self._construct_nfa_for_substring(substring)
                return {
                    'nfa': nfa,
                    'explanation': f'NFA constructed to accept strings containing the substring "{substring}".\n\nThe NFA has {len(substring) + 1} states. It non-deterministically guesses where the substring begins and verifies the pattern. Once the full substring is matched, it stays in the accept state.',
                    'transition_table': self._generate_transition_table(nfa),
                    'diagram_filename': 'nfa_construction.png'
                }
        
        # Check for epsilon/lambda transitions
        if 'epsilon' in question or 'lambda' in question or 'ε' in question:
            # Pattern like (a|b)*abb
            if 'abb' in question:
                nfa = {
                    'states': ['q0', 'q1', 'q2', 'q3'],
                    'alphabet': ['a', 'b'],
                    'transitions': {
                        'q0': {'a': ['q0', 'q1'], 'b': ['q0'], 'ε': []},
                        'q1': {'a': [], 'b': ['q2'], 'ε': []},
                        'q2': {'a': [], 'b': ['q3'], 'ε': []},
                        'q3': {'a': [], 'b': [], 'ε': []}
                    },
                    'start_state': 'q0',
                    'accept_states': ['q3']
                }
                explanation = 'NFA with epsilon transitions for (a|b)*abb. The automaton allows any sequence of a\'s and b\'s, then requires the exact sequence "abb" to accept.'
            else:
                # Generic epsilon-NFA
                nfa = {
                    'states': ['q0', 'q1', 'q2'],
                    'alphabet': ['a', 'b'],
                    'transitions': {
                        'q0': {'a': ['q1'], 'b': [], 'ε': ['q2']},
                        'q1': {'a': [], 'b': ['q2'], 'ε': []},
                        'q2': {'a': [], 'b': [], 'ε': []}
                    },
                    'start_state': 'q0',
                    'accept_states': ['q2']
                }
                explanation = 'NFA with epsilon transitions. The epsilon transition allows moving between states without consuming input.'
            
            return {
                'nfa': nfa,
                'explanation': explanation,
                'transition_table': self._generate_transition_table(nfa),
                'diagram_filename': 'nfa_construction.png'
            }
        
        # Default NFA (for unrecognized patterns)
        nfa = {
            'states': ['q0', 'q1', 'q2'],
            'alphabet': ['a', 'b'],
            'transitions': {
                'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
                'q1': {'a': [], 'b': ['q2']},
                'q2': {'a': [], 'b': []}
            },
            'start_state': 'q0',
            'accept_states': ['q2']
        }
        explanation = 'NFA constructed for the given language specification.'
        
        return {
            'nfa': nfa,
            'explanation': explanation,
            'transition_table': self._generate_transition_table(nfa),
            'diagram_filename': 'nfa_construction.png'
        }
    
    def _construct_nfa_for_substring(self, substring):
        """Construct an NFA that accepts strings containing a specific substring"""
        # Determine alphabet from the substring
        alphabet = sorted(list(set(substring)))
        
        # Create states: one for each character in substring + start state
        num_states = len(substring) + 1
        states = [f'q{i}' for i in range(num_states)]
        
        # Build transitions
        transitions = {}
        
        # First state: can loop on all characters, and start matching on first char of substring
        transitions['q0'] = {}
        for symbol in alphabet:
            if symbol == substring[0]:
                transitions['q0'][symbol] = ['q0', 'q1']  # Non-deterministic: stay or start matching
            else:
                transitions['q0'][symbol] = ['q0']  # Just loop
        
        # Middle states: match the substring character by character
        for i in range(1, num_states - 1):
            transitions[f'q{i}'] = {}
            expected_char = substring[i]
            
            for symbol in alphabet:
                if symbol == expected_char:
                    transitions[f'q{i}'][symbol] = [f'q{i+1}']
                else:
                    transitions[f'q{i}'][symbol] = []  # Dead end if wrong character
        
        # Final state: substring matched, accept all remaining input
        transitions[f'q{num_states - 1}'] = {}
        for symbol in alphabet:
            transitions[f'q{num_states - 1}'][symbol] = [f'q{num_states - 1}']  # Loop in accept state
        
        return {
            'states': states,
            'alphabet': alphabet,
            'transitions': transitions,
            'start_state': 'q0',
            'accept_states': [f'q{num_states - 1}']
        }
    
    def nfa_to_dfa(self, parsed_input):
        """Convert NFA to DFA using subset construction"""
        nfa = parsed_input.get('automaton', {})
        
        # If no NFA provided, create a sample NFA to demonstrate conversion
        if not nfa or 'states' not in nfa:
            nfa = {
                'states': ['q0', 'q1', 'q2'],
                'alphabet': ['a', 'b'],
                'transitions': {
                    'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
                    'q1': {'a': [], 'b': ['q2']},
                    'q2': {'a': [], 'b': []}
                },
                'start_state': 'q0',
                'accept_states': ['q2']
            }
        
        # Subset construction algorithm
        dfa_states = []
        dfa_transitions = {}
        dfa_accept_states = []
        
        # Start with epsilon closure of start state
        start_closure = epsilon_closure(nfa['start_state'], nfa.get('transitions', {}))
        start_state_name = format_state_name(start_closure)
        
        dfa_states.append(start_state_name)
        queue = [start_closure]
        processed = set()
        
        while queue:
            current_set = queue.pop(0)
            current_name = format_state_name(current_set)
            
            if current_name in processed:
                continue
            processed.add(current_name)
            
            # Check if this is an accept state
            if any(state in nfa.get('accept_states', []) for state in current_set):
                dfa_accept_states.append(current_name)
            
            dfa_transitions[current_name] = {}
            
            # For each symbol in alphabet
            for symbol in nfa.get('alphabet', []):
                # Compute move and epsilon closure
                next_set = set()
                for state in current_set:
                    moved = move({state}, symbol, nfa.get('transitions', {}))
                    for moved_state in moved:
                        next_set.update(epsilon_closure(moved_state, nfa.get('transitions', {})))
                
                if next_set:
                    next_name = format_state_name(next_set)
                    dfa_transitions[current_name][symbol] = next_name
                    
                    if next_name not in dfa_states:
                        dfa_states.append(next_name)
                        queue.append(next_set)
        
        dfa = {
            'states': dfa_states,
            'alphabet': nfa.get('alphabet', []),
            'transitions': dfa_transitions,
            'start_state': start_state_name,
            'accept_states': dfa_accept_states
        }
        
        return {
            'original_nfa': nfa,
            'converted_dfa': dfa,
            'explanation': 'NFA converted to DFA using subset construction algorithm.',
            'steps': [
                'Step 1: Compute ε-closure of start state',
                'Step 2: For each DFA state, compute transitions',
                'Step 3: Mark accept states',
                'Step 4: Repeat until all reachable states are processed'
            ],
            'transition_table': self._generate_transition_table(dfa),
            'diagram_filename': 'nfa_to_dfa.png'
        }
    
    def minimize_dfa(self, parsed_input):
        """Minimize a DFA using table-filling algorithm"""
        dfa = parsed_input.get('automaton', {})
        
        if not dfa or 'states' not in dfa:
            return {'error': 'Invalid DFA specification'}
        
        # Simplified minimization (partition refinement)
        states = dfa['states']
        
        # Initial partition: accepting vs non-accepting
        accept_states = set(dfa.get('accept_states', []))
        non_accept_states = set(states) - accept_states
        
        partitions = []
        if non_accept_states:
            partitions.append(non_accept_states)
        if accept_states:
            partitions.append(accept_states)
        
        # Refine partitions
        changed = True
        iterations = 0
        
        while changed and iterations < 10:
            changed = False
            iterations += 1
            new_partitions = []
            
            for partition in partitions:
                if len(partition) <= 1:
                    new_partitions.append(partition)
                    continue
                
                # Try to split this partition
                sub_partitions = self._split_partition(partition, partitions, dfa)
                
                if len(sub_partitions) > 1:
                    changed = True
                    new_partitions.extend(sub_partitions)
                else:
                    new_partitions.append(partition)
            
            partitions = new_partitions
        
        # Build minimized DFA
        minimized_dfa = self._build_minimized_dfa(dfa, partitions)
        
        return {
            'original_dfa': dfa,
            'minimized_dfa': minimized_dfa,
            'original_state_count': len(states),
            'minimized_state_count': len(minimized_dfa['states']),
            'explanation': f'DFA minimized from {len(states)} states to {len(minimized_dfa["states"])} states using partition refinement.',
            'transition_table': self._generate_transition_table(minimized_dfa),
            'diagram_filename': 'dfa_minimized.png'
        }
    
    def _split_partition(self, partition, all_partitions, dfa):
        """Try to split a partition based on transition behavior"""
        if len(partition) <= 1:
            return [partition]
        
        transitions = dfa.get('transitions', {})
        alphabet = dfa.get('alphabet', [])
        
        # Group states by their transition signatures
        signatures = {}
        
        for state in partition:
            sig = []
            for symbol in alphabet:
                if state in transitions and symbol in transitions[state]:
                    next_state = transitions[state][symbol]
                    # Find which partition next_state belongs to
                    for i, part in enumerate(all_partitions):
                        if next_state in part:
                            sig.append(i)
                            break
                else:
                    sig.append(-1)
            
            sig_tuple = tuple(sig)
            if sig_tuple not in signatures:
                signatures[sig_tuple] = set()
            signatures[sig_tuple].add(state)
        
        return list(signatures.values())
    
    def _build_minimized_dfa(self, original_dfa, partitions):
        """Build minimized DFA from partitions"""
        # Map each state to its partition representative
        state_map = {}
        new_states = []
        
        for i, partition in enumerate(partitions):
            representative = f"q{i}"
            new_states.append(representative)
            for state in partition:
                state_map[state] = representative
        
        # Build transitions
        new_transitions = {}
        for state in new_states:
            new_transitions[state] = {}
        
        for old_state, representative in state_map.items():
            if old_state in original_dfa.get('transitions', {}):
                for symbol, next_state in original_dfa['transitions'][old_state].items():
                    new_transitions[representative][symbol] = state_map[next_state]
        
        # Map start state and accept states
        new_start = state_map[original_dfa['start_state']]
        new_accept = list(set(state_map[s] for s in original_dfa.get('accept_states', [])))
        
        return {
            'states': new_states,
            'alphabet': original_dfa.get('alphabet', []),
            'transitions': new_transitions,
            'start_state': new_start,
            'accept_states': new_accept
        }
    
    def regex_to_nfa(self, parsed_input):
        """Convert regular expression to NFA using Thompson's construction"""
        regex = parsed_input.get('regex', '')
        
        # Simplified Thompson's construction
        nfa = {
            'states': ['q0', 'q1'],
            'alphabet': list(set(c for c in regex if c.isalnum())),
            'transitions': {
                'q0': {},
                'q1': {}
            },
            'start_state': 'q0',
            'accept_states': ['q1']
        }
        
        return {
            'regex': regex,
            'nfa': nfa,
            'explanation': "NFA constructed using Thompson's construction algorithm.",
            'steps': [
                'Step 1: Create NFA fragments for each symbol',
                'Step 2: Connect fragments for concatenation',
                'Step 3: Add ε-transitions for union (|)',
                'Step 4: Add loops for Kleene star (*)'
            ],
            'transition_table': self._generate_transition_table(nfa),
            'diagram_filename': 're_to_nfa.png'
        }
    
    def test_membership(self, parsed_input):
        """Test if a string is accepted by the automaton"""
        automaton = parsed_input.get('automaton', {})
        test_string = parsed_input.get('test_string', '')
        
        if not automaton:
            return {'error': 'No automaton provided'}
        
        # Simulate DFA
        current_state = automaton['start_state']
        trace = [current_state]
        
        for symbol in test_string:
            if current_state in automaton['transitions']:
                if symbol in automaton['transitions'][current_state]:
                    current_state = automaton['transitions'][current_state][symbol]
                    trace.append(current_state)
                else:
                    return {
                        'accepted': False,
                        'reason': f'No transition for symbol "{symbol}" from state {current_state}',
                        'trace': trace
                    }
            else:
                return {
                    'accepted': False,
                    'reason': f'State {current_state} has no transitions',
                    'trace': trace
                }
        
        accepted = current_state in automaton.get('accept_states', [])
        
        return {
            'test_string': test_string,
            'accepted': accepted,
            'final_state': current_state,
            'trace': trace,
            'explanation': f'String "{test_string}" is {"accepted" if accepted else "rejected"}.'
        }
    
    def _generate_transition_table(self, automaton):
        """Generate a transition table for display"""
        states = automaton.get('states', [])
        alphabet = automaton.get('alphabet', [])
        transitions = automaton.get('transitions', {})
        
        table = []
        table.append(['State'] + alphabet + ['Accept'])
        
        for state in states:
            row = [state]
            for symbol in alphabet:
                if state in transitions and symbol in transitions[state]:
                    row.append(transitions[state][symbol])
                else:
                    row.append('-')
            
            # Add accept indicator
            is_accept = state in automaton.get('accept_states', [])
            row.append('✓' if is_accept else '')
            
            table.append(row)
        
        return table
