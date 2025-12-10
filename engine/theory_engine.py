"""
Theory Engine - Handles Pumping Lemma and Closure Properties
"""

class TheoryEngine:
    """Engine for theoretical concepts like Pumping Lemma and Closure Properties"""
    
    def __init__(self):
        pass
    
    def solve(self, task_type, parsed_input):
        """Main solver dispatcher"""
        
        if task_type == 'pumping_lemma_regular':
            return self.pumping_lemma_regular(parsed_input)
        
        elif task_type == 'pumping_lemma_cfl':
            return self.pumping_lemma_cfl(parsed_input)
        
        elif task_type == 'closure_regular':
            return self.closure_properties_regular(parsed_input)
        
        elif task_type == 'closure_cfl':
            return self.closure_properties_cfl(parsed_input)
        
        else:
            return {'error': f'Unsupported theory task: {task_type}'}
    
    def pumping_lemma_regular(self, parsed_input):
        """Explain and apply Pumping Lemma for Regular Languages"""
        question = parsed_input.get('question', '')
        
        return {
            'theorem': 'Pumping Lemma for Regular Languages',
            'statement': 'If L is a regular language, then there exists a constant n (pumping length) such that for every string w ∈ L with |w| ≥ n, we can write w = xyz satisfying: (1) |xy| ≤ n, (2) |y| > 0, (3) xy^i z ∈ L for all i ≥ 0',
            'explanation': 'The Pumping Lemma is used to prove that certain languages are NOT regular. It states that any sufficiently long string in a regular language can be "pumped" (repeated) and still remain in the language.',
            'conditions': [
                '|xy| ≤ n: The pumpable portion is in the first n characters',
                '|y| > 0: The pumpable portion is non-empty',
                'xy^i z ∈ L for all i ≥ 0: Pumping y any number of times keeps string in L'
            ],
            'how_to_use': [
                'Step 1: Assume L is regular (for contradiction)',
                'Step 2: Let n be the pumping length (choose arbitrary n)',
                'Step 3: Choose a string w ∈ L with |w| ≥ n',
                'Step 4: By Pumping Lemma, w = xyz with given conditions',
                'Step 5: Show that xy^i z ∉ L for some i ≥ 0',
                'Step 6: This contradicts Pumping Lemma, so L is not regular'
            ],
            'example': {
                'language': 'L = {a^n b^n | n ≥ 0}',
                'proof': [
                    'Assume L is regular with pumping length n',
                    'Choose w = a^n b^n (clearly |w| = 2n ≥ n)',
                    'By PL, w = xyz where |xy| ≤ n and |y| > 0',
                    'Since |xy| ≤ n, both x and y consist only of a\'s',
                    'Let y = a^k for some k > 0',
                    'Then xy^2z = a^n+k b^n',
                    'But xy^2z ∉ L because it has more a\'s than b\'s',
                    'Contradiction! Therefore L is not regular'
                ],
                'conclusion': 'The language {a^n b^n} is NOT regular'
            },
            'common_applications': [
                '{a^n b^n | n ≥ 0} - NOT regular',
                '{ww | w ∈ {a,b}*} - NOT regular',
                '{a^(n^2) | n ≥ 0} - NOT regular',
                '{a^p | p is prime} - NOT regular',
                'Balanced parentheses - NOT regular'
            ],
            'diagram_filename': 'pumping_lemma_regular.png'
        }
    
    def pumping_lemma_cfl(self, parsed_input):
        """Explain and apply Pumping Lemma for Context-Free Languages"""
        question = parsed_input.get('question', '')
        
        return {
            'theorem': 'Pumping Lemma for Context-Free Languages',
            'statement': 'If L is a context-free language, then there exists a constant n (pumping length) such that for every string w ∈ L with |w| ≥ n, we can write w = uvxyz satisfying: (1) |vxy| ≤ n, (2) |vy| > 0, (3) uv^i xy^i z ∈ L for all i ≥ 0',
            'explanation': 'The CFL Pumping Lemma is used to prove that certain languages are NOT context-free. It states that sufficiently long strings in a CFL have two portions that can be pumped together.',
            'conditions': [
                '|vxy| ≤ n: The pumpable portions are within n characters',
                '|vy| > 0: At least one of v or y is non-empty',
                'uv^i xy^i z ∈ L for all i ≥ 0: Pumping v and y together keeps string in L'
            ],
            'how_to_use': [
                'Step 1: Assume L is context-free (for contradiction)',
                'Step 2: Let n be the pumping length',
                'Step 3: Choose a string w ∈ L with |w| ≥ n',
                'Step 4: By Pumping Lemma, w = uvxyz with given conditions',
                'Step 5: Show that uv^i xy^i z ∉ L for some i ≥ 0',
                'Step 6: This contradicts Pumping Lemma, so L is not context-free'
            ],
            'example': {
                'language': 'L = {a^n b^n c^n | n ≥ 0}',
                'proof': [
                    'Assume L is context-free with pumping length n',
                    'Choose w = a^n b^n c^n (clearly |w| = 3n ≥ n)',
                    'By PL, w = uvxyz where |vxy| ≤ n and |vy| > 0',
                    'Since |vxy| ≤ n, vxy can contain at most 2 different symbols',
                    'Case 1: If vxy contains only a\'s and b\'s, then pumping increases a\'s and b\'s but not c\'s',
                    'Case 2: If vxy contains only b\'s and c\'s, then pumping increases b\'s and c\'s but not a\'s',
                    'In both cases, uv^2xy^2z ∉ L because counts become unequal',
                    'Contradiction! Therefore L is not context-free'
                ],
                'conclusion': 'The language {a^n b^n c^n} is NOT context-free'
            },
            'common_applications': [
                '{a^n b^n c^n | n ≥ 0} - NOT context-free',
                '{ww | w ∈ {a,b}*} - NOT context-free',
                '{a^i b^j c^k | i = j or j = k} - Context-free',
                '{a^(n^2) | n ≥ 0} - NOT context-free'
            ],
            'diagram_filename': 'pumping_lemma_cfl.png'
        }
    
    def closure_properties_regular(self, parsed_input):
        """Explain closure properties of Regular Languages"""
        question = parsed_input.get('question', '')
        
        return {
            'topic': 'Closure Properties of Regular Languages',
            'explanation': 'Regular languages are closed under various operations. If L1 and L2 are regular languages, then the result of these operations is also regular.',
            'closed_operations': [
                {
                    'operation': 'Union (L1 ∪ L2)',
                    'description': 'The set of strings in either L1 or L2',
                    'proof_method': 'Construct DFA/NFA that simulates both machines in parallel',
                    'example': 'If L1 = {a^n | n ≥ 0} and L2 = {b^n | n ≥ 0}, then L1 ∪ L2 is regular'
                },
                {
                    'operation': 'Intersection (L1 ∩ L2)',
                    'description': 'The set of strings in both L1 and L2',
                    'proof_method': 'Construct product DFA with states (q1, q2)',
                    'example': 'If L1 = {strings with even a\'s} and L2 = {strings with even b\'s}, then L1 ∩ L2 is regular'
                },
                {
                    'operation': 'Concatenation (L1 · L2)',
                    'description': 'The set {xy | x ∈ L1, y ∈ L2}',
                    'proof_method': 'Construct NFA with ε-transitions from L1\'s accept states to L2\'s start state',
                    'example': 'If L1 = {a^n} and L2 = {b^n}, then L1 · L2 = {a^n b^m} is regular'
                },
                {
                    'operation': 'Kleene Star (L*)',
                    'description': 'The set of strings formed by concatenating zero or more strings from L',
                    'proof_method': 'Add ε-transitions from accept states back to start state',
                    'example': 'If L = {ab}, then L* = {ε, ab, abab, ababab, ...} is regular'
                },
                {
                    'operation': 'Complement (L̄)',
                    'description': 'The set of strings NOT in L (over the same alphabet)',
                    'proof_method': 'Swap accept and non-accept states in DFA',
                    'example': 'If L = {strings with even a\'s}, then L̄ = {strings with odd a\'s} is regular'
                },
                {
                    'operation': 'Reversal (L^R)',
                    'description': 'The set {w^R | w ∈ L}',
                    'proof_method': 'Reverse all transitions and swap start/accept states',
                    'example': 'If L = {ab, abc}, then L^R = {ba, cba} is regular'
                },
                {
                    'operation': 'Difference (L1 - L2)',
                    'description': 'The set of strings in L1 but not in L2',
                    'proof_method': 'L1 - L2 = L1 ∩ L̄2 (use intersection and complement)',
                    'example': 'Difference of two regular languages is regular'
                }
            ],
            'not_closed_operations': [],
            'summary': 'Regular languages are closed under: union, intersection, concatenation, Kleene star, complement, reversal, and difference.',
            'diagram_filename': 'closure_regular.png'
        }
    
    def closure_properties_cfl(self, parsed_input):
        """Explain closure properties of Context-Free Languages"""
        question = parsed_input.get('question', '')
        
        return {
            'topic': 'Closure Properties of Context-Free Languages',
            'explanation': 'Context-free languages are closed under some operations but NOT all. This is an important distinction from regular languages.',
            'closed_operations': [
                {
                    'operation': 'Union (L1 ∪ L2)',
                    'description': 'The set of strings in either L1 or L2',
                    'proof_method': 'Create new start symbol S → S1 | S2 where S1, S2 are start symbols of L1, L2',
                    'example': 'Union of {a^n b^n} and {a^n b^(2n)} is context-free'
                },
                {
                    'operation': 'Concatenation (L1 · L2)',
                    'description': 'The set {xy | x ∈ L1, y ∈ L2}',
                    'proof_method': 'Create new start symbol S → S1 S2',
                    'example': 'Concatenation of two CFLs is context-free'
                },
                {
                    'operation': 'Kleene Star (L*)',
                    'description': 'Zero or more concatenations of strings from L',
                    'proof_method': 'Create new start symbol S → ε | S S1',
                    'example': 'Star of {a^n b^n} is context-free'
                },
                {
                    'operation': 'Reversal (L^R)',
                    'description': 'The set {w^R | w ∈ L}',
                    'proof_method': 'Reverse all production rules',
                    'example': 'Reversal of a CFL is context-free'
                },
                {
                    'operation': 'Homomorphism',
                    'description': 'Apply a homomorphism h to all strings',
                    'proof_method': 'Replace each terminal a with h(a) in the grammar',
                    'example': 'Homomorphic image of CFL is context-free'
                }
            ],
            'not_closed_operations': [
                {
                    'operation': 'Intersection (L1 ∩ L2)',
                    'description': 'CFLs are NOT closed under intersection',
                    'counterexample': 'L1 = {a^n b^n c^m}, L2 = {a^m b^n c^n} are CFLs, but L1 ∩ L2 = {a^n b^n c^n} is NOT context-free',
                    'note': 'However, intersection with regular language IS closed'
                },
                {
                    'operation': 'Complement (L̄)',
                    'description': 'CFLs are NOT closed under complement',
                    'proof_method': 'Proven using intersection: if closed under complement and intersection, could prove {a^n b^n c^n} is CFL',
                    'note': 'Deterministic CFLs ARE closed under complement'
                },
                {
                    'operation': 'Difference (L1 - L2)',
                    'description': 'CFLs are NOT closed under difference',
                    'proof_method': 'L1 - L2 = L1 ∩ L̄2, requires intersection and complement',
                    'note': 'Difference with regular language IS closed'
                }
            ],
            'special_cases': [
                'CFL ∩ Regular = CFL (closed)',
                'CFL - Regular = CFL (closed)',
                'DCFL (Deterministic CFL) ∩ DCFL = may not be CFL'
            ],
            'summary': 'CFLs are closed under: union, concatenation, Kleene star, reversal, homomorphism. NOT closed under: intersection, complement, difference.',
            'diagram_filename': 'closure_cfl.png'
        }
