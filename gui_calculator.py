"""
Windows GUI-kalkulator bygget med Tkinter.
Konvertert fra CLI-versjon, beholder all matematikklogikk.
Inkluderer tallknapper 0-9, desimalknapper, backspace og +/- funksjonalitet.
"""
import tkinter as tk
from tkinter import messagebox
import math
from typing import Optional


class CalculatorApp:
    """
    Hoved-GUI-klasse for kalkulatoren.
    Håndterer all brukerinteraksjon og beregninger.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialiserer GUI-komponenter og minnevariabel.

        Args:
            root: Tkinter root-vindu
        """
        self.root = root
        self.root.title("Kalkulator")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        # Minnevariabel (samme som i CLI-versjon)
        self.memory: float = 0.0

        # Holder styr på siste valgte operasjon for Enter-snarvei
        self.last_operation: str = "+"

        self._create_widgets()
        self._setup_keyboard_shortcuts()

        # Sett fokus på første tall ved oppstart
        self.entry_a.focus_set()

    def _create_widgets(self) -> None:
        """Oppretter alle GUI-komponenter."""
        # Hovedcontainer med padding
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Tittel
        title_label = tk.Label(
            main_frame,
            text="Kalkulator",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Input-felt for første tall
        input_frame_a = tk.Frame(main_frame)
        input_frame_a.pack(fill=tk.X, pady=5)

        tk.Label(
            input_frame_a,
            text="Første tall:",
            font=("Arial", 11),
            width=12,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.entry_a = tk.Entry(
            input_frame_a,
            font=("Arial", 14),
            width=30,
            justify="right"
        )
        self.entry_a.pack(side=tk.LEFT, padx=(5, 0))

        # Input-felt for andre tall
        input_frame_b = tk.Frame(main_frame)
        input_frame_b.pack(fill=tk.X, pady=5)

        tk.Label(
            input_frame_b,
            text="Andre tall:",
            font=("Arial", 11),
            width=12,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.entry_b = tk.Entry(
            input_frame_b,
            font=("Arial", 14),
            width=30,
            justify="right"
        )
        self.entry_b.pack(side=tk.LEFT, padx=(5, 0))

        # Resultatfelt (readonly)
        result_frame = tk.Frame(main_frame)
        result_frame.pack(fill=tk.X, pady=(10, 5))

        tk.Label(
            result_frame,
            text="Resultat:",
            font=("Arial", 11, "bold"),
            width=12,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.result_var = tk.StringVar(value="")
        result_entry = tk.Entry(
            result_frame,
            textvariable=self.result_var,
            font=("Arial", 14, "bold"),
            width=30,
            state="readonly",
            readonlybackground="white",
            fg="blue",
            justify="right"
        )
        result_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Minnevisning
        memory_frame = tk.Frame(main_frame)
        memory_frame.pack(fill=tk.X, pady=5)

        self.memory_label = tk.Label(
            memory_frame,
            text="Minne: 0.0",
            font=("Arial", 10, "italic"),
            fg="gray"
        )
        self.memory_label.pack(anchor="w")

        # Hovedknapp-container (side ved side layout)
        buttons_container = tk.Frame(main_frame)
        buttons_container.pack(pady=15, fill=tk.BOTH, expand=True)

        # Venstre side: Tallpanel
        numpad_frame = tk.Frame(buttons_container)
        numpad_frame.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            numpad_frame,
            text="Tallpanel",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=(0, 5))

        # Tallknapper 7-8-9 / 4-5-6 / 1-2-3 / 0
        numpad_buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2),
            ("0", 4, 0),
        ]

        for text, row, col in numpad_buttons:
            btn = tk.Button(
                numpad_frame,
                text=text,
                command=lambda t=text: self._append_digit(t),
                font=("Arial", 14, "bold"),
                width=5,
                height=2,
                bg="#e0e0e0"
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

        # Desimal og komma knapper
        decimal_btn = tk.Button(
            numpad_frame,
            text=".",
            command=lambda: self._append_digit("."),
            font=("Arial", 14, "bold"),
            width=5,
            height=2,
            bg="#d0d0d0"
        )
        decimal_btn.grid(row=4, column=1, padx=2, pady=2)

        comma_btn = tk.Button(
            numpad_frame,
            text=",",
            command=lambda: self._append_digit("."),  # Konverterer til .
            font=("Arial", 14, "bold"),
            width=5,
            height=2,
            bg="#d0d0d0"
        )
        comma_btn.grid(row=4, column=2, padx=2, pady=2)

        # Backspace knapp
        backspace_btn = tk.Button(
            numpad_frame,
            text="⌫",
            command=self._backspace,
            font=("Arial", 14, "bold"),
            width=5,
            height=2,
            bg="#ffcccc"
        )
        backspace_btn.grid(row=5, column=0, padx=2, pady=2)

        # +/- knapp
        plusminus_btn = tk.Button(
            numpad_frame,
            text="+/-",
            command=self._toggle_sign,
            font=("Arial", 12, "bold"),
            width=5,
            height=2,
            bg="#ccddff"
        )
        plusminus_btn.grid(row=5, column=1, padx=2, pady=2)

        # Clear knapp
        clear_btn = tk.Button(
            numpad_frame,
            text="C",
            command=self._clear,
            font=("Arial", 12, "bold"),
            width=5,
            height=2,
            bg="#ffcccc"
        )
        clear_btn.grid(row=5, column=2, padx=2, pady=2)

        # Høyre side: Operasjoner
        operations_frame = tk.Frame(buttons_container)
        operations_frame.pack(side=tk.LEFT)

        tk.Label(
            operations_frame,
            text="Operasjoner",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 5))

        # Aritmetiske operasjoner
        operation_buttons = [
            ("+", lambda: self._perform_operation("+"), 1, 0),
            ("-", lambda: self._perform_operation("-"), 1, 1),
            ("*", lambda: self._perform_operation("*"), 2, 0),
            ("/", lambda: self._perform_operation("/"), 2, 1),
            ("%", lambda: self._perform_operation("%"), 3, 0),
            ("sqrt", lambda: self._perform_operation("sqrt"), 3, 1),
        ]

        for text, command, row, col in operation_buttons:
            btn = tk.Button(
                operations_frame,
                text=text,
                command=command,
                font=("Arial", 12, "bold"),
                width=7,
                height=2,
                bg="#cceeff"
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

        # Minneknapper
        tk.Label(
            operations_frame,
            text="Minne",
            font=("Arial", 10, "bold")
        ).grid(row=4, column=0, columnspan=2, pady=(10, 5))

        memory_buttons = [
            ("M+", self._memory_add, 5, 0),
            ("M-", self._memory_subtract, 5, 1),
            ("MR", self._memory_recall, 6, 0),
            ("MC", self._memory_clear, 6, 1),
        ]

        for text, command, row, col in memory_buttons:
            btn = tk.Button(
                operations_frame,
                text=text,
                command=command,
                font=("Arial", 11, "bold"),
                width=7,
                height=2,
                bg="#ffffcc"
            )
            btn.grid(row=row, column=col, padx=2, pady=2)

        # Avslutt-knapp
        quit_btn = tk.Button(
            operations_frame,
            text="Avslutt",
            command=self._quit,
            font=("Arial", 11, "bold"),
            width=15,
            height=2,
            bg="#ffcccc"
        )
        quit_btn.grid(row=7, column=0, columnspan=2, padx=2, pady=(10, 2))

        # Hjelpetekst
        help_frame = tk.Frame(main_frame)
        help_frame.pack(pady=(10, 0))

        help_text = (
            "Tips: Bruk tallknapper eller tastatur • Både '.' og ',' som desimal\n"
            "⌫ = slett siste tegn • +/- = bytt fortegn • % = b prosent av a\n"
            "sqrt = kvadratrot (kun første tall) • M+ = legg til minne • M- = trekk fra minne\n"
            "MR = hent fra minne • MC = tøm minne\n"
            "\n"
            "Tastatursnarveier: Enter = beregn • Ctrl+R = beregn på nytt • Esc = tøm felter"
        )

        help_label = tk.Label(
            help_frame,
            text=help_text,
            font=("Arial", 8),
            justify=tk.LEFT,
            fg="gray"
        )
        help_label.pack(anchor="w")

    def _setup_keyboard_shortcuts(self) -> None:
        """Setter opp tastatursnarveier."""
        # Enter = utfør siste operasjon
        self.root.bind("<Return>", lambda e: self._perform_operation(self.last_operation))

        # Ctrl+R = beregn på nytt (samme som Enter)
        self.root.bind("<Control-r>", lambda e: self._perform_operation(self.last_operation))

        # Esc = clear
        self.root.bind("<Escape>", lambda e: self._clear())

    def _get_focused_entry(self) -> Optional[tk.Entry]:
        """
        Returnerer Entry-widgeten som har fokus.

        Returns:
            Entry-widget med fokus, eller None hvis ingen har fokus
        """
        focused = self.root.focus_get()
        if focused == self.entry_a:
            return self.entry_a
        elif focused == self.entry_b:
            return self.entry_b
        # Hvis ingen har fokus, returner entry_a som default
        return self.entry_a

    def _append_digit(self, digit: str) -> None:
        """
        Legger til et siffer eller desimaltegn til feltet med fokus.

        Args:
            digit: Sifferet eller tegnet som skal legges til
        """
        entry = self._get_focused_entry()
        if entry:
            current_pos = entry.index(tk.INSERT)
            entry.insert(current_pos, digit)
            entry.focus_set()

    def _backspace(self) -> None:
        """Fjerner siste tegn fra feltet med fokus (⌫)."""
        entry = self._get_focused_entry()
        if entry:
            current_value = entry.get()
            if current_value:
                entry.delete(len(current_value) - 1, tk.END)
            entry.focus_set()

    def _toggle_sign(self) -> None:
        """Bytter fortegn på tallet i feltet med fokus (+/-)."""
        entry = self._get_focused_entry()
        if entry:
            current_value = entry.get().strip()
            if not current_value:
                return

            # Prøv å parse som tall
            num = self._parse_number(current_value)
            if num is not None:
                # Bytt fortegn
                new_value = -num
                entry.delete(0, tk.END)
                entry.insert(0, str(new_value))
            elif current_value.startswith("-"):
                # Fjern minustegn hvis strengen starter med det
                entry.delete(0, tk.END)
                entry.insert(0, current_value[1:])
            else:
                # Legg til minustegn
                entry.delete(0, tk.END)
                entry.insert(0, "-" + current_value)

            entry.focus_set()

    def _parse_number(self, value: str) -> Optional[float]:
        """
        Parser et tall fra string, støtter både '.' og ','.

        Args:
            value: String-representasjon av tall

        Returns:
            Float-verdi hvis gyldig, None ellers
        """
        value = value.strip().replace(",", ".")  # Støtt norsk komma
        try:
            return float(value)
        except ValueError:
            return None

    def _calculate(self, a: float, b: float, op: str) -> float:
        """
        Utfører beregning (samme logikk som CLI-versjon).

        Args:
            a: Første tall
            b: Andre tall
            op: Operasjon (+, -, *, /, %)

        Returns:
            Resultat av beregningen

        Raises:
            ZeroDivisionError: Ved deling på 0
            ValueError: Ved ukjent operasjon
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

    def _perform_operation(self, op: str) -> None:
        """
        Utfører valgt operasjon og viser resultat.

        Args:
            op: Operasjon som skal utføres
        """
        try:
            # Lagre operasjon for Enter-snarvei
            if op in {"+", "-", "*", "/", "%"}:
                self.last_operation = op

            # sqrt krever kun første tall
            if op == "sqrt":
                value_a = self.entry_a.get()
                a = self._parse_number(value_a)

                if a is None:
                    messagebox.showerror(
                        "Ugyldig input",
                        "Første tall må være et gyldig tall."
                    )
                    self.entry_a.focus_set()
                    return

                if a < 0:
                    messagebox.showerror(
                        "Ugyldig operasjon",
                        "Kan ikke ta kvadratrot av negativt tall."
                    )
                    self.entry_a.focus_set()
                    return

                result = math.sqrt(a)
                self.result_var.set(str(result))
                self.last_operation = "sqrt"
                return

            # Binære operasjoner krever begge tall
            if op in {"+", "-", "*", "/", "%"}:
                value_a = self.entry_a.get()
                value_b = self.entry_b.get()

                a = self._parse_number(value_a)
                b = self._parse_number(value_b)

                if a is None:
                    messagebox.showerror(
                        "Ugyldig input",
                        "Første tall må være et gyldig tall."
                    )
                    self.entry_a.focus_set()
                    return

                if b is None:
                    messagebox.showerror(
                        "Ugyldig input",
                        "Andre tall må være et gyldig tall."
                    )
                    self.entry_b.focus_set()
                    return

                result = self._calculate(a, b, op)
                self.result_var.set(str(result))
                return

        except ZeroDivisionError as e:
            messagebox.showerror("Feil", str(e))
            self.entry_b.focus_set()

        except Exception as e:
            messagebox.showerror("Feil", f"En feil oppstod: {str(e)}")

    def _memory_add(self) -> None:
        """Legger resultatet til minnet (M+)."""
        result_str = self.result_var.get().strip()

        if not result_str:
            messagebox.showinfo(
                "Info",
                "Ingen resultat å legge til i minne. Utfør en beregning først."
            )
            return

        result = self._parse_number(result_str)
        if result is None:
            messagebox.showerror("Feil", "Ugyldig resultatverdi.")
            return

        self.memory += result
        self._update_memory_display()
        messagebox.showinfo("Minne", f"Lagt til i minne.\nNytt minne: {self.memory}")

    def _memory_subtract(self) -> None:
        """Trekker resultatet fra minnet (M-)."""
        result_str = self.result_var.get().strip()

        if not result_str:
            messagebox.showinfo(
                "Info",
                "Ingen resultat å trekke fra minne. Utfør en beregning først."
            )
            return

        result = self._parse_number(result_str)
        if result is None:
            messagebox.showerror("Feil", "Ugyldig resultatverdi.")
            return

        self.memory -= result
        self._update_memory_display()
        messagebox.showinfo("Minne", f"Trukket fra minne.\nNytt minne: {self.memory}")

    def _memory_recall(self) -> None:
        """Viser minnets verdi i resultatfeltet (MR)."""
        self.result_var.set(str(self.memory))
        messagebox.showinfo("Minne", f"Minne: {self.memory}")

    def _memory_clear(self) -> None:
        """Tømmer minnet (MC)."""
        self.memory = 0.0
        self._update_memory_display()
        messagebox.showinfo("Minne", "Minnet er tømt.")

    def _update_memory_display(self) -> None:
        """Oppdaterer minnevisningen."""
        self.memory_label.config(text=f"Minne: {self.memory}")

    def _clear(self) -> None:
        """Tømmer alle inputfelt og resultat (C / Esc)."""
        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.result_var.set("")
        self.entry_a.focus_set()

    def _quit(self) -> None:
        """Avslutter applikasjonen."""
        if messagebox.askokcancel("Avslutt", "Er du sikker på at du vil avslutte?"):
            self.root.quit()


def main() -> None:
    """Hovedfunksjon som starter GUI-applikasjonen."""
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
