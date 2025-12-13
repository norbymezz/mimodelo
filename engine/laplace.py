# engine/laplace.py
# Inversión Laplace PRO: Stehfest y Gaver–Euler altamente estables.

import numpy as np
import math

# ====================== STEHFEST ======================

def stehfest_weights(N: int) -> np.ndarray:
    assert N > 0 and N % 2 == 0
    V = np.zeros(N + 1)
    half = N // 2
    for k in range(1, N + 1):
        s = 0.0
        jmin = (k + 1) // 2
        jmax = min(k, half)
        for j in range(jmin, jmax + 1):
            num = j**half * math.factorial(2*j)
            den = (
                math.factorial(half-j)
                * math.factorial(j)
                * math.factorial(j-1)
                * math.factorial(k-j)
                * math.factorial(2*j-k)
            )
            s += num / den
        V[k] = s * ((-1)**(k + half))
    return V[1:]  # quitamos el 0

def invert_stehfest(F, t: float, N: int = 12):
    if t <= 0.0:
        return np.nan
    V = stehfest_weights(N)
    ln2 = math.log(2.0)
    s_nodes = (np.arange(1, N+1) * ln2) / max(t,1e-30)
    vals = np.stack([np.asarray(F(s)) for s in s_nodes], axis=0)
    return (ln2/t) * (V[:,None] * vals).sum(axis=0)

# ====================== GAVER-EULER ======================

def invert_gaver_euler(F, t: float, M: int = 18, P: int = 8):
    ln2 = math.log(2.0)
    S = []
    for n in range(1, M+P+1):
        acc = None
        for k in range(1, n+1):
            s = (k*ln2)/max(t,1e-30)
            term = ((-1)**k)*math.comb(n,k)*np.asarray(F(s))
            acc = term if acc is None else acc + term
        S.append(acc)
    S = np.stack(S, axis=0)
    E = sum(math.comb(P,p)*S[(M-1)+p] for p in range(P+1)) / (2**P)
    return (-ln2/max(t,1e-30)) * E
