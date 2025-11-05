def parse_number(prompt: str) -> float:
    """
    Leser et tall fra input. Godtar både 3.5 og 3,5.
    Spør på nytt til brukeren skriver et gyldig tall eller 'q' for å avslutte.
    """
    while True:
        s = input(prompt).strip().lower()
        if s == "q":
            raise KeyboardInterrupt  # Brukes for å avbryte programmet ryddig
        s = s.replace(",", ".")  # støtt norsk komma
        try:
            return float(s)
        except ValueError:
            print("Ugyldig tall. Prøv igjen (skriv 'q' for å avslutte).")

def read_op() -> str:
    """
    Leser operasjon. Tillater +, -, *, / eller q for å avslutte.
    """
    valid = {"+", "-", "*", "/", "q"}
    while True:
        op = input("Velg operasjon (+, -, *, /) eller 'q' for å avslutte: ").strip().lower()
        if op in valid:
            return op
        print("Ukjent operasjon. Prøv igjen.")

def calculate(a: float, b: float, op: str) -> float:
    """
    Utfører selve beregningen. Kaster ZeroDivisionError ved deling på 0.
    """
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("Kan ikke dele på 0.")
        return a / b
    raise ValueError(f"Ukjent operasjon: {op}")

def main() -> None:
    print("=== Enkel kalkulator (skriv 'q' når som helst for å avslutte) ===")
    while True:
        try:
            a = parse_number("Første tall: ")
            b = parse_number("Andre tall: ")
            op = read_op()
            if op == "q":
                print("Avslutter.")
                return
            result = calculate(a, b, op)
            print("Resultat:", result)
        except ZeroDivisionError as e:
            print(e)
        except KeyboardInterrupt:
            print("\nAvslutter.")
            return

if __name__ == "__main__":
    main()
