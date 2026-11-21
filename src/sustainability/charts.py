"""The savings graph on the dashboard, drawn as SVG by our own code (no chart library and nothing loaded from
outside). This module only works out the positions; the template draws them and writes the dates and amounts
in the user's language."""

from math import ceil, floor, log10

WIDTH, HEIGHT = 960, 280
LEFT, RIGHT, TOP, BOTTOM = 72, 28, 24, 40
MAX_LABELS = 8


def nice_step(rough):
    """A round step for the value axis: 1, 2 or 5 times a power of ten."""
    if rough <= 0:
        return 1
    power = 10 ** floor(log10(rough))
    for factor in (1, 2, 5, 10):
        if factor * power >= rough:
            return factor * power
    return 10 * power


def savings_chart(months):
    """months: [(first day of the month, running total)] from SustainabilityIndicators.savings_by_month().
    Returns what the template needs to draw the line, or None when there is nothing to draw."""
    if not months:
        return None
    values = [float(v) for _, v in months]
    high, low = max(values + [0.0]), min(values + [0.0])
    step = nice_step((high - low) / 4 or 1)
    high, low = ceil(high / step) * step or step, floor(low / step) * step
    plot_w, plot_h = WIDTH - LEFT - RIGHT, HEIGHT - TOP - BOTTOM

    def x(i):
        return LEFT + (plot_w * i / (len(months) - 1) if len(months) > 1 else plot_w / 2)

    def y(value):
        return TOP + (high - value) * plot_h / (high - low)

    points = [{"x": round(x(i), 1), "y": round(y(v), 1), "month": m, "value": total}
              for i, ((m, total), v) in enumerate(zip(months, values))]
    every = ceil(len(months) / MAX_LABELS)
    zero = round(y(0), 1)
    line = " ".join(f"{p['x']},{p['y']}" for p in points)
    area = f"M{points[0]['x']},{zero} L" + " L".join(f"{p['x']},{p['y']}" for p in points) + f" L{points[-1]['x']},{zero} Z"
    ticks, value = [], low
    while value <= high + step / 2:
        ticks.append({"y": round(y(value), 1), "value": value})
        value += step
    last = points[-1]
    return {
        "width": WIDTH, "height": HEIGHT, "left": LEFT, "right": WIDTH - RIGHT, "bottom": HEIGHT - BOTTOM,
        "label_y": HEIGHT - 12, "tick_x": LEFT - 8, "zero": zero, "line": line, "area": area, "points": points,
        "ticks": ticks,
        # Month names under the line; the last one ends at its point so it is never cut off.
        "labels": [{**p, "anchor": "end" if i == len(points) - 1 and len(points) > 1 else "middle"}
                   for i, p in enumerate(points) if i % every == 0 or i == len(points) - 1],
        "last": last, "good": last["value"] >= 0,
        # Keep the last amount inside the drawing: write it left of the point when the point is near the edge.
        "last_anchor": "end" if last["x"] > WIDTH - 160 else "start",
        "last_x": last["x"] - 8 if last["x"] > WIDTH - 160 else last["x"] + 8,
    }
