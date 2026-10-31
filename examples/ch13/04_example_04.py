# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 4 (рукопис: 13-optymizatsiya.md, рядок 221)
from trembita.costs import cache_break_even

print(cache_break_even("gemini-3.8-flash", hours=1))   # ≈ 1,75
print(cache_break_even("gemini-3.8-flash", hours=8))   # ≈ 6,7
