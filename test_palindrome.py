#!/usr/bin/env python3
"""
Test Palindrome PDA Construction
"""
import requests
import json

def test_palindrome():
    """Test palindrome PDA construction"""
    
    url = "http://localhost:5000/api/solve"
    
    # Test case 1: General palindrome
    test_cases = [
        {
            "name": "General Palindrome",
            "question": "A palindrome is a sequence of symbols that reads the same backward as forward (i.e., aba). If a palindrome contains an even length, it is also called an even palindrome (i.e., abaaba)",
            "grammar": ""
        },
        {
            "name": "Explicit Palindrome Request",
            "question": "Construct a PDA for palindromes over {a, b}",
            "grammar": ""
        },
        {
            "name": "Even Palindrome",
            "question": "Build a PDA for even-length palindromes",
            "grammar": ""
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {test_case['name']}")
        print(f"{'='*60}")
        print(f"Question: {test_case['question']}")
        
        try:
            response = requests.post(
                url,
                json={
                    "question": test_case["question"],
                    "grammar": test_case["grammar"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    print(f"\n✅ SUCCESS!")
                    print(f"\nTask Type: {result.get('task_type')}")
                    print(f"\nExplanation:\n{result.get('explanation', 'N/A')[:200]}...")
                    
                    # Show PDA details
                    if 'tables' in result:
                        print(f"\n📊 Tables Generated: {len(result['tables'])}")
                        for table in result['tables']:
                            print(f"  - {table.get('title', 'Untitled')}")
                    
                    # Show diagrams
                    if 'diagrams' in result:
                        print(f"\n🎨 Diagrams Generated: {len(result['diagrams'])}")
                        for diagram in result['diagrams']:
                            print(f"  - {diagram.get('filename', 'N/A')}")
                    
                    # Show steps
                    if 'steps' in result and result['steps']:
                        print(f"\n📝 Steps:")
                        for step in result['steps'][:3]:
                            print(f"  {step}")
                else:
                    print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing Palindrome PDA Construction...")
    test_palindrome()
    print("\n" + "="*60)
    print("Testing complete!")
