print("Kalkulator (q for å avslutte)")

while True:
    inp = input("\nOperasjon (f.eks. 5 + 3): ").strip()

    if inp.lower() == 'q':
        print("Avslutter...")
        break

    try:
        parts = inp.split()
        if len(parts) != 3:
            raise ValueError("Ugyldig format")

        tall1, operator, tall2 = float(parts[0]), parts[1], float(parts[2])

        if operator == '+': resultat = tall1 + tall2
        elif operator == '-': resultat = tall1 - tall2
        elif operator == '*': resultat = tall1 * tall2
        elif operator == '/': resultat = tall1 / tall2 if tall2 != 0 else "Kan ikke dele på 0"
        else: raise ValueError(f"Ukjent operator: {operator}")

        print(f"Resultat: {resultat}")
    except (ValueError, IndexError) as e:
        print(f"Feil: {e}. Prøv igjen (format: tall operator tall)")