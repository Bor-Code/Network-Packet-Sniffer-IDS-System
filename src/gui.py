import customtkinter as ctk
from tkinter import ttk

class IDSGui(ctk.CTk):
    def __init__(self, start_callback):
        super().__init__()

        self.title("NeuralLock IDS - Network Monitor")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")

        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=10, padx=10, fill="x")

        self.title_label = ctk.CTkLabel(self.top_frame, text="Network IDS Monitor", font=("Helvetica", 20, "bold"))
        self.title_label.pack(side="left", padx=20)

        self.start_btn = ctk.CTkButton(self.top_frame, text="Sniffing Başlat", command=start_callback)
        self.start_btn.pack(side="right", padx=20)

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(self.table_frame, columns=("src", "dst", "proto", "len"), show="headings")
        self.tree.heading("src", text="Kaynak IP")
        self.tree.heading("dst", text="Hedef IP")
        self.tree.heading("proto", text="Protokol")
        self.tree.heading("len", text="Boyut")
        self.tree.pack(fill="both", expand=True)

        self.alert_text = ctk.CTkTextbox(self, height=150, fg_color="black", text_color="red")
        self.alert_text.pack(pady=10, padx=10, fill="x")
        self.alert_text.insert("0.0", "--- Sistem Hazır. Uyarılar burada görünecek ---\n")

    def update_table(self, data):
        self.tree.insert("", "end", values=(data['src_ip'], data['dst_ip'], data['protocol'], "64"))
        if len(self.tree.get_children()) > 20:
            self.tree.delete(self.tree.get_children()[0])

    def log_alert(self, message):
        self.alert_text.insert("end", f"[!] {message}\n")
        self.alert_text.see("end")