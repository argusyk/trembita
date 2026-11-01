# Chapter 4. How Gemini Is Trained: TPUs, Pre-training, Fine-tuning and Thinking – example 2 (manuscript: 04-navchannia.md, line 96)
import numpy as np

E, A, B, alpha, beta = 1.69, 406.4, 410.7, 0.34, 0.28   # Chinchilla fit

def optimum(C: float) -> tuple[float, float, float]:
    N = np.logspace(8, 13, 4000)          # candidates: from 100M to 10T parameters
    D = C / (6 * N)                       # tokens that fit into the budget (4.2)
    L = E + A / N**alpha + B / D**beta    # formula (4.4)
    i = L.argmin()
    return N[i], D[i], L[i]

for C in (1e22, 1e23, 1e24):
    n, d, l = optimum(C)
    print(f"C={C:.0e}: N={n/1e9:.1f}B, D={d/1e12:.2f}T, D/N={d/n:.0f}, L={l:.3f}")
