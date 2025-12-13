# engine/ozkan_multiwell.py
# Solver analítico multiwell general (n pozos)
# Construye la matriz R(s) usando las funciones base del Ozkan PRO.

import numpy as np
from typing import Sequence
from .ozkan_core import R_self, R_cross
from .units import L_SI

def build_distance_matrix(well_y_ft: Sequence[float]) -> np.ndarray:
    """
    Genera la matriz de distancias entre pozos (en pies).
    well_y_ft: posiciones y de cada pozo (ft).
    """
    n = len(well_y_ft)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = abs(well_y_ft[i] - well_y_ft[j])
    return D

def R_matrix_multi(
    mu_SI: float,
    ct_SI: float,
    k_SRV_SI: Sequence[float],
    k_ORV_SI: Sequence[float],
    h_SI: Sequence[float],
    LSRV_SI: Sequence[float],
    LORV_SI: Sequence[float],
    D12_ft: Sequence[float],
    s: float,
):
    """
    Construye matriz R(s) para n pozos (general).
    Todos los arreglos deben ser de longitud n:
    - k_SRV_SI[i], k_ORV_SI[i]
    - h_SI[i], LSRV_SI[i], LORV_SI[i]
    - D12_ft[i] = y_i (posición del pozo i en ft)
    """

    n = len(k_SRV_SI)

    # Convertimos separaciones a SI (metros)
    y_SI = [L_SI(y_ft) for y_ft in D12_ft]
    Dmat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            Dmat[i, j] = abs(y_SI[i] - y_SI[j])

    R = np.zeros((n, n), float)

    for i in range(n):
        # SELF
        R[i, i] = R_self(
            mu_SI, ct_SI,
            k_SRV_SI[i],
            k_ORV_SI[i],
            h_SI[i],
            LSRV_SI[i],
            LORV_SI[i],
            s,
        )

        # CROSS
        for j in range(n):
            if i != j:
                R[i, j] = R_cross(
                    mu_SI,
                    ct_SI,
                    k_ORV_SI[i],   # Siempre ORV del "i", como en Ozkan
                    h_SI[i],
                    Dmat[i, j],
                    s,
                )

    return R
