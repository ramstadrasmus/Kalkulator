import math

# Global variabel for minnefunksjon
memory = 0.0

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
    Leser operasjon. Tillater +, -, *, /, %, sqrt, M+, M-, MR eller q for å avslutte.
    """
    valid = {"+", "-", "*", "/", "%", "sqrt", "m+", "m-", "mr", "q"}
    while True:
        op = input("Velg operasjon (+, -, *, /, %, sqrt, M+, M-, MR) eller 'q' for å avslutte: ").strip().lower()
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
    if op == "%":
        # Beregner b prosent av a: (a * b) / 100
        return (a * b) / 100
    raise ValueError(f"Ukjent operasjon: {op}")

def main() -> None:
    global memory
    print("=== Enkel kalkulator (skriv 'q' når som helst for å avslutte) ===")
    print("Tilgjengelige operasjoner: +, -, *, /, %, sqrt, M+, M-, MR")
    print("  % : Beregner b prosent av a (f.eks. 200 % 10 = 20)")
    print("  sqrt : Beregner kvadratroten av første tall")
    print("  M+ : Legger resultatet til minnet")
    print("  M- : Trekker resultatet fra minnet")
    print("  MR : Viser minnets verdi\n")

    while True:
        try:
            op = read_op()
            if op == "q":
                print("Avslutter.")
                return

            # Minneoperasjoner
            if op == "mr":
                print(f"Minne: {memory}")
                continue

            # Operasjoner som krever ett tall (unære)
            if op == "sqrt":
                a = parse_number("Tall: ")
                if a < 0:
                    print("Kan ikke ta kvadratrot av negativt tall.")
                    continue
                result = math.sqrt(a)
                print("Resultat:", result)

            # Operasjoner som krever to tall (binære)
            elif op in {"+", "-", "*", "/", "%"}:
                a = parse_number("Første tall: ")
                b = parse_number("Andre tall: ")
                result = calculate(a, b, op)
                print("Resultat:", result)

            # Lagre resultat i minne
            elif op == "m+":
                a = parse_number("Tall å legge til minnet: ")
                memory += a
                print(f"Lagt til i minne. Nytt minne: {memory}")
                continue

            elif op == "m-":
                a = parse_number("Tall å trekke fra minnet: ")
                memory -= a
                print(f"Trukket fra minne. Nytt minne: {memory}")
                continue

        except ZeroDivisionError as e:
            print(e)
        except KeyboardInterrupt:
            print("\nAvslutter.")
            return

if __name__ == "__main__":
    main()
