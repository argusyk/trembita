# Chapter 2. Architecture: the Transformer, Mixture of Experts and Multimodality – example 1 (manuscript: 02-arkhitektura.md, line 109)
import numpy as np

def softmax(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)    # the shift does not change the distribution
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)

def causal_attention(X, W_q, W_k, W_v):
    Q, K, V = X @ W_q, X @ W_k, X @ W_v         # formula (2.7)
    n, d_k = Q.shape
    scores = Q @ K.T / np.sqrt(d_k)             # pairwise scores n x n
    mask = np.triu(np.full((n, n), -np.inf), k=1)  # (2.9): future -> -inf
    weights = softmax(scores + mask)            # each row sums to 1
    return weights @ V, weights

rng = np.random.default_rng(0)
X = rng.normal(size=(5, 16))                    # 5 tokens, d = 16
W_q, W_k, W_v = (rng.normal(size=(16, 8)) for _ in range(3))
out, w = causal_attention(X, W_q, W_k, W_v)
print(out.shape)          # (5, 8)
print(np.round(w, 2))     # lower-triangular weight matrix
