# Розділ 4. Як навчають Gemini: TPU, попереднє навчання, донавчання й мислення – приклад 2 (рукопис: 04-navchannia.md, рядок 104)
import numpy as np

E, A, B, alpha, beta = 1.69, 406.4, 410.7, 0.34, 0.28   # підгонка Chinchilla

def optimum(C: float) -> tuple[float, float, float]:
    N = np.logspace(8, 13, 4000)          # кандидати: від 100 млн до 10 трлн параметрів
    D = C / (6 * N)                       # токени, що вміщуються в бюджет (4.4)
    L = E + A / N**alpha + B / D**beta    # формула (4.6)
    i = L.argmin()
    return N[i], D[i], L[i]

for C in (1e22, 1e23, 1e24):
    n, d, l = optimum(C)
    print(f"C={C:.0e}: N={n/1e9:.1f} млрд, D={d/1e12:.2f} трлн, D/N={d/n:.0f}, L={l:.3f}")
