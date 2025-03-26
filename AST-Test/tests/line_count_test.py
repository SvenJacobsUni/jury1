import sys
import os

# Füge den übergeordneten Ordner zum Pfad hinzu, um die Hilfsfunktionen zu importieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ast_test_utils import send_ast_request, create_line_count_conditions

def test_line_count(code_file, factorial_max=5, fib_max=7, server_url="http://localhost:3000"):
    """
    Testet, ob die Funktionen im Code die maximale Anzahl von Zeilen nicht überschreiten.
    
    Args:
        code_file (str): Pfad zur Python-Datei, die analysiert werden soll
        factorial_max (int): Maximale Anzahl der Zeilen für factorial
        fib_max (int): Maximale Anzahl der Zeilen für fib
        server_url (str): URL des Jury1-Servers
    """
    # AST-Bedingungen für Zeilenanzahl erstellen
    ast_conditions = create_line_count_conditions(factorial_max, fib_max)
    
    # Anfrage senden und Ergebnis anzeigen
    return send_ast_request(code_file, ast_conditions, server_url)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python line_count_test.py <python_file> [factorial_max] [fib_max] [server_url]")
        sys.exit(1)
    
    code_file = sys.argv[1]
    factorial_max = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    fib_max = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    server_url = sys.argv[4] if len(sys.argv) > 4 else "http://localhost:3000"
    
    test_line_count(code_file, factorial_max, fib_max, server_url)
