# engine/ozkan_core.py
# Núcleo físico PRO basado en Ozkan, SPE-215031 + estabilidad industrial.

import numpy as np
import math
from .units import FT_TO_M

# ---------- ESTABILIDAD NUMERICA ----------

def _coth_stable(x):
    x = float(x)
    ax = abs(x)
    if ax < 1e-8:
        return 1.0/x + x/3.0
    if x > 700:   # evita overflow exp(+x)
        return 1.0
    if x < -700:  # evita overflow exp(-x)
        return -1.0
    return math.cosh(x) / math.sinh(x)

def _exp_stable(z):
    return math.exp(max(min(z, 700.0), -700.0))

# ---------- DIFUSIVIDAD ----------

def lambda_block(mu, ct, k, s):
    """λ(s) estable: sqrt(mu*ct*s/k)."""
    return math.sqrt(max(mu*ct*s, 1e-40) / max(k,1e-40))

# ---------- R SELF ----------

def R_slab(mu, ct, k, h, L, s):
    lam = lambda_block(mu, ct, k, s)
    x = lam * max(L, 1e-30)
    return (mu/(k*max(h,1e-30))) * (_coth_stable(x) / max(lam,1e-30))

def R_semi_inf(mu, ct, k, h, s):
    lam = lambda_block(mu, ct, k, s)
    return (mu/(k*max(h,1e-30))) * (1.0 / max(lam,1e-30))

def R_self(mu, ct, k_srv, k_orv, h, L_srv, L_orv, s):
    """Forma pura Ozkan: SRV en slab finito + ORV finito o semiinfinito."""
    R_srv = R_slab(mu, ct, k_srv, h, L_srv, s)
    if L_orv > 0:
        R_orv = R_slab(mu, ct, k_orv, h, L_orv, s)
    else:
        R_orv = R_semi_inf(mu, ct, k_orv, h, s)
    return R_srv + R_orv

# ---------- R CROSS ----------

def R_cross(mu, ct, k_orv, h, D, s):
    lam = lambda_block(mu, ct, k_orv, s)
    return (mu/(k_orv*max(h,1e-30))) * (_exp_stable(-lam*max(D,0.0))) / max(lam,1e-30)

