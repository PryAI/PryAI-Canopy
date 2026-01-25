# src/plots.py
import altair as alt
import pandas as pd
import numpy as np

def gerar_graficos_interativos(results, df_original, alias_map):
    """
    Gera gráficos interativos com Altair.
    Tooltips formatados e linha zero destacada.
    """
    
    y_real = results['data_points']['y_real']
    y_pred = results['data_points']['y_pred']
    
    df_plot = pd.DataFrame({
        'Observado': y_real,
        'Previsto': y_pred,
        'Residuo_Pct': ((np.array(y_pred) - np.array(y_real)) / np.array(y_real)) * 100
    })
    
    # Adiciona metadados
    cols_info = df_original.columns[:3].tolist()
    for col in cols_info:
        df_plot[col] = df_original[col].values[:len(df_plot)]

    # Eixo X
    x_col_name = None
    x_alias = "X"
    for alias, col in alias_map.items():
        if 'dap' in col.lower() or 'dbh' in col.lower() or 'diam' in col.lower():
            x_col_name = col
            x_alias = alias
            break
            
    if x_col_name:
        df_plot[x_alias] = df_original[x_col_name].values[:len(df_plot)]

    # Tooltips
    tooltips_padrao = [alt.Tooltip(c) for c in cols_info]
    tooltips_obs_prev = tooltips_padrao + [
        alt.Tooltip('Observado', format='.4f', title='Real'),
        alt.Tooltip('Previsto', format='.4f', title='Estimado'),
        alt.Tooltip('Residuo_Pct', format='.2f', title='Erro %')
    ]
    if x_col_name:
        tooltips_obs_prev.append(alt.Tooltip(x_alias, format='.2f'))

    # GRÁFICO 1: PRECISÃO
    line_min = min(min(y_real), min(y_pred))
    line_max = max(max(y_real), max(y_pred))
    line_data = pd.DataFrame({'x': [line_min, line_max], 'y': [line_min, line_max]})
    
    line_1_1 = alt.Chart(line_data).mark_line(color='#e74c3c', strokeDash=[5,5]).encode(x='x', y='y')
    
    scatter_obs = alt.Chart(df_plot).mark_circle(size=60, color='#27AE60', opacity=0.7).encode(
        x=alt.X('Observado', title='Valores Reais'),
        y=alt.Y('Previsto', title='Valores Estimados'),
        tooltip=tooltips_obs_prev
    ).interactive()

    chart1 = (scatter_obs + line_1_1).properties(title="Aderência (Obs vs Prev)")

    # GRÁFICO 2: RESÍDUOS
    scatter_res = alt.Chart(df_plot).mark_circle(size=60, color='#E67E22').encode(
        x=alt.X('Previsto', title='Valor Estimado'),
        y=alt.Y('Residuo_Pct', title='Erro Relativo (%)'),
        tooltip=tooltips_obs_prev
    )
    
    # AJUSTE 1: Linha zero destacada em VERMELHO
    rule = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='red', opacity=1, size=2).encode(y='y')
    
    chart2 = (scatter_res + rule).properties(title="Distribuição de Resíduos").interactive()

    # GRÁFICO 3: TENDÊNCIA
    if x_col_name:
        points_real = alt.Chart(df_plot).mark_circle(color='gray', opacity=0.3).encode(
            x=alt.X(x_alias, title=f'{x_alias}'),
            y=alt.Y('Observado', title='Biomassa/Volume'),
            tooltip=tooltips_obs_prev
        )
        
        line_trend = alt.Chart(df_plot).mark_line(color='#2E8B57', size=4).transform_loess(
            x_alias, 'Previsto', bandwidth=0.5
        ).encode(
            x=x_alias, y='Previsto',
            tooltip=tooltips_obs_prev
        )
        
        chart3 = (points_real + line_trend).properties(title=f"Curva de Crescimento ({x_alias})").interactive()
        
        return (chart1 | chart2 | chart3)
    else:
        return (chart1 | chart2)