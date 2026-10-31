# Розділ 2. Архітектура: трансформер, суміш експертів і мультимодальність – приклад 1 (рукопис: 02-arkhitektura.md, рядок 109)
import numpy as np

def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)    # зсув не змінює розподіл
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)

def causal_attention(X, W_q, W_k, W_v):
    Q, K, V = X @ W_q, X @ W_k, X @ W_v         # формула (2.7)
    n, d_k = Q.shape
    scores = Q @ K.T / np.sqrt(d_k)             # попарні бали n x n
    mask = np.triu(np.full((n, n), -np.inf), k=1)  # (2.9): майбутнє -> -inf
    weights = softmax(scores + mask)            # кожен рядок сумується в 1
    return weights @ V, weights

rng = np.random.default_rng(0)
X = rng.normal(size=(5, 16))                    # 5 токенів, d = 16
W_q, W_k, W_v = (rng.normal(size=(16, 8)) for _ in range(3))
out, w = causal_attention(X, W_q, W_k, W_v)
print(out.shape)          # (5, 8)
print(np.round(w, 2))     # нижньотрикутна матриця ваг
