# Chapter 2. Architecture: the Transformer, Mixture of Experts and Multimodality – example 2 (manuscript: 02-arkhitektura.md, line 316)
import numpy as np

rng = np.random.default_rng(1)
T, d, N, k = 32, 16, 8, 2                  # tokens, dimension, experts, top-k
X = rng.normal(size=(T, d))
W_r = rng.normal(size=(d, N)) * 0.3        # router matrix

logits = X @ W_r                            # expert scores, T x N
p = np.exp(logits - logits.max(1, keepdims=True))
p /= p.sum(1, keepdims=True)                # full router distribution

top = np.argsort(-logits, axis=1)[:, :k]    # the k best experts for each token
g = np.take_along_axis(p, top, axis=1)
g /= g.sum(1, keepdims=True)                # weights G_i(x), formula (2.25)

f = np.bincount(top[:, 0], minlength=N) / T # fraction of tokens by first choice
P = p.mean(axis=0)                          # average probability of each expert
aux = 0.01 * N * np.sum(f * P)              # formula (2.26), alpha = 0.01
print("load:", np.bincount(top.ravel(), minlength=N))
print("balancing loss:", round(aux, 4), "(minimum 0.01)")
