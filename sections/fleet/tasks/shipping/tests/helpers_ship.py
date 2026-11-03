def P(l, w, h, kg, unit="metric"):
    return {"length": l, "width": w, "height": h, "weight": kg, "unit": unit}


def S(origin="10115", dest="34117", parcel=None, ship_at="2026-03-02T09:00", residential=False):
    return {"origin": origin, "dest": dest, "parcel": parcel or P(40, 30, 20, "3.2"), "ship_at": ship_at,
            "residential": residential}
