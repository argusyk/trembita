# Chapter 4. How Gemini Is Trained: TPUs, Pre-training, Fine-tuning and Thinking – example 1 (manuscript: 04-navchannia.md, line 53)
import numpy as np

# probabilities the model assigned to the true next tokens
p_true = np.array([0.62, 0.35, 0.08])  # "arrived", "in", "Uzhhorod"
loss = -np.log(p_true).mean()          # average cross-entropy, formula (2.2)
ppl = np.exp(loss)                     # perplexity
print(f"loss = {loss:.3f} nats, perplexity = {ppl:.2f}")
# loss = 1.351 nats, perplexity = 3.86
