# Трембіта

Супровідний код навчального посібника **«Секрети Gemini AI»** (Я. Ю. Дорогий, ДонНТУ, 2026): асистент «Трембіта» вигаданої логістичної компанії «Смерека», який у книзі еволюціонує від одного виклику Gemini API до мультиагентної системи.

| Тека | Вміст |
|---|---|
| `trembita/` | пакет Python: клієнт із повторами й резервними моделями, інструменти та підтвердження дій, схеми накладних, вартість і кешування, RAG, оцінювання, захисні шари, команда агентів на ADK |
| `tests/` | тести пакета; працюють без мережі й ключа API |
| `examples/` | усі приклади Python з книги за розділами (`examples/README.md`) |
| `examples_en/` | ті самі приклади з англійського видання «Secrets of Gemini AI» (коментарі й підказки англійською) |
| `scripts/check_examples.py` | перевірка прикладів без мережі: синтаксис, імпорти, імена класів і методів SDK |

## Швидкий старт

```bash
git clone https://github.com/argusyk/trembita
cd trembita
python -m pip install -e ".[agents,test]"
python -m pytest                      # тести без мережі
python scripts/check_examples.py      # перевірка прикладів книги проти встановленого SDK

export GEMINI_API_KEY="..."            # ключ з Google AI Studio
python -c "from trembita.client import ask; print(ask('Скільки коштує 20 кг зі Львова до Києва?'))"
```

Більшість прикладів працює на безкоштовному рівні Gemini API з моделлю `gemini-3.8-flash`. Моделі змінюють змінними середовища `TREMBITA_MODEL`, `TREMBITA_MODEL_SMART`, `TREMBITA_MODEL_LITE`; для Gemini Enterprise Agent Platform задайте `GOOGLE_GENAI_USE_VERTEXAI=true`, `GOOGLE_CLOUD_PROJECT` і `GOOGLE_CLOUD_LOCATION`.

Ідентифікатори моделей, ціни й ліміти відповідають стану Gemini на жовтень 2026 року; перед використанням у проєкті звіряйте їх з документацією Google. Дані «Смереки» в `trembita/data.py` вигадані.

## Ліцензія

MIT – див. `LICENSE`.

## English

Companion code for the textbook *Secrets of Gemini AI* (English edition). The package `trembita/` is shared by both editions; its comments, prompts and demo data are in Ukrainian because the running example is a Ukrainian logistics company. English versions of all book examples are in `examples_en/`. Quick start: `pip install -e ".[agents,test]"`, `pytest`, `python scripts/check_examples.py`.
