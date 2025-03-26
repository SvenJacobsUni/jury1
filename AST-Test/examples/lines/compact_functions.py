def factorial(n):
    """Berechnet die Fakultät einer Zahl rekursiv."""
    if n <= 1: return 1
    else: return n * factorial(n-1)

def fib(n):
    """Berechnet die n-te Fibonacci-Zahl rekursiv."""
    if n <= 1: return n
    else: return fib(n-1) + fib(n-2)

# Beispielaufruf
if __name__ == "__main__":
    print(f"factorial(5) = {factorial(5)}")
    print(f"fib(5) = {fib(5)}")
