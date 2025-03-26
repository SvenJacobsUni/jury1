import requests
import json
import base64
import sys

def test_kapitalwert_analysis(code_file, server_url="http://localhost:3000"):
    """
    Testet die AST-Analyse-Funktionalität für die Kapitalwert-Funktion über einen HTTP-Aufruf.
    
    Args:
        code_file (str): Pfad zur Python-Datei mit der Kapitalwert-Funktion
        server_url (str): URL des Jury1-Servers
    """
    # Python-Datei lesen
    with open(code_file, 'r') as f:
        code = f.read()
    
    # Base64-Kodierung des Codes
    code_base64 = base64.b64encode(code.encode()).decode()
    
    # Testdatei erstellen
    test_code = """
# Kapitalwert_test.py

import unittest
from Kapitalwert import kapitalWert

class TestKapitalWert(unittest.TestCase):
    # Defines a series of unit tests for the kapitalWert function.
    
    def test_case1(self):
        # Test case 1: Standard input.
        result = kapitalWert(2000, 5, 2)
        self.assertEqual(result, 2205.0, "Expected 2205.0")
        
    def test_case2(self):
        # Test case 2: Different input.
        result = kapitalWert(500, 3, 7)
        self.assertAlmostEqual(result, 614.9369327124335, places=5, msg="Expected approximately 614.937")
        
    def test_case3(self):
        # Test case 3: Another input variation.
        result = kapitalWert(100, 2, 18)
        self.assertAlmostEqual(result, 142.82462475762728, places=5, msg="Expected approximately 142.825")

if __name__ == '__main__':
    unittest.main()
"""
    test_code_base64 = base64.b64encode(test_code.encode()).decode()
    
    # AST-Bedingungen definieren
    ast_conditions = [
        {
            "type": "common.recursion",
            "parameters": {
                "functionName": "kapitalWert"
            },
            "message": "Die Funktion 'kapitalWert' muss rekursiv implementiert sein",
            "required": True
        }
    ]
    
    # Request-Payload erstellen
    payload = {
        "mainFile": {
            "Kapitalwert.py": code_base64
        },
        "additionalFiles": {},
        "testFiles": {
            "test_Kapitalwert.py": test_code_base64
        },
        "runMethod": "kapitalWert",  # Methode, die ausgeführt werden soll
        "input": "1000,5,3",         # Eingabe für die Methode
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
        print("Verwendung: python test_kapitalwert_analysis.py <python_file> [server_url]")
        sys.exit(1)
    
    code_file = sys.argv[1]
    server_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:3000"
    
    test_kapitalwert_analysis(code_file, server_url)
