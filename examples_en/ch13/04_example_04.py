# Chapter 13. Optimization: context caching, batch processing and cost – example 4 (manuscript: 13-optymizatsiya.md, line 221)
from trembita.costs import cache_break_even

print(cache_break_even("gemini-3.8-flash", hours=1))   # ≈ 1.75
print(cache_break_even("gemini-3.8-flash", hours=8))   # ≈ 6.7
