"""
Renderer - Main diagram rendering coordinator
"""
from diagrams.graphviz_builder import GraphvizBuilder
from diagrams.tree_renderer import TreeRenderer

class DiagramRenderer:
    """Coordinate diagram generation"""
    
    def __init__(self, output_dir='static'):
        self.graphviz_builder = GraphvizBuilder(output_dir)
        self.tree_renderer = TreeRenderer(output_dir)
        self.output_dir = output_dir
    
    def render_automaton(self, automaton_type, automaton_data, filename):
        """
        Render an automaton diagram
        
        Args:
            automaton_type: 'dfa', 'nfa', 'pda', or 'tm'
            automaton_data: Automaton specification
            filename: Output filename
        
        Returns:
            str: Filename of generated diagram
        """
        try:
            if automaton_type in ['dfa', 'nfa']:
                return self.graphviz_builder.build_dfa_diagram(automaton_data, filename)
            
            elif automaton_type == 'pda':
                return self.graphviz_builder.build_pda_diagram(automaton_data, filename)
            
            elif automaton_type == 'tm':
                return self.graphviz_builder.build_tm_diagram(automaton_data, filename)
            
            else:
                return None
        
        except Exception as e:
            print(f"Error rendering {automaton_type} diagram: {e}")
            return None
    
    def render_parse_tree(self, tree_data, filename):
        """Render a parse tree"""
        try:
            return self.tree_renderer.render_parse_tree(tree_data, filename)
        except Exception as e:
            print(f"Error rendering parse tree: {e}")
            return None
    
    def render_derivation(self, derivation_steps, filename):
        """Render a derivation tree"""
        try:
            return self.tree_renderer.render_derivation_tree(derivation_steps, filename)
        except Exception as e:
            print(f"Error rendering derivation: {e}")
            return None
