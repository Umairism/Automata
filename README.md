# 🤖 Automata Solver - Theory of Computation Helper

A comprehensive, professional Flask-based web application for solving Theory of Computation problems. Features a modern UI with dedicated sections for DFA, NFA, PDA, CFG, Turing Machines, Moore/Mealy machines, and theoretical concepts.

## ✨ Key Features

### 🎨 **Enhanced User Interface (v2.0)**
- **Professional Landing Page**: Hero section with interactive feature cards
- **Sticky Navigation Bar**: Quick access to all sections
- **8 Dedicated Sections**: Home, General Solver, DFA, NFA, PDA, CFG, TM, Theory
- **30+ Example Questions**: Categorized by topic for easy learning
- **Responsive Design**: Works on desktop, tablet, and mobile
- **High-Quality Diagrams**: 300 DPI resolution with optimized layouts

### 🤖 **Automata & Machines**
- **DFA (Deterministic Finite Automaton)**
  - Construction from language descriptions
  - State minimization
  - Transition table generation
  - Acceptance testing

- **NFA (Non-deterministic Finite Automaton)**
  - NFA construction
  - NFA to DFA conversion (subset construction)
  - Epsilon transition handling

- **PDA (Pushdown Automaton)**
  - PDA design for context-free languages
  - CFG to PDA conversion
  - Stack operation visualization
  - Acceptance by final state/empty stack

- **Turing Machines**
  - TM construction for complex languages
  - Multi-tape support
  - Configuration tracing
  - Tape visualization

- **Moore & Mealy Machines**
  - Machine construction
  - Conversion between types
  - Output function visualization

- **Linear Bounded Automata (LBA)**
  - LBA construction
  - Context-sensitive language recognition

### 📝 **Context-Free Grammars**
- Ambiguity detection with timeout protection
- Leftmost/rightmost derivations
- Parse tree generation
- Derivation tree visualization
- CFG construction for languages
- CFG to PDA conversion

### 🎓 **Theory & Proofs**
- **Pumping Lemma**
  - Regular languages
  - Context-free languages
  - Step-by-step proofs

- **Closure Properties**
  - Regular languages (union, intersection, complement, concatenation, Kleene star)
  - Context-free languages (union, concatenation, Kleene star)

### 📊 **Visualization**
- State diagrams (DFA, NFA, PDA, TM)
- Parse trees with proper formatting
- Derivation trees
- Transition tables
- High-resolution PNG export (300 DPI)
- Professional styling with gradients and colors

## Installation

### Prerequisites

- Python 3.8 or higher
- Graphviz (system installation required)

#### Install Graphviz

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
Download and install from [graphviz.org](https://graphviz.org/download/)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Umairism/Automata.git
cd Automata
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Production Mode

Using Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Usage

### Web Interface (v2.0)

1. **Launch**: Open `http://localhost:5000` in your browser
2. **Navigate**: Use the navigation bar or click feature cards on the landing page
3. **Choose Section**: Select from General Solver, DFA, NFA, PDA, CFG, TM, or Theory
4. **Enter Question**: Type your question or click an example to auto-load
5. **Add Grammar** (if needed): For CFG/PDA problems, add grammar in the format:
   ```
   S → aSb | ε
   E → E+E | E*E | (E) | id
   ```
6. **Solve**: Click the solve button for your section
7. **View Results**: See diagrams, tables, steps, and explanations

### Section Overview

- **🏠 Home**: Landing page with feature cards
- **📝 General Solver**: Universal solver for any ToC question
- **📊 DFA**: Deterministic Finite Automaton problems
- **🔀 NFA**: Non-deterministic Finite Automaton problems
- **📚 PDA**: Pushdown Automaton problems
- **🌳 CFG**: Context-Free Grammar analysis
- **⚙️ TM**: Turing Machine construction
- **🎓 Theory**: Pumping lemmas, closures, Moore/Mealy, LBA

### API Endpoints

#### POST /api/solve
Solve an automata problem.

**Request:**
```json
{
  "question": "Prove that the given grammar is ambiguous",
  "grammar": "E → E+E | E*E | (E) | id"
}
```

**Response:**
```json
{
  "task_type": "cfg_ambiguity",
  "success": true,
  "explanation": "The grammar is ambiguous...",
  "diagrams": [...],
  "tables": [...],
  "steps": [...]
}
```

#### GET /api/diagram/{filename}
Retrieve a generated diagram.

#### GET /api/status
Health check endpoint.

## Project Structure

```
Automata/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Construction.md             # Project specification
├── README.md                   # This file
│
├── engine/                     # Core automata engines
│   ├── __init__.py
│   ├── classifier.py           # Query classification
│   ├── parser.py               # Input parsing
│   ├── cfg_engine.py           # CFG processor
│   ├── dfa_engine.py           # DFA/NFA processor
│   ├── pda_engine.py           # PDA processor
│   ├── tm_engine.py            # Turing Machine processor
│   └── utils.py                # Utility functions
│
├── diagrams/                   # Diagram generation
│   ├── __init__.py
│   ├── renderer.py             # Main renderer
│   ├── graphviz_builder.py     # State diagram builder
│   └── tree_renderer.py        # Parse tree builder
│
├── builders/                   # Solution assembly
│   ├── __init__.py
│   ├── solution_builder.py     # Solution assembler
│   └── explanation_templates.py # Explanation templates
│
├── templates/                  # HTML templates
│   └── index.html              # Main web interface
│
└── static/                     # Generated diagrams and assets
```

## Example Questions

**CFG Ambiguity:**
```
Question: Prove that the given grammar is ambiguous
Grammar: E → E+E | E*E | (E) | id
```

**DFA Construction:**
```
Question: Construct a DFA that accepts strings with even number of a's over alphabet {a, b}
```

**PDA Construction:**
```
Question: Construct a PDA for the language {a^n b^n | n ≥ 0}
```

**NFA to DFA:**
```
Question: Convert the given NFA to DFA
(Provide NFA specification in automaton parameter)
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t automata-solver .
```

### Run Container
```bash
docker run -p 5000:5000 automata-solver
```

## Development

### Adding New Automata Types

1. Create a new engine in `engine/` directory
2. Add task type patterns to `engine/classifier.py`
3. Update `engine/parser.py` to handle new input format
4. Add diagram rendering in `diagrams/` if needed
5. Update `builders/solution_builder.py` to format output

### Testing

Run basic tests:
```bash
# Test the API
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"question": "Construct a DFA for even a'\''s", "grammar": ""}'
```

## Troubleshooting

**Graphviz not found:**
- Ensure Graphviz is installed on your system
- Check that `dot` command is in your PATH: `which dot`

**Module import errors:**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**Port already in use:**
- Change port in `app.py` or use: `python app.py --port 8000`

## Limitations

- Ambiguity detection limited to strings of depth ≤ 10
- Maximum 1000 steps for Turing Machine simulation
- PDA simulation limited to 100 moves
- Grammar must be in standard BNF notation

## Future Enhancements

- Interactive automaton editor
- Step-by-step derivation animator
- Export to LaTeX
- Multi-language support
- Regular expression simplification
- More complex grammar transformations

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built based on formal language theory and automata theory principles.

## Contact

For questions or issues, please open a GitHub issue or contact the maintainer.
