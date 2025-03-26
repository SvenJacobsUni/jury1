# AST-Analyse-Test für Jury1

Dieses Verzeichnis enthält Skripte zum Testen der AST-Analyse-Funktionalität von Jury1.

## Dateien

- `test_ast_analysis.py`: Ein Python-Skript zum Testen der AST-Analyse über HTTP
- `recursive_functions.py`: Eine Beispieldatei mit rekursiven Implementierungen von Fakultät und Fibonacci
- `non_recursive_functions.py`: Eine Beispieldatei mit nicht-rekursiven Implementierungen zum Vergleich

## Voraussetzungen

- Python 3.6 oder höher
- Das `requests`-Modul (`pip install requests`)
- Ein laufender Jury1-Server (standardmäßig auf http://localhost:3000)

## Verwendung

1. Stellen Sie sicher, dass der Jury1-Server läuft.

2. Führen Sie das Test-Skript mit einer Python-Datei als Argument aus:

   ```bash
   python test_ast_analysis.py recursive_functions.py
   ```

   oder

   ```bash
   python test_ast_analysis.py non_recursive_functions.py
   ```

3. Optional können Sie eine andere Server-URL angeben:

   ```bash
   python test_ast_analysis.py recursive_functions.py http://example.com:3000
   ```

## Erwartete Ergebnisse

### Für rekursive Funktionen

Wenn Sie `recursive_functions.py` testen, sollten beide AST-Bedingungen erfüllt sein:

```
=== AST-Analyse ===
AST-Bedingungen erfüllt: True

Einzelne Bedingungen:
✅ Die Funktion 'factorial' muss rekursiv implementiert sein
   Details: Function 'factorial' is recursive
✅ Die Funktion 'fib' muss rekursiv implementiert sein
   Details: Function 'fib' is recursive
```

### Für nicht-rekursive Funktionen

Wenn Sie `non_recursive_functions.py` testen, sollten beide AST-Bedingungen nicht erfüllt sein:

```
=== AST-Analyse ===
AST-Bedingungen erfüllt: False

Einzelne Bedingungen:
❌ Die Funktion 'factorial' muss rekursiv implementiert sein
   Details: Function 'factorial' is not recursive
❌ Die Funktion 'fib' muss rekursiv implementiert sein
   Details: Function 'fib' is not recursive
```

## Anpassung

Sie können das Test-Skript anpassen, um andere AST-Bedingungen zu testen, indem Sie die `ast_conditions`-Liste im Skript ändern.
