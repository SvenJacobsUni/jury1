import sys
import os

# Füge den übergeordneten Ordner zum Pfad hinzu, um die Hilfsfunktionen zu importieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ast_test_utils import send_ast_request, create_recursion_conditions

def test_recursion(code_file, server_url="http://localhost:3000"):
    """
    Testet, ob die Funktionen im Code rekursiv implementiert sind.
    
    Args:
        code_file (str): Pfad zur Python-Datei, die analysiert werden soll
        server_url (str): URL des Jury1-Servers
    """
    # AST-Bedingungen für Rekursion erstellen
    ast_conditions = create_recursion_conditions()
    
    # Anfrage senden und Ergebnis anzeigen
    return send_ast_request(code_file, ast_conditions, server_url)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python recursion_test.py <python_file> [server_url]")
        sys.exit(1)
    
    code_file = sys.argv[1]
    server_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:3000"
    
    test_recursion(code_file, server_url)
