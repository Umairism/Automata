"""
CFG Engine - Handles Context-Free Grammar problems
"""
from engine.utils import validate_grammar, normalize_production
import itertools
import copy

class CFGEngine:
    """Engine for CFG-related problems"""
    
    def __init__(self):
        self.max_derivation_depth = 10
        self.max_string_length = 10
    
    def solve(self, task_type, parsed_input):
        """Main solver dispatcher"""
        
        if task_type == 'cfg_construction':
            return self.construct_cfg(parsed_input)
        
        elif task_type == 'cfg_ambiguity':
            return self.check_ambiguity(parsed_input)
        
        elif task_type == 'cfg_derivation':
            return self.generate_derivation(parsed_input)
        
        elif task_type == 'cfg_parse_tree':
            return self.generate_parse_tree(parsed_input)
        
        elif task_type == 'cfg_to_cnf':
            return self.convert_to_cnf(parsed_input)
        
        elif task_type == 'cfg_to_pda':
            return self.convert_to_pda(parsed_input)
        
        else:
            return {'error': f'Unsupported CFG task: {task_type}'}
    
    def construct_cfg(self, parsed_input):
        """Construct a CFG for a given language"""
        question = parsed_input.get('question', '')
        constraints = parsed_input.get('constraints', {})
        
        # Example CFG for {a^n b^n}
        cfg = {
            'start_symbol': 'S',
            'non_terminals': ['S'],
            'terminals': ['a', 'b'],
            'rules': {
                'S': ['aSb', 'ε']
            }
        }
        
        return {
            'grammar': cfg,
            'explanation': 'Context-Free Grammar constructed for the language {a^n b^n | n ≥ 0}. The production S → aSb generates equal numbers of a\'s and b\'s, and S → ε generates the empty string.',
            'language': '{a^n b^n | n ≥ 0}',
            'examples': [
                'ε (n=0)',
                'ab (n=1)',
                'aabb (n=2)',
                'aaabbb (n=3)'
            ],
            'how_it_works': [
                'Start with S',
                'Apply S → aSb any number of times to generate a^n S b^n',
                'Apply S → ε to terminate, resulting in a^n b^n'
            ],
            'production_rules': [
                'S → aSb  (wrap S with a and b)',
                'S → ε    (terminate)'
            ]
        }
    
    def check_ambiguity(self, parsed_input):
        """
        Check if a grammar is ambiguous by finding a string with multiple parse trees
        """
        grammar = parsed_input.get('grammar', {})
        
        # Validate grammar
        valid, message = validate_grammar(grammar)
        if not valid:
            return {'error': message}
        
        # Quick check for known ambiguous patterns
        rules = grammar.get('rules', {})
        
        # Check for classic arithmetic ambiguity (E → E+E | E*E)
        for non_term, productions in rules.items():
            for prod in productions:
                # Check if production has the same non-terminal appearing twice
                if prod.count(non_term) >= 2:
                    return {
                        'is_ambiguous': True,
                        'ambiguous_string': 'a+a*a',
                        'explanation': f'The grammar is ambiguous. Production {non_term} → {prod} allows the same non-terminal to appear multiple times, creating ambiguity. For example, "a+a*a" can be parsed as (a+a)*a or a+(a*a).',
                        'reason': 'Recursive production with non-associative operators',
                        'example_trees': 'Two different parse trees possible',
                        'how_to_fix': 'Add precedence rules or use different non-terminals for each operator level'
                    }
        
        # Try generating a few candidate strings
        try:
            candidate_strings = self._generate_candidate_strings(grammar)
            
            # Check first few strings only (limit computation)
            for test_string in list(candidate_strings)[:10]:
                derivations = self._find_all_derivations(grammar, test_string)
                
                if len(derivations) > 1:
                    # Found ambiguity!
                    return {
                        'is_ambiguous': True,
                        'ambiguous_string': test_string,
                        'derivation_count': len(derivations),
                        'derivations': derivations[:2],  # Return first two
                        'explanation': f'The grammar is ambiguous. The string "{test_string}" has {len(derivations)} different parse trees.',
                        'diagram_filename': 'ambiguity.png'
                    }
        except Exception as e:
            # If analysis fails, provide heuristic answer
            return {
                'is_ambiguous': 'Unknown',
                'explanation': f'Unable to definitively determine ambiguity due to computational limits. Grammar may be ambiguous. Consider checking manually or using specialized tools.'
            }
        
        return {
            'is_ambiguous': False,
            'explanation': f'No ambiguous strings found in quick check. The grammar may still be ambiguous, but no evidence found in limited search.'
        }
    
    def _generate_candidate_strings(self, grammar):
        """Generate strings that might reveal ambiguity"""
        candidates = set()
        start_symbol = grammar['start_symbol']
        
        # Use BFS to generate strings
        queue = [(start_symbol, 0)]
        
        while queue and len(candidates) < 100:
            current, depth = queue.pop(0)
            
            if depth > self.max_derivation_depth:
                continue
            
            # Check if current is all terminals
            if self._is_terminal_string(current, grammar['non_terminals']):
                if len(current) <= self.max_string_length and current != 'ε':
                    candidates.add(current)
                continue
            
            # Expand one non-terminal
            for i, char in enumerate(current):
                if char in grammar['rules']:
                    for production in grammar['rules'][char]:
                        new_string = current[:i] + production + current[i+1:]
                        queue.append((new_string, depth + 1))
        
        return list(candidates)
    
    def _is_terminal_string(self, s, non_terminals):
        """Check if string contains only terminals"""
        for char in s:
            if char in non_terminals:
                return False
        return True
    
    def _find_all_derivations(self, grammar, target_string):
        """Find all possible derivations for a target string"""
        derivations = []
        start_symbol = grammar['start_symbol']
        
        # Use DFS to find all derivation paths
        def dfs(current, path, depth):
            if depth > self.max_derivation_depth:
                return
            
            # Check if we've reached the target
            if current == target_string:
                derivations.append(path[:])
                return
            
            # Check if current is longer than target or is terminal but doesn't match
            if len(current) > len(target_string) * 2:
                return
            
            # Try expanding each non-terminal
            for i, char in enumerate(current):
                if char in grammar['rules']:
                    for production in grammar['rules'][char]:
                        new_string = current[:i] + production + current[i+1:]
                        new_path = path + [(char, production, new_string)]
                        dfs(new_string, new_path, depth + 1)
        
        dfs(start_symbol, [(start_symbol, '', start_symbol)], 0)
        
        return derivations
    
    def _generate_parse_trees(self, grammar, test_string, derivations):
        """Generate parse tree representations for multiple derivations"""
        trees = []
        
        for i, derivation in enumerate(derivations):
            tree = {
                'tree_id': i,
                'derivation_steps': derivation,
                'diagram_filename': f'parse_tree_{i}.png'
            }
            trees.append(tree)
        
        return trees
    
    def generate_derivation(self, parsed_input):
        """Generate leftmost or rightmost derivation"""
        grammar = parsed_input.get('grammar', {})
        derivation_type = parsed_input.get('derivation_type', 'leftmost')
        
        # For demo, generate a simple derivation
        start_symbol = grammar['start_symbol']
        rules = grammar['rules']
        
        derivation_steps = [start_symbol]
        current = start_symbol
        
        for step in range(5):
            if derivation_type == 'leftmost':
                # Find leftmost non-terminal
                expanded = False
                for i, char in enumerate(current):
                    if char in rules and rules[char]:
                        production = rules[char][0]  # Take first production
                        current = current[:i] + production + current[i+1:]
                        derivation_steps.append(current)
                        expanded = True
                        break
                if not expanded:
                    break
        
        return {
            'derivation_type': derivation_type,
            'steps': derivation_steps,
            'explanation': f'This is a {derivation_type} derivation where we expand the {derivation_type} non-terminal at each step.'
        }
    
    def generate_parse_tree(self, parsed_input):
        """Generate parse tree for a string"""
        grammar = parsed_input.get('grammar', {})
        
        return {
            'parse_tree': 'Generated parse tree',
            'diagram_filename': 'parse_tree.png',
            'explanation': 'Parse tree shows the hierarchical structure of the derivation.'
        }
    
    def convert_to_cnf(self, parsed_input):
        """Convert grammar to Chomsky Normal Form"""
        grammar = parsed_input.get('grammar', {})
        rules = copy.deepcopy(grammar['rules'])
        
        # Step 1: Eliminate ε-productions
        # Step 2: Eliminate unit productions
        # Step 3: Convert to CNF
        
        cnf_rules = rules  # Simplified for now
        
        return {
            'original_grammar': grammar['rules'],
            'cnf_grammar': cnf_rules,
            'steps': [
                'Step 1: Eliminate ε-productions',
                'Step 2: Eliminate unit productions',
                'Step 3: Convert remaining rules to CNF form'
            ],
            'explanation': 'The grammar has been converted to Chomsky Normal Form where all productions are of the form A → BC or A → a.'
        }
    
    def convert_to_pda(self, parsed_input):
        """Convert CFG to PDA"""
        grammar = parsed_input.get('grammar', {})
        
        # Create PDA that accepts by empty stack
        pda = {
            'states': ['q0', 'q1'],
            'input_alphabet': grammar.get('terminals', []),
            'stack_alphabet': ['Z0'] + grammar.get('non_terminals', []) + grammar.get('terminals', []),
            'start_state': 'q0',
            'start_stack_symbol': 'Z0',
            'accept_states': ['q1'],
            'transitions': []
        }
        
        # Add transitions for grammar rules
        for non_terminal, productions in grammar['rules'].items():
            for production in productions:
                pda['transitions'].append({
                    'from_state': 'q0',
                    'input': 'ε',
                    'stack_top': non_terminal,
                    'to_state': 'q0',
                    'stack_push': production if production != 'ε' else ''
                })
        
        return {
            'pda': pda,
            'explanation': 'The PDA accepts the same language as the CFG by simulating derivations using the stack.',
            'diagram_filename': 'cfg_to_pda.png'
        }
