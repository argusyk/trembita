from trembita import tools


def test_track_known_unknown_and_malformed():
    assert tools.track_shipment(" sm-2610-0042 ")["status"] == "у дорозі"
    assert "не знайдено" in tools.track_shipment("SM-0000-0000")["error"]
    assert "SM-РРММ-NNNN" in tools.track_shipment("42")["error"]


def test_tariff_uses_volumetric_weight():
    light = tools.get_tariff("Львів", "Київ", 20)
    bulky = tools.get_tariff("м. Львів", "КИЇВ", 20, volume_m3=0.5)   # 0.5 м³ -> 125 кг
    assert light["price_uah"] == 350.0                                  # мінімальна вартість
    assert bulky["chargeable_kg"] == 125.0 and bulky["price_uah"] == 812.5


def test_tariff_errors():
    assert "error" in tools.get_tariff("Львів", "Париж", 10)
    assert "error" in tools.get_tariff("Львів", "Київ", -1)
    assert "error" in tools.get_tariff("Львів", "Київ", "багато")


def test_warehouse():
    assert tools.find_warehouse("Ужгород")["code"] == "UZH"
    assert tools.find_warehouse("м. Чернівці")["code"] == "CWC"
    assert "error" in tools.find_warehouse("Одеса")


def test_create_pickup_never_creates_by_itself():
    r = tools.create_pickup("м. Львів, вул. Зелена, 1", "2099-10-31", 10)
    assert r["status"] == "awaiting_human_confirmation" and "pickup_id" not in r
    assert tools.create_pickup("Львів", "31.10.2026", 10)["status"] == "rejected"


def test_tools_build_function_declarations():
    from google.genai import types
    for f in tools.READ_ONLY + [tools.create_pickup]:
        decl = types.FunctionDeclaration.from_callable_with_api_option(callable=f)
        assert decl.name == f.__name__ and decl.description
