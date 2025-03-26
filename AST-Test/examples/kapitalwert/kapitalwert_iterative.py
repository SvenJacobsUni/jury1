def kapitalWert(principal, rate, n):
    """
    Berechnet den Kapitalwert iterativ (nicht-rekursiv).
    
    Args:
        principal (float): Das Anfangskapital
        rate (float): Der Zinssatz in Prozent
        n (int): Die Anzahl der Perioden
        
    Returns:
        float: Der Kapitalwert nach n Perioden
    """
    current_principal = principal
    
    for i in range(n):
        interest = current_principal * (rate / 100)
        current_principal += interest
    
    print(current_principal)
    return current_principal

# Beispielaufruf
if __name__ == "__main__":
    result = kapitalWert(1000, 5, 3)
    print(f"Kapitalwert nach 3 Jahren: {result}")
