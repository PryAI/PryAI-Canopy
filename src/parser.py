# src/parser.py

import pandas as pd
import numpy as np
from collections import Counter

def _make_unique_columns(cols):
    """Garante nomes únicos para as colunas."""
    seen = Counter()
    unique = []
    for c in cols:
        base = str(c).strip()
        seen[base] += 1
        if seen[base] == 1:
            unique.append(base)
        else:
            unique.append(f"{base}_{seen[base]}")
    return unique

def _looks_like_good_header(cols):
    """Decide se a primeira linha parece um cabeçalho válido."""
    cols_str = [str(c).strip() for c in cols]
    
    # Se tudo for "Unnamed" ou vazio, é ruim
    if all(c.lower().startswith("unnamed") for c in cols_str): return False
    
    # Se mais de 50% for número, provavelmente é DADO, não cabeçalho
    def is_numeric_like(x):
        try:
            float(str(x).replace(",", "."))
            return True
        except:
            return False

    numeric_count = sum(is_numeric_like(c) for c in cols_str)
    if numeric_count > (len(cols_str) * 0.5): return False

    # Pelo menos uma letra para ser cabeçalho
    if not any(any(ch.isalpha() for ch in c) for c in cols_str): return False

    return True

def clean_and_convert_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    BLINDAGEM NÍVEL 1: Tipagem Rigorosa
    1. Mata colunas de data (que atrapalham regressão).
    2. Resolve conflito Ponto vs Vírgula (padrão BR vs US).
    3. Converte texto inválido ("Vinte", "Erro") para NaN.
    """
    df_clean = df.copy()
    
    for col in df_clean.columns:
        # --- TRAVA 1: DATAS ---
        # Se o pandas detectou data (ex: 2026-05-15), força NaN.
        # Datas viram números gigantescos se convertidas, destruindo a regressão.
        if pd.api.types.is_datetime64_any_dtype(df_clean[col]):
            df_clean[col] = np.nan
            continue

        # Se já for numérico, apenas limpa infinitos
        if pd.api.types.is_numeric_dtype(df_clean[col]):
            df_clean[col] = df_clean[col].replace([np.inf, -np.inf], np.nan)
            continue
            
        # --- TRAVA 2: STRINGS & DECIMAIS ---
        if df_clean[col].dtype == 'object':
            # Remove espaços extras
            df_clean[col] = df_clean[col].astype(str).str.strip()
            
            # Detecção inteligente de Vírgula vs Ponto
            sample = df_clean[col].dropna().tolist()
            text_blob = "".join(sample)
            
            # Se tem vírgula e parece ser decimal (heurística simples)
            if ',' in text_blob:
                # Remove ponto de milhar (1.000,00 -> 1000,00) e troca vírgula por ponto
                df_clean[col] = df_clean[col].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
            
            # --- TRAVA 3: COERÇÃO ---
            # Tenta converter TUDO para número. O que falhar (ex: "Vinte") vira NaN
            converted = pd.to_numeric(df_clean[col], errors='coerce')
            
            # Validação: Só aceita a conversão se a maioria da coluna for válida
            # Isso evita transformar uma coluna de Observações inteira em NaN
            valid_ratio = converted.notna().sum() / len(df_clean) if len(df_clean) > 0 else 0
            
            # Se mais de 40% da coluna for número válido, assumimos que É numérica
            if valid_ratio > 0.4:
                df_clean[col] = converted
            else:
                # Se falhou muito, mantém como texto original (provavelmente é ID ou Obs)
                pass
                
    return df_clean

def initial_preprocess(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline de Limpeza Total.
    """
    # 1. Ajuste de Cabeçalho (Header)
    if _looks_like_good_header(df_raw.columns):
        df = df_raw.copy()
    else:
        if df_raw.shape[0] == 0: return df_raw.copy()
        df = df_raw.iloc[1:].copy()
        df.columns = df_raw.iloc[0].tolist()

    # 2. Garante nomes únicos
    df.columns = _make_unique_columns(df.columns)
    
    # 3. Remove linhas/colunas TOTALMENTE vazias
    df = df.dropna(axis=1, how="all")
    df = df.dropna(how="all")

    # 4. Limpa espaços em branco dentro das células de texto
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # 5. O PULO DO GATO: Limpeza Numérica Profunda
    df = clean_and_convert_data(df)

    # 6. Reset final
    df = df.reset_index(drop=True)

    return df