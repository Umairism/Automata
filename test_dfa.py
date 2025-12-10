#!/usr/bin/env python3
import requests
import json

# Test the DFA construction endpoint
url = "http://localhost:5000/api/solve"
data = {
    "question": "Construct a DFA with ∑ = {a, b} that accepts only the input \"aaab\"",
    "grammar": ""
}

print("Testing DFA Construction...")
print("Question:", data["question"])
print("\nSending request...")

try:
    response = requests.post(url, json=data)
    result = response.json()
    
    print("\n" + "="*60)
    if result.get('success'):
        print("✅ SUCCESS!")
        print(f"\nTask Type: {result.get('task_type')}")
        print(f"\nExplanation:\n{result.get('explanation')}")
        
        if result.get('tables'):
            print("\n📊 Transition Table:")
            for table in result['tables']:
                print(f"\n{table['title']}:")
                for row in table['data']:
                    print("  " + " | ".join(str(cell).ljust(10) for cell in row))
        
        if result.get('diagrams'):
            print(f"\n🎨 Diagrams generated: {len(result['diagrams'])}")
            for diagram in result['diagrams']:
                print(f"   - {diagram['title']}: {diagram['filename']}")
        
        if result.get('details', {}).get('dfa'):
            dfa = result['details']['dfa']
            print(f"\n🤖 DFA Details:")
            print(f"   States: {len(dfa['states'])}")
            print(f"   Start: {dfa['start_state']}")
            print(f"   Accept: {dfa['accept_states']}")
    else:
        print("❌ ERROR!")
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    print("="*60)
    
except Exception as e:
    print(f"❌ Request failed: {e}")
