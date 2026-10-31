from types import SimpleNamespace as NS

from trembita import evals


def test_exact_and_token_f1():
    assert evals.exact_match("  Доставлено. ", "доставлено")
    assert 0 < evals.token_f1("Київ, склад на Березняках", "склад Київ Березняки") < 1


def test_per_class():
    pr, rc, f1 = evals.per_class(["claim"] * 50 + ["other"] * 15, ["claim"] * 45 + ["other"] * 5 + ["claim"] * 15)["claim"]
    assert round(pr, 2) == 0.90 and round(rc, 2) == 0.75


def test_statistics_match_chapter_numbers():
    assert round(evals.mcnemar_p(8, 22), 3) == 0.018
    assert [round(x, 3) for x in evals.wilson(176, 200)] == [0.828, 0.918]
    assert evals.sample_size(0.85, 0.03) == 545


def test_pairwise_swaps_positions():
    answers = iter(["A", "A"])                     # суддя завжди обирає першу – маємо нічию
    fake = NS(models=NS(generate_content=lambda **kw: NS(parsed=NS(winner=next(answers)))))
    assert evals.pairwise("q", "r", "x", "y", client=fake) == "tie"


def test_classify_intent_uses_enum():
    fake = NS(models=NS(generate_content=lambda **kw: NS(parsed=evals.Intent.claim)))
    assert evals.classify_intent("Розбили палету!", client=fake) == "claim"
