from trembita import tools


def test_track_known_and_unknown():
    assert tools.track_shipment("sm-2610-0042")["status"] == "у дорозі"
    assert "error" in tools.track_shipment("SM-0000-0000")


def test_tariff_uses_volumetric_weight():
    light = tools.get_tariff("Львів", "Київ", 20)
    bulky = tools.get_tariff("Львів", "Київ", 20, volume_m3=0.5)   # 0.5 м³ -> 125 кг
    assert light["price_uah"] == 350.0                              # мінімальна вартість
    assert bulky["chargeable_kg"] == 125.0 and bulky["price_uah"] == 812.5


def test_tariff_errors():
    assert "error" in tools.get_tariff("Львів", "Париж", 10)
    assert "error" in tools.get_tariff("Львів", "Київ", -1)


def test_pickup_validation_and_determinism():
    assert "error" in tools.create_pickup("Львів", "31.10.2026", 10)
    a = tools.create_pickup("м. Львів, вул. Зелена, 1", "2026-10-31", 10)
    b = tools.create_pickup("м. Львів, вул. Зелена, 1", "2026-10-31", 10)
    assert a == b and a["status"] == "створено"


def test_warehouse():
    assert tools.find_warehouse("Ужгород")["code"] == "UZH"
