# -*- coding: utf-8 -*-
"""Перевірка блоків коду Python у рукописі без мережі.

Для кожного блоку ```python: 1) синтаксис (ast.parse); 2) імпорти з google.* і trembita.* —
чи існують модуль і імена (trembita пропускається, якщо пакета немає); 3) атрибути `types.X` —
чи є такий клас/енум у google.genai.types; 4) виклики `client.<ресурс>.<метод>` — чи є такий
ресурс і метод у genai.Client. Використання: py build/check_code.py [manuscript/NN-*.md | examples/.../*.py ...]
Без аргументів перевіряє manuscript/*.md, а якщо рукопису немає (репозиторій коду) – examples/**/*.py.
"""
import ast, glob, importlib, os, re, sys, warnings
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r"^```python\s*\n(.*?)^```", re.S | re.M)

try:
    from google import genai
    from google.genai import types as T
    CLIENT = genai.Client(api_key="offline-check")
except Exception as e:                       # SDK не встановлено – лише синтаксис
    print("google-genai недоступний:", e)
    T = CLIENT = None


def check_block(code):
    errs = []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"синтаксис: рядок {e.lineno}: {e.msg}"]
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] in ("google", "trembita"):
            if node.module.startswith("trembita"):
                continue
            try:
                mod = importlib.import_module(node.module)
            except Exception as e:
                errs.append(f"імпорт {node.module}: {e.__class__.__name__}")
                continue
            for a in node.names:
                if a.name != "*" and not hasattr(mod, a.name):
                    try:
                        importlib.import_module(f"{node.module}.{a.name}")
                    except Exception:
                        errs.append(f"у {node.module} немає {a.name}")
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] == "google":
                    try:
                        importlib.import_module(a.name)
                    except Exception as e:
                        errs.append(f"імпорт {a.name}: {e.__class__.__name__}")
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if T is not None and node.value.id == "types" and not hasattr(T, node.attr):
                errs.append(f"types.{node.attr} не існує")
        if CLIENT is not None and isinstance(node, ast.Attribute) and isinstance(node.value, ast.Attribute):
            base = node.value
            chain = [node.attr, base.attr]
            while isinstance(base.value, ast.Attribute):
                base = base.value; chain.append(base.attr)
            if isinstance(base.value, ast.Name) and base.value.id == "client":
                obj, path = CLIENT, "client"
                for attr in reversed(chain):
                    if not hasattr(obj, attr):
                        errs.append(f"{path}.{attr} не існує"); break
                    obj, path = getattr(obj, attr), f"{path}.{attr}"
                    if not path.count(".") < 3:
                        break
    return sorted(set(errs))


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "manuscript", "*.md"))) \
        or sorted(glob.glob(os.path.join(ROOT, "examples*", "**", "*.py"), recursive=True))
    total = bad = 0
    for p in files:
        s = open(p, encoding="utf-8").read()
        blocks = [(1, s)] if p.endswith(".py") else \
            [(s[:m.start()].count("\n") + 1, m.group(1)) for m in BLOCK.finditer(s)]
        for line, code in blocks:
            total += 1
            errs = check_block(code)
            if errs:
                bad += 1
                print(f"{os.path.relpath(p, ROOT)}:{line}: " + "; ".join(errs))
    print(f"блоків python: {total}, з проблемами: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
