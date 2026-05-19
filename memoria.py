import tkinter as tk
from tkinter import ttk, messagebox
import random

MEMORIA_TOTAL = 100


class SimuladorMemoria:

    def __init__(self, root):

        self.root = root
        self.root.title("Gestión de Memoria PRO MAX")
        self.root.geometry("1100x700")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        self.algoritmo = tk.StringVar(value="First Fit")
        self.anim_offset = 0

        self.colores = [
            "#FF6B6B",
            "#4ECDC4",
            "#FFD93D",
            "#6C5CE7",
            "#00CEC9",
            "#E17055",
            "#0984E3",
            "#FD79A8"
        ]

        self.bloques = []

        self.reiniciar_memoria()

        self.crear_interfaz()

        self.animar_fondo()

        # CORREGIDO
        self.animacion_redibujar()



    def crear_interfaz(self):

        titulo = tk.Label(
            self.root,
            text="🧠 SIMULADOR DE GESTIÓN DE MEMORIA",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#0f172a"
        )

        titulo.pack(pady=20)

        subtitulo = tk.Label(
            self.root,
            text="First Fit • Best Fit • Worst Fit",
            font=("Segoe UI", 11),
            fg="#94a3b8",
            bg="#0f172a"
        )

        subtitulo.pack()

        panel = tk.Frame(
            self.root,
            bg="#111827"
        )

        panel.pack(
            pady=25,
            padx=20,
            fill="x"
        )

        frame_inputs = tk.Frame(
            panel,
            bg="#111827"
        )

        frame_inputs.pack(pady=20)

        self.crear_input(
            frame_inputs,
            "ID Proceso",
            0
        )

        self.crear_input(
            frame_inputs,
            "Tamaño",
            1
        )

        tk.Label(
            frame_inputs,
            text="Algoritmo",
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg="#111827"
        ).grid(
            row=0,
            column=2,
            padx=20
        )

        estilo = ttk.Style()

        estilo.theme_use("clam")

        estilo.configure(
            "TCombobox",
            fieldbackground="#1e293b",
            background="#1e293b",
            foreground="white",
            padding=8
        )

        self.combo = ttk.Combobox(
            frame_inputs,
            textvariable=self.algoritmo,
            values=[
                "First Fit",
                "Best Fit",
                "Worst Fit"
            ],
            state="readonly",
            width=15,
            font=("Segoe UI", 10)
        )

        self.combo.grid(
            row=1,
            column=2,
            padx=20
        )

        # BOTONES

        botones = tk.Frame(
            panel,
            bg="#111827"
        )

        botones.pack(pady=20)

        self.crear_boton(
            botones,
            "➕ Asignar",
            "#10b981",
            self.asignar
        ).grid(
            row=0,
            column=0,
            padx=15
        )

        self.crear_boton(
            botones,
            "🗑 Liberar",
            "#ef4444",
            self.liberar
        ).grid(
            row=0,
            column=1,
            padx=15
        )

        self.crear_boton(
            botones,
            "🔄 Reiniciar",
            "#3b82f6",
            self.reiniciar_memoria
        ).grid(
            row=0,
            column=2,
            padx=15
        )

        # CANVAS

        self.canvas = tk.Canvas(
            self.root,
            width=1000,
            height=260,
            bg="#0b1120",
            highlightthickness=0
        )

        self.canvas.pack(pady=25)

        # INFO

        self.info = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#0f172a"
        )

        self.info.pack(pady=10)

        # BARRA PROGRESO

        self.barra_frame = tk.Frame(
            self.root,
            bg="#1e293b",
            width=500,
            height=28
        )

        self.barra_frame.pack(pady=10)

        self.barra_frame.pack_propagate(False)

        self.barra_uso = tk.Frame(
            self.barra_frame,
            bg="#22c55e",
            width=0
        )

        self.barra_uso.pack(
            side="left",
            fill="y"
        )

    def crear_input(self, parent, texto, col):

        tk.Label(
            parent,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg="#111827"
        ).grid(
            row=0,
            column=col,
            padx=20
        )

        entry = tk.Entry(
            parent,
            font=("Segoe UI", 12),
            bg="#1e293b",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=18
        )

        entry.grid(
            row=1,
            column=col,
            padx=20,
            ipady=8
        )

        if texto == "ID Proceso":
            self.id_entry = entry
        else:
            self.size_entry = entry

    def crear_boton(self, parent, texto, color, comando):

        btn = tk.Button(
            parent,
            text=texto,
            command=comando,
            font=("Segoe UI", 11, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2"
        )

        # HOVER

        btn.bind(
            "<Enter>",
            lambda e: btn.config(
                font=("Segoe UI", 12, "bold")
            )
        )

        btn.bind(
            "<Leave>",
            lambda e: btn.config(
                font=("Segoe UI", 11, "bold")
            )
        )

        return btn



    def first_fit(self, size):

        for i, b in enumerate(self.bloques):

            if b["libre"] and b["tam"] >= size:
                return i

        return -1

    def best_fit(self, size):

        mejor = -1
        min_tam = float("inf")

        for i, b in enumerate(self.bloques):

            if (
                b["libre"]
                and b["tam"] >= size
                and b["tam"] < min_tam
            ):

                min_tam = b["tam"]
                mejor = i

        return mejor

    def worst_fit(self, size):

        peor = -1
        max_tam = -1

        for i, b in enumerate(self.bloques):

            if (
                b["libre"]
                and b["tam"] >= size
                and b["tam"] > max_tam
            ):

                max_tam = b["tam"]
                peor = i

        return peor


    def asignar(self):

        pid = self.id_entry.get()

        try:
            size = int(self.size_entry.get())

        except:
            messagebox.showerror(
                "Error",
                "Tamaño inválido"
            )
            return

        if size <= 0:
            return

        if self.algoritmo.get() == "First Fit":

            idx = self.first_fit(size)

        elif self.algoritmo.get() == "Best Fit":

            idx = self.best_fit(size)

        else:

            idx = self.worst_fit(size)

        if idx == -1:

            messagebox.showwarning(
                "Sin espacio",
                "No hay bloque disponible"
            )

            return

        b = self.bloques[idx]

        color = random.choice(self.colores)

        nuevo = {
            "inicio": b["inicio"],
            "tam": size,
            "libre": False,
            "proceso": pid,
            "color": color
        }

        restante = b["tam"] - size

        self.bloques[idx] = nuevo

        if restante > 0:

            self.bloques.insert(
                idx + 1,
                {
                    "inicio": b["inicio"] + size,
                    "tam": restante,
                    "libre": True,
                    "proceso": None,
                    "color": "#334155"
                }
            )

        self.animacion_redibujar()

    def liberar(self):

        pid = self.id_entry.get()

        for b in self.bloques:

            if (
                not b["libre"]
                and b["proceso"] == pid
            ):

                b["libre"] = True
                b["proceso"] = None
                b["color"] = "#334155"

                self.unir()

                self.animacion_redibujar()

                return

        messagebox.showerror(
            "Error",
            "Proceso no encontrado"
        )

    def unir(self):

        i = 0

        while i < len(self.bloques) - 1:

            if (
                self.bloques[i]["libre"]
                and self.bloques[i + 1]["libre"]
            ):

                self.bloques[i]["tam"] += self.bloques[i + 1]["tam"]

                del self.bloques[i + 1]

            else:
                i += 1

    def reiniciar_memoria(self):

        self.bloques = [
            {
                "inicio": 0,
                "tam": MEMORIA_TOTAL,
                "libre": True,
                "proceso": None,
                "color": "#334155"
            }
        ]

        if hasattr(self, "canvas"):
            self.animacion_redibujar()



    def animar_fondo(self):

        self.anim_offset += 1

        self.canvas.delete("particles")

        for i in range(20):

            x = (
                i * 50
                + self.anim_offset * 2
            ) % 1000

            y = 20 + (i * 11 % 180)

            self.canvas.create_oval(
                x,
                y,
                x + 4,
                y + 4,
                fill="#1e40af",
                outline="",
                tags="particles"
            )

        self.root.after(
            50,
            self.animar_fondo
        )

    def animacion_redibujar(self):

        self.canvas.delete("all")

        pasos = 15

        def animar(step=0):

            self.canvas.delete("bloques")

            x = 40

            for b in self.bloques:

                ancho_final = (
                    b["tam"] / MEMORIA_TOTAL
                ) * 900

                ancho = (
                    ancho_final * (step / pasos)
                )

                # SOMBRA

                self.canvas.create_rectangle(
                    x + 5,
                    55,
                    x + ancho + 5,
                    165,
                    fill="#000000",
                    outline="",
                    tags="bloques"
                )

                # BLOQUE

                self.canvas.create_rectangle(
                    x,
                    50,
                    x + ancho,
                    160,
                    fill=b["color"],
                    outline="white",
                    width=2,
                    tags="bloques"
                )

                texto = (
                    f"{b['proceso'] if b['proceso'] else 'LIBRE'}"
                    f"\n{b['tam']} MB"
                )

                self.canvas.create_text(
                    x + ancho / 2,
                    105,
                    text=texto,
                    fill="white",
                    font=("Segoe UI", 11, "bold"),
                    tags="bloques"
                )

                x += ancho_final

            if step < pasos:

                self.root.after(
                    20,
                    lambda: animar(step + 1)
                )

            else:
                self.calcular_metricas()

        animar()


    def calcular_metricas(self):

        usados = sum(
            b["tam"]
            for b in self.bloques
            if not b["libre"]
        )

        libres = [
            b["tam"]
            for b in self.bloques
            if b["libre"]
        ]

        uso = (
            usados / MEMORIA_TOTAL
        ) * 100

        if len(libres) > 1:

            frag_externa = (
                sum(libres) - max(libres)
            )

        else:

            frag_externa = 0

        self.info.config(
            text=(
                f"💾 Uso de Memoria: {uso:.2f}%"
                f"   |   "
                f"🧩 Fragmentación Externa: {frag_externa}"
            )
        )

        ancho = int(
            (uso / 100) * 500
        )

        self.barra_uso.config(
            width=ancho
        )




root = tk.Tk()

app = SimuladorMemoria(root)

root.mainloop()