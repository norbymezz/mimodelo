# visuals/regime_detect.py
import numpy as np

def detect_regimes(t, p):
    """Devuelve lista de (regimen, t_min, t_max)."""
    m = np.gradient(np.log(p)) / np.gradient(np.log(t))
    regimes = []
    N = len(t)

    # Rules (expert heuristic)
    # ------------------------
    # Linear flow: m ~ 0.5
    # SRV dominance: m between 0.2 and 0.4
    # Crossflow interference: abrupt changes in m
    # Late-time ORV / boundary: m → negative small
    # ------------------------

    def segment(name, mask):
        if np.any(mask):
            ts = t[mask]
            return (name, ts[0], ts[-1])

    regimes.append(segment("Linear flow", (m > 0.4) & (m < 0.6)))
    regimes.append(segment("SRV-dominated", (m > 0.2) & (m < 0.4)))
    regimes.append(segment("Interference", np.abs(np.gradient(m)) > 0.2))
    regimes.append(segment("Boundary-dominated", m < 0.0))

    return [r for r in regimes if r is not None]
