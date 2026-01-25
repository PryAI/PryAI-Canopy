# src/external_model.py

import re
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from typing import Dict, Any, Tuple

def _extract_dependent_variable(equation: str) -> Tuple[str, bool]:
    if "=" not in equation: raise ValueError("A equação deve conter um sinal de igual '='.")
    eq_left = equation.split("=")[0].strip()
    if eq_left.lower().startswith("ln(") and eq_left.endswith(")"):
        var_name = eq_left[3:-1].strip()
        return var_name, True
    else:
        return eq_left.strip(), False

def fit_regression_from_formula(df: pd.DataFrame, equation: str, alias_map: Dict[str, str]) -> Dict[str, Any]:
    """
    Ajuste OLS Blindado (PryAI Shielded).
    Filtra erros físicos (negativos) e estatísticos (outliers extremos) automaticamente.
    """
    
    # 1. Validação Y
    try:
        y_var_sym, is_log_y = _extract_dependent_variable(equation)
    except ValueError as e: return {"error": str(e)}

    y_col_real = alias_map.get(y_var_sym)
    if not y_col_real: return {"error": f"Variável '{y_var_sym}' não encontrada nos apelidos."}
    if y_col_real not in df.columns: return {"error": f"Coluna '{y_col_real}' inexistente."}
    
    # 2. Variáveis X
    rhs_equation = equation.split("=")[1]
    potential_vars = set(re.findall(r"[a-zA-Z_]\w*", rhs_equation))
    math_reserved = {"ln", "log", "exp", "sqrt", "pow", "pi", "e", "sin", "cos", "tan"}
    x_vars_sym = [v for v in potential_vars if v not in math_reserved and not v.startswith("b")]
    
    # 3. Preparação e BLINDAGEM de Dados
    df_filtered = df.copy()
    
    try:
        # === INÍCIO DA BLINDAGEM PryAI ===
        
        # Lista de colunas críticas (Y e Xs)
        cols_to_check = [y_col_real]
        for sym in x_vars_sym:
            real = alias_map.get(sym)
            if real and real in df_filtered.columns:
                cols_to_check.append(real)
        
        # A. Limpeza Física e Numérica
        for col in cols_to_check:
            # Garante numérico (caso algo tenha passado pelo parser)
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')
            
            # FILTRO FÍSICO: Remove valores <= 0
            # Motivo: Em florestal, DAP, HT e Vol não podem ser negativos ou zero.
            # Além disso, log(0) ou log(-1) quebra o script.
            mask_invalid = df_filtered[col] <= 0
            if mask_invalid.any():
                df_filtered.loc[mask_invalid, col] = np.nan

        # Remove linhas com NaN gerados acima
        df_filtered = df_filtered.dropna(subset=cols_to_check)

        # B. Filtro Estatístico (IQR - Caça Alienígenas)
        # Remove outliers extremos (como DAP=500 quando a média é 15)
        # Usa 3x IQR, que é um critério bem conservador (só remove erros grotescos)
        for col in cols_to_check:
            if len(df_filtered) < 5: continue # Não filtra se tiver poucos dados

            Q1 = df_filtered[col].quantile(0.25)
            Q3 = df_filtered[col].quantile(0.75)
            IQR = Q3 - Q1
            
            if IQR > 0:
                lower_bound = Q1 - 3.0 * IQR
                upper_bound = Q3 + 3.0 * IQR
                
                df_filtered = df_filtered[
                    (df_filtered[col] >= lower_bound) & 
                    (df_filtered[col] <= upper_bound)
                ]
        
        # === FIM DA BLINDAGEM ===

        if len(df_filtered) < 3:
            return {"error": "Dados insuficientes após remoção de erros e outliers."}

        # Preparação Y
        if is_log_y:
            y_data = np.log(df_filtered[y_col_real])
        else:
            y_data = df_filtered[y_col_real]
            
        # Preparação X
        local_env = {}
        for sym in x_vars_sym:
            real_col = alias_map.get(sym)
            # Verifica log interno em X (ex: 1/DAP ou ln(DAP))
            # Como já filtramos <= 0 na blindagem, aqui deve estar seguro
            local_env[sym] = df_filtered[real_col].values

        # Avalia Termos da Equação
        terms = rhs_equation.replace("-", "+-").split("+")
        X_dict = {}
        
        for term in terms:
            term = term.strip()
            if not term: continue
            
            term_clean = re.sub(r"^[+-]?\s*[\d\.]+\s*\*", "", term) 
            term_clean = re.sub(r"^[+-]?\s*b\d+\s*\*", "", term_clean)
            
            if not term_clean or term_clean.lower() in ["b0", "const", "intercept"]:
                X_dict["const"] = 1.0
                continue
                
            safe_locals = local_env.copy()
            safe_locals.update({"ln": np.log, "log": np.log, "exp": np.exp, "sqrt": np.sqrt})
            
            try:
                val = eval(term_clean, {"__builtins__": {}}, safe_locals)
                X_dict[term_clean] = val
            except Exception as e:
                return {"error": f"Erro matemático no termo '{term_clean}': {e}"}

        X_df = pd.DataFrame(X_dict, index=df_filtered.index)
        
        # Garante alinhamento final (caso o eval tenha gerado NaNs/Infs)
        X_df = X_df.replace([np.inf, -np.inf], np.nan).dropna()
        
        common_idx = X_df.index.intersection(y_data.index)
        Y_final = y_data.loc[common_idx]
        X_final = X_df.loc[common_idx]
        
        if len(Y_final) < 3:
            return {"error": "Número insuficiente de dados válidos (< 3) para regressão."}

        # 4. Ajuste OLS
        model = sm.OLS(Y_final, X_final)
        results = model.fit()

    except Exception as e:
        return {"error": f"Erro crítico no processamento: {str(e)}"}

    # 5. Métricas e Retorno
    r2_adj = results.rsquared_adj
    rmse = np.sqrt(results.mse_resid)
    
    if is_log_y:
        fc = float(np.exp(results.mse_resid / 2.0))
    else:
        fc = None

    aic = results.aic
    bic = results.bic
    dw_stat = durbin_watson(results.resid)
    
    # Syx%
    y_mean_real = df_filtered.loc[common_idx, y_col_real].mean()
    
    if is_log_y:
        y_pred_log = results.fittedvalues
        y_pred_real = np.exp(y_pred_log) * fc
        y_obs_real = df_filtered.loc[common_idx, y_col_real]
        rmse_real = np.sqrt(((y_obs_real - y_pred_real) ** 2).mean())
        syx_pct = (rmse_real / y_mean_real) * 100 if y_mean_real != 0 else 0
    else:
        syx_pct = (rmse / y_mean_real) * 100 if y_mean_real != 0 else 0

    # Montagem da String da Equação
    eq_parts = []
    for k, v in results.params.items():
        if k == "const": eq_parts.append(f"{v:.4f}")
        else:
            signal = "+" if v >= 0 else ""
            eq_parts.append(f"{signal} {v:.4f}*({k})")
            
    eq_final_str = f"{'ln(' if is_log_y else ''}{y_var_sym}{')' if is_log_y else ''} = " + " ".join(eq_parts)

    return {
        "success": True,
        "equation_original": equation,
        "equation_fitted": eq_final_str,
        "r2_adj": r2_adj,
        "rmse": rmse,
        "fc_meyer": fc,
        "syx_pct": syx_pct,
        "aic": aic,
        "bic": bic,
        "durbin_watson": dw_stat,
        "n_obs": int(results.nobs),
        "coefs": results.params.to_dict(),
        "is_log": is_log_y,
        "y_col_real": y_col_real,
        "data_points": {
            "y_real": Y_final.tolist(),
            "y_pred": results.fittedvalues.tolist()
        }
    }