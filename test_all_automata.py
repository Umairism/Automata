#!/usr/bin/env python3
import requests
import json

url = "http://localhost:5000/api/solve"

tests = [
    {
        "name": "CFG Ambiguity Detection",
        "data": {
            "question": "Prove that the given grammar is ambiguous",
            "grammar": "E → E+E | E*E | id"
        }
    },
    {
        "name": "CFG Leftmost Derivation",
        "data": {
            "question": "Show leftmost derivation for string id+id*id",
            "grammar": "E → E+E | E*E | id"
        }
    },
    {
        "name": "PDA Construction",
        "data": {
            "question": "Construct a PDA for the language {a^n b^n | n >= 0}",
            "grammar": ""
        }
    },
    {
        "name": "CFG to PDA Conversion",
        "data": {
            "question": "Convert the given CFG to PDA",
            "grammar": "S → aSb | ε"
        }
    },
    {
        "name": "Turing Machine Construction",
        "data": {
            "question": "Construct a Turing Machine for the language {a^n b^n | n >= 0}",
            "grammar": ""
        }
    }
]

print("="*70)
print("TESTING ALL AUTOMATA TYPES")
print("="*70)

for test in tests:
    print(f"\n🧪 Testing: {test['name']}")
    print("-"*70)
    
    try:
        response = requests.post(url, json=test['data'])
        result = response.json()
        
        if result.get('success'):
            print(f"✅ SUCCESS")
            print(f"   Task Type: {result.get('task_type')}")
            print(f"   Explanation: {result.get('explanation', '')[:100]}...")
            
            if result.get('tables'):
                print(f"   Tables: {len(result['tables'])} generated")
            
            if result.get('diagrams'):
                print(f"   Diagrams: {len(result['diagrams'])} generated")
                for diag in result['diagrams']:
                    print(f"      - {diag['filename']}")
            
            if result.get('details'):
                details = result['details']
                if 'is_ambiguous' in details:
                    print(f"   Is Ambiguous: {details['is_ambiguous']}")
                if 'derivation_steps' in details:
                    print(f"   Derivation Steps: {len(details['derivation_steps'])}")
        else:
            print(f"❌ FAILED")
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ REQUEST FAILED: {e}")

print("\n" + "="*70)
print("TESTING COMPLETE")
print("="*70)
