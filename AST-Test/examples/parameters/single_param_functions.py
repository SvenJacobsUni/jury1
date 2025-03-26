def factorial(n):
    """
    Berechnet die Fakultät einer Zahl rekursiv.
    
    Args:
        n (int): Die Zahl, deren Fakultät berechnet werden soll
        
    Returns:
        int: Die Fakultät von n
    """
    if n <= 1:
        return 1
    else:
        return n * factorial(n-1)

def fib(n):
    """
    Berechnet die n-te Fibonacci-Zahl rekursiv.
    
    Args:
        n (int): Der Index der Fibonacci-Zahl
        
    Returns:
        int: Die n-te Fibonacci-Zahl
    """
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

# Beispielaufruf
if __name__ == "__main__":
    print(f"factorial(5) = {factorial(5)}")
    print(f"fib(5) = {fib(5)}")
