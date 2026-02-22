import customtkinter as ctk
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Arayüz Ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DTMFApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DTMF Signal Studio Pro - Sound Enabled")
        # MacBook M2 için optimize edilmiş boyutlar
        self.geometry("680x760") 
        self.configure(fg_color="#1a1a1a")

        # DTMF Frekans Verileri
        self.row_freqs = [697, 770, 852, 941]
        self.col_freqs = [1209, 1336, 1477, 1633]
        self.keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], 
                     ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

        # --- DETAYLI VE KOMPAKT GRAFİK ---
        self.fig, self.ax = plt.subplots(figsize=(6, 1.5), facecolor='white', dpi=110)
        self.ax.set_facecolor('white')
        self.fig.subplots_adjust(bottom=0.35, left=0.15, top=0.85, right=0.95)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(pady=(10, 2), padx=30, fill="x")

        self.setup_detailed_axes()

        # Klavye Alanı
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(pady=2, expand=True)
        self.create_keypad_matrix()

    def setup_detailed_axes(self, key="None"):
        self.ax.clear()
        # Kareli Izgara Ayarları
        self.ax.xaxis.set_major_locator(ticker.MultipleLocator(0.002)) 
        self.ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.0005))
        self.ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
        self.ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
        
        self.ax.grid(which='major', linestyle='-', linewidth=0.7, color='#d0d0d0')
        self.ax.grid(which='minor', linestyle=':', linewidth=0.3, color='#e0e0e0')
        self.ax.minorticks_on()

        # Eksen İsimleri
        self.ax.set_title(f"Waveform: Key '{key}'", fontsize=9, fontweight='bold', pad=5)
        self.ax.set_xlabel("Time (s)", fontsize=8, fontweight='bold', labelpad=2, color='black')
        self.ax.set_ylabel("Amp (V)", fontsize=8, fontweight='bold', labelpad=2, color='black')
        self.ax.set_ylim([-1.1, 1.1])
        self.ax.tick_params(axis='both', which='major', labelsize=7, colors='black')

    def create_keypad_matrix(self):
        for c, f_high in enumerate(self.col_freqs):
            lbl = ctk.CTkLabel(self.main_container, text=f"{f_high} Hz", font=("Inter", 11, "bold"), text_color="#5dade2")
            lbl.grid(row=0, column=c+1, pady=(0, 2))

        for r, f_low in enumerate(self.row_freqs):
            lbl = ctk.CTkLabel(self.main_container, text=f"{f_low} Hz", font=("Inter", 11, "bold"), text_color="#5dade2")
            lbl.grid(row=r+1, column=0, padx=12)

            for c, key in enumerate(self.keys[r]):
                f_high = self.col_freqs[c]
                btn = ctk.CTkButton(self.main_container, text=key, width=85, height=85, corner_radius=12, 
                                    font=("Inter", 24, "bold"), fg_color="#262626", hover_color="#2e86c1",
                                    command=lambda k=key, fl=f_low, fh=f_high: self.process_signal(k, fl, fh))
                btn.grid(row=r+1, column=c+1, padx=4, pady=4)

    def process_signal(self, key, f_low, f_high):
        fs = 44100
        duration = 0.3 # Sesi biraz daha uzun yaptık (0.3 sn)
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        
        # Sentez: Genliği 0.8 yaparak sesi güçlendirdik
        signal = (np.sin(2 * np.pi * f_low * t) + np.sin(2 * np.pi * f_high * t)) * 0.4
        
        try:
            # Sesi çalma komutu
            sd.play(signal, fs)
            # sd.wait() komutunu eklemiyoruz çünkü arayüzün donmasını istemeyiz
        except Exception as e:
            print(f"Ses çalınamadı: {e}")

        self.setup_detailed_axes(key)
        self.ax.plot(t[:550], signal[:550] / 0.4 * 0.5, color='#1a5276', linewidth=1.8, antialiased=True)
        self.canvas.draw()

if __name__ == "__main__":
    app = DTMFApp()
    app.mainloop()