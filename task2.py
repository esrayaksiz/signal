import customtkinter as ctk
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import sys

# ==========================================================
# PROJECT: DTMF SIGNAL GENERATION AND ANALYSIS
# GROUP MEMBERS:
# 1. Esra [Soyadın]
# 2. [Arkadaşının Adı]
# 3. [Arkadaşının Adı]
# ==========================================================

try:
    if sys.platform.startswith('win'):
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DTMFAnalyzer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DTMF Signal Studio - Final Report Version")
        self.geometry("680x740") 
        self.configure(fg_color="#ffffff")

        self.row_freqs = [697, 770, 852, 941]
        self.col_freqs = [1209, 1336, 1477, 1633]
        self.keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], 
                     ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

        self.fig, (self.ax_time, self.ax_freq) = plt.subplots(2, 1, figsize=(5.8, 3.0), facecolor='#ffffff', dpi=100)
        self.fig.subplots_adjust(hspace=1.0, bottom=0.20, top=0.90, left=0.12, right=0.95)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.config(bg='white')
        self.canvas_widget.pack(pady=(5, 0), padx=20, fill="x")

        self.setup_plots()

        self.keypad_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        self.keypad_frame.pack(pady=(5, 10), expand=True)
        self.create_keypad()

    def setup_grid(self, ax, is_freq=False):
        ax.set_facecolor('#ffffff')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        if is_freq:
            ax.set_xlim([0, 4000])
            ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(100))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
            ax.yaxis.set_minor_locator(ticker.MultipleLocator(20))
        else:
            ax.set_xlim([0, 0.05])
            ax.xaxis.set_major_locator(ticker.MultipleLocator(0.01))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.002))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
            ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
            
        ax.grid(which='major', linestyle='-', linewidth=0.6, color='#dcdcdc')
        ax.grid(which='minor', linestyle=':', linewidth=0.4, color='#eeeeee')
        ax.minorticks_on()
        ax.tick_params(labelsize=7, colors='#444444')

    def setup_plots(self, key="None"):
        # Başlıklar artık SİYAH (color='black')
        self.ax_time.clear()
        self.ax_time.set_title(f"Time Domain Signal (Key: {key})", fontsize=9, fontweight='bold', pad=8, color='black')
        self.ax_time.set_ylabel("Amplitude", fontsize=8)
        self.ax_time.set_xlabel("Time (s)", fontsize=8, labelpad=2)
        self.setup_grid(self.ax_time)
        self.ax_time.set_ylim([-1.1, 1.1])

        self.ax_freq.clear()
        self.ax_freq.set_title("Frequency Domain (FFT Analysis)", fontsize=9, fontweight='bold', pad=8, color='black')
        self.ax_freq.set_ylabel("Magnitude", fontsize=8)
        self.ax_freq.set_xlabel("Frequency (Hz)", fontsize=8, labelpad=2)
        self.setup_grid(self.ax_freq, is_freq=True)
        self.ax_freq.set_ylim([0, 600])

    def create_keypad(self):
        for c, f in enumerate(self.col_freqs):
            lbl = ctk.CTkLabel(self.keypad_frame, text=f"{f}Hz", font=("Inter", 9, "bold"), text_color="#1f77b4")
            lbl.grid(row=0, column=c+1, pady=(0, 1))

        for r, f_low in enumerate(self.row_freqs):
            lbl = ctk.CTkLabel(self.keypad_frame, text=f"{f_low}Hz", font=("Inter", 9, "bold"), text_color="#1f77b4")
            lbl.grid(row=r+1, column=0, padx=8)

            for c, key in enumerate(self.keys[r]):
                f_high = self.col_freqs[c]
                btn = ctk.CTkButton(self.keypad_frame, text=key, width=58, height=58, corner_radius=10,
                                    font=("Inter", 15, "bold"), fg_color="#333333", hover_color="#1f77b4",
                                    command=lambda k=key, fl=f_low, fh=f_high: self.process(k, fl, fh))
                btn.grid(row=r+1, column=c+1, padx=3, pady=3)

    def process(self, key, f_low, f_high):
        fs = 8000
        t = np.linspace(0, 0.2, int(fs * 0.2), endpoint=False)
        signal = (np.sin(2 * np.pi * f_low * t) + np.sin(2 * np.pi * f_high * t)) * 0.5
        
        sd.play(signal, fs)
        self.setup_plots(key)

        # Çizgi kalınlığı daha ince (linewidth=0.9)
        self.ax_time.plot(t[:400], signal[:400], color='#1f77b4', linewidth=0.9)
        
        n = len(signal)
        yf = np.fft.fft(signal)
        xf = np.fft.fftfreq(n, 1/fs)
        pos = (xf >= 0) & (xf <= 4000)
        self.ax_freq.plot(xf[pos], np.abs(yf[pos]), color='#d62728', linewidth=0.9)
        
        self.canvas.draw()

if __name__ == "__main__":
    app = DTMFAnalyzer()
    app.mainloop()