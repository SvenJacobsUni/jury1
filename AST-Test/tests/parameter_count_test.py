import sys
import os

# Füge den übergeordneten Ordner zum Pfad hinzu, um die Hilfsfunktionen zu importieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ast_test_utils import send_ast_request, create_parameter_count_conditions

def test_parameter_count(code_file, factorial_count=1, fib_count=1, server_url="http://localhost:3000"):
    """
    Testet, ob die Funktionen im Code die angegebene Anzahl von Parametern haben.
    
    Args:
        code_file (str): Pfad zur Python-Datei, die analysiert werden soll
        factorial_count (int): Erwartete Anzahl der Parameter für factorial
        fib_count (int): Erwartete Anzahl der Parameter für fib
        server_url (str): URL des Jury1-Servers
    """
    # AST-Bedingungen für Parameteranzahl erstellen
    ast_conditions = create_parameter_count_conditions(factorial_count, fib_count)
    
    # Anfrage senden und Ergebnis anzeigen
    return send_ast_request(code_file, ast_conditions, server_url)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python parameter_count_test.py <python_file> [factorial_count] [fib_count] [server_url]")
        sys.exit(1)
    
    code_file = sys.argv[1]
    factorial_count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    fib_count = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    server_url = sys.argv[4] if len(sys.argv) > 4 else "http://localhost:3000"
    
    test_parameter_count(code_file, factorial_count, fib_count, server_url)
