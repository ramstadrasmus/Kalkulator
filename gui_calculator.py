"""
Windows GUI-kalkulator bygget med Tkinter.
Konvertert fra CLI-versjon, beholder all matematikklogikk.
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
        self.root.geometry("450x550")
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
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Tittel
        title_label = tk.Label(
            main_frame,
            text="Kalkulator",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 15))

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
            font=("Arial", 12),
            width=25
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
            font=("Arial", 12),
            width=25
        )
        self.entry_b.pack(side=tk.LEFT, padx=(5, 0))

        # Resultatfelt (readonly)
        result_frame = tk.Frame(main_frame)
        result_frame.pack(fill=tk.X, pady=(15, 5))

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
            font=("Arial", 12, "bold"),
            width=25,
            state="readonly",
            readonlybackground="white",
            fg="blue"
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

        # Operasjonsknapper
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)

        # Definerer knapper: (tekst, kommando, rad, kolonne, colspan)
        buttons = [
            ("+", lambda: self._perform_operation("+"), 0, 0, 1),
            ("-", lambda: self._perform_operation("-"), 0, 1, 1),
            ("*", lambda: self._perform_operation("*"), 0, 2, 1),
            ("/", lambda: self._perform_operation("/"), 0, 3, 1),

            ("%", lambda: self._perform_operation("%"), 1, 0, 1),
            ("sqrt", lambda: self._perform_operation("sqrt"), 1, 1, 1),
            ("M+", self._memory_add, 1, 2, 1),
            ("M-", self._memory_subtract, 1, 3, 1),

            ("MR", self._memory_recall, 2, 0, 1),
            ("C", self._clear, 2, 1, 1),
            ("Avslutt", self._quit, 2, 2, 2),
        ]

        # Oppretter knapper i grid
        for text, command, row, col, colspan in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 11, "bold"),
                width=8 if colspan == 1 else 17,
                height=2,
                bg="#f0f0f0"
            )
            btn.grid(row=row, column=col, columnspan=colspan, padx=3, pady=3)

        # Hjelpetekst
        help_frame = tk.Frame(main_frame)
        help_frame.pack(pady=(10, 0))

        help_text = (
            "Tips:\n"
            "• Bruk både '.' og ',' som desimalskille\n"
            "• % beregner b prosent av a (200 % 10 = 20)\n"
            "• sqrt bruker kun første tall\n"
            "• M+/M- legger til/trekker fra resultat i minne\n"
            "• MR viser minnets verdi\n"
            "\n"
            "Tastatursnarveier:\n"
            "• Enter = beregn med siste operasjon\n"
            "• Ctrl+R = beregn på nytt\n"
            "• Esc = tøm felter"
        )

        help_label = tk.Label(
            help_frame,
            text=help_text,
            font=("Arial", 9),
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
