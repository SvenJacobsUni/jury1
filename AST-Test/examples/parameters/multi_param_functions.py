def factorial(n, base=1):
    """
    Berechnet die Fakultät einer Zahl rekursiv mit einem optionalen Basiswert.
    
    Args:
        n (int): Die Zahl, deren Fakultät berechnet werden soll
        base (int, optional): Der Basiswert für die Berechnung. Standardwert ist 1.
        
    Returns:
        int: Die Fakultät von n
    """
    if n <= 1:
        return base
    else:
        return n * factorial(n-1, base)

def fib(n, a=0, b=1):
    """
    Berechnet die n-te Fibonacci-Zahl rekursiv mit optionalen Startwerten.
    
    Args:
        n (int): Der Index der Fibonacci-Zahl
        a (int, optional): Der erste Startwert. Standardwert ist 0.
        b (int, optional): Der zweite Startwert. Standardwert ist 1.
        
    Returns:
        int: Die n-te Fibonacci-Zahl
    """
    if n <= 0:
        return a
    elif n == 1:
        return b
    else:
        return fib(n-1, b, a+b)

# Beispielaufruf
if __name__ == "__main__":
    print(f"factorial(5) = {factorial(5)}")
    print(f"factorial(5, 2) = {factorial(5, 2)}")
    print(f"fib(5) = {fib(5)}")
    print(f"fib(5, 1, 1) = {fib(5, 1, 1)}")
