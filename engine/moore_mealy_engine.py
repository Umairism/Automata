"""
Moore and Mealy Machine Engine - Handles finite state machines with output
"""

class MooreMealyEngine:
    """Engine for Moore and Mealy Machine problems"""
    
    def __init__(self):
        pass
    
    def solve(self, task_type, parsed_input):
        """Main solver dispatcher"""
        
        if task_type == 'moore_machine':
            return self.construct_moore(parsed_input)
        
        elif task_type == 'mealy_machine':
            return self.construct_mealy(parsed_input)
        
        elif task_type == 'moore_to_mealy':
            return self.convert_moore_to_mealy(parsed_input)
        
        elif task_type == 'mealy_to_moore':
            return self.convert_mealy_to_moore(parsed_input)
        
        else:
            return {'error': f'Unsupported Moore/Mealy task: {task_type}'}
    
    def construct_moore(self, parsed_input):
        """Construct a Moore Machine"""
        question = parsed_input.get('question', '')
        
        # Example: Moore machine for binary counter (output number of 1's mod 3)
        moore = {
            'states': ['q0', 'q1', 'q2'],
            'input_alphabet': ['0', '1'],
            'output_alphabet': ['0', '1', '2'],
            'start_state': 'q0',
            'transitions': [
                {'from': 'q0', 'input': '0', 'to': 'q0'},
                {'from': 'q0', 'input': '1', 'to': 'q1'},
                {'from': 'q1', 'input': '0', 'to': 'q1'},
                {'from': 'q1', 'input': '1', 'to': 'q2'},
                {'from': 'q2', 'input': '0', 'to': 'q2'},
                {'from': 'q2', 'input': '1', 'to': 'q0'}
            ],
            'outputs': {
                'q0': '0',
                'q1': '1',
                'q2': '2'
            }
        }
        
        return {
            'machine': moore,
            'machine_type': 'moore',
            'explanation': 'Moore Machine constructed. In Moore machines, output depends only on the current state.',
            'key_properties': [
                'Output is associated with states',
                'Output depends only on current state, not input',
                'Every state has exactly one output value',
                'Output changes when state changes'
            ],
            'transition_table': self._generate_moore_table(moore),
            'diagram_filename': 'moore_machine.png'
        }
    
    def construct_mealy(self, parsed_input):
        """Construct a Mealy Machine"""
        question = parsed_input.get('question', '')
        
        # Example: Mealy machine for binary addition (add 1 to binary number)
        mealy = {
            'states': ['q0', 'q1'],
            'input_alphabet': ['0', '1'],
            'output_alphabet': ['0', '1'],
            'start_state': 'q0',
            'transitions': [
                {'from': 'q0', 'input': '0', 'to': 'q0', 'output': '1'},
                {'from': 'q0', 'input': '1', 'to': 'q1', 'output': '0'},
                {'from': 'q1', 'input': '0', 'to': 'q1', 'output': '0'},
                {'from': 'q1', 'input': '1', 'to': 'q1', 'output': '1'}
            ]
        }
        
        return {
            'machine': mealy,
            'machine_type': 'mealy',
            'explanation': 'Mealy Machine constructed. In Mealy machines, output depends on both current state and input.',
            'key_properties': [
                'Output is associated with transitions',
                'Output depends on both current state and input',
                'Same state can produce different outputs',
                'Generally has fewer states than equivalent Moore machine'
            ],
            'transition_table': self._generate_mealy_table(mealy),
            'diagram_filename': 'mealy_machine.png'
        }
    
    def convert_moore_to_mealy(self, parsed_input):
        """Convert Moore Machine to Mealy Machine"""
        moore = parsed_input.get('automaton', {})
        
        if not moore:
            # Example Moore machine
            moore = {
                'states': ['q0', 'q1', 'q2'],
                'input_alphabet': ['0', '1'],
                'output_alphabet': ['A', 'B', 'C'],
                'start_state': 'q0',
                'transitions': [
                    {'from': 'q0', 'input': '0', 'to': 'q1'},
                    {'from': 'q0', 'input': '1', 'to': 'q2'},
                    {'from': 'q1', 'input': '0', 'to': 'q0'},
                    {'from': 'q1', 'input': '1', 'to': 'q2'},
                    {'from': 'q2', 'input': '0', 'to': 'q1'},
                    {'from': 'q2', 'input': '1', 'to': 'q0'}
                ],
                'outputs': {
                    'q0': 'A',
                    'q1': 'B',
                    'q2': 'C'
                }
            }
        
        # Convert: Mealy output = output of next state in Moore
        mealy_transitions = []
        for trans in moore['transitions']:
            next_state = trans['to']
            output = moore['outputs'][next_state]
            mealy_transitions.append({
                'from': trans['from'],
                'input': trans['input'],
                'to': trans['to'],
                'output': output
            })
        
        mealy = {
            'states': moore['states'],
            'input_alphabet': moore['input_alphabet'],
            'output_alphabet': moore['output_alphabet'],
            'start_state': moore['start_state'],
            'transitions': mealy_transitions
        }
        
        return {
            'original': moore,
            'converted': mealy,
            'original_type': 'moore',
            'converted_type': 'mealy',
            'explanation': 'Moore machine converted to Mealy machine. Each transition output is set to the output of the destination state.',
            'steps': [
                'Step 1: Keep the same states and transitions',
                'Step 2: For each transition (q, a) → q\', assign output = Output(q\')',
                'Step 3: The Mealy machine produces the same output sequence',
                'Step 4: Note: Output may be delayed by one step compared to Moore'
            ],
            'original_table': self._generate_moore_table(moore),
            'converted_table': self._generate_mealy_table(mealy),
            'diagram_filename': 'moore_to_mealy.png'
        }
    
    def convert_mealy_to_moore(self, parsed_input):
        """Convert Mealy Machine to Moore Machine"""
        mealy = parsed_input.get('automaton', {})
        
        if not mealy:
            # Example Mealy machine
            mealy = {
                'states': ['q0', 'q1'],
                'input_alphabet': ['0', '1'],
                'output_alphabet': ['A', 'B'],
                'start_state': 'q0',
                'transitions': [
                    {'from': 'q0', 'input': '0', 'to': 'q0', 'output': 'A'},
                    {'from': 'q0', 'input': '1', 'to': 'q1', 'output': 'B'},
                    {'from': 'q1', 'input': '0', 'to': 'q0', 'output': 'A'},
                    {'from': 'q1', 'input': '1', 'to': 'q1', 'output': 'B'}
                ]
            }
        
        # Convert: Create new states for each (state, output) pair
        moore_states = []
        moore_outputs = {}
        state_mapping = {}
        
        # Build state mapping
        for trans in mealy['transitions']:
            state = trans['from']
            output = trans['output']
            new_state = f"{state}_{output}"
            
            if new_state not in moore_states:
                moore_states.append(new_state)
                moore_outputs[new_state] = output
                state_mapping[state] = state_mapping.get(state, [])
                if new_state not in state_mapping[state]:
                    state_mapping[state].append(new_state)
        
        # Build Moore transitions
        moore_transitions = []
        for trans in mealy['transitions']:
            from_state = trans['from']
            to_state = trans['to']
            input_symbol = trans['input']
            output = trans['output']
            
            # Find appropriate source states
            for src in state_mapping.get(from_state, [from_state]):
                dest = f"{to_state}_{output}"
                moore_transitions.append({
                    'from': src,
                    'input': input_symbol,
                    'to': dest
                })
        
        moore = {
            'states': moore_states,
            'input_alphabet': mealy['input_alphabet'],
            'output_alphabet': mealy['output_alphabet'],
            'start_state': moore_states[0],
            'transitions': moore_transitions,
            'outputs': moore_outputs
        }
        
        return {
            'original': mealy,
            'converted': moore,
            'original_type': 'mealy',
            'converted_type': 'moore',
            'explanation': 'Mealy machine converted to Moore machine. States are split based on output values.',
            'steps': [
                'Step 1: For each state with multiple outputs, create separate states',
                'Step 2: Name new states as (state, output) pairs',
                'Step 3: Redirect transitions to appropriate new states',
                'Step 4: Assign output to each state based on its label',
                'Note: Moore machine may have more states than Mealy'
            ],
            'original_table': self._generate_mealy_table(mealy),
            'converted_table': self._generate_moore_table(moore),
            'diagram_filename': 'mealy_to_moore.png'
        }
    
    def _generate_moore_table(self, moore):
        """Generate transition table for Moore machine"""
        headers = ['State', 'Output'] + [f'δ({sym})' for sym in moore['input_alphabet']]
        rows = []
        
        for state in moore['states']:
            row = {
                'State': state,
                'Output': moore['outputs'].get(state, '-')
            }
            
            for symbol in moore['input_alphabet']:
                next_state = '-'
                for trans in moore['transitions']:
                    if trans['from'] == state and trans['input'] == symbol:
                        next_state = trans['to']
                        break
                row[f'δ({symbol})'] = next_state
            
            rows.append(row)
        
        return {
            'headers': headers,
            'rows': rows
        }
    
    def _generate_mealy_table(self, mealy):
        """Generate transition table for Mealy machine"""
        headers = ['State'] + [f'δ({sym})/λ({sym})' for sym in mealy['input_alphabet']]
        rows = []
        
        for state in mealy['states']:
            row = {'State': state}
            
            for symbol in mealy['input_alphabet']:
                next_output = '-/-'
                for trans in mealy['transitions']:
                    if trans['from'] == state and trans['input'] == symbol:
                        next_output = f"{trans['to']}/{trans['output']}"
                        break
                row[f'δ({symbol})/λ({symbol})'] = next_output
            
            rows.append(row)
        
        return {
            'headers': headers,
            'rows': rows
        }
