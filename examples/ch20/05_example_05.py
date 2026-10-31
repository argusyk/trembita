# Розділ 20. Оцінювання застосунків на Gemini – приклад 5 (рукопис: 20-otsiniuvannia.md, рядок 359)
import math

def mcnemar_p(b: int, c: int) -> float:
    """Двобічне p-значення тесту Мак-Немара; b, c – розбіжності на користь A і B."""
    n = b + c
    if n == 0:
        return 1.0
    if n < 25:                                    # мало розбіжностей: точний біноміальний тест
        k = min(b, c)
        return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)
    chi2 = (abs(b - c) - 1) ** 2 / n              # формула (20.5)
    return math.erfc(math.sqrt(chi2 / 2))         # хвіст хі-квадрат з 1 ступенем свободи

def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Довірчий інтервал Вілсона для частки k/n, формула (20.4)."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, centre - half), min(1.0, centre + half)

def sample_size(p: float, margin: float, z: float = 1.96) -> int:
    """Кількість випадків для оцінки точності p з похибкою margin, формула (20.6)."""
    return math.ceil(z * z * p * (1 - p) / margin ** 2)

print(round(mcnemar_p(8, 22), 3))                  # 0.018
print([round(x, 3) for x in wilson(176, 200)])     # [0.828, 0.918]
print(sample_size(0.85, 0.03))                     # 545
