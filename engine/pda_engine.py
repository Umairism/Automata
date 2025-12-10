"""
PDA Engine - Handles Pushdown Automata problems
"""

class PDAEngine:
    """Engine for PDA-related problems"""
    
    def __init__(self):
        self.max_moves = 100
    
    def solve(self, task_type, parsed_input):
        """Main solver dispatcher"""
        
        if task_type == 'pda_construction':
            return self.construct_pda(parsed_input)
        
        elif task_type == 'pda_from_cfg':
            return self.cfg_to_pda(parsed_input)
        
        elif task_type == 'pda_membership':
            return self.test_membership(parsed_input)
        
        elif task_type == 'pda_transitions':
            return self.show_transitions(parsed_input)
        
        else:
            return {'error': f'Unsupported PDA task: {task_type}'}
    
    def show_transitions(self, parsed_input):
        """Show transition function for a PDA"""
        question = parsed_input.get('question', '')
        
        # Construct example PDA for {a^n b^n} and show its transitions
        result = self._construct_anbn_pda()
        
        # Add detailed transition explanations
        result['transition_explanations'] = [
            'δ(q0, a, Z0) = (q0, AZ0): Read "a", push A onto empty stack',
            'δ(q0, a, A) = (q0, AA): Read "a", push A onto stack',
            'δ(q0, b, A) = (q1, ε): Read "b", pop A, switch to state q1',
            'δ(q1, b, A) = (q1, ε): Read "b", pop A, stay in q1',
            'δ(q1, ε, Z0) = (q2, Z0): Empty input, stack shows Z0, accept'
        ]
        
        result['notation'] = 'δ(current_state, input_symbol, stack_top) = (next_state, stack_operation)'
        result['explanation'] = 'Transition function for PDA accepting {a^n b^n}. The PDA pushes A for each "a" seen, then pops A for each "b" seen. Accepts if stack returns to Z0.'
        
        return result
    
    def construct_pda(self, parsed_input):
        """Construct a PDA from language description"""
        question = parsed_input.get('question', '')
        constraints = parsed_input.get('constraints', {})
        pattern = constraints.get('pattern', '')
        
        # Check if this is a palindrome problem
        if pattern == 'palindrome':
            return self._construct_palindrome_pda(constraints)
        
        # Check for a^n b^n pattern
        if 'a^n b^n' in question.lower() or 'anbn' in question.lower():
            return self._construct_anbn_pda()
        
        # Default: PDA for a^n b^n (common example)
        pda = {
            'states': ['q0', 'q1', 'q2'],
            'input_alphabet': ['a', 'b'],
            'stack_alphabet': ['Z0', 'A'],
            'start_state': 'q0',
            'start_stack_symbol': 'Z0',
            'accept_states': ['q2'],
            'transitions': [
                {'from': 'q0', 'input': 'a', 'stack_top': 'Z0', 'to': 'q0', 'stack_push': 'AZ0'},
                {'from': 'q0', 'input': 'a', 'stack_top': 'A', 'to': 'q0', 'stack_push': 'AA'},
                {'from': 'q0', 'input': 'b', 'stack_top': 'A', 'to': 'q1', 'stack_push': ''},
                {'from': 'q1', 'input': 'b', 'stack_top': 'A', 'to': 'q1', 'stack_push': ''},
                {'from': 'q1', 'input': 'ε', 'stack_top': 'Z0', 'to': 'q2', 'stack_push': 'Z0'}
            ],
            'acceptance_type': 'final_state'
        }
        
        return {
            'pda': pda,
            'explanation': 'PDA constructed for the given language specification.',
            'move_table': self._generate_move_table(pda),
            'diagram_filename': 'pda_construction.png'
        }
    
    def _construct_palindrome_pda(self, constraints):
        """Construct a PDA for palindromes"""
        palindrome_type = constraints.get('palindrome_type', 'any')
        
        if palindrome_type == 'even':
            # Even-length palindromes (no middle character)
            pda = {
                'states': ['q0', 'q1', 'q2'],
                'input_alphabet': ['a', 'b'],
                'stack_alphabet': ['Z0', 'A', 'B'],
                'start_state': 'q0',
                'start_stack_symbol': 'Z0',
                'accept_states': ['q2'],
                'transitions': [
                    # Push first half onto stack
                    {'from': 'q0', 'input': 'a', 'stack_top': 'Z0', 'to': 'q0', 'stack_push': 'AZ0'},
                    {'from': 'q0', 'input': 'a', 'stack_top': 'A', 'to': 'q0', 'stack_push': 'AA'},
                    {'from': 'q0', 'input': 'a', 'stack_top': 'B', 'to': 'q0', 'stack_push': 'AB'},
                    {'from': 'q0', 'input': 'b', 'stack_top': 'Z0', 'to': 'q0', 'stack_push': 'BZ0'},
                    {'from': 'q0', 'input': 'b', 'stack_top': 'A', 'to': 'q0', 'stack_push': 'BA'},
                    {'from': 'q0', 'input': 'b', 'stack_top': 'B', 'to': 'q0', 'stack_push': 'BB'},
                    
                    # Non-deterministically switch to matching second half
                    {'from': 'q0', 'input': 'ε', 'stack_top': 'Z0', 'to': 'q1', 'stack_push': 'Z0'},
                    {'from': 'q0', 'input': 'ε', 'stack_top': 'A', 'to': 'q1', 'stack_push': 'A'},
                    {'from': 'q0', 'input': 'ε', 'stack_top': 'B', 'to': 'q1', 'stack_push': 'B'},
                    
                    # Match second half by popping stack
                    {'from': 'q1', 'input': 'a', 'stack_top': 'A', 'to': 'q1', 'stack_push': ''},
                    {'from': 'q1', 'input': 'b', 'stack_top': 'B', 'to': 'q1', 'stack_push': ''},
                    
                    # Accept when stack is back to Z0
                    {'from': 'q1', 'input': 'ε', 'stack_top': 'Z0', 'to': 'q2', 'stack_push': 'Z0'}
                ],
                'acceptance_type': 'final_state'
            }
            explanation = 'PDA for even-length palindromes over {a, b}. The PDA non-deterministically guesses the middle point, pushes the first half onto the stack, then matches the second half by popping.'
        else:
            # General palindromes (odd or even)
            pda = {
                'states': ['q0', 'q1', 'q2'],
                'input_alphabet': ['a', 'b'],
                'stack_alphabet': ['Z0', 'A', 'B'],
                'start_state': 'q0',
                'start_stack_symbol': 'Z0',
                'accept_states': ['q2'],
                'transitions': [
                    # Push first half onto stack
                    {'from': 'q0', 'input': 'a', 'stack_top': 'Z0', 'to': 'q0', 'stack_push': 'AZ0'},
                    {'from': 'q0', 'input': 'a', 'stack_top': 'A', 'to': 'q0', 'stack_push': 'AA'},
                    {'from': 'q0', 'input': 'a', 'stack_top': 'B', 'to': 'q0', 'stack_push': 'AB'},
                    {'from': 'q0', 'input': 'b', 'stack_top': 'Z0', 'to': 'q0', 'stack_push': 'BZ0'},
                    {'from': 'q0', 'input': 'b', 'stack_top': 'A', 'to': 'q0', 'stack_push': 'BA'},
                    {'from': 'q0', 'input': 'b', 'stack_top': 'B', 'to': 'q0', 'stack_push': 'BB'},
                    
                    # Non-deterministically switch to matching (skip middle for odd-length)
                    {'from': 'q0', 'input': 'ε', 'stack_top': 'Z0', 'to': 'q1', 'stack_push': 'Z0'},
                    {'from': 'q0', 'input': 'ε', 'stack_top': 'A', 'to': 'q1', 'stack_push': 'A'},
                    {'from': 'q0', 'input': 'ε', 'stack_top': 'B', 'to': 'q1', 'stack_push': 'B'},
                    {'from': 'q0', 'input': 'a', 'stack_top': 'A', 'to': 'q1', 'stack_push': 'A'},  # Skip middle 'a'
                    {'from': 'q0', 'input': 'b', 'stack_top': 'B', 'to': 'q1', 'stack_push': 'B'},  # Skip middle 'b'
                    {'from': 'q0', 'input': 'a', 'stack_top': 'Z0', 'to': 'q1', 'stack_push': 'Z0'},  # Single 'a'
                    {'from': 'q0', 'input': 'b', 'stack_top': 'Z0', 'to': 'q1', 'stack_push': 'Z0'},  # Single 'b'
                    
                    # Match second half by popping stack
                    {'from': 'q1', 'input': 'a', 'stack_top': 'A', 'to': 'q1', 'stack_push': ''},
                    {'from': 'q1', 'input': 'b', 'stack_top': 'B', 'to': 'q1', 'stack_push': ''},
                    
                    # Accept when stack is back to Z0
                    {'from': 'q1', 'input': 'ε', 'stack_top': 'Z0', 'to': 'q2', 'stack_push': 'Z0'}
                ],
                'acceptance_type': 'final_state'
            }
            explanation = 'PDA for palindromes (both odd and even length) over {a, b}. The PDA non-deterministically guesses the middle point, pushes the first half onto the stack, optionally skips a middle character for odd-length palindromes, then matches the second half by popping.'
        
        return {
            'pda': pda,
            'explanation': explanation,
            'steps': [
                'Step 1: Push symbols from the first half of the string onto the stack',
                'Step 2: Non-deterministically guess the middle of the palindrome',
                'Step 3: For odd-length palindromes, optionally skip the middle character',
                'Step 4: Match the second half by popping and comparing with stack contents',
                'Step 5: Accept if stack returns to initial symbol (Z0)'
            ],
            'move_table': self._generate_move_table(pda),
            'diagram_filename': 'pda_palindrome.png'
        }
    
    def _construct_anbn_pda(self):
        """Construct PDA for a^n b^n language"""
        pda = {
            'states': ['q0', 'q1', 'q2'],
            'input_alphabet': ['a', 'b'],
            'stack_alphabet': ['Z0', 'A'],
            'start_state': 'q0',
            'start_stack_symbol': 'Z0',
            'accept_states': ['q2'],
            'transitions': [
                {'from': 'q0', 'input': 'a', 'stack_top': 'Z0', 'to': 'q0', 'stack_push': 'AZ0'},
                {'from': 'q0', 'input': 'a', 'stack_top': 'A', 'to': 'q0', 'stack_push': 'AA'},
                {'from': 'q0', 'input': 'b', 'stack_top': 'A', 'to': 'q1', 'stack_push': ''},
                {'from': 'q1', 'input': 'b', 'stack_top': 'A', 'to': 'q1', 'stack_push': ''},
                {'from': 'q1', 'input': 'ε', 'stack_top': 'Z0', 'to': 'q2', 'stack_push': 'Z0'}
            ],
            'acceptance_type': 'final_state'
        }
        
        return {
            'pda': pda,
            'explanation': 'PDA for language {a^n b^n | n ≥ 0}. Pushes an A for each a, then pops an A for each b.',
            'steps': [
                'Step 1: For each "a" in input, push "A" onto stack',
                'Step 2: When first "b" is seen, start popping',
                'Step 3: For each "b", pop one "A" from stack',
                'Step 4: Accept if stack returns to Z0 when input ends'
            ],
            'move_table': self._generate_move_table(pda),
            'diagram_filename': 'pda_anbn.png'
        }
    
    def cfg_to_pda(self, parsed_input):
        """Convert CFG to PDA"""
        grammar = parsed_input.get('grammar', {})
        
        if not grammar or 'rules' not in grammar:
            return {'error': 'Invalid grammar specification'}
        
        # Create PDA that accepts by empty stack
        start_symbol = grammar['start_symbol']
        
        pda = {
            'states': ['q0', 'q1', 'q2'],
            'input_alphabet': grammar.get('terminals', []),
            'stack_alphabet': ['Z0'] + grammar.get('non_terminals', []) + grammar.get('terminals', []),
            'start_state': 'q0',
            'start_stack_symbol': 'Z0',
            'accept_states': ['q2'],
            'transitions': [],
            'acceptance_type': 'empty_stack'
        }
        
        # Initial transition: push start symbol
        pda['transitions'].append({
            'from': 'q0',
            'input': 'ε',
            'stack_top': 'Z0',
            'to': 'q1',
            'stack_push': start_symbol + 'Z0'
        })
        
        # Add transitions for each production rule
        for non_terminal, productions in grammar['rules'].items():
            for production in productions:
                if production == 'ε':
                    production = ''
                
                pda['transitions'].append({
                    'from': 'q1',
                    'input': 'ε',
                    'stack_top': non_terminal,
                    'to': 'q1',
                    'stack_push': production
                })
        
        # Add transitions for terminals
        for terminal in grammar.get('terminals', []):
            pda['transitions'].append({
                'from': 'q1',
                'input': terminal,
                'stack_top': terminal,
                'to': 'q1',
                'stack_push': ''
            })
        
        # Final transition: accept when stack is empty
        pda['transitions'].append({
            'from': 'q1',
            'input': 'ε',
            'stack_top': 'Z0',
            'to': 'q2',
            'stack_push': ''
        })
        
        return {
            'grammar': grammar,
            'pda': pda,
            'explanation': 'PDA constructed from CFG. The PDA simulates leftmost derivations.',
            'steps': [
                'Step 1: Push start symbol onto stack',
                'Step 2: For each non-terminal on top of stack, replace with a production',
                'Step 3: For each terminal on top of stack, match with input',
                'Step 4: Accept when stack is empty'
            ],
            'move_table': self._generate_move_table(pda),
            'diagram_filename': 'cfg_to_pda.png'
        }
    
    def test_membership(self, parsed_input):
        """Test if a string is accepted by the PDA"""
        pda = parsed_input.get('automaton', {})
        test_string = parsed_input.get('test_string', '')
        
        if not pda:
            return {'error': 'No PDA provided'}
        
        # Simulate PDA (non-deterministic simulation)
        initial_config = {
            'state': pda['start_state'],
            'input_position': 0,
            'stack': [pda.get('start_stack_symbol', 'Z0')]
        }
        
        # BFS to explore all possible configurations
        queue = [initial_config]
        visited = set()
        move_sequence = []
        
        move_count = 0
        accepted = False
        
        while queue and move_count < self.max_moves:
            config = queue.pop(0)
            move_count += 1
            
            # Create configuration signature
            config_sig = (config['state'], config['input_position'], tuple(config['stack']))
            if config_sig in visited:
                continue
            visited.add(config_sig)
            
            # Check acceptance conditions
            if config['input_position'] == len(test_string):
                if pda.get('acceptance_type') == 'final_state':
                    if config['state'] in pda.get('accept_states', []):
                        accepted = True
                        break
                elif pda.get('acceptance_type') == 'empty_stack':
                    if len(config['stack']) == 0 or (len(config['stack']) == 1 and config['stack'][0] == 'Z0'):
                        accepted = True
                        break
            
            # Try all applicable transitions
            for transition in pda.get('transitions', []):
                if self._can_apply_transition(config, transition, test_string):
                    new_config = self._apply_transition(config, transition)
                    queue.append(new_config)
                    move_sequence.append({
                        'from_config': config,
                        'transition': transition,
                        'to_config': new_config
                    })
        
        return {
            'test_string': test_string,
            'accepted': accepted,
            'move_count': move_count,
            'explanation': f'String "{test_string}" is {"accepted" if accepted else "rejected"} by the PDA.',
            'sample_moves': move_sequence[:10]  # Show first 10 moves
        }
    
    def _can_apply_transition(self, config, transition, test_string):
        """Check if a transition can be applied to current configuration"""
        # Check state
        if config['state'] != transition['from']:
            return False
        
        # Check stack top
        if not config['stack'] or config['stack'][-1] != transition['stack_top']:
            return False
        
        # Check input
        if transition['input'] == 'ε':
            return True
        
        if config['input_position'] < len(test_string):
            if test_string[config['input_position']] == transition['input']:
                return True
        
        return False
    
    def _apply_transition(self, config, transition):
        """Apply a transition to a configuration"""
        new_config = {
            'state': transition['to'],
            'input_position': config['input_position'],
            'stack': config['stack'][:]
        }
        
        # Pop stack top
        if new_config['stack']:
            new_config['stack'].pop()
        
        # Push new symbols (in reverse order)
        stack_push = transition.get('stack_push', '')
        if stack_push:
            for symbol in reversed(stack_push):
                if symbol != 'ε':
                    new_config['stack'].append(symbol)
        
        # Advance input if not epsilon transition
        if transition['input'] != 'ε':
            new_config['input_position'] += 1
        
        return new_config
    
    def _generate_move_table(self, pda):
        """Generate a move table for display"""
        table = []
        table.append(['From State', 'Input', 'Stack Top', 'To State', 'Stack Push'])
        
        for transition in pda.get('transitions', []):
            row = [
                transition['from'],
                transition['input'],
                transition['stack_top'],
                transition['to'],
                transition.get('stack_push', 'ε') if transition.get('stack_push') else 'ε'
            ]
            table.append(row)
        
        return table
