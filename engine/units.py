# engine/units.py
# Conversión coherente FIELD ↔ SI, robusta y estable numéricamente.

import numpy as np

PSI_TO_PA = 6894.757293168
FT_TO_M   = 0.3048
CP_TO_PAS = 1e-3
ND_TO_M2  = 9.869233e-22
DAY_TO_S  = 86400.0
STB_TO_M3 = 0.158987294928

def mu_SI(mu_cp: float) -> float:
    return mu_cp * CP_TO_PAS

def k_SI(k_nD: float) -> float:
    return k_nD * ND_TO_M2

def ct_SI(ct_invpsi: float) -> float:
    return ct_invpsi / PSI_TO_PA

def h_SI(h_ft: float) -> float:
    return h_ft * FT_TO_M

def L_SI(L_ft: float) -> float:
    return L_ft * FT_TO_M

def pressure_field(p_pa: float) -> float:
    return p_pa / PSI_TO_PA

def R_SI_to_field(R_SI: float) -> float:
    # R in SI: [Pa·s/m³] → convert to [psi·day/STB]
    return R_SI * (1/PSI_TO_PA) * DAY_TO_S / (STB_TO_M3/DAY_TO_S)
