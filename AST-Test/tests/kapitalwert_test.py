import sys
import os

# Füge den übergeordneten Ordner zum Pfad hinzu, um die Hilfsfunktionen zu importieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ast_test_utils import send_ast_request, create_kapitalwert_recursion_condition

def test_kapitalwert(code_file, server_url="http://localhost:3000"):
    """
    Testet, ob die Kapitalwert-Funktion rekursiv implementiert ist.
    
    Args:
        code_file (str): Pfad zur Python-Datei, die analysiert werden soll
        server_url (str): URL des Jury1-Servers
    """
    # AST-Bedingungen für Kapitalwert-Rekursion erstellen
    ast_conditions = create_kapitalwert_recursion_condition()
    
    # Testdatei für Kapitalwert erstellen
    test_code = """
import unittest
from Kapitalwert import kapitalWert

class TestKapitalWert(unittest.TestCase):
    def test_case1(self):
        result = kapitalWert(2000, 5, 2)
        self.assertEqual(result, 2205.0, "Expected 2205.0")
        
    def test_case2(self):
        result = kapitalWert(500, 3, 7)
        self.assertAlmostEqual(result, 614.9369327124335, places=5, msg="Expected approximately 614.937")
        
    def test_case3(self):
        result = kapitalWert(100, 2, 18)
        self.assertAlmostEqual(result, 142.82462475762728, places=5, msg="Expected approximately 142.825")

if __name__ == '__main__':
    unittest.main()
"""
    
    # Anfrage senden und Ergebnis anzeigen
    # Wir verwenden hier spezielle Parameter für die Kapitalwert-Funktion
    return send_ast_request(
        code_file, 
        ast_conditions, 
        server_url, 
        run_method="kapitalWert", 
        input_value="1000,5,3"
    )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python kapitalwert_test.py <python_file> [server_url]")
        sys.exit(1)
    
    code_file = sys.argv[1]
    server_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:3000"
    
    test_kapitalwert(code_file, server_url)
