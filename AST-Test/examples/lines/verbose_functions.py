def factorial(n):
    """
    Berechnet die Fakultät einer Zahl rekursiv.
    
    Diese Funktion verwendet einen rekursiven Ansatz, um die Fakultät zu berechnen.
    Die Fakultät einer Zahl n ist das Produkt aller positiven ganzen Zahlen kleiner oder gleich n.
    
    Args:
        n (int): Die Zahl, deren Fakultät berechnet werden soll
        
    Returns:
        int: Die Fakultät von n
    """
    # Basisfall: Fakultät von 0 oder 1 ist 1
    if n <= 1:
        return 1
    
    # Rekursiver Fall: n * Fakultät von (n-1)
    else:
        result = n * factorial(n-1)
        return result

def fib(n):
    """
    Berechnet die n-te Fibonacci-Zahl rekursiv.
    
    Diese Funktion verwendet einen rekursiven Ansatz, um die Fibonacci-Zahl zu berechnen.
    Die Fibonacci-Folge ist definiert als: F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) für n > 1.
    
    Args:
        n (int): Der Index der Fibonacci-Zahl
        
    Returns:
        int: Die n-te Fibonacci-Zahl
    """
    # Basisfall: Fibonacci von 0 ist 0, Fibonacci von 1 ist 1
    if n <= 1:
        return n
    
    # Rekursiver Fall: Fibonacci von (n-1) + Fibonacci von (n-2)
    else:
        result = fib(n-1) + fib(n-2)
        return result

# Beispielaufruf
if __name__ == "__main__":
    # Berechne und gib die Fakultät von 5 aus
    factorial_result = factorial(5)
    print(f"factorial(5) = {factorial_result}")
    
    # Berechne und gib die 5. Fibonacci-Zahl aus
    fibonacci_result = fib(5)
    print(f"fib(5) = {fibonacci_result}")
