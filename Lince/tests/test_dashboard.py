import customtkinter as ctk

from ui.components.ioc_dashboard import IOCDashboard
from services.ioc_engine import IOCEngine

texto = """

8.8.8.8
8.8.8.8
8.8.8.8

1.1.1.1

admin@test.com

admin@test.com

github.com

github.com

github.com

github.com

github.com

CVE-2025-1234

"""

ioc = IOCEngine.extract_all(texto)

app = ctk.CTk()

app.geometry("1150x700")

dashboard = IOCDashboard(app)

dashboard.pack(fill="both", expand=True, padx=20, pady=20)

dashboard.update_dashboard(ioc)

app.mainloop()