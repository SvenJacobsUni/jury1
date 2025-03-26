import requests
import json
import base64
import sys

def test_ast_analysis(code_file, server_url="http://localhost:3000"):
    """
    Testet die AST-Analyse-Funktionalität über einen HTTP-Aufruf.
    
    Args:
        code_file (str): Pfad zur Python-Datei, die analysiert werden soll
        server_url (str): URL des Jury1-Servers
    """
    # Python-Datei lesen
    with open(code_file, 'r') as f:
        code = f.read()
    
    # Base64-Kodierung des Codes
    code_base64 = base64.b64encode(code.encode()).decode()
    
    # Testdatei erstellen
    test_code = f"""
import unittest
from main import factorial, fib

class TestFunctions(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual(factorial(5), 120)
        
    def test_fibonacci(self):
        self.assertEqual(fib(5), 5)

if __name__ == '__main__':
    unittest.main()
"""
    test_code_base64 = base64.b64encode(test_code.encode()).decode()
    
    # AST-Bedingungen definieren
    ast_conditions = [
        {
            "type": "common.recursion",
            "parameters": {
                "functionName": "factorial"
            },
            "message": "Die Funktion 'factorial' muss rekursiv implementiert sein",
            "required": True
        },
        {
            "type": "common.recursion",
            "parameters": {
                "functionName": "fib"
            },
            "message": "Die Funktion 'fib' muss rekursiv implementiert sein",
            "required": True
        }
    ]
    
    # Request-Payload erstellen
    payload = {
        "mainFile": {
            "main.py": code_base64
        },
        "additionalFiles": {},
        "testFiles": {
            "test_main.py": test_code_base64
        },
        "runMethod": "factorial",  # Methode, die ausgeführt werden soll
        "input": "5",              # Eingabe für die Methode
        "astConditions": ast_conditions
    }
    
    # HTTP-Request senden
    endpoint = f"{server_url}/execute/python-assignment"
    headers = {"Content-Type": "application/json"}
    
    print(f"Sende Anfrage an {endpoint}...")
    response = requests.post(endpoint, json=payload, headers=headers)
    
    # Antwort verarbeiten
    print(f"Statuscode: {response.status_code}")
    
    # Erfolg, wenn Statuscode 200 oder 201 ist
    if response.status_code in [200, 201]:
        result = response.json()
        print("\n=== Ergebnis ===")
        print(f"Ausgabe: {result.get('output', '')}")
        print(f"Tests bestanden: {result.get('testsPassed', False)}")
        print(f"Test-Score: {result.get('score', 0)}%")
        
        # AST-Analyseergebnisse anzeigen
        ast_results = result.get('astResults', {})
        ast_conditions_passed = result.get('astConditionsPassed', False)
        
        print("\n=== AST-Analyse ===")
        print(f"AST-Bedingungen erfüllt: {ast_conditions_passed}")
        
        if ast_results and 'conditions' in ast_results:
            print("\nEinzelne Bedingungen:")
            for condition in ast_results['conditions']:
                status = "✅" if condition.get('passed', False) else "❌"
                print(f"{status} {condition.get('condition', '')}")
                print(f"   Details: {condition.get('details', '')}")
        
        return True
    else:
        print(f"Fehler: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python test_ast_analysis.py <python_file> [server_url]")
        sys.exit(1)
    
    code_file = sys.argv[1]
    server_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:3000"
    
    test_ast_analysis(code_file, server_url)
