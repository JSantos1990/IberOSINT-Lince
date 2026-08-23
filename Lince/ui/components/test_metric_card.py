import customtkinter as ctk

from ui.components.metric_card import MetricCard

app = ctk.CTk()

app.geometry("900x250")

cards = [
    MetricCard(app, "IPv4", 18, "🌐"),
    MetricCard(app, "Emails", 6, "✉️"),
    MetricCard(app, "Dominios", 11, "🌍"),
    MetricCard(app, "Hashes", 25, "🔒"),
]

for i, card in enumerate(cards):
    card.grid(row=0, column=i, padx=15, pady=20)

app.mainloop()