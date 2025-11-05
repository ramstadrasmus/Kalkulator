# Kalkulator - CLI og Windows GUI

Lite Python-program for å gjøre enkle beregninger, tilgjengelig i både CLI og GUI-versjon.

## Versjoner

- **main.py**: Opprinnelig CLI-versjon
- **gui_calculator.py**: Windows GUI-versjon med Tkinter

## Funksjoner

- **Aritmetiske operasjoner**: +, -, *, /, %
- **Kvadratrot (sqrt)**: Beregner kvadratroten av første tall
- **Prosentberegning (%)**: Beregner b prosent av a (f.eks. 200 % 10 = 20)
- **Minnefunksjoner**:
  - **M+**: Legger resultatet til minnet
  - **M-**: Trekker resultatet fra minnet
  - **MR**: Viser minnets verdi
  - **MC**: Tømmer minnet
- **Støtte for norsk komma**: Både '.' og ',' fungerer som desimalskille
- **Tallknapper (GUI)**: 0-9 for å legge til siffer i fokusert felt
- **Desimalknapper (GUI)**: . og , (konverteres automatisk til .)
- **Backspace (⌫)**: Fjerner siste tegn fra fokusert felt
- **+/- knapp**: Bytter fortegn på tallet i fokusert felt

## Krav
- Python 3.7 eller nyere
- Tkinter (følger med standard Python-installasjon)

## Kjøring

### CLI-versjon
```bash
python main.py
# eller
py main.py
```

### GUI-versjon
```bash
python gui_calculator.py
# eller
py gui_calculator.py
```

## GUI-funksjoner

### Layout

GUI-kalkulatoren har følgende komponenter:
- **Inputfelt**: To felt for "Første tall" og "Andre tall"
- **Resultatfelt**: Viser resultat av beregninger (readonly)
- **Minnevisning**: Viser nåværende verdi i minnet
- **Tallpanel (venstre)**:
  - Tallknapper 0-9 arrangert som et standard nummerpanel
  - Desimalknapper: . og , (begge gir .)
  - ⌫ (Backspace): Sletter siste tegn
  - +/-: Bytter fortegn
  - C: Tømmer alle felt
- **Operasjonspanel (høyre)**:
  - Aritmetiske operasjoner: +, -, *, /, %, sqrt
  - Minneknapper: M+, M-, MR, MC
  - Avslutt-knapp

### Bruksanvisning

1. **Skriv inn tall**: Bruk enten tastatur eller tallknappene (0-9)
   - Tallknappene legger til siffer i feltet som har fokus
   - Klikk i et felt for å gi det fokus
2. **Desimal**: Klikk på . eller , for desimaltegn
3. **Endre fortegn**: Klikk +/- for å gjøre tall negativt/positivt
4. **Velg operasjon**: Klikk på ønsket operasjon (+, -, *, /, %, sqrt)
5. **Se resultat**: Resultatet vises i resultatfeltet
6. **Minneoperasjoner**:
   - Etter en beregning, klikk **M+** for å legge resultatet til minnet
   - Klikk **M-** for å trekke resultatet fra minnet
   - Klikk **MR** for å hente minnets verdi
   - Klikk **MC** for å tømme minnet
7. **Tøm felt**: Klikk **C** eller trykk **Esc**

### Tastatursnarveier
- **Enter**: Beregn med siste operasjon
- **Ctrl+R**: Beregn på nytt
- **Esc**: Tøm alle felt

### Eksempler

#### Grunnleggende addisjon med tallknapper
1. Klikk i "Første tall"-feltet
2. Klikk tallknappene: 1, 5
3. Klikk i "Andre tall"-feltet
4. Klikk tallknappene: 7
5. Klikk på **+**-knappen
6. Resultat: `22`

#### Prosentberegning
- Første tall: `200`
- Andre tall: `10`
- Operasjon: `%`
- Resultat: `20` (10% av 200)

#### Kvadratrot
- Første tall: `16`
- Operasjon: `sqrt`
- Resultat: `4`

#### Bruk av +/- knapp
1. Klikk i "Første tall"-feltet
2. Skriv inn eller klikk: 5, 0
3. Klikk **+/-** knappen
4. Tallet endres til `-50`

#### Bruk av desimal med komma
1. Klikk i "Første tall"-feltet
2. Klikk: 3, **,**, 1, 4
3. Internt konverteres dette til `3.14`

## Pakking til .exe med PyInstaller

### Installasjon av PyInstaller
```bash
pip install pyinstaller
```

### Bygg enkeltstående .exe (uten konsollvindu)
```bash
pyinstaller --onefile --noconsole --name "Kalkulator" gui_calculator.py
```

Dette vil generere en `Kalkulator.exe` i `dist`-mappen.

### Valgfritt: Legg til ikon
Hvis du har en `icon.ico`-fil:
```bash
pyinstaller --onefile --noconsole --icon=icon.ico --name "Kalkulator" gui_calculator.py
```

### Kjør .exe-filen
Etter bygging, finn `Kalkulator.exe` i `dist`-mappen og dobbeltklikk for å kjøre.

## Tekniske detaljer

- **Språk**: Python 3
- **GUI-bibliotek**: Tkinter (standard library)
- **Matematikk**: math-modulen (standard library)
- **Type hints**: Fullt annotert kode
- **Feilhåndtering**: Validering av input og brukervennlige feilmeldinger

## Validering og feilhåndtering

Applikasjonen håndterer:
- Ugyldig tallformat (viser feilmelding)
- Deling på 0 (viser feilmelding)
- Negativt tall for kvadratrot (viser feilmelding)
- Tom input (ber brukeren om å skrive inn tall)

## Filstruktur

```
Kalkulator/
├── main.py              # CLI-versjon
├── gui_calculator.py    # GUI-versjon (Tkinter)
└── README.md            # Denne filen
```

## Lisens

Dette prosjektet er laget som en læringsressurs
