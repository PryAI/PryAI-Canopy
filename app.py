import streamlit as st
import pandas as pd
import numpy as np
import re

# Importando módulos do Backend
from src.parser import initial_preprocess
from src.config import APP_NAME, APP_VERSION
# Importamos a função de ajuste OLS
from src.external_model import fit_regression_from_formula
# Importamos a geração de PDF
from src.report_export import gerar_pdf_relatorio
# Importamos os gráficos interativos
from src.plots import gerar_graficos_interativos

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title=f"{APP_NAME}",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { background-color: #2E8B57; color: white; border-radius: 5px; }
    div[data-testid="stMetricValue"] { color: #2E8B57; }
    .stTextInput>div>div>input { font-family: 'Courier New', monospace; }
    
    /* Estilo para tabelas de erro */
    .error-row { background-color: #ffe6e6; }
    .warning-row { background-color: #fff9e6; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. INICIALIZAÇÃO DO ESTADO
# ==============================================================================
def init_session_state():
    if 'df_raw' not in st.session_state: st.session_state['df_raw'] = None
    if 'df_filtered' not in st.session_state: st.session_state['df_filtered'] = None
    if 'file_name' not in st.session_state: st.session_state['file_name'] = ""
    if 'saved_models' not in st.session_state: st.session_state['saved_models'] = []
    if 'last_results' not in st.session_state: st.session_state['last_results'] = None
    if 'chart_key' not in st.session_state: st.session_state['chart_key'] = 0
    if 'audit_report' not in st.session_state: st.session_state['audit_report'] = None
    
    # Garante que a chave do input exista para evitar o erro de widget
    if 'model_name_input' not in st.session_state: st.session_state['model_name_input'] = ""
    
    # NOVA BIBLIOTECA DE EQUAÇÕES (Já vem com algumas clássicas)
    if 'equation_library' not in st.session_state:
        st.session_state['equation_library'] = {
            "Linear Simples": "Y = b0 + b1*DAP",
            "Linear Múltiplo": "Y = b0 + b1*DAP + b2*HT",
            "Schumacher-Hall (Log)": "ln(Y) = b0 + b1*ln(DAP) + b2*ln(HT)",
            "Spurr (Potência)": "Y = b0 + b1 * (DAP**2 * HT)",
            "Hipsométrica (Log-Lin)": "ln(HT) = b0 + b1 * (1/DAP)",
            "Polinomial Quadrática": "Y = b0 + b1*DAP + b2*(DAP**2)"
        }
    if 'selected_eq_name' not in st.session_state: st.session_state['selected_eq_name'] = ""

init_session_state()

def reset_zoom():
    st.session_state['chart_key'] += 1

# ==============================================================================
# 3. FUNÇÕES AUXILIARES
# ==============================================================================
def auditar_qualidade_dados(df):
    """
    Analisa o DataFrame e identifica problemas potenciais para avisar o usuário.
    Não apaga nada, apenas reporta.
    """
    report = {
        "critical": [], # Erros que impedem cálculo (Texto em nº, Zeros em Log)
        "warning": [],  # Suspeitas (Outliers extremos)
        "clean": True
    }
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        # 1. Checar Valores Nulos (que podem ter sido textos como "Vinte" removidos pelo parser)
        n_nans = df[col].isna().sum()
        if n_nans > 0:
            report["critical"].append(f"Coluna **'{col}'**: Possui {n_nans} linhas vazias ou com texto inválido (ex: 'Vinte', Datas).")

        # 2. Checar Valores <= 0 (Fisicamente impossível para DAP/Altura)
        # Ignoramos NaNs aqui para não duplicar aviso
        n_zeros = (df[col] <= 0).sum()
        if n_zeros > 0:
            report["critical"].append(f"Coluna **'{col}'**: Possui {n_zeros} valores negativos ou zero (impossível para medidas físicas).")
            
        # 3. Checar Outliers Extremos (Alienígenas)
        # Usamos IQR x 3 (Critério bem frouxo, só pega absurdo mesmo)
        valid_data = df[col].dropna()
        if len(valid_data) > 10:
            Q1 = valid_data.quantile(0.25)
            Q3 = valid_data.quantile(0.75)
            IQR = Q3 - Q1
            if IQR > 0:
                upper_limit = Q3 + 3 * IQR
                outliers = valid_data[valid_data > upper_limit]
                if not outliers.empty:
                    max_val = outliers.max()
                    report["warning"].append(f"Coluna **'{col}'**: Valor suspeito detectado ({max_val:.2f}). Muito acima do padrão.")

    if report["critical"] or report["warning"]:
        report["clean"] = False
        
    return report

@st.cache_data
def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'): df = pd.read_csv(uploaded_file)
        else: df = pd.read_excel(uploaded_file)
        # O preprocessamento já limpa textos ruins transformando em NaN
        return initial_preprocess(df)
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
        return None

def extract_coefficients_from_formula(equation):
    return sorted(list(set(re.findall(r"\b(b\d+)\b", equation))))

def calculate_manual_prediction(df, equation, alias_map, coef_values):
    local_env = {}
    for alias, col_real in alias_map.items():
        if col_real in df.columns:
            local_env[alias] = df[col_real].values
        else:
            return None, f"Coluna '{col_real}' não encontrada."

    local_env.update(coef_values)
    safe_math = {"ln": np.log, "log": np.log, "exp": np.exp, "sqrt": np.sqrt, "np": np}
    local_env.update(safe_math)

    try:
        rhs = equation.split("=")[1].strip()
        y_pred = eval(rhs, {"__builtins__": {}}, local_env)
        
        lhs = equation.split("=")[0].strip()
        is_log = "ln(" in lhs or "log(" in lhs
        if is_log:
            y_pred = np.exp(y_pred)
        
        return y_pred, None
    except Exception as e:
        return None, str(e)

# ==============================================================================
# 4. SIDEBAR
# ==============================================================================
with st.sidebar:
    st.title("🌲 PryAI Canopy")
    st.caption(f"v{APP_VERSION}")
    st.divider()

    uploaded_file = st.file_uploader("Importar Dados", type=['csv', 'xlsx', 'xls'])
    if uploaded_file:
        if st.session_state['file_name'] != uploaded_file.name:
            df_loaded = load_data(uploaded_file)
            if df_loaded is not None:
                st.session_state['df_raw'] = df_loaded
                st.session_state['df_filtered'] = df_loaded.copy()
                st.session_state['file_name'] = uploaded_file.name
                st.session_state['last_results'] = None 
                
                # RODAR AUDITORIA IMEDIATAMENTE AO CARREGAR
                st.session_state['audit_report'] = auditar_qualidade_dados(df_loaded)
                
                st.success("Carregado!")
                st.rerun()

    if st.session_state['df_raw'] is not None:
        st.divider()
        st.subheader("🔍 Filtros em Cascata")
        df_funnel = st.session_state['df_raw'].copy()
        cols_to_filter = st.multiselect("Colunas de Filtro:", df_funnel.columns.tolist())
        
        for col in cols_to_filter:
            available = sorted(df_funnel[col].astype(str).unique())
            sel = st.multiselect(f"Valores de '{col}':", available)
            if sel: df_funnel = df_funnel[df_funnel[col].astype(str).isin(sel)]
            
        st.session_state['df_filtered'] = df_funnel
        rows = len(df_funnel)
        st.metric("Linhas", rows)

# ==============================================================================
# 5. ÁREA PRINCIPAL
# ==============================================================================
if st.session_state['df_raw'] is not None:
    
    # --- NOVO: PAINEL DE INTEGRIDADE DE DADOS ---
    # Mostra avisos ANTES das abas para garantir que o usuário veja
    report = st.session_state.get('audit_report')
    if report and not report['clean']:
        with st.expander("⚠️ **Relatório de Integridade da Planilha (Verifique Antes de Prosseguir)**", expanded=True):
            st.markdown("O **PryAI** detectou inconsistências que podem afetar a precisão do seu modelo.")
            
            # Mostra Erros Críticos (Vermelho)
            if report['critical']:
                st.error("⛔ **Erros Críticos detectados (Corrija na planilha original):**")
                for msg in report['critical']:
                    st.markdown(f"- {msg}")
            
            # Mostra Avisos (Amarelo)
            if report['warning']:
                st.warning("⚠️ **Alertas de Atenção (Valores suspeitos/Outliers):**")
                for msg in report['warning']:
                    st.markdown(f"- {msg}")
            
            st.info("💡 **Nota:** O sistema tentará blindar o modelo ignorando essas linhas automaticamente se você prosseguir, mas recomenda-se corrigir a fonte.")
    
    # --------------------------------------------

    tab1, tab2, tab3 = st.tabs(["📊 Dados", "📐 Modelagem (Regressão)", "🧪 ANOVA"])
    
    # --- ABA 1 ---
    with tab1:
        st.dataframe(st.session_state['df_filtered'].head(50), use_container_width=True)

    # --- ABA 2 ---
    with tab2:
        df_work = st.session_state['df_filtered']
        cols = df_work.columns.tolist()

        st.header("Construtor de Modelos")
        
        # 1. Variáveis
        with st.container():
            c1, c2 = st.columns([1, 2])
            with c1:
                y_col = st.selectbox("Selecione Y (Alvo):", cols)
                y_alias_input = st.text_input("Apelido para Y:", value="Y").strip()
                y_alias = y_alias_input if y_alias_input else "Y"
            
            with c2:
                x_cols = st.multiselect("Selecione Xs:", [c for c in cols if c != y_col])
                alias_map = {y_alias: y_col}
                if x_cols:
                    cols_alias = st.columns(len(x_cols))
                    for i, x_col in enumerate(x_cols):
                        def_al = "DAP" if "dap" in x_col.lower() else ("HT" if "h" in x_col.lower() else f"X{i+1}")
                        with cols_alias[i]:
                            alias_input = st.text_input(f"Apelido '{x_col}':", value=def_al, key=f"alias_{x_col}").strip()
                            final_alias = alias_input if alias_input else def_al
                            alias_map[final_alias] = x_col

        st.divider()

        # 2. Equação e Método
        
        # --- NOVIDADE: BIBLIOTECA DE EQUAÇÕES ---
        col_lib, col_save = st.columns([3, 1])
        with col_lib:
            eq_options = ["Personalizada..."] + list(st.session_state['equation_library'].keys())
            selected_eq = st.selectbox("📂 Carregar Equação da Biblioteca:", eq_options)
        
        # Lógica para preencher o campo se selecionar da biblioteca
        default_eq = ""
        if selected_eq != "Personalizada...":
            default_eq = st.session_state['equation_library'][selected_eq]
            # Atualiza o nome do modelo na sessão
            st.session_state['model_name_input'] = selected_eq 

        # CORREÇÃO AQUI: Removemos 'value=' pois 'key=' já faz o binding com st.session_state
        model_name = st.text_input("Nome do Modelo:", key="model_name_input", placeholder="Ex: Schumacher-Hall Sítio A")
        
        # Se tiver selecionado algo, usa como value, senão deixa o usuário digitar
        if selected_eq != "Personalizada...":
            equation_input = st.text_input("Equação:", value=default_eq)
        else:
            equation_input = st.text_input("Equação:", placeholder=f"Ex: ln({y_alias}) = b0 + b1*ln(DAP) + b2*ln(HT)")

        # Botão para SALVAR na biblioteca
        with col_save:
            st.write("") # Espaço para alinhar
            st.write("") 
            if st.button("💾 Salvar na Bibl."):
                if model_name and equation_input:
                    st.session_state['equation_library'][model_name] = equation_input
                    st.success(f"Salvo!")
                    st.rerun() # Atualiza a lista
                else:
                    st.warning("Nome e Equação necessários.")

        # --- SINTAXE DETALHADA ---
        with st.expander("📚 Guia de Sintaxe & Exemplos"):
            st.markdown("""
            **Operadores Matemáticos:**
            | Operação | Símbolo | Exemplo |
            | :--- | :---: | :--- |
            | Adição | `+` | `b0 + b1` |
            | Subtração | `-` | `Y - Y_pred` |
            | Multiplicação | `*` | `b1 * DAP` |
            | Divisão | `/` | `1 / DAP` |
            | Potência | `**` | `DAP ** 2` (DAP ao quadrado) |

            **Funções:**
            * `ln(x)`: Logaritmo Natural (Base e)
            * `log(x)`: Logaritmo Natural (Alias para ln)
            * `exp(x)`: Exponencial ($e^x$)
            * `sqrt(x)`: Raiz Quadrada

            **Exemplos para Copiar:**
            * **Schumacher-Hall:** `ln(Y) = b0 + b1*ln(DAP) + b2*ln(HT)`
            * **Spurr (Variável Combinada):** `Y = b0 + b1 * (DAP**2 * HT)`
            * **Polinomial:** `Y = b0 + b1*DAP + b2*(DAP**2)`
            * **Hipsométrica:** `ln(HT) = b0 + b1 * (1/DAP)`
            """)

        method = st.radio("Método:", ["🤖 Automático (OLS)", "✍️ Manual"], horizontal=True)

        # Botão Calcular
        if st.button("🚀 Calcular Modelo", type="primary"):
            if method.startswith("🤖"):
                if not equation_input: st.warning("Digite a equação.")
                else:
                    with st.spinner("Processando..."):
                        res = fit_regression_from_formula(df_work, equation_input, alias_map)
                        if "error" in res: st.error(res["error"])
                        else:
                            res['method'] = 'OLS'
                            res['name'] = model_name or "Sem Nome"
                            res['is_log'] = "ln(" in equation_input.split("=")[0]
                            res['alias_map_used'] = alias_map
                            res['y_col_name'] = y_col
                            st.session_state['last_results'] = res
                            st.session_state['chart_key'] += 1
            else:
                coefs = extract_coefficients_from_formula(equation_input)
                if not coefs: st.warning("Sem coeficientes (b0, b1...).")
                else:
                    st.session_state['manual_mode_trigger'] = True 
                    st.warning("Para o modo manual completo, use a interface de input abaixo.")

        # 3. Resultados
        results = st.session_state['last_results']
        
        if results:
            st.divider()
            st.markdown(f"### 📊 Resultados: {results['name']}")
            st.code(results['equation_fitted'], language="python")

            # Tabela
            r2 = results.get('r2_adj')
            syx = results.get('syx_pct')
            rmse = results.get('rmse')
            meyer = results.get('fc_meyer')
            aic = results.get('aic')
            dw = results.get('durbin_watson')
            is_log_model = results.get('is_log', False)

            table_data = []
            table_data.append({"Métrica": "R² Ajustado", "Valor": f"{r2:.4f}" if r2 else "N/A", "Referência Técnica": "Quanto mais próximo de 1.0, melhor."})
            table_data.append({"Métrica": "Syx %", "Valor": f"{syx:.2f}%" if syx else "N/A", "Referência Técnica": "Erro Relativo (<15% é bom)."})
            
            rmse_label = "RMSE (Escala Log)" if is_log_model else "RMSE"
            rmse_ref = "Erro padrão na escala log." if is_log_model else f"Erro médio na unidade de Y ({results.get('y_col_real','Y')})."
            table_data.append({"Métrica": rmse_label, "Valor": f"{rmse:.4f}" if rmse else "N/A", "Referência Técnica": rmse_ref})

            if meyer: table_data.append({"Métrica": "Fator de Meyer", "Valor": f"{meyer:.6f}", "Referência Técnica": "Correção viés log."})
            if aic: table_data.append({"Métrica": "AIC", "Valor": f"{int(aic)}", "Referência Técnica": "Menor valor = Melhor ajuste."})
            if dw: table_data.append({"Métrica": "Durbin-Watson", "Valor": f"{dw:.2f}", "Referência Técnica": "Ideal: 1.5 a 2.5."})

            st.table(pd.DataFrame(table_data))

            # Gráficos
            st.subheader("📈 Diagnóstico do Modelo")
            
            col_info, col_reset = st.columns([4, 1])
            with col_info:
                st.info("💡 Passe o mouse para ver detalhes. Se perder o zoom, clique em 'Restaurar Visão'.")
            with col_reset:
                st.button("🔄 Restaurar Visão", on_click=reset_zoom)

            chart = gerar_graficos_interativos(results, df_work, results['alias_map_used'])
            st.altair_chart(chart, use_container_width=True, key=f"chart_{st.session_state['chart_key']}")

            # Botões
            c_btn1, c_btn2 = st.columns([1, 4])
            with c_btn1:
                if st.button("💾 Salvar Modelo"):
                    st.session_state['saved_models'].append(results)
                    st.success("Salvo!")
            with c_btn2:
                if st.button("📄 Gerar Relatório PDF"):
                    try:
                        path = gerar_pdf_relatorio(results, plot_paths=[])
                        st.success(f"PDF Gerado: {path}")
                        with open(path, "rb") as f: st.download_button("Baixar PDF", f, file_name=f"Relatorio_{results['name']}.pdf")
                    except Exception as e: st.error(f"Erro PDF: {e}")

        if st.session_state['saved_models']:
            st.divider()
            st.subheader("📚 Modelos na Memória")
            for mod in st.session_state['saved_models']:
                st.write(f"- **{mod['name']}**: R² {mod.get('r2_adj',0):.4f}")

    # --- ABA 3 ---
    with tab3:
        st.info("🚧 Módulo ANOVA/DBC está em construção.")

else:
    st.title(f"Bem-vindo ao {APP_NAME}")
    st.info("Carregue um arquivo para começar.")