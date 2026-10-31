# Розділ 2. Архітектура: трансформер, суміш експертів і мультимодальність – приклад 2 (рукопис: 02-arkhitektura.md, рядок 316)
import numpy as np

rng = np.random.default_rng(1)
T, d, N, k = 32, 16, 8, 2                  # токени, розмірність, експерти, top-k
X = rng.normal(size=(T, d))
W_r = rng.normal(size=(d, N)) * 0.3        # матриця маршрутизатора

logits = X @ W_r                            # бали експертів, T x N
p = np.exp(logits - logits.max(1, keepdims=True))
p /= p.sum(1, keepdims=True)                # повний розподіл маршрутизатора

top = np.argsort(-logits, axis=1)[:, :k]    # k найкращих експертів для токена
g = np.take_along_axis(p, top, axis=1)
g /= g.sum(1, keepdims=True)                # ваги G_i(x), формула (2.25)

f = np.bincount(top[:, 0], minlength=N) / T # частка токенів за першим вибором
P = p.mean(axis=0)                          # середня ймовірність експерта
aux = 0.01 * N * np.sum(f * P)              # формула (2.26), alpha = 0.01
print("навантаження:", np.bincount(top.ravel(), minlength=N))
print("втрата балансування:", round(aux, 4), "(мінімум 0.01)")
