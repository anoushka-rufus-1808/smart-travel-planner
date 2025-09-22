import math

def compute_per_day(budget_total, days):
    return math.floor(budget_total / days)

def estimate_activity_cost(activity, travel_style):
    base = int(activity.get("base_cost", 100))
    style_multiplier = {"cheap":0.6, "standard":1.0, "luxury":1.8}
    return int(base * style_multiplier.get(travel_style, 1.0))

def build_itinerary(days, activities, per_day_budget, travel_style):
    itinerary = {f"Day {i+1}": [] for i in range(days)}
    day_remaining = {k: per_day_budget for k in itinerary}

    for act in activities:
        cost = estimate_activity_cost(act, travel_style)
        for d in range(days):
            day = f"Day {d+1}"
            if day_remaining[day] >= cost:
                itinerary[day].append({**act, "cost": cost})
                day_remaining[day] -= cost
                break
        else:
            itinerary.setdefault("Extras", []).append({**act, "cost": cost})

    return itinerary, day_remaining
