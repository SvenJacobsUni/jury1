def kapitalWert(principal, rate, n):
    """
    Berechnet den Kapitalwert rekursiv.
    
    Args:
        principal (float): Das Anfangskapital
        rate (float): Der Zinssatz in Prozent
        n (int): Die Anzahl der Perioden
        
    Returns:
        float: Der Kapitalwert nach n Perioden
    """
    if n == 0:
        print(principal)
        return principal
    else:
        interest = principal * (rate / 100)
        new_principal = principal + interest
        return kapitalWert(new_principal, rate, n-1)

# Beispielaufruf
if __name__ == "__main__":
    result = kapitalWert(1000, 5, 3)
    print(f"Kapitalwert nach 3 Jahren: {result}")
