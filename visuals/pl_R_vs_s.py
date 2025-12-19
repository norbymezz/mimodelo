# visuals/pl_R_vs_s.py
import numpy as np
import plotly.graph_objects as go

def plot_R_vs_s(Rfun, s_min=1e-8, s_max=1e2, n=120):
    """
    Rfun(s) debe devolver R(s) en FIELD units (matriz).
    """
    ss = np.logspace(np.log10(s_min), np.log10(s_max), n)
    vals = []
    for s in ss:
        R = Rfun(s)
        vals.append(np.mean(np.diag(R)))   # valor self típico
    vals = np.array(vals)

    fig = go.Figure()
    fig.add_scatter(
        x=ss, y=vals, mode="lines",
        name="R_self(s)", line=dict(width=2)
    )
    fig.update_xaxes(type="log", title="s [1/s]")
    fig.update_yaxes(type="log", title="R(s) [psi·day/STB]")
    fig.update_layout(height=380, title="Kernel R_self(s) — Diagnóstico de Ozkan")
    return fig
