"""
LBA Engine - Handles Linear Bounded Automaton problems
"""

class LBAEngine:
    """Engine for Linear Bounded Automaton (LBA) problems"""
    
    def __init__(self):
        pass
    
    def solve(self, task_type, parsed_input):
        """Main solver dispatcher"""
        
        if task_type == 'lba_construction':
            return self.construct_lba(parsed_input)
        
        else:
            return {'error': f'Unsupported LBA task: {task_type}'}
    
    def construct_lba(self, parsed_input):
        """Construct a Linear Bounded Automaton"""
        question = parsed_input.get('question', '')
        constraints = parsed_input.get('constraints', {})
        
        # Example: LBA for a^n b^n c^n
        lba = {
            'states': ['q0', 'q1', 'q2', 'q3', 'q4', 'qaccept'],
            'input_alphabet': ['a', 'b', 'c'],
            'tape_alphabet': ['a', 'b', 'c', 'X', 'Y', 'Z', '⊔'],
            'start_state': 'q0',
            'accept_states': ['qaccept'],
            'transitions': [
                # Mark first 'a' with 'X'
                {'from': 'q0', 'read': 'a', 'to': 'q1', 'write': 'X', 'move': 'R'},
                
                # Find corresponding 'b', mark with 'Y'
                {'from': 'q1', 'read': 'a', 'to': 'q1', 'write': 'a', 'move': 'R'},
                {'from': 'q1', 'read': 'Y', 'to': 'q1', 'write': 'Y', 'move': 'R'},
                {'from': 'q1', 'read': 'b', 'to': 'q2', 'write': 'Y', 'move': 'R'},
                
                # Find corresponding 'c', mark with 'Z'
                {'from': 'q2', 'read': 'b', 'to': 'q2', 'write': 'b', 'move': 'R'},
                {'from': 'q2', 'read': 'Z', 'to': 'q2', 'write': 'Z', 'move': 'R'},
                {'from': 'q2', 'read': 'c', 'to': 'q3', 'write': 'Z', 'move': 'L'},
                
                # Return to start and repeat
                {'from': 'q3', 'read': 'a', 'to': 'q3', 'write': 'a', 'move': 'L'},
                {'from': 'q3', 'read': 'b', 'to': 'q3', 'write': 'b', 'move': 'L'},
                {'from': 'q3', 'read': 'Y', 'to': 'q3', 'write': 'Y', 'move': 'L'},
                {'from': 'q3', 'read': 'Z', 'to': 'q3', 'write': 'Z', 'move': 'L'},
                {'from': 'q3', 'read': 'X', 'to': 'q0', 'write': 'X', 'move': 'R'},
                
                # Check if all marked
                {'from': 'q0', 'read': 'Y', 'to': 'q4', 'write': 'Y', 'move': 'R'},
                {'from': 'q4', 'read': 'Y', 'to': 'q4', 'write': 'Y', 'move': 'R'},
                {'from': 'q4', 'read': 'Z', 'to': 'q4', 'write': 'Z', 'move': 'R'},
                {'from': 'q4', 'read': '⊔', 'to': 'qaccept', 'write': '⊔', 'move': 'R'}
            ],
            'tape_bound': 'linear'  # Tape length = input length
        }
        
        return {
            'lba': lba,
            'machine_type': 'Linear Bounded Automaton',
            'explanation': 'Linear Bounded Automaton (LBA) constructed. An LBA is a Turing Machine where the tape head cannot move beyond the input length.',
            'key_properties': [
                'Tape length is bounded by a linear function of input length',
                'Can recognize context-sensitive languages',
                'More powerful than PDA, less powerful than TM',
                'Tape head cannot move beyond input boundaries',
                'Uses special tape alphabet with markers'
            ],
            'algorithm': [
                'Step 1: Mark the first \'a\' with \'X\'',
                'Step 2: Scan right to find first unmarked \'b\', mark with \'Y\'',
                'Step 3: Continue right to find first unmarked \'c\', mark with \'Z\'',
                'Step 4: Return to leftmost \'X\' and repeat',
                'Step 5: Accept if all symbols are marked and counts match'
            ],
            'example_language': '{a^n b^n c^n | n ≥ 1}',
            'complexity_class': 'Context-Sensitive Language (CSL)',
            'transition_table': self._generate_lba_table(lba),
            'comparison': {
                'vs_PDA': 'LBA can recognize {a^n b^n c^n}, PDA cannot',
                'vs_TM': 'LBA has bounded tape, TM has unbounded tape',
                'power': 'PDA < LBA < TM'
            },
            'diagram_filename': 'lba_construction.png'
        }
    
    def _generate_lba_table(self, lba):
        """Generate transition table for LBA"""
        headers = ['Current State', 'Read Symbol', 'Next State', 'Write Symbol', 'Move']
        rows = []
        
        for trans in lba['transitions']:
            rows.append({
                'Current State': trans['from'],
                'Read Symbol': trans['read'],
                'Next State': trans['to'],
                'Write Symbol': trans['write'],
                'Move': trans['move']
            })
        
        return {
            'headers': headers,
            'rows': rows
        }
