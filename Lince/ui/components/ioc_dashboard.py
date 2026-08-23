from datetime import datetime
import customtkinter as ctk


from ui.components.metric_card import MetricCard
from collections import Counter


class IOCDashboard(ctk.CTkFrame):

    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1), weight=1)

        #
        # CABECERA
        #

        from datetime import datetime

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=(15,20)
        )

        header.grid_columnconfigure(0, weight=1)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.grid(row=0,column=0,sticky="w")

        title = ctk.CTkLabel(
            left,
            text="Resumen del análisis",
            font=("Arial",28,"bold")
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            left,
            text="Indicadores de compromiso (IOC)",
            font=("Arial",15)
        )
        subtitle.pack(anchor="w")


        #
        # Último análisis
        #

        right = ctk.CTkFrame(
            header,
            corner_radius=12
        )

        right.grid(
            row=0,
            column=1,
            sticky="e"
        )

        ctk.CTkLabel(
            right,
            text="Último análisis",
            font=("Arial",14,"bold")
        ).pack(padx=18,pady=(12,0))

        self.last_analysis_date = ctk.CTkLabel(
            right,
            text="-"
        )

        self.last_analysis_date.pack()

        self.last_analysis_time = ctk.CTkLabel(
            right,
            text="-"
        )

        self.last_analysis_time.pack(pady=(0,12))

        #
        # TARJETAS
        #

        cards = ctk.CTkFrame(self, fg_color="transparent")
        cards.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15)

        cards.grid_columnconfigure((0,1,2,3), weight=1)

        self.card_ipv4 = MetricCard(cards,"IPv4",18,"🌐")
        self.card_email = MetricCard(cards,"Email",6,"✉️")
        self.card_domain = MetricCard(cards,"Dominios",11,"🌍")
        self.card_hash = MetricCard(cards,"Hashes",25,"🔒")

        self.card_ipv4.grid(row=0,column=0,padx=10,pady=10,sticky="ew")
        self.card_email.grid(row=0,column=1,padx=10,pady=10,sticky="ew")
        self.card_domain.grid(row=0,column=2,padx=10,pady=10,sticky="ew")
        self.card_hash.grid(row=0,column=3,padx=10,pady=10,sticky="ew")

        #
        # PANEL IZQUIERDO
        #

        self.left = ctk.CTkFrame(self, corner_radius=12)
        self.left.grid(row=2,column=0,sticky="nsew",padx=(20,10),pady=20)

        ctk.CTkLabel(
            self.left,
            text="IOC más frecuentes",
            font=("Arial",20,"bold")
        ).pack(anchor="w",padx=20,pady=(15,10))

        datos = [
            ("8.8.8.8",15),
            ("admin@test.com",8),
            ("github.com",6),
            ("CVE-2025-1234",3),
            ("SHA256...",2)
        ]

        for nombre,valor in datos:

            fila=ctk.CTkFrame(self.left,fg_color="transparent")
            fila.pack(fill="x",padx=20,pady=6)

            ctk.CTkLabel(
                fila,
                text=nombre
            ).pack(side="left")

            ctk.CTkLabel(
                fila,
                text=str(valor),
                font=("Arial",15,"bold")
            ).pack(side="right")

        #
        # PANEL DERECHO
        #

        self.right=ctk.CTkFrame(self,corner_radius=12)
        self.right.grid(row=2,column=1,sticky="nsew",padx=(10,20),pady=20)

        ctk.CTkLabel(
            self.right,
            text="Distribución IOC",
            font=("Arial",20,"bold")
        ).pack(anchor="w",padx=20,pady=(15,10))

        barras=[
            ("IPv4",0.90),
            ("Email",0.55),
            ("Dominios",0.42),
            ("Hashes",0.25)
        ]

        for texto,valor in barras:

            ctk.CTkLabel(
                self.right,
                text=texto
            ).pack(anchor="w",padx=20)

            barra=ctk.CTkProgressBar(self.right,width=320)

            barra.pack(padx=20,pady=(0,12))

            barra.set(valor)

    def update_dashboard(self, ioc):

        #
        # Tarjetas
        #

        self.card_ipv4.set_value(len(ioc.ipv4))

        self.card_email.set_value(len(ioc.emails))

        self.card_domain.set_value(len(ioc.domains))

        hashes = (
            len(ioc.md5)
            + len(ioc.sha1)
            + len(ioc.sha256)
        )

        self.card_hash.set_value(hashes)

        #
        # IOC más frecuentes
        #

        total_counter = Counter()

        total_counter.update(ioc.ipv4_counter)

        total_counter.update(ioc.email_counter)

        total_counter.update(ioc.domain_counter)

        total_counter.update(ioc.md5_counter)

        total_counter.update(ioc.sha1_counter)

        total_counter.update(ioc.sha256_counter)

        total_counter.update(ioc.cve_counter)

        top = total_counter.most_common(5)

        for widget in self.left.winfo_children():

            widget.destroy()

        ctk.CTkLabel(
            self.left,
            text="IOC más frecuentes",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))

        if not top:

            ctk.CTkLabel(
                self.left,
                text="No se han encontrado IOC."
            ).pack(pady=40)

        else:

            for nombre, valor in top:

                fila = ctk.CTkFrame(
                    self.left,
                    fg_color="transparent"
                )

                fila.pack(fill="x", padx=20, pady=5)

                ctk.CTkLabel(
                    fila,
                    text=nombre
                ).pack(side="left")

                ctk.CTkLabel(
                    fila,
                    text=str(valor),
                    font=("Arial", 15, "bold")
                ).pack(side="right")

        #
        # Distribución
        #

        total = max(ioc.total(), 1)

        barras = [

            ("IPv4", len(ioc.ipv4)),

            ("Email", len(ioc.emails)),

            ("Dominios", len(ioc.domains)),

            ("Hashes", hashes)

        ]

        for widget in self.right.winfo_children():

            widget.destroy()

        ctk.CTkLabel(
            self.right,
            text="Distribución IOC",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))

        for titulo, cantidad in barras:

            fila = ctk.CTkFrame(
                self.right,
                fg_color="transparent"
            )

            fila.pack(fill="x", padx=20, pady=(5, 0))

            ctk.CTkLabel(
                fila,
                text=titulo
            ).pack(side="left")

            ctk.CTkLabel(
                fila,
                text=str(cantidad),
                font=("Arial", 14, "bold")
            ).pack(side="right")

            barra = ctk.CTkProgressBar(
                self.right,
                width=330
            )

            barra.pack(
                padx=20,
                pady=(2, 12)
            )

            barra.set(cantidad / total)

            now = datetime.now()

            self.last_analysis_date.configure(
                text=now.strftime("%d/%m/%Y")
            )

            self.last_analysis_time.configure(
                text=now.strftime("%H:%M:%S")
            )