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
- **Støtte for norsk komma**: Både '.' og ',' fungerer som desimalskille

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

### Tastatursnarveier
- **Enter**: Beregn med siste operasjon
- **Ctrl+R**: Beregn på nytt
- **Esc**: Tøm alle felt

### Bruksanvisning

1. **Skriv inn tall**: Skriv inn verdier i "Første tall" og "Andre tall"
2. **Velg operasjon**: Klikk på ønsket operasjon (+, -, *, /, %, sqrt)
3. **Se resultat**: Resultatet vises i resultatfeltet
4. **Minneoperasjoner**:
   - Etter en beregning, klikk **M+** for å legge resultatet til minnet
   - Klikk **M-** for å trekke resultatet fra minnet
   - Klikk **MR** for å se minnets verdi
5. **Tøm felt**: Klikk **C** eller trykk **Esc**

### Eksempler

#### Grunnleggende addisjon
- Første tall: `15`
- Andre tall: `7`
- Operasjon: `+`
- Resultat: `22`

#### Prosentberegning
- Første tall: `200`
- Andre tall: `10`
- Operasjon: `%`
- Resultat: `20` (10% av 200)

#### Kvadratrot
- Første tall: `16`
- Operasjon: `sqrt`
- Resultat: `4`

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
