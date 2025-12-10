#!/usr/bin/env python3
"""
Test Failed Features Specifically
"""
import requests
import json

BASE_URL = "http://localhost:5000/api/solve"

def test_feature(name, question, grammar=""):
    """Test a single feature"""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"{'='*70}")
    
    try:
        response = requests.post(
            BASE_URL,
            json={"question": question, "grammar": grammar},
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ SUCCESS")
                print(f"Task Type: {result.get('task_type')}")
                print(f"Explanation: {result.get('explanation', 'N/A')[:150]}...")
                if 'diagrams' in result and result['diagrams']:
                    print(f"Diagrams: {len(result['diagrams'])} generated")
                if 'tables' in result and result['tables']:
                    print(f"Tables: {len(result['tables'])} generated")
                return True
            else:
                print(f"❌ FAILED")
                print(f"Error: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP ERROR {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print(f"⏱️ TIMEOUT - Request took longer than 15 seconds")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("TESTING PREVIOUSLY FAILED FEATURES")
    print("="*70)
    
    # Test 1: CFG Ambiguity
    test_feature(
        "CFG Ambiguity",
        "Prove that the grammar is ambiguous",
        "E → E+E | E*E | id"
    )
    
    # Test 2: CFG Construction (without grammar)
    test_feature(
        "CFG Construction",
        "Construct a CFG for the language {a^n b^n | n >= 0}"
    )
    
    # Test 3: PDA from CFG
    test_feature(
        "PDA from CFG",
        "Convert the given grammar to PDA",
        "S → aSb | ε"
    )
    
    # Test 4: PDA Transitions
    test_feature(
        "PDA Transitions",
        "Show the transition function for a PDA that accepts {a^n b^n}"
    )
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
