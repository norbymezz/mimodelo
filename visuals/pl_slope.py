# visuals/pl_slope.py
import numpy as np
import plotly.graph_objects as go

def slope_loglog(x, y):
    """Devuelve pendiente local d(log y)/d(log x)."""
    lx = np.log(x)
    ly = np.log(y)
    dly = np.gradient(ly)
    dlx = np.gradient(lx)
    return dly / dlx

def plot_slope(t, p, label="Well 1"):
    m = slope_loglog(t, p)
    fig = go.Figure()
    fig.add_scatter(x=t, y=m, mode="lines", name=label)
    fig.update_xaxes(type="log", title="t [day]")
    fig.update_yaxes(title="d(log p) / d(log t)")
    fig.update_layout(height=350, title=f"Slope Plot — {label}")
    return fig
