# engine/schedules.py
# Manejo general de q(t) por tramos y q̂(s) estable.

import math
from dataclasses import dataclass
from typing import List
import numpy as np
from .units import DAY_TO_S

@dataclass
class WellSchedule:
    t_days: List[float]
    q_stbd: List[float]

def clean_schedule(ws: WellSchedule) -> WellSchedule:
    """Ordena, elimina duplicados y asegura monotonicidad en tiempo."""
    pairs = sorted(zip(ws.t_days, ws.q_stbd), key=lambda z: z[0])
    t = []
    q = []
    for ti, qi in pairs:
        if not t or ti != t[-1]:
            t.append(ti)
            q.append(qi)
        else:
            q[-1] = qi
    return WellSchedule(t, q)

def q_hat_piecewise(ws: WellSchedule, s: float) -> float:
    """Transformada de Laplace del caudal por tramos."""
    acc = 0.0
    last_q = 0.0
    for tk_day, qk in zip(ws.t_days, ws.q_stbd):
        tk = tk_day * DAY_TO_S
        acc += (qk - last_q) * math.exp(-s * tk)
        last_q = qk
    return acc / max(s, 1e-30)
