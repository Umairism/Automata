"""
Graphviz Builder - Generates state diagrams for automata
"""
import graphviz
import os

class GraphvizBuilder:
    """Build state diagrams using Graphviz"""
    
    def __init__(self, output_dir='static'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # High-quality diagram settings
        self.graph_attrs = {
            'dpi': '300',  # High resolution
            'bgcolor': 'white',
            'rankdir': 'LR',
            'ranksep': '1.0',  # More space between ranks
            'nodesep': '0.8',  # More space between nodes
            'splines': 'true',  # Smooth edges
            'margin': '0.5'
        }
        
        self.node_attrs = {
            'style': 'filled',
            'fillcolor': 'lightblue',
            'fontname': 'Arial',
            'fontsize': '14',
            'width': '0.6',
            'height': '0.6',
            'penwidth': '2.0'
        }
        
        self.edge_attrs = {
            'fontname': 'Arial',
            'fontsize': '12',
            'penwidth': '1.5',
            'arrowsize': '1.0'
        }
    
    def build_dfa_diagram(self, dfa, filename='dfa_diagram'):
        """
        Build a DFA/NFA state diagram
        
        Args:
            dfa: Dictionary with states, transitions, start_state, accept_states
            filename: Output filename (without extension)
        
        Returns:
            str: Path to generated PNG file
        """
        dot = graphviz.Digraph(comment='DFA Diagram', format='png')
        
        # Apply high-quality graph attributes
        dot.attr(**self.graph_attrs)
        
        # Apply default node attributes
        dot.attr('node', **self.node_attrs)
        
        # Apply default edge attributes
        dot.attr('edge', **self.edge_attrs)
        
        # Add invisible start node
        dot.node('__start__', '', shape='none', width='0', height='0', style='')
        
        # Add states
        for state in dfa.get('states', []):
            if state in dfa.get('accept_states', []):
                # Accepting state (double circle with different color)
                dot.node(state, state, shape='doublecircle', fillcolor='lightgreen', penwidth='2.5')
            else:
                # Normal state
                dot.node(state, state, shape='circle')
        
        # Add start arrow
        start_state = dfa.get('start_state')
        if start_state:
            dot.edge('__start__', start_state)
        
        # Add transitions
        transitions = dfa.get('transitions', {})
        
        # Group transitions with same source and destination
        edge_labels = {}
        
        for from_state, trans in transitions.items():
            for symbol, to_state in trans.items():
                edge_key = (from_state, to_state)
                if edge_key not in edge_labels:
                    edge_labels[edge_key] = []
                edge_labels[edge_key].append(symbol)
        
        # Add edges with combined labels
        for (from_state, to_state), symbols in edge_labels.items():
            label = ', '.join(symbols)
            dot.edge(from_state, to_state, label=label)
        
        # Render
        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format='png', cleanup=True)
        
        return f'{filename}.png'
    
    def build_pda_diagram(self, pda, filename='pda_diagram'):
        """
        Build a PDA state diagram
        
        Args:
            pda: Dictionary with PDA specification
            filename: Output filename
        
        Returns:
            str: Path to generated PNG file
        """
        dot = graphviz.Digraph(comment='PDA Diagram', format='png')
        
        # Apply high-quality graph attributes
        dot.attr(**self.graph_attrs)
        
        # Apply default node attributes
        dot.attr('node', **self.node_attrs)
        
        # Apply default edge attributes
        dot.attr('edge', **self.edge_attrs)        # Add invisible start node
        dot.node('__start__', '', shape='none', width='0', height='0', style='')
        
        # Add states
        for state in pda.get('states', []):
            if state in pda.get('accept_states', []):
                dot.node(state, state, shape='doublecircle', fillcolor='lightgreen', penwidth='2.5')
            else:
                dot.node(state, state, shape='circle')
        
        # Add start arrow
        start_state = pda.get('start_state')
        if start_state:
            dot.edge('__start__', start_state)
        
        # Add transitions
        for transition in pda.get('transitions', []):
            from_state = transition['from']
            to_state = transition['to']
            input_sym = transition.get('input', 'ε')
            stack_top = transition.get('stack_top', '')
            stack_push = transition.get('stack_push', 'ε')
            
            # Format: input, stack_top → stack_push
            label = f'{input_sym}, {stack_top} → {stack_push if stack_push else "ε"}'
            
            dot.edge(from_state, to_state, label=label)
        
        # Render
        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format='png', cleanup=True)
        
        return f'{filename}.png'
    
    def build_tm_diagram(self, tm, filename='tm_diagram'):
        """
        Build a Turing Machine state diagram
        
        Args:
            tm: Dictionary with TM specification
            filename: Output filename
        
        Returns:
            str: Path to generated PNG file
        """
        dot = graphviz.Digraph(comment='TM Diagram', format='png')
        
        # Apply high-quality graph attributes
        dot.attr(**self.graph_attrs)
        
        # Apply default node attributes
        dot.attr('node', **self.node_attrs)
        
        # Apply default edge attributes
        dot.attr('edge', **self.edge_attrs)
        
        # Add invisible start node
        dot.node('__start__', '', shape='none', width='0', height='0', style='')
        
        # Add states
        for state in tm.get('states', []):
            if state == tm.get('accept_state'):
                dot.node(state, state, shape='doublecircle', fillcolor='lightgreen', penwidth='2.5')
            elif state == tm.get('reject_state'):
                dot.node(state, state, shape='circle', fillcolor='#ffcccc', penwidth='2.0')
            else:
                dot.node(state, state, shape='circle')
        
        # Add start arrow
        start_state = tm.get('start_state')
        if start_state:
            dot.edge('__start__', start_state)
        
        # Add transitions
        for transition in tm.get('transitions', []):
            from_state = transition['from']
            to_state = transition['to']
            read_sym = transition['read']
            write_sym = transition['write']
            move = transition['move']
            
            # Format: read → write, move
            label = f'{read_sym} → {write_sym}, {move}'
            
            dot.edge(from_state, to_state, label=label)
        
        # Render
        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format='png', cleanup=True)
        
        return f'{filename}.png'
