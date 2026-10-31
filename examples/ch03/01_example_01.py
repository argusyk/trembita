# Розділ 3. Токени, мультимодальні токени й довгий контекст – приклад 1 (рукопис: 03-tokeny-kontekst.md, рядок 77)
import math

# іграшковий словник уніграмної моделі: фрагмент -> імовірність
vocab = {"пере": 0.020, "ве": 0.015, "зен": 0.004, "ня": 0.030,
         "везення": 0.0004, "перевез": 0.0003, "ення": 0.006}
for ch in "перевезення":            # окремі літери є завжди
    vocab.setdefault(ch, 0.001)

def viterbi(word: str) -> tuple[list[str], float]:
    n = len(word)
    best = [(-math.inf, 0)] * (n + 1)  # (log P найкращого шляху, початок фрагмента)
    best[0] = (0.0, 0)
    for end in range(1, n + 1):
        for start in range(end):
            piece = word[start:end]
            if piece in vocab:
                score = best[start][0] + math.log(vocab[piece])
                if score > best[end][0]:
                    best[end] = (score, start)
    pieces, end = [], n                # відновлюємо шлях з кінця
    while end > 0:
        start = best[end][1]
        pieces.append(word[start:end])
        end = start
    return pieces[::-1], round(best[n][0], 2)

print(viterbi("перевезення"))  # (['пере', 'везення'], -11.74)
