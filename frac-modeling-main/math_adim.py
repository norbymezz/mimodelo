import streamlit as st

def adim_tab(params=None):
    st.subheader("📊 Variables adimensionales — SPE-215031-PA")

    # === Definición presión adimensional ===
    st.markdown("**Referencia: Eq. (1)**")
    st.latex(r"""
    p_{tKiD} = \frac{\psi \, k_R h}{q_R B \mu} \, (p_{ini} - p_{tKi})
    """)
    st.markdown(r"""
    **Definiciones:**
    - $p_{tKiD}$: presión adimensional en bloque $Ki$.  
    - $p_{ini}$: presión inicial $[psi]$.  
    - $p_{tKi}$: presión en bloque $Ki$ $[psi]$.  
    - $k_R$: permeabilidad de referencia.  
    - $h$: espesor del bloque $[ft]$.  
    - $q_R$: caudal de referencia.  
    - $B$: factor volumétrico.  
    - $\mu$: viscosidad $[cp]$.  

    **Índices:**
    - $K = I$: inner block (fractura).  
    - $K = O$: outer block (matriz).  
    - $i = 1,\dots,n$: índice del bloque/fractura.  

    **Concepto:**  
    La presión se adimensionaliza para poder comparar bloques con distintas propiedades 
    usando la misma escala de referencia.
    """)

    # === Distancias adimensionales ===
    st.markdown("**Distancias adimensionales**")
    st.latex(r"""
    x_{KiD} = \frac{x_{Ki}}{x_{FR}}, \quad 
    y_{KiD} = \frac{y_{Ki}}{y_{el}}, \quad 
    z_{KiD} = \frac{z_{Ki}}{h_{mKi}/2}
    """)
    st.markdown(r"""
    **Definiciones:**
    - $x_{Ki}, y_{Ki}, z_{Ki}$: distancias reales $[ft]$.  
    - $x_{FR}$: longitud característica de fractura $[ft]$.  
    - $y_{el}$: ancho de celda $[ft]$.  
    - $h_{mKi}$: espesor de bloque matriz $[ft]$.  

    **Índices:**  
    - $i$: bloque o fractura.  
    - $K$: dominio (I u O).
    """)

    st.latex(r"w_{FiD} = \frac{w_{Fi}}{x_{FR}}")
    st.markdown(r"""
    - $w_{FiD}$: ancho adimensional de la fractura.  
    - Código: `params['w_f']` / `params['xe']`.  
    """)

    # === Tiempo adimensional ===
    st.markdown("**Tiempo adimensional**")
    st.latex(r"t_{KiD} = \frac{\eta_{Ki}}{x_{FR}^2} \, t")
    st.markdown(r"""
    - $t_{KiD}$: tiempo adimensional.  
    - $t_{KiD}$: tiempo adimensional.  
    - $ \eta_{Ki}$: difusividad hidráulica del bloque.  
    - $x_{FR}$: longitud característica de fractura.  
    - $t$: tiempo real.  

    **Concepto:**  
    Esta transformación permite que la evolución temporal de presión se 
    represente en curvas únicas (type curves).
    """)

    # === Conexión con el código ===
    if params is not None:
        st.markdown("**Ejemplo con inputs actuales:**")
        h = params["h"]
        LxI = params["LxI"]
        xe = params["xe"]
        st.markdown(f"- h = {h} ft → espesor")
        st.markdown(f"- LxI = {LxI} ft → longitud inner block")
        st.markdown(f"- 2xe = {xe} ft → ancho outer block")
