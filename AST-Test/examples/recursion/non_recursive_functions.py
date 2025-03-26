def factorial(n):
    """
    Berechnet die Fakultät einer Zahl iterativ (nicht-rekursiv).
    
    Args:
        n (int): Die Zahl, deren Fakultät berechnet werden soll
        
    Returns:
        int: Die Fakultät von n
    """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def fib(n):
    """
    Berechnet die n-te Fibonacci-Zahl iterativ (nicht-rekursiv).
    
    Args:
        n (int): Der Index der Fibonacci-Zahl
        
    Returns:
        int: Die n-te Fibonacci-Zahl
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Beispielaufruf
if __name__ == "__main__":
    print(f"factorial(5) = {factorial(5)}")
    print(f"fib(5) = {fib(5)}")
