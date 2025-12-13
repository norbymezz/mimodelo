# visuals/pl_interference_map.py
import numpy as np
import plotly.graph_objects as go


def interference_map(P):  
    """
    P: matriz (n_times × n_wells)
    Devuelve mapa de |P_i(t) - P_j(t)|.

############################################################
  
    Interpretación:

    M[i,j] grande → interferencia fuerte.

    Diagonal = 0.

    Simetría esperada: M[i,j] = M[j,i].

    """
    nt, nw = P.shape
    M = np.zeros((nw, nw))
    for i in range(nw):
        for j in range(nw):
            M[i, j] = np.max(np.abs(P[:, i] - P[:, j]))

    fig = go.Figure(data=go.Heatmap(
        z=M,
        x=[f"W{j+1}" for j in range(nw)],
        y=[f"W{i+1}" for i in range(nw)],
        colorscale="Viridis"
    ))
    fig.update_layout(
        title="Interference Map — max |ΔP_ij(t)|",
        height=380
    )
    return fig
