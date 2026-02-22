import numpy as np
import matplotlib.pyplot as plt

def main():

    # TEMEL PARAMETRELER
    # Grup üyelerinin okul numaralarının son iki basamağı:
    # 31, 26, 17

    f0 = 74   # f0 = 31 + 26 + 17 = 74 Hz

    # Ödevde istenen frekanslar
    f1 = f0        # 74 Hz
    f2 = f0 / 2    # 37 Hz
    f3 = 10 * f0   # 740 Hz


    # ÖRNEKLEME FREKANSI (Sampling Frequency)

    # Nyquist Kriteri:
    # Bir sinyalin aliasing olmadan doğru örneklenmesi için:
    #        fs > 2 * f_max
    #
    # fs  → örnekleme frekansı
    # f_max → sinyaldeki en yüksek frekans
   
    f_max = f3  # 740 Hz

     # Nyquist sınırı:
     # fs > 2 * 740 = 1480 Hz olmalı

    # Güvenli seçim:
    fs = 8000 

    # Neden 8000 Hz seçildi?
    # Nyquist şartını fazlasıyla sağlar.
    # Dalga formu düzgün görünür.
    # Hesaplama yükü düşük.
    # Grafik için yeterli çözünürlük.


  
    # ORTAK ZAMAN EKSENİ
    
    duration = 0.08  

    """
    0.08 s seçildi çünkü:

    - En düşük frekans = 37 Hz
    - T = 1/37 ≈ 0.027 s
    - 3T ≈ 0.081 s
    - Yani en az 3 periyot gösteriliyor
    """

    t = np.arange(0, duration, 1/fs)

    
    # SİNYALLER
   
    x1 = np.sin(2 * np.pi * f1 * t)
    x2 = np.sin(2 * np.pi * f2 * t)
    x3 = np.sin(2 * np.pi * f3 * t)

  
    # TOPLAM SİNYAL
   
    x_sum = x1 + x2 + x3
# GRAFİKLER
   
    plt.figure(figsize=(10, 9))

    plt.subplot(4, 1, 1)
    plt.plot(t, x1)
    plt.title("Sinyal 1: f₁ = 74 Hz")
    plt.xlabel("Zaman (s)")
    plt.ylabel("Genlik")
    plt.grid(True)

    plt.subplot(4, 1, 2)
    plt.plot(t, x2, color='green')
    plt.title("Sinyal 2: f₂ = 37 Hz")
    plt.xlabel("Zaman (s)")
    plt.ylabel("Genlik")
    plt.grid(True)

    plt.subplot(4, 1, 3)
    plt.plot(t, x3, color='orange')
    plt.title("Sinyal 3: f₃ = 740 Hz")
    plt.xlabel("Zaman (s)")
    plt.ylabel("Genlik")
    plt.grid(True)

    plt.subplot(4, 1, 4)
    plt.plot(t, x_sum, color='purple')
    plt.title("Üç Sinyalin Toplamı (f₁ + f₂ + f₃)")
    plt.xlabel("Zaman (s)")
    plt.ylabel("Genlik")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Program başlangıç noktası
if __name__ == "__main__":
    main()