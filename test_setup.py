"""
Quick test script to verify the application setup
"""
import sys
sys.path.insert(0, '/home/umairism/Desktop/Github/Automata')

from engine.classifier import classify_query
from engine.parser import parse_input
from engine.cfg_engine import CFGEngine

def test_cfg_ambiguity():
    """Test CFG ambiguity detection"""
    print("Testing CFG Ambiguity Detection...")
    
    question = "Prove that the grammar is ambiguous"
    grammar = "E → E+E | E*E | id"
    
    # Classify
    classification = classify_query(question, grammar)
    print(f"✓ Classification: {classification['task_type']}")
    
    # Parse
    parsed = parse_input(classification, grammar)
    print(f"✓ Grammar parsed: {len(parsed['grammar']['rules'])} rules")
    
    # Solve
    engine = CFGEngine()
    result = engine.check_ambiguity(parsed)
    print(f"✓ Ambiguity check complete")
    print(f"  Result: {result.get('is_ambiguous', 'Unknown')}")
    
    return True

def test_imports():
    """Test that all modules can be imported"""
    print("\nTesting imports...")
    
    modules = [
        'engine.classifier',
        'engine.parser',
        'engine.cfg_engine',
        'engine.dfa_engine',
        'engine.pda_engine',
        'engine.tm_engine',
        'diagrams.renderer',
        'diagrams.graphviz_builder',
        'diagrams.tree_renderer',
        'builders.solution_builder'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except Exception as e:
            print(f"  ✗ {module}: {e}")
            return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Automata Solver - Quick Test")
    print("=" * 60)
    
    try:
        if test_imports():
            print("\n✅ All imports successful!")
        else:
            print("\n❌ Some imports failed")
            sys.exit(1)
        
        if test_cfg_ambiguity():
            print("\n✅ CFG test passed!")
        else:
            print("\n❌ CFG test failed")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("All tests passed! ✨")
        print("=" * 60)
        print("\nYou can now run the application:")
        print("  python app.py")
        print("\nOr use the setup script:")
        print("  ./setup.sh")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
