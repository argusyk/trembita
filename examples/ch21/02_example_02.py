# Розділ 21. Пошук доповненою генерацією: ембедінги, File Search і RAG Engine – приклад 2 (рукопис: 21-rag.md, рядок 138)
import re


def chunk_regulation(doc_title: str, text: str,
                     max_chars: int = 1800, overlap: int = 200) -> list[dict]:
    """Ріже регламент за заголовками; довгі розділи – вікном з перекриттям."""
    chunks = []
    for sec in re.split(r"\n(?=#{1,3} )", text):     # межі – заголовки Markdown
        heading = sec.strip().splitlines()[0].lstrip("# ").strip()
        body, start = sec.strip(), 0
        while start < len(body):
            end = min(start + max_chars, len(body))
            if end < len(body):                       # шукаємо кінець речення
                cut = body.rfind(". ", start, end)
                if cut > start + max_chars // 2:
                    end = cut + 1
            chunks.append({
                "id": f"{doc_title}#{len(chunks)}",
                "title": doc_title,
                "section": heading,
                # контекстний заголовок бачать і пошук, і модель
                "text": f"{doc_title} / {heading}\n{body[start:end].strip()}",
            })
            if end >= len(body):
                break
            start = end - overlap
    return chunks
