"""The line of stages at the top of a request or transfer page."""

from audit.models import AuditLog


def journey(record, stages):
    """(label, done, current, stopped) for each stage.

    The last stage counts as done once it is reached (Fulfilled, Receipt confirmed). A record that ended early
    (rejected, cancelled, closed, expired) shows the stage where it stopped, found from its history.
    """
    last = len(stages) - 1
    current = next((i for i, (_, codes) in enumerate(stages) if record.status in codes), None)
    stopped = None
    if current is None:
        entry = AuditLog.for_record(record).filter(after_value__startswith=record.status).order_by("-pk").first()
        before = (entry.before_value or "")[:5] if entry else ""
        stopped = next((i for i, (_, codes) in enumerate(stages) if before in codes), None)
    reached = current if current is not None else stopped
    return [(label,
             reached is not None and (i < reached or i == current == last),
             current is not None and i == current != last,
             stopped is not None and i == stopped)
            for i, (label, _) in enumerate(stages)]
