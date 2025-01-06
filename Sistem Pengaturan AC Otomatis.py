import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt  # Diperlukan untuk menampilkan grafik

# Variabel input
suhu = ctrl.Antecedent(np.arange(16, 36, 1), 'suhu')  # °C
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')  # %

# Variabel output
kecepatan_kipas = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan_kipas')  # %

# Himpunan fuzzy untuk Suhu
suhu['dingin'] = fuzz.trimf(suhu.universe, [16, 16, 22])
suhu['normal'] = fuzz.trimf(suhu.universe, [20, 25, 30])
suhu['panas'] = fuzz.trimf(suhu.universe, [28, 35, 35])

# Himpunan fuzzy untuk Kelembapan
kelembapan['rendah'] = fuzz.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['sedang'] = fuzz.trimf(kelembapan.universe, [30, 50, 70])
kelembapan['tinggi'] = fuzz.trimf(kelembapan.universe, [60, 100, 100])

# Himpunan fuzzy untuk Kecepatan Kipas
kecepatan_kipas['lambat'] = fuzz.trimf(kecepatan_kipas.universe, [0, 0, 50])
kecepatan_kipas['sedang'] = fuzz.trimf(kecepatan_kipas.universe, [30, 50, 70])
kecepatan_kipas['cepat'] = fuzz.trimf(kecepatan_kipas.universe, [60, 100, 100])

# Rule base
rules = [
    ctrl.Rule(suhu['dingin'] & kelembapan['rendah'], kecepatan_kipas['lambat']),
    ctrl.Rule(suhu['dingin'] & kelembapan['sedang'], kecepatan_kipas['lambat']),
    ctrl.Rule(suhu['dingin'] & kelembapan['tinggi'], kecepatan_kipas['sedang']),
    ctrl.Rule(suhu['normal'] & kelembapan['rendah'], kecepatan_kipas['sedang']),
    ctrl.Rule(suhu['normal'] & kelembapan['sedang'], kecepatan_kipas['sedang']),
    ctrl.Rule(suhu['normal'] & kelembapan['tinggi'], kecepatan_kipas['cepat']),
    ctrl.Rule(suhu['panas'] & kelembapan['rendah'], kecepatan_kipas['cepat']),
    ctrl.Rule(suhu['panas'] & kelembapan['sedang'], kecepatan_kipas['cepat']),
    ctrl.Rule(suhu['panas'] & kelembapan['tinggi'], kecepatan_kipas['cepat']),
]

# Sistem kontrol
kipas_ctrl = ctrl.ControlSystem(rules)
kipas_simulasi = ctrl.ControlSystemSimulation(kipas_ctrl)

# Simulasi
kipas_simulasi.input['suhu'] = 30  # Masukkan suhu
kipas_simulasi.input['kelembapan'] = 65  # Masukkan kelembapan
kipas_simulasi.compute()  # Hitung hasil berdasarkan aturan fuzzy

# Output
print(f"Kecepatan Kipas: {kipas_simulasi.output['kecepatan_kipas']:.2f}%")

# Menampilkan grafik fungsi keanggotaan
suhu.view()
kelembapan.view()
kecepatan_kipas.view(sim=kipas_simulasi)

# Menampilkan semua grafik
plt.show()
