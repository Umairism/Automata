#!/usr/bin/env python3
"""
Test all examples from the UI to ensure they work correctly
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/solve"

# All examples from the HTML UI
EXAMPLES = {
    "DFA - Even a's": {
        "question": "Construct a DFA that accepts strings with even number of 'a's",
        "grammar": ""
    },
    "DFA - Ending 01": {
        "question": "Design a DFA that accepts strings ending with '01'",
        "grammar": ""
    },
    "DFA - Divisible by 3": {
        "question": "Construct a DFA for binary strings divisible by 3",
        "grammar": ""
    },
    "DFA - No consecutive": {
        "question": "Construct a DFA that doesn't allow consecutive 'a's",
        "grammar": ""
    },
    "NFA - Contains 010": {
        "question": "Construct an NFA for strings containing '010'",
        "grammar": ""
    },
    "NFA - Convert to DFA": {
        "question": "Convert NFA to DFA",
        "grammar": ""
    },
    "NFA - Epsilon transitions": {
        "question": "Construct NFA with epsilon transitions for (a|b)*abb",
        "grammar": ""
    },
    "PDA - a^n b^n": {
        "question": "Construct PDA for {a^n b^n | n >= 0}",
        "grammar": ""
    },
    "PDA - Palindrome": {
        "question": "Design PDA for palindromes over {a,b}",
        "grammar": ""
    },
    "PDA - wcw^r": {
        "question": "Construct PDA for {wcw^r | w in {a,b}*}",
        "grammar": ""
    },
    "PDA - Unequal": {
        "question": "Design PDA for unequal number of a's and b's",
        "grammar": ""
    },
    "CFG - Ambiguity": {
        "question": "Check if the given grammar is ambiguous",
        "grammar": "E → E+E | E*E | (E) | id"
    },
    "CFG - Leftmost derivation": {
        "question": "Show leftmost derivation for string 'id+id*id'",
        "grammar": "E → E+E | E*E | (E) | id"
    },
    "CFG - Rightmost derivation": {
        "question": "Show rightmost derivation for string 'id+id*id'",
        "grammar": "E → E+E | E*E | (E) | id"
    },
    "CFG - Parse tree": {
        "question": "Generate parse tree for string 'id+id*id'",
        "grammar": "E → E+E | E*E | (E) | id"
    },
    "CFG - Construct": {
        "question": "Construct CFG for {a^n b^n | n >= 0}",
        "grammar": ""
    },
    "TM - a^n b^n c^n": {
        "question": "Construct TM for {a^n b^n c^n | n >= 1}",
        "grammar": ""
    },
    "TM - Palindrome": {
        "question": "Design a Turing Machine for checking palindromes",
        "grammar": ""
    },
    "TM - Binary addition": {
        "question": "Design a Turing Machine for binary addition",
        "grammar": ""
    },
    "Theory - Pumping Regular": {
        "question": "Prove using pumping lemma that {a^n b^n | n >= 0} is not regular",
        "grammar": ""
    },
    "Theory - Pumping CFL": {
        "question": "Use pumping lemma for CFLs to prove {a^n b^n c^n | n >= 0} is not context-free",
        "grammar": ""
    },
    "Theory - Closure Regular": {
        "question": "Explain closure properties of regular languages",
        "grammar": ""
    },
    "Theory - Moore Machine": {
        "question": "Construct Moore machine for binary divisibility by 3",
        "grammar": ""
    },
    "Theory - LBA": {
        "question": "Construct LBA for {a^n b^n c^n | n >= 1}",
        "grammar": ""
    }
}

def test_example(name, data):
    """Test a single example"""
    try:
        response = requests.post(BASE_URL, json=data, timeout=10)
        result = response.json()
        
        if result.get('success'):
            task_type = result.get('task_type', 'unknown')
            diagrams = len(result.get('diagrams', []))
            tables = len(result.get('tables', []))
            steps = len(result.get('steps', []))
            return True, f"✅ {task_type} (D:{diagrams}, T:{tables}, S:{steps})"
        else:
            error = result.get('error', 'Unknown error')
            return False, f"❌ {error}"
    except Exception as e:
        return False, f"❌ Exception: {str(e)}"

def main():
    """Run all tests"""
    print("=" * 70)
    print("Testing All UI Examples")
    print("=" * 70)
    
    passed = 0
    failed = 0
    failed_tests = []
    
    for name, data in EXAMPLES.items():
        success, message = test_example(name, data)
        print(f"{name:35} {message}")
        
        if success:
            passed += 1
        else:
            failed += 1
            failed_tests.append(name)
    
    print("=" * 70)
    print(f"\nResults: {passed}/{len(EXAMPLES)} passed ({failed} failed)")
    
    if failed_tests:
        print("\n❌ Failed tests:")
        for test in failed_tests:
            print(f"  - {test}")
    else:
        print("\n🎉 All examples working correctly!")
    
    return failed == 0

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
