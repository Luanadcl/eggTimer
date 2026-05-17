import tkinter as tk
import time

MODOS = {
    "Mole":   {"tempo": 4 * 6, "cor": "#FAC775"},
    "Médio":  {"tempo": 6 * 6, "cor": "#EF9F27"},
    "Duro":   {"tempo": 10 * 6, "cor": "#BA7517"},
    "Salada": {"tempo": 12 * 6, "cor": "#1D9E75"},
}

class EggTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Temporizador de Ovo")
        self.root.geometry("320x420")
        self.root.resizable(False, False)

        self.modo_atual = "Mole"
        self.total = MODOS["Mole"]["tempo"]
        self.restante = self.total
        self.rodando = False
        self.job = None

        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="🥚 temporizador de ovos",
                 font=("Helvetica", 16, "bold")).pack(pady=16)

        frame_modos = tk.Frame(self.root)
        frame_modos.pack()
        for nome in MODOS:
            tk.Button(frame_modos, text=nome, width=7,
                      command=lambda n=nome: self.selecionar(n)
                      ).pack(side="left", padx=4)

        self.lbl_modo = tk.Label(self.root, text="mole",
                                  font=("Helvetica", 12), fg="gray")
        self.lbl_modo.pack(pady=8)

        self.lbl_tempo = tk.Label(self.root, text="4:00",
                                   font=("Helvetica", 56, "bold"))
        self.lbl_tempo.pack(pady=8)

        self.lbl_status = tk.Label(self.root, text="pronto para começar",
                                    font=("Helvetica", 11), fg="gray",
                                    wraplength=280)
        self.lbl_status.pack(pady=4)

        frame_ctrl = tk.Frame(self.root)
        frame_ctrl.pack(pady=16)
        self.btn_start = tk.Button(frame_ctrl, text="Iniciar", width=10,
                                    command=self.toggle)
        self.btn_start.pack(side="left", padx=6)
        tk.Button(frame_ctrl, text="Reset", width=8,
                  command=self.reset).pack(side="left", padx=6)

    def selecionar(self, nome):
        if self.rodando:
            return
        self.modo_atual = nome
        self.total = MODOS[nome]["tempo"]
        self.restante = self.total
        self.lbl_modo.config(text=nome.lower())
        self.lbl_tempo.config(text=self._fmt(self.restante))
        self.lbl_status.config(text="pronto para começar")
        self.btn_start.config(text="Iniciar")

    def toggle(self):
        if self.restante == 0:
            self.reset()
            return
        self.rodando = not self.rodando
        self.btn_start.config(text="Pausar" if self.rodando else "Continuar")
        if self.rodando:
            self._tick()

    def _tick(self):
        if not self.rodando:
            return
        if self.restante > 0:
            self.restante -= 1
            self.lbl_tempo.config(text=self._fmt(self.restante))
            self.lbl_status.config(text=f"cozinhando... {self._fmt(self.restante)} restantes")
            self.job = self.root.after(1000, self._tick)
        else:
            self.rodando = False
            self.btn_start.config(text="Iniciar")
            self.lbl_status.config(text="✅ pronto! retire o ovo agora")
            self.root.bell()

    def reset(self):
        if self.job:
            self.root.after_cancel(self.job)
        self.rodando = False
        self.restante = self.total
        self.lbl_tempo.config(text=self._fmt(self.restante))
        self.lbl_status.config(text="pronto para começar")
        self.btn_start.config(text="Iniciar")

    def _fmt(self, s):
        return f"{s // 60}:{s % 60:02d}"

root = tk.Tk()
EggTimer(root)
root.mainloop()