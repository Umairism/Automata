"""
Automata Solver Web Application
Main Flask Application
"""
from flask import Flask, request, jsonify, render_template, send_file
from engine.classifier import classify_query
from engine.parser import parse_input
from engine.cfg_engine import CFGEngine
from engine.dfa_engine import DFAEngine
from engine.pda_engine import PDAEngine
from engine.tm_engine import TMEngine
from engine.moore_mealy_engine import MooreMealyEngine
from engine.theory_engine import TheoryEngine
from engine.lba_engine import LBAEngine
from builders.solution_builder import SolutionBuilder
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['STATIC_FOLDER'] = 'static'

# Ensure static directory exists
os.makedirs('static', exist_ok=True)

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def solve():
    """
    Main endpoint for solving automata problems
    Expected JSON:
    {
        "question": "string",
        "grammar": "string (optional)",
        "automaton": "dict (optional)"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required'}), 400
        
        question = data.get('question', '')
        grammar = data.get('grammar', '')
        automaton = data.get('automaton', {})
        
        # Step 1: Classify the query
        classification = classify_query(question, grammar, automaton)
        
        # Step 2: Parse the input
        parsed_input = parse_input(classification, grammar, automaton)
        
        # Step 3: Route to appropriate engine
        task_type = classification['task_type']
        result = None
        
        if task_type in ['cfg_construction', 'cfg_ambiguity', 'cfg_derivation', 'cfg_parse_tree', 'cfg_to_cnf', 'cfg_to_pda']:
            engine = CFGEngine()
            result = engine.solve(task_type, parsed_input)
            
        elif task_type in ['dfa_construction', 'nfa_to_dfa', 'dfa_minimization', 're_to_nfa', 'dfa_membership']:
            engine = DFAEngine()
            result = engine.solve(task_type, parsed_input)
            
        elif task_type in ['pda_construction', 'pda_from_cfg', 'pda_membership', 'pda_transitions']:
            engine = PDAEngine()
            result = engine.solve(task_type, parsed_input)
            
        elif task_type in ['tm_construction', 'tm_trace', 'tm_membership']:
            engine = TMEngine()
            result = engine.solve(task_type, parsed_input)
        
        elif task_type in ['moore_machine', 'mealy_machine', 'moore_to_mealy', 'mealy_to_moore']:
            engine = MooreMealyEngine()
            result = engine.solve(task_type, parsed_input)
        
        elif task_type in ['pumping_lemma_regular', 'pumping_lemma_cfl', 'closure_regular', 'closure_cfl']:
            engine = TheoryEngine()
            result = engine.solve(task_type, parsed_input)
        
        elif task_type in ['lba_construction']:
            engine = LBAEngine()
            result = engine.solve(task_type, parsed_input)
        
        else:
            return jsonify({'error': f'Unsupported task type: {task_type}'}), 400
        
        # Step 4: Build solution
        builder = SolutionBuilder()
        solution = builder.build(result, task_type)
        
        return jsonify(solution)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/diagram/<filename>')
def get_diagram(filename):
    """Serve generated diagram files"""
    try:
        filepath = os.path.join('static', filename)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/png')
        else:
            return jsonify({'error': 'Diagram not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'version': '1.0.0',
        'supported_tasks': [
            'CFG Ambiguity Detection',
            'DFA/NFA Construction',
            'PDA Construction',
            'Turing Machine Construction',
            'Regular Expression to NFA',
            'Grammar Derivations',
            'Parse Trees'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
