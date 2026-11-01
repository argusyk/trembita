# Chapter 4. How Gemini Is Trained: TPUs, Pre-training, Fine-tuning and Thinking – example 3 (manuscript: 04-navchannia.md, line 251)
import numpy as np

def softmax(z: np.ndarray, T: float = 1.0) -> np.ndarray:
    e = np.exp((z - z.max()) / T)
    return e / e.sum()

# logits for the tokens "Uzhhorod", "Chop", "Lviv", "Paris"
teacher = np.array([6.0, 4.5, 3.0, -2.0])
student = np.array([5.0, 2.0, 2.5, 0.5])
T, lam, true_id = 2.0, 0.5, 0

pt, ps = softmax(teacher, T), softmax(student, T)
kl = np.sum(pt * np.log(pt / ps))                     # D_KL(teacher || student)
ce = -np.log(softmax(student)[true_id])               # ordinary loss on the correct token
loss = (1 - lam) * ce + lam * T**2 * kl               # formula (4.14)
print(np.round(pt, 3), np.round(ps, 3), round(loss, 3))
# [0.583 0.276 0.13  0.011] [0.619 0.138 0.177 0.065] 0.259
