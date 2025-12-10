"""
Tree Renderer - Generates parse trees and derivation trees
"""
import graphviz
import os

class TreeRenderer:
    """Render parse trees and derivation trees"""
    
    def __init__(self, output_dir='static'):
        self.output_dir = output_dir
        self.node_counter = 0
        os.makedirs(output_dir, exist_ok=True)
        
        # High-quality tree diagram settings
        self.graph_attrs = {
            'dpi': '300',
            'bgcolor': 'white',
            'rankdir': 'TB',
            'ranksep': '0.8',
            'nodesep': '0.6',
            'splines': 'true',
            'margin': '0.5'
        }
        
        self.node_attrs = {
            'style': 'filled',
            'fontname': 'Arial',
            'fontsize': '14',
            'penwidth': '2.0'
        }
        
        self.edge_attrs = {
            'penwidth': '1.5',
            'arrowsize': '0.8'
        }
    
    def render_parse_tree(self, tree_data, filename='parse_tree'):
        """
        Render a parse tree
        
        Args:
            tree_data: Dictionary representing the parse tree
            filename: Output filename
        
        Returns:
            str: Path to generated PNG file
        """
        dot = graphviz.Digraph(comment='Parse Tree', format='png')
        
        # Apply high-quality graph attributes
        dot.attr(**self.graph_attrs)
        
        # Apply default node attributes
        dot.attr('node', **self.node_attrs)
        
        # Apply default edge attributes
        dot.attr('edge', **self.edge_attrs)
        
        self.node_counter = 0
        
        # Build tree recursively
        if isinstance(tree_data, dict):
            self._add_tree_node(dot, tree_data)
        
        # Render
        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format='png', cleanup=True)
        
        return f'{filename}.png'
    
    def _add_tree_node(self, dot, node, parent_id=None):
        """Recursively add tree nodes"""
        node_id = f'node_{self.node_counter}'
        self.node_counter += 1
        
        label = node.get('label', '?')
        
        # Add node with better styling
        if node.get('is_terminal', False):
            dot.node(node_id, label, shape='box', fillcolor='#ffffcc', 
                    width='0.5', height='0.4')
        else:
            dot.node(node_id, label, shape='ellipse', fillcolor='lightblue',
                    width='0.6', height='0.5')
        
        # Add edge from parent
        if parent_id:
            dot.edge(parent_id, node_id)
        
        # Add children
        for child in node.get('children', []):
            self._add_tree_node(dot, child, node_id)
        
        return node_id
    
    def render_derivation_tree(self, derivation_steps, filename='derivation_tree'):
        """
        Render a derivation sequence as a tree
        
        Args:
            derivation_steps: List of derivation steps
            filename: Output filename
        
        Returns:
            str: Path to generated PNG file
        """
        dot = graphviz.Digraph(comment='Derivation Tree', format='png')
        
        # Apply high-quality graph attributes
        dot.attr(**self.graph_attrs)
        
        # Apply default node attributes
        dot.attr('node', **self.node_attrs)
        
        # Apply default edge attributes
        dot.attr('edge', **self.edge_attrs)
        
        # Add nodes for each step
        for i, step in enumerate(derivation_steps):
            node_id = f'step_{i}'
            dot.node(node_id, step, shape='box')
            
            if i > 0:
                dot.edge(f'step_{i-1}', node_id)
        
        # Render
        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format='png', cleanup=True)
        
        return f'{filename}.png'
    
    def create_sample_parse_tree(self, root_symbol, productions):
        """
        Create a sample parse tree structure
        
        Args:
            root_symbol: Root non-terminal
            productions: List of productions used in derivation
        
        Returns:
            dict: Parse tree structure
        """
        # Simplified tree creation
        tree = {
            'label': root_symbol,
            'is_terminal': False,
            'children': []
        }
        
        # Add children based on first production
        if productions:
            first_prod = productions[0]
            for symbol in first_prod:
                child = {
                    'label': symbol,
                    'is_terminal': symbol.islower() or symbol.isdigit(),
                    'children': []
                }
                tree['children'].append(child)
        
        return tree
