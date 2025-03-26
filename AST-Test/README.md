# AST-Analyse-Test für Jury1

Dieses Verzeichnis enthält Skripte und Beispiele zum Testen der AST-Analyse-Funktionalität von Jury1.

## Ordnerstruktur

```
AST-Test/
├── examples/                  # Beispielcode für verschiedene Tests
│   ├── recursion/             # Beispiele für Rekursion
│   ├── parameters/            # Beispiele für Parameteranzahl
│   ├── lines/                 # Beispiele für Zeilenanzahl
│   └── kapitalwert/           # Beispiele für Kapitalwert
├── tests/                     # Test-Skripte
│   ├── recursion_test.py      # Test für Rekursion
│   ├── parameter_count_test.py # Test für Parameteranzahl
│   ├── line_count_test.py     # Test für Zeilenanzahl
│   └── kapitalwert_test.py    # Test für Kapitalwert
└── utils/                     # Hilfsfunktionen
    └── ast_test_utils.py      # Gemeinsame Funktionen für Tests
```

## Voraussetzungen

- Python 3.6 oder höher
- Das `requests`-Modul (`pip install requests`)
- Ein laufender Jury1-Server (standardmäßig auf http://localhost:3000)

## Schnellstart

Hier sind einige Beispiele, wie Sie die Tests ausführen können:

### Rekursionstest

Prüft, ob die Funktionen `factorial` und `fib` rekursiv implementiert sind:

```bash
cd AST-Test
python tests/recursion_test.py examples/recursion/recursive_functions.py
```

Erwartete Ausgabe:
```
=== AST-Analyse ===
AST-Bedingungen erfüllt: True

Einzelne Bedingungen:
✅ Die Funktion 'factorial' muss rekursiv implementiert sein
   Details: Function 'factorial' is recursive
✅ Die Funktion 'fib' muss rekursiv implementiert sein
   Details: Function 'fib' is recursive
```

### Parameteranzahl-Test

Prüft, ob die Funktionen `factorial` und `fib` die angegebene Anzahl von Parametern haben:

```bash
cd AST-Test
# Prüft auf genau einen Parameter
python tests/parameter_count_test.py examples/parameters/single_param_functions.py

# Prüft auf mehrere Parameter (2 für factorial, 3 für fib)
python tests/parameter_count_test.py examples/parameters/multi_param_functions.py 2 3
```

### Zeilenanzahl-Test

Prüft, ob die Funktionen `factorial` und `fib` die maximale Anzahl von Zeilen nicht überschreiten:

```bash
cd AST-Test
# Prüft auf maximal 3 Zeilen für factorial und 3 Zeilen für fib
python tests/line_count_test.py examples/lines/compact_functions.py 3 3

# Prüft auf maximal 20 Zeilen für factorial und 20 Zeilen für fib
python tests/line_count_test.py examples/lines/verbose_functions.py 20 20
```

### Kapitalwert-Test

Prüft, ob die Funktion `kapitalWert` rekursiv implementiert ist:

```bash
cd AST-Test
python tests/kapitalwert_test.py examples/kapitalwert/kapitalwert_recursive.py
```

## Detaillierte Verwendung

### Rekursionstest

```bash
python tests/recursion_test.py <python_file> [server_url]
```

Parameter:
- `<python_file>`: Pfad zur Python-Datei, die analysiert werden soll
- `[server_url]`: (Optional) URL des Jury1-Servers (Standard: http://localhost:3000)

Beispiele:
```bash
# Rekursive Implementierung testen
python tests/recursion_test.py examples/recursion/recursive_functions.py

# Nicht-rekursive Implementierung testen
python tests/recursion_test.py examples/recursion/non_recursive_functions.py

# Mit anderer Server-URL
python tests/recursion_test.py examples/recursion/recursive_functions.py http://example.com:3000
```

### Parameteranzahl-Test

```bash
python tests/parameter_count_test.py <python_file> [factorial_count] [fib_count] [server_url]
```

Parameter:
- `<python_file>`: Pfad zur Python-Datei, die analysiert werden soll
- `[factorial_count]`: (Optional) Erwartete Anzahl der Parameter für factorial (Standard: 1)
- `[fib_count]`: (Optional) Erwartete Anzahl der Parameter für fib (Standard: 1)
- `[server_url]`: (Optional) URL des Jury1-Servers (Standard: http://localhost:3000)

Beispiele:
```bash
# Funktionen mit einem Parameter testen
python tests/parameter_count_test.py examples/parameters/single_param_functions.py

# Funktionen mit mehreren Parametern testen
python tests/parameter_count_test.py examples/parameters/multi_param_functions.py 2 3
```

### Zeilenanzahl-Test

```bash
python tests/line_count_test.py <python_file> [factorial_max] [fib_max] [server_url]
```

Parameter:
- `<python_file>`: Pfad zur Python-Datei, die analysiert werden soll
- `[factorial_max]`: (Optional) Maximale Anzahl der Zeilen für factorial (Standard: 5)
- `[fib_max]`: (Optional) Maximale Anzahl der Zeilen für fib (Standard: 7)
- `[server_url]`: (Optional) URL des Jury1-Servers (Standard: http://localhost:3000)

Beispiele:
```bash
# Kompakte Funktionen testen
python tests/line_count_test.py examples/lines/compact_functions.py 3 3

# Ausführliche Funktionen testen
python tests/line_count_test.py examples/lines/verbose_functions.py 20 20
```

### Kapitalwert-Test

```bash
python tests/kapitalwert_test.py <python_file> [server_url]
```

Parameter:
- `<python_file>`: Pfad zur Python-Datei, die analysiert werden soll
- `[server_url]`: (Optional) URL des Jury1-Servers (Standard: http://localhost:3000)

Beispiele:
```bash
# Rekursive Implementierung testen
python tests/kapitalwert_test.py examples/kapitalwert/kapitalwert_recursive.py

# Nicht-rekursive Implementierung testen
python tests/kapitalwert_test.py examples/kapitalwert/kapitalwert_iterative.py
```

## Eigene Tests erstellen

Sie können die Hilfsfunktionen in `utils/ast_test_utils.py` verwenden, um eigene Tests zu erstellen. Die Hilfsfunktionen bieten Methoden zum Erstellen von AST-Bedingungen und zum Senden von Anfragen an den Jury1-Server.

Beispiel:
```python
import sys
import os

# Füge den übergeordneten Ordner zum Pfad hinzu, um die Hilfsfunktionen zu importieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ast_test_utils import send_ast_request, create_recursion_conditions

def test_my_condition(code_file, server_url="http://localhost:3000"):
    # AST-Bedingungen erstellen
    ast_conditions = create_recursion_conditions()
    
    # Anfrage senden und Ergebnis anzeigen
    return send_ast_request(code_file, ast_conditions, server_url)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python my_test.py <python_file> [server_url]")
        sys.exit(1)
    
    code_file = sys.argv[1]
    server_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:3000"
    
    test_my_condition(code_file, server_url)
