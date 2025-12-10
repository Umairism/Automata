"""
Turing Machine Engine - Handles Turing Machine problems
"""

class TMEngine:
    """Engine for Turing Machine-related problems"""
    
    def __init__(self):
        self.max_steps = 1000
        self.blank_symbol = 'B'
    
    def solve(self, task_type, parsed_input):
        """Main solver dispatcher"""
        
        if task_type == 'tm_construction':
            return self.construct_tm(parsed_input)
        
        elif task_type == 'tm_trace':
            return self.trace_tm(parsed_input)
        
        elif task_type == 'tm_membership':
            return self.test_membership(parsed_input)
        
        else:
            return {'error': f'Unsupported TM task: {task_type}'}
    
    def construct_tm(self, parsed_input):
        """Construct a Turing Machine from language description"""
        question = parsed_input.get('question', '').lower()
        constraints = parsed_input.get('constraints', {})
        
        # Detect pattern: a^n b^2n
        if 'b2n' in question or 'b^2n' in question or ('anb' in question and '2n' in question):
            tm = {
                'states': ['q0', 'q1', 'q2', 'q3', 'q4', 'q_accept', 'q_reject'],
                'input_alphabet': ['a', 'b'],
                'tape_alphabet': ['a', 'b', 'X', 'Y', 'B'],
                'start_state': 'q0',
                'accept_state': 'q_accept',
                'reject_state': 'q_reject',
                'blank_symbol': 'B',
                'transitions': [
                    # Mark first 'a' with 'X' and move right
                    {'from': 'q0', 'read': 'a', 'to': 'q1', 'write': 'X', 'move': 'R'},
                    
                    # State q1: Scan right past unmarked 'a's and marked 'Y's (skip loop)
                    {'from': 'q1', 'read': 'a', 'to': 'q1', 'write': 'a', 'move': 'R'},
                    {'from': 'q1', 'read': 'Y', 'to': 'q1', 'write': 'Y', 'move': 'R'},  # SKIP LOOP
                    {'from': 'q1', 'read': 'b', 'to': 'q2', 'write': 'Y', 'move': 'R'},
                    
                    # State q2: Find and mark second 'b' with 'Y'
                    {'from': 'q2', 'read': 'b', 'to': 'q3', 'write': 'Y', 'move': 'L'},
                    
                    # State q3: Rewind to the leftmost 'X', passing over marked symbols
                    {'from': 'q3', 'read': 'Y', 'to': 'q3', 'write': 'Y', 'move': 'L'},  # SKIP LOOP
                    {'from': 'q3', 'read': 'a', 'to': 'q3', 'write': 'a', 'move': 'L'},
                    {'from': 'q3', 'read': 'X', 'to': 'q0', 'write': 'X', 'move': 'R'},
                    
                    # All 'a's processed, check if all 'b's are marked
                    {'from': 'q0', 'read': 'Y', 'to': 'q4', 'write': 'Y', 'move': 'R'},
                    {'from': 'q4', 'read': 'Y', 'to': 'q4', 'write': 'Y', 'move': 'R'},
                    {'from': 'q4', 'read': 'B', 'to': 'q_accept', 'write': 'B', 'move': 'R'}
                ]
            }
            explanation = 'Turing Machine for L={aⁿb²ⁿ|n≥1}. The TM marks each "a" with X, then marks two "b"s with Y for each X, and rewinds to repeat until all symbols are marked.'
        
        # Default: TM for a^n b^n c^n
        else:
            tm = {
                'states': ['q0', 'q1', 'q2', 'q3', 'q_accept', 'q_reject'],
                'input_alphabet': ['a', 'b', 'c'],
                'tape_alphabet': ['a', 'b', 'c', 'X', 'Y', 'Z', 'B'],
                'start_state': 'q0',
                'accept_state': 'q_accept',
                'reject_state': 'q_reject',
                'blank_symbol': 'B',
                'transitions': [
                    {'from': 'q0', 'read': 'a', 'to': 'q1', 'write': 'X', 'move': 'R'},
                    {'from': 'q1', 'read': 'a', 'to': 'q1', 'write': 'a', 'move': 'R'},
                    {'from': 'q1', 'read': 'Y', 'to': 'q1', 'write': 'Y', 'move': 'R'},  # SKIP LOOP
                    {'from': 'q1', 'read': 'b', 'to': 'q2', 'write': 'Y', 'move': 'R'},
                    {'from': 'q2', 'read': 'b', 'to': 'q2', 'write': 'b', 'move': 'R'},
                    {'from': 'q2', 'read': 'Z', 'to': 'q2', 'write': 'Z', 'move': 'R'},  # SKIP LOOP
                    {'from': 'q2', 'read': 'c', 'to': 'q3', 'write': 'Z', 'move': 'L'},
                    {'from': 'q3', 'read': 'Z', 'to': 'q3', 'write': 'Z', 'move': 'L'},  # SKIP LOOP
                    {'from': 'q3', 'read': 'Y', 'to': 'q3', 'write': 'Y', 'move': 'L'},  # SKIP LOOP
                    {'from': 'q3', 'read': 'b', 'to': 'q3', 'write': 'b', 'move': 'L'},
                    {'from': 'q3', 'read': 'a', 'to': 'q3', 'write': 'a', 'move': 'L'},
                    {'from': 'q3', 'read': 'X', 'to': 'q0', 'write': 'X', 'move': 'R'},
                    {'from': 'q0', 'read': 'Y', 'to': 'q_accept', 'write': 'Y', 'move': 'R'}
                ]
            }
            explanation = 'Turing Machine for L={aⁿbⁿcⁿ|n≥1}. The TM marks one a, one b, and one c in each pass, then rewinds to repeat until all symbols are marked.'
        
        return {
            'tm': tm,
            'explanation': explanation,
            'move_table': self._generate_move_table(tm),
            'diagram_filename': 'tm_construction.png'
        }
    
    def trace_tm(self, parsed_input):
        """Trace execution of a Turing Machine on an input"""
        tm = parsed_input.get('automaton', {})
        input_string = parsed_input.get('input_string', '')
        
        if not tm:
            return {'error': 'No Turing Machine provided'}
        
        # Initialize tape
        tape = list(input_string) + [self.blank_symbol] * 10
        head_position = 0
        current_state = tm.get('start_state', 'q0')
        
        configurations = []
        step = 0
        
        while step < self.max_steps:
            # Record current configuration
            config = {
                'step': step,
                'state': current_state,
                'tape': ''.join(tape),
                'head_position': head_position
            }
            configurations.append(config)
            
            # Check for halt
            if current_state == tm.get('accept_state') or current_state == tm.get('reject_state'):
                break
            
            # Find applicable transition
            current_symbol = tape[head_position]
            transition = self._find_transition(tm, current_state, current_symbol)
            
            if not transition:
                # No transition found, halt and reject
                current_state = tm.get('reject_state', 'q_reject')
                break
            
            # Apply transition
            tape[head_position] = transition['write']
            current_state = transition['to']
            
            # Move head
            if transition['move'] == 'R':
                head_position += 1
                if head_position >= len(tape):
                    tape.append(self.blank_symbol)
            elif transition['move'] == 'L':
                head_position = max(0, head_position - 1)
            
            step += 1
        
        # Final configuration
        final_config = {
            'step': step,
            'state': current_state,
            'tape': ''.join(tape),
            'head_position': head_position
        }
        configurations.append(final_config)
        
        accepted = current_state == tm.get('accept_state')
        
        return {
            'input_string': input_string,
            'accepted': accepted,
            'final_state': current_state,
            'total_steps': step,
            'configurations': configurations,
            'explanation': f'TM {"accepted" if accepted else "rejected"} the input after {step} steps.',
            'tape_diagram_filename': 'tm_tape_trace.png'
        }
    
    def test_membership(self, parsed_input):
        """Test if a string is accepted by the Turing Machine"""
        return self.trace_tm(parsed_input)
    
    def _find_transition(self, tm, state, symbol):
        """Find a transition for the given state and symbol"""
        for transition in tm.get('transitions', []):
            if transition['from'] == state and transition['read'] == symbol:
                return transition
        return None
    
    def _generate_move_table(self, tm):
        """Generate a move table for display"""
        table = []
        table.append(['Current State', 'Read Symbol', 'Next State', 'Write Symbol', 'Move'])
        
        for transition in tm.get('transitions', []):
            row = [
                transition['from'],
                transition['read'],
                transition['to'],
                transition['write'],
                transition['move']
            ]
            table.append(row)
        
        return table
