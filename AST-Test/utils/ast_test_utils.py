import requests
import json
import base64
import sys

def send_ast_request(code_file, ast_conditions, server_url="http://localhost:3000", run_method="factorial", input_value="5"):
    """
    Sendet eine Anfrage an den Jury1-Server, um die AST-Analyse durchzuführen.
    
    Args:
        code_file (str): Pfad zur Python-Datei, die analysiert werden soll
        ast_conditions (list): Liste der AST-Bedingungen
        server_url (str): URL des Jury1-Servers
        run_method (str): Methode, die ausgeführt werden soll
        input_value (str): Eingabe für die Methode
        
    Returns:
        dict: Die Antwort des Servers
    """
    # Python-Datei lesen
    with open(code_file, 'r') as f:
        code = f.read()
    
    # Base64-Kodierung des Codes
    code_base64 = base64.b64encode(code.encode()).decode()
    
    # Testdatei erstellen
    test_code = """
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
    
    # Request-Payload erstellen
    payload = {
        "mainFile": {
            "main.py": code_base64
        },
        "additionalFiles": {},
        "testFiles": {
            "test_main.py": test_code_base64
        },
        "runMethod": run_method,
        "input": input_value,
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
        
        return result
    else:
        print(f"Fehler: {response.status_code}")
        print(response.text)
        return None

def create_recursion_conditions():
    """
    Erstellt AST-Bedingungen für die Rekursionsprüfung.
    
    Returns:
        list: Liste der AST-Bedingungen
    """
    return [
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

def create_parameter_count_conditions(factorial_count=1, fib_count=1):
    """
    Erstellt AST-Bedingungen für die Parameteranzahl-Prüfung.
    
    Args:
        factorial_count (int): Erwartete Anzahl der Parameter für factorial
        fib_count (int): Erwartete Anzahl der Parameter für fib
        
    Returns:
        list: Liste der AST-Bedingungen
    """
    # Benutzerdefinierter Code für die AST-Analyse
    # Dieser Code prüft, ob die Funktion die angegebene Anzahl von Parametern hat
    custom_code = """
# Suche nach der Funktion
function_name = parameters.get('functionName', 'factorial')
param_count = parameters.get('paramCount', 1)

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == function_name:
        actual_param_count = len(node.args.args)
        if actual_param_count == param_count:
            result = (True, f"Function '{function_name}' has exactly {param_count} parameter(s)")
        else:
            result = (False, f"Function '{function_name}' has {actual_param_count} parameter(s), but {param_count} expected")
        break
else:
    result = (False, f"Function '{function_name}' not found")
"""
    
    return [
        {
            "type": "custom",
            "parameters": {
                "code": custom_code,
                "functionName": "factorial",
                "paramCount": factorial_count
            },
            "message": f"Die Funktion 'factorial' muss genau {factorial_count} Parameter haben",
            "required": True
        },
        {
            "type": "custom",
            "parameters": {
                "code": custom_code,
                "functionName": "fib",
                "paramCount": fib_count
            },
            "message": f"Die Funktion 'fib' muss genau {fib_count} Parameter haben",
            "required": True
        }
    ]

def create_line_count_conditions(factorial_max=5, fib_max=7):
    """
    Erstellt AST-Bedingungen für die Zeilenanzahl-Prüfung.
    
    Args:
        factorial_max (int): Maximale Anzahl der Zeilen für factorial
        fib_max (int): Maximale Anzahl der Zeilen für fib
        
    Returns:
        list: Liste der AST-Bedingungen
    """
    # Benutzerdefinierter Code für die AST-Analyse
    # Dieser Code prüft, ob die Funktion eine bestimmte Anzahl von Zeilen hat
    custom_code = """
# Suche nach der Funktion
function_name = parameters.get('functionName', 'factorial')
max_lines = parameters.get('maxLines', 5)

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == function_name:
        # Bestimme die Start- und Endzeile der Funktion
        start_line = node.lineno
        end_line = 0
        
        # Finde die letzte Zeile der Funktion
        for child in ast.walk(node):
            if hasattr(child, 'lineno'):
                end_line = max(end_line, child.lineno)
        
        # Berechne die Anzahl der Zeilen
        line_count = end_line - start_line + 1
        
        if line_count <= max_lines:
            result = (True, f"Function '{function_name}' has {line_count} lines, which is within the limit of {max_lines}")
        else:
            result = (False, f"Function '{function_name}' has {line_count} lines, which exceeds the limit of {max_lines}")
        break
else:
    result = (False, f"Function '{function_name}' not found")
"""
    
    return [
        {
            "type": "custom",
            "parameters": {
                "code": custom_code,
                "functionName": "factorial",
                "maxLines": factorial_max
            },
            "message": f"Die Funktion 'factorial' darf maximal {factorial_max} Zeilen haben",
            "required": True
        },
        {
            "type": "custom",
            "parameters": {
                "code": custom_code,
                "functionName": "fib",
                "maxLines": fib_max
            },
            "message": f"Die Funktion 'fib' darf maximal {fib_max} Zeilen haben",
            "required": True
        }
    ]

def create_kapitalwert_recursion_condition():
    """
    Erstellt AST-Bedingungen für die Rekursionsprüfung der Kapitalwert-Funktion.
    
    Returns:
        list: Liste der AST-Bedingungen
    """
    return [
        {
            "type": "common.recursion",
            "parameters": {
                "functionName": "kapitalWert"
            },
            "message": "Die Funktion 'kapitalWert' muss rekursiv implementiert sein",
            "required": True
        }
    ]
