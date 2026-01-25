# src/report_export.py
from fpdf import FPDF
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        # Cabeçalho VERDE (Mantido)
        self.set_fill_color(46, 139, 87) 
        self.rect(0, 0, 210, 35, 'F')
        
        # Título Branco
        self.set_font('Arial', 'B', 22)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 10)
        self.cell(0, 10, 'PryAI Canopy', 0, 1, 'L')
        
        # Subtítulo Branco
        self.set_font('Arial', '', 11)
        self.set_xy(10, 20)
        self.cell(0, 10, 'Relatório Técnico de Modelagem Biométrica', 0, 1, 'L')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")} | Página ' + str(self.page_no()), 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(46, 139, 87) # Verde nos títulos
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_draw_color(46, 139, 87)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def data_row(self, label, value, fill=False):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0, 0, 0) # PRETO NO RÓTULO
        self.set_fill_color(240, 240, 240)
        self.cell(50, 8, label, 1, 0, 'L', fill)
        
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0) # PRETO NO VALOR
        self.cell(0, 8, str(value), 1, 1, 'L', False)

def gerar_plots_estaticos_para_pdf(results):
    temp_files = []
    y_real = np.array(results['data_points']['y_real'])
    y_pred = np.array(results['data_points']['y_pred'])
    
    plt.style.use('default')
    
    # Plot 1: Aderência
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.scatter(y_real, y_pred, alpha=0.5, color='#2E8B57', edgecolors='grey')
    min_v, max_v = min(y_real.min(), y_pred.min()), max(y_real.max(), y_pred.max())
    ax1.plot([min_v, max_v], [min_v, max_v], 'r--', label='1:1 Ideal')
    ax1.set_title("Aderência (Real vs Estimado)", fontweight='bold', color='black') # Título Preto
    ax1.set_xlabel("Observado"); ax1.set_ylabel("Estimado")
    ax1.grid(True, linestyle=':', alpha=0.5)
    
    f1 = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig1.savefig(f1.name, dpi=150, bbox_inches='tight')
    temp_files.append(f1.name)
    plt.close(fig1)

    # Plot 2: Resíduos
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    resid = ((y_pred - y_real) / y_real) * 100
    ax2.scatter(y_pred, resid, alpha=0.5, color='#E67E22', edgecolors='grey')
    # LINHA ZERO VERMELHA NO PDF TAMBÉM
    ax2.axhline(0, color='red', linestyle='-', linewidth=1.5)
    ax2.set_title("Distribuição de Resíduos (%)", fontweight='bold', color='black') # Título Preto
    ax2.set_xlabel("Estimado"); ax2.set_ylabel("Erro %")
    ax2.set_ylim(-50, 50)
    ax2.grid(True, linestyle=':', alpha=0.5)

    f2 = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    fig2.savefig(f2.name, dpi=150, bbox_inches='tight')
    temp_files.append(f2.name)
    plt.close(fig2)

    return temp_files

def gerar_pdf_relatorio(results, plot_paths=[]):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 1. Resumo
    pdf.section_title("Resumo do Modelo")
    pdf.data_row("Nome do Modelo:", results.get('name', 'Sem Nome'), True)
    pdf.data_row("Variável Alvo (Y):", results.get('y_col_real', 'Y'), True)
    pdf.data_row("Total de Árvores:", f"{len(results['data_points']['y_real'])} obs", True)
    pdf.ln(5)

    # 2. Equação
    pdf.section_title("Equação Ajustada")
    pdf.set_font('Courier', '', 11)
    pdf.set_text_color(0, 0, 0) # PRETO NA EQUAÇÃO
    pdf.set_fill_color(250, 250, 250)
    pdf.multi_cell(0, 12, results['equation_fitted'], border=1, align='C', fill=True)
    pdf.ln(8)

    # 3. Métricas (Tabela Profissional)
    pdf.section_title("Indicadores Estatísticos")
    
    # Header Tabela
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(0, 0, 0) # PRETO NO HEADER
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(40, 8, "Métrica", 1, 0, 'C', True)
    pdf.cell(30, 8, "Valor", 1, 0, 'C', True)
    pdf.cell(0, 8, "Interpretação Técnica", 1, 1, 'L', True)
    
    # Linhas
    rows = [
        ("R2 Ajustado", f"{results.get('r2_adj',0):.4f}", "Explicação da variância (0 a 1)."),
        ("Syx %", f"{results.get('syx_pct',0):.2f}%", "Erro relativo médio."),
        ("RMSE", f"{results.get('rmse',0):.4f}", "Erro padrão na escala do ajuste."),
        ("AIC", f"{int(results.get('aic',0))}", "Critério de Akaike (Menor é melhor)."),
        ("Durbin-Watson", f"{results.get('durbin_watson',0):.2f}", "Autocorrelação (Ideal: 1.5 - 2.5).")
    ]
    if results.get('fc_meyer'):
        rows.insert(3, ("Fator Meyer", f"{results.get('fc_meyer'):.6f}", "Correção para viés logarítmico."))

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(0, 0, 0) # PRETO NAS LINHAS
    for m, v, d in rows:
        pdf.cell(40, 8, m, 1, 0, 'L')
        pdf.cell(30, 8, v, 1, 0, 'C')
        pdf.cell(0, 8, d, 1, 1, 'L')
    pdf.ln(10)

    # 4. Gráficos
    pdf.section_title("Diagnóstico Visual")
    img_files = gerar_plots_estaticos_para_pdf(results)
    
    # Layout lado a lado
    y_pos = pdf.get_y()
    if len(img_files) >= 1:
        pdf.image(img_files[0], x=10, y=y_pos, w=90)
    if len(img_files) >= 2:
        pdf.image(img_files[1], x=105, y=y_pos, w=90)
    
    pdf.ln(65) # Espaço das imagens

    # Limpeza
    for f in img_files:
        try: os.remove(f)
        except: pass

    filename = f"Relatorio_{results['name'].replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename