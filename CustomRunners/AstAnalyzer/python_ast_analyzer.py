import ast
import json
import sys
import os

class AstAnalyzer:
    def __init__(self):
        # Registrierung von Bedingungsprüfern
        self.condition_checkers = {
            'common.recursion': self.check_recursion,
            'common.dataType': self.check_data_type,
            'python.forLoop': self.check_for_loop,
            'python.whileLoop': self.check_while_loop,
            'python.listComprehension': self.check_list_comprehension,
            'python.functionCall': self.check_function_call,
            'python.import': self.check_import,
            'custom': self.check_custom
        }

    def analyze(self, code_file, conditions_file, output_file):
        """
        Führt die AST-Analyse für den gegebenen Code mit den gegebenen Bedingungen durch
        und schreibt die Ergebnisse in die Ausgabedatei.
        
        Args:
            code_file (str): Pfad zur Codedatei
            conditions_file (str): Pfad zur JSON-Datei mit den Bedingungen
            output_file (str): Pfad zur Ausgabedatei für die Ergebnisse
        """
        # Code aus Datei lesen
        try:
            with open(code_file, 'r') as f:
                code = f.read()
        except Exception as e:
            # Bei Fehlern beim Lesen der Datei ein Fehlerergebnis zurückgeben
            results = {
                'conditions': [],
                'passed': False,
                'score': 0,
                'error': f'Failed to read code file: {str(e)}'
            }
            with open(output_file, 'w') as f:
                json.dump(results, f)
            return

        # Bedingungen aus JSON-Datei lesen
        try:
            with open(conditions_file, 'r') as f:
                conditions = json.load(f)
        except Exception as e:
            # Bei Fehlern beim Lesen der Bedingungen ein Fehlerergebnis zurückgeben
            results = {
                'conditions': [],
                'passed': False,
                'score': 0,
                'error': f'Failed to read conditions file: {str(e)}'
            }
            with open(output_file, 'w') as f:
                json.dump(results, f)
            return

        # AST parsen
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            # Bei Syntaxfehlern ein Fehlerergebnis zurückgeben
            results = {
                'conditions': [],
                'passed': False,
                'score': 0,
                'error': f'Syntax error: {str(e)}'
            }
            with open(output_file, 'w') as f:
                json.dump(results, f)
            return

        # Jede Bedingung prüfen
        condition_results = []
        required_passed = True
        passed_count = 0

        for condition in conditions:
            condition_type = condition['type']
            parameters = condition.get('parameters', {})
            message = condition['message']
            required = condition.get('required', True)

            # Bedingung mit dem entsprechenden Prüfer prüfen
            checker = self.condition_checkers.get(condition_type)
            if checker:
                passed, details = checker(tree, parameters)
            else:
                passed, details = False, f"Unknown condition type: {condition_type}"

            # Ergebnis speichern
            condition_results.append({
                'condition': message,
                'passed': passed,
                'details': details
            })

            # Gesamtergebnis aktualisieren
            if required and not passed:
                required_passed = False
            if passed:
                passed_count += 1

        # Gesamtergebnis berechnen
        score = (passed_count / len(conditions)) * 100 if conditions else 0

        # Ergebnisse in Ausgabedatei schreiben
        results = {
            'conditions': condition_results,
            'passed': required_passed,
            'score': score
        }
        with open(output_file, 'w') as f:
            json.dump(results, f)

    def check_recursion(self, tree, parameters):
        """
        Prüft, ob eine Funktion sich selbst rekursiv aufruft.
        
        Args:
            tree (ast.AST): Der AST des Codes
            parameters (dict): Die Parameter der Bedingung
                - functionName (str): Der Name der zu prüfenden Funktion
                
        Returns:
            tuple: (passed, details)
                - passed (bool): Ob die Bedingung erfüllt wurde
                - details (str): Details zum Ergebnis
        """
        function_name = parameters.get('functionName')
        if not function_name:
            return False, "No function name provided"
        
        # Rekursive Funktionsaufrufe finden
        class RecursionVisitor(ast.NodeVisitor):
            def __init__(self):
                self.functions = {}
                self.recursive_functions = set()
                
            def visit_FunctionDef(self, node):
                self.functions[node.name] = node
                # Funktionskörper besuchen
                self.generic_visit(node)
                
            def visit_Call(self, node):
                # Prüfen, ob es sich um einen Funktionsaufruf handelt
                if isinstance(node.func, ast.Name):
                    # Prüfen, ob die Funktion sich selbst aufruft
                    caller = self.get_parent_function(node)
                    if caller and node.func.id == caller.name:
                        self.recursive_functions.add(caller.name)
                # Weiter besuchen
                self.generic_visit(node)
                
            def get_parent_function(self, node):
                # Findet die umgebende Funktion für einen Knoten
                parent = node
                while hasattr(parent, 'parent'):
                    parent = parent.parent
                    if isinstance(parent, ast.FunctionDef):
                        return parent
                return None
        
        # AST mit Elternknoten anreichern
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
                
        # AST besuchen
        visitor = RecursionVisitor()
        visitor.visit(tree)
        
        # Prüfen, ob die gesuchte Funktion rekursiv ist
        if function_name in visitor.recursive_functions:
            return True, f"Function '{function_name}' is recursive"
        elif function_name in visitor.functions:
            return False, f"Function '{function_name}' is not recursive"
        else:
            return False, f"Function '{function_name}' not found"

    def check_data_type(self, tree, parameters):
        """
        Prüft, ob ein bestimmter Datentyp verwendet wird.
        
        Args:
            tree (ast.AST): Der AST des Codes
            parameters (dict): Die Parameter der Bedingung
                - dataType (str): Der zu prüfende Datentyp
                
        Returns:
            tuple: (passed, details)
                - passed (bool): Ob die Bedingung erfüllt wurde
                - details (str): Details zum Ergebnis
        """
        # Grundgerüst für die Datentyp-Prüfung
        return False, "Data type check not implemented yet"

    def check_for_loop(self, tree, parameters):
        """
        Prüft, ob For-Schleifen verwendet werden.
        
        Args:
            tree (ast.AST): Der AST des Codes
            parameters (dict): Die Parameter der Bedingung
                
        Returns:
            tuple: (passed, details)
                - passed (bool): Ob die Bedingung erfüllt wurde
                - details (str): Details zum Ergebnis
        """
        # Grundgerüst für die For-Loop-Prüfung
        return False, "For loop check not implemented yet"

    def check_while_loop(self, tree, parameters):
        """
        Prüft, ob While-Schleifen verwendet werden.
        
        Args:
            tree (ast.AST): Der AST des Codes
            parameters (dict): Die Parameter der Bedingung
                
        Returns:
            tuple: (passed, details)
                - passed (bool): Ob die Bedingung erfüllt wurde
                - details (str): Details zum Ergebnis
        """
        # Grundgerüst für die While-Loop-Prüfung
        return False, "While loop check not implemented yet"

    def check_list_comprehension(self, tree, parameters):
        """
        Prüft, ob List Comprehensions verwendet werden.
        
        Args:
            tree (ast.AST): Der AST des Codes
            parameters (dict): Die Parameter der Bedingung
                
        Returns:
            tuple: (passed, details)
                - passed (bool): Ob die Bedingung erfüllt wurde
                - details (str): Details zum Ergebnis
        """
        # Grundgerüst für die List-Comprehension-Prüfung
        return False, "List comprehension check not implemented yet"

    def check_function_call(self, tree, parameters):
        """
        Prüft, ob eine bestimmte Funktion aufgerufen wird.
        
        Args:
            tree (ast.AST): Der AST des Codes
            parameters (dict): Die Parameter der Bedingung
                - functionName (str): Der Name der zu prüfenden Funktion
                
        Returns:
            tuple: (passed, details)
                - passed (bool): Ob die Bedingung erfüllt wurde
                - details (str): Details zum Ergebnis
        """
        # Grundgerüst für die Funktionsaufruf-Prüfung
        return False, "Function call check not implemented yet"

    def check_import(self, tree, parameters):
        """
        Prüft, ob ein bestimmtes Modul importiert wird.
        
        Args:
            tree (ast.AST): Der AST des Codes
            parameters (dict): Die Parameter der Bedingung
                - moduleName (str): Der Name des zu prüfenden Moduls
                
        Returns:
            tuple: (passed, details)
                - passed (bool): Ob die Bedingung erfüllt wurde
                - details (str): Details zum Ergebnis
        """
        # Grundgerüst für die Import-Prüfung
        return False, "Import check not implemented yet"

    def check_custom(self, tree, parameters):
        """
        Führt eine benutzerdefinierte Bedingungsprüfung aus.
        
        Args:
            tree (ast.AST): Der AST des Codes
            parameters (dict): Die Parameter der Bedingung
                - code (str): Der auszuführende Code
                
        Returns:
            tuple: (passed, details)
                - passed (bool): Ob die Bedingung erfüllt wurde
                - details (str): Details zum Ergebnis
        """
        # Grundgerüst für die benutzerdefinierte Bedingungsprüfung
        return False, "Custom check not implemented yet"


if __name__ == "__main__":
    # Pfade für Code, Bedingungen und Ausgabe
    code_file = sys.argv[1] if len(sys.argv) > 1 else '/usr/src/app/main.py'
    conditions_file = sys.argv[2] if len(sys.argv) > 2 else '/usr/src/app/ast-conditions.json'
    output_file = sys.argv[3] if len(sys.argv) > 3 else '/usr/src/app/ast-results.json'

    # AST-Analyse durchführen
    analyzer = AstAnalyzer()
    analyzer.analyze(code_file, conditions_file, output_file)
