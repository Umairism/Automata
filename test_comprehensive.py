#!/usr/bin/env python3
"""
Comprehensive Test for All New Automata Features
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/solve"

def test_feature(name, question, grammar=""):
    """Test a single feature"""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"{'='*70}")
    print(f"Question: {question[:80]}...")
    
    try:
        response = requests.post(
            BASE_URL,
            json={"question": question, "grammar": grammar},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ SUCCESS - Task Type: {result.get('task_type')}")
                if 'diagrams' in result and result['diagrams']:
                    print(f"📊 Diagrams: {len(result['diagrams'])}")
                if 'tables' in result and result['tables']:
                    print(f"📋 Tables: {len(result['tables'])}")
                return True
            else:
                print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("COMPREHENSIVE AUTOMATA SOLVER TEST SUITE")
    print("="*70)
    
    tests = [
        # Moore and Mealy Machines
        ("Moore Machine", "Construct a Moore machine for binary counter"),
        ("Mealy Machine", "Construct a Mealy machine for binary addition"),
        ("Moore to Mealy", "Convert Moore machine to Mealy machine"),
        ("Mealy to Moore", "Convert Mealy machine to Moore machine"),
        
        # Pumping Lemma
        ("Pumping Lemma - Regular", "Explain the pumping lemma for regular languages"),
        ("Pumping Lemma - CFL", "Explain the pumping lemma for context-free languages"),
        ("Pumping Lemma Application", "Use pumping lemma to prove {a^n b^n} is not regular"),
        
        # Closure Properties
        ("Closure - Regular", "What are the closure properties of regular languages?"),
        ("Closure - CFL", "What are the closure properties of context-free languages?"),
        ("Closure under Union", "Are regular expressions closed under union?"),
        
        # Derivation Trees
        ("Derivation Tree", "Generate a derivation tree for the string", "S → aSb | ε"),
        ("Parse Tree", "Show the parse tree for id+id*id", "E → E+E | E*E | id"),
        
        # Leftmost/Rightmost Derivation
        ("Leftmost Derivation", "Show leftmost derivation for id+id", "E → E+E | id"),
        ("Rightmost Derivation", "Show rightmost derivation for id+id", "E → E+E | id"),
        
        # Ambiguity
        ("CFG Ambiguity", "Prove the grammar is ambiguous", "E → E+E | E*E | id"),
        
        # CFG
        ("CFG Construction", "Construct a CFG for {a^n b^n}"),
        ("CNF Conversion", "Convert to Chomsky Normal Form", "S → aSb | ε"),
        
        # PDA
        ("PDA Construction", "Construct a PDA for {a^n b^n}"),
        ("PDA from CFG", "Convert the grammar to PDA", "S → aSb | ε"),
        ("PDA Transitions", "Show transition function for the PDA"),
        ("Palindrome PDA", "Build a PDA for palindromes"),
        
        # LBA
        ("LBA Construction", "Construct a Linear Bounded Automaton for {a^n b^n c^n}"),
        ("LBA Explanation", "What is an LBA and how does it work?"),
        
        # DFA (existing feature)
        ("DFA Construction", "Construct a DFA for strings with even number of a's"),
        
        # Turing Machine (existing feature)
        ("Turing Machine", "Construct a Turing Machine for {a^n b^n}"),
    ]
    
    results = []
    for name, question, *grammar_args in tests:
        grammar = grammar_args[0] if grammar_args else ""
        success = test_feature(name, question, grammar)
        results.append((name, success))
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {total - passed} ❌")
    print(f"Success Rate: {(passed/total)*100:.1f}%\n")
    
    # Show failed tests
    failed_tests = [name for name, success in results if not success]
    if failed_tests:
        print("Failed Tests:")
        for name in failed_tests:
            print(f"  - {name}")
    else:
        print("🎉 ALL TESTS PASSED! 🎉")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
