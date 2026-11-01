# Chapter 20. Evaluating Gemini Applications – example 5 (manuscript: 20-otsiniuvannia.md, line 359)
import math

def mcnemar_p(b: int, c: int) -> float:
    """Two-sided p-value of McNemar's test; b, c are disagreements in favor of A and B."""
    n = b + c
    if n == 0:
        return 1.0
    if n < 25:                                    # few disagreements: exact binomial test
        k = min(b, c)
        return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)
    chi2 = (abs(b - c) - 1) ** 2 / n              # formula (20.5)
    return math.erfc(math.sqrt(chi2 / 2))         # chi-square tail with 1 degree of freedom

def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson confidence interval for the proportion k/n, formula (20.4)."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, centre - half), min(1.0, centre + half)

def sample_size(p: float, margin: float, z: float = 1.96) -> int:
    """Number of cases to estimate accuracy p with margin of error margin, formula (20.6)."""
    return math.ceil(z * z * p * (1 - p) / margin ** 2)

print(round(mcnemar_p(8, 22), 3))                  # 0.018
print([round(x, 3) for x in wilson(176, 200)])     # [0.828, 0.918]
print(sample_size(0.85, 0.03))                     # 545
