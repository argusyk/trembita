# Розділ 4. Як навчають Gemini: TPU, попереднє навчання, донавчання й мислення – приклад 3 (рукопис: 04-navchannia.md, рядок 261)
import numpy as np

def softmax(z: np.ndarray, T: float = 1.0) -> np.ndarray:
    e = np.exp((z - z.max()) / T)
    return e / e.sum()

# логіти для токенів «Ужгорода», «Чопа», «Львова», «Парижа»
teacher = np.array([6.0, 4.5, 3.0, -2.0])
student = np.array([5.0, 2.0, 2.5, 0.5])
T, lam, true_id = 2.0, 0.5, 0

pt, ps = softmax(teacher, T), softmax(student, T)
kl = np.sum(pt * np.log(pt / ps))                     # D_KL(вчитель || учень)
ce = -np.log(softmax(student)[true_id])               # звичайна втрата на правильному токені
loss = (1 - lam) * ce + lam * T**2 * kl               # формула (4.17)
print(np.round(pt, 3), np.round(ps, 3), round(loss, 3))
# [0.583 0.276 0.13  0.011] [0.619 0.138 0.177 0.065] 0.259
