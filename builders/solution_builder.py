"""
Solution Builder - Assembles final solutions with diagrams and explanations
"""
from diagrams.renderer import DiagramRenderer
import uuid

class SolutionBuilder:
    """Build comprehensive solutions from engine results"""
    
    def __init__(self):
        self.renderer = DiagramRenderer()
    
    def build(self, result, task_type):
        """
        Build a complete solution from engine result
        
        Args:
            result: Dictionary from engine
            task_type: Type of task
        
        Returns:
            dict: Complete solution with diagrams, tables, and explanation
        """
        if 'error' in result:
            return result
        
        solution = {
            'task_type': task_type,
            'success': True,
            'explanation': result.get('explanation', ''),
            'diagrams': [],
            'tables': [],
            'steps': result.get('steps', []),
            'details': {}
        }
        
        # Generate diagrams based on task type
        if task_type in ['cfg_ambiguity']:
            solution = self._build_cfg_ambiguity_solution(result, solution)
        
        elif task_type in ['cfg_derivation']:
            solution = self._build_derivation_solution(result, solution)
        
        elif task_type in ['dfa_construction', 'nfa_to_dfa', 'dfa_minimization']:
            solution = self._build_dfa_solution(result, solution)
        
        elif task_type in ['re_to_nfa']:
            solution = self._build_regex_solution(result, solution)
        
        elif task_type in ['pda_construction', 'pda_from_cfg']:
            solution = self._build_pda_solution(result, solution)
        
        elif task_type in ['tm_construction', 'tm_trace']:
            solution = self._build_tm_solution(result, solution)
        
        # Add transition/move tables if present
        if 'transition_table' in result:
            solution['tables'].append({
                'title': 'Transition Table',
                'data': result['transition_table']
            })
        
        if 'move_table' in result:
            solution['tables'].append({
                'title': 'Move Table',
                'data': result['move_table']
            })
        
        return solution
    
    def _build_cfg_ambiguity_solution(self, result, solution):
        """Build solution for CFG ambiguity detection"""
        solution['details']['is_ambiguous'] = result.get('is_ambiguous', False)
        
        if result.get('is_ambiguous'):
            solution['details']['ambiguous_string'] = result.get('ambiguous_string', '')
            solution['details']['derivation_count'] = result.get('derivation_count', 0)
            
            # Generate parse tree diagrams
            for i, tree_info in enumerate(result.get('parse_trees', [])):
                filename = f'parse_tree_{i}_{uuid.uuid4().hex[:8]}'
                
                # Create a sample parse tree
                tree_data = {
                    'label': 'E',
                    'is_terminal': False,
                    'children': [
                        {'label': 'E', 'is_terminal': False, 'children': []},
                        {'label': '+', 'is_terminal': True, 'children': []},
                        {'label': 'E', 'is_terminal': False, 'children': []}
                    ]
                }
                
                diagram_file = self.renderer.render_parse_tree(tree_data, filename)
                
                if diagram_file:
                    solution['diagrams'].append({
                        'title': f'Parse Tree {i+1}',
                        'filename': diagram_file,
                        'type': 'parse_tree'
                    })
        
        return solution
    
    def _build_derivation_solution(self, result, solution):
        """Build solution for derivation generation"""
        solution['details']['derivation_type'] = result.get('derivation_type', 'leftmost')
        solution['details']['derivation_steps'] = result.get('steps', [])
        
        # Generate derivation diagram
        if result.get('steps'):
            filename = f'derivation_{uuid.uuid4().hex[:8]}'
            diagram_file = self.renderer.render_derivation(result['steps'], filename)
            
            if diagram_file:
                solution['diagrams'].append({
                    'title': 'Derivation Steps',
                    'filename': diagram_file,
                    'type': 'derivation'
                })
        
        return solution
    
    def _build_dfa_solution(self, result, solution):
        """Build solution for DFA-related tasks"""
        # Determine which DFA to diagram
        dfa = None
        diagram_title = 'DFA Diagram'
        
        if 'converted_dfa' in result:
            dfa = result['converted_dfa']
            diagram_title = 'Converted DFA'
            solution['details']['original_nfa'] = result.get('original_nfa')
        
        elif 'minimized_dfa' in result:
            dfa = result['minimized_dfa']
            diagram_title = 'Minimized DFA'
            solution['details']['original_state_count'] = result.get('original_state_count')
            solution['details']['minimized_state_count'] = result.get('minimized_state_count')
        
        elif 'dfa' in result:
            dfa = result['dfa']
        
        # Generate diagram
        if dfa:
            filename = f'dfa_{uuid.uuid4().hex[:8]}'
            diagram_file = self.renderer.render_automaton('dfa', dfa, filename)
            
            if diagram_file:
                solution['diagrams'].append({
                    'title': diagram_title,
                    'filename': diagram_file,
                    'type': 'dfa'
                })
            
            solution['details']['dfa'] = dfa
        
        return solution
    
    def _build_regex_solution(self, result, solution):
        """Build solution for regex to NFA conversion"""
        solution['details']['regex'] = result.get('regex', '')
        
        if 'nfa' in result:
            nfa = result['nfa']
            filename = f'nfa_{uuid.uuid4().hex[:8]}'
            diagram_file = self.renderer.render_automaton('nfa', nfa, filename)
            
            if diagram_file:
                solution['diagrams'].append({
                    'title': 'NFA from Regular Expression',
                    'filename': diagram_file,
                    'type': 'nfa'
                })
            
            solution['details']['nfa'] = nfa
        
        return solution
    
    def _build_pda_solution(self, result, solution):
        """Build solution for PDA-related tasks"""
        if 'pda' in result:
            pda = result['pda']
            filename = f'pda_{uuid.uuid4().hex[:8]}'
            diagram_file = self.renderer.render_automaton('pda', pda, filename)
            
            if diagram_file:
                solution['diagrams'].append({
                    'title': 'PDA Diagram',
                    'filename': diagram_file,
                    'type': 'pda'
                })
            
            solution['details']['pda'] = pda
        
        if 'grammar' in result:
            solution['details']['grammar'] = result['grammar']
        
        return solution
    
    def _build_tm_solution(self, result, solution):
        """Build solution for Turing Machine tasks"""
        if 'tm' in result:
            tm = result['tm']
            filename = f'tm_{uuid.uuid4().hex[:8]}'
            diagram_file = self.renderer.render_automaton('tm', tm, filename)
            
            if diagram_file:
                solution['diagrams'].append({
                    'title': 'Turing Machine Diagram',
                    'filename': diagram_file,
                    'type': 'tm'
                })
            
            solution['details']['tm'] = tm
        
        if 'configurations' in result:
            solution['details']['configurations'] = result['configurations']
            solution['details']['accepted'] = result.get('accepted', False)
            solution['details']['total_steps'] = result.get('total_steps', 0)
        
        return solution
