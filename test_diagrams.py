#!/usr/bin/env python3
"""
Test Improved Diagram Quality
"""
import requests
import os

BASE_URL = "http://localhost:5000/api/solve"

def test_diagram(name, question, grammar=""):
    """Test diagram generation"""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"{'='*70}")
    
    try:
        response = requests.post(
            BASE_URL,
            json={"question": question, "grammar": grammar},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success') and result.get('diagrams'):
                print(f"✅ SUCCESS - Diagrams generated")
                for diagram in result['diagrams']:
                    filename = diagram.get('filename', '')
                    filepath = f"static/{filename}"
                    if os.path.exists(filepath):
                        size = os.path.getsize(filepath)
                        print(f"   📊 {filename} - {size:,} bytes")
                    else:
                        print(f"   ⚠️ {filename} - File not found")
                return True
            else:
                print(f"❌ No diagrams generated")
                return False
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("TESTING IMPROVED DIAGRAM QUALITY")
    print("="*70)
    
    # Test different diagram types
    tests = [
        ("DFA Diagram", "Construct a DFA that accepts strings with even number of a's"),
        ("PDA Diagram", "Build a PDA for palindromes over {a,b}"),
        ("Turing Machine", "Construct a Turing Machine for {a^n b^n}"),
        ("Parse Tree", "Show parse tree for id+id", "E → E+E | id"),
    ]
    
    for name, question, *grammar_args in tests:
        grammar = grammar_args[0] if grammar_args else ""
        test_diagram(name, question, grammar)
    
    print("\n" + "="*70)
    print("DIAGRAM TESTING COMPLETE")
    print("Check the static/ folder for improved high-quality diagrams!")
    print("="*70)

if __name__ == "__main__":
    main()
