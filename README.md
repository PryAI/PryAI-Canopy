# 🌲 PryAI Canopy

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.42-red)
![Status](https://img.shields.io/badge/Status-Production-success)
![License](https://img.shields.io/badge/License-MIT-green)

> **Ferramenta de Inteligência Computacional para Modelagem Biométrica Florestal de Alta Precisão.**

O **PryAI Canopy** não é apenas uma calculadora de regressão. É um ecossistema robusto desenvolvido para transformar dados brutos de campo — muitas vezes "sujos" e inconsistentes — em modelos matemáticos precisos e relatórios de consultoria prontos para entrega.

Diferente de softwares tradicionais que travam com erros de digitação, o Canopy implementa o **PryAI Shield™**, um motor de blindagem que detecta, isola e neutraliza inconsistências antes que elas afetem a estatística.

---

## 🚀 O Diferencial: PryAI Shield™

A verdadeira inteligência do Canopy está no que você não vê. O módulo `src/parser.py` atua como um "firewall" estatístico:

* **🛡️ Detecção Universal de Decimais:** O sistema identifica automaticamente se a planilha está no padrão brasileiro (vírgula) ou americano (ponto) e normaliza os dados.
* **🧹 Limpeza Semântica:** Textos acidentais em colunas numéricas (ex: "Vinte", "Erro") são convertidos e tratados sem travar a aplicação.
* **🚫 Proteção Matemática:** Bloqueio proativo de operações ilegais (como `ln(0)` ou números negativos em transformações logarítmicas), com avisos claros ao invés de falhas de sistema.

---

## ⚡ Funcionalidades Principais

### 1. Modelagem Flexível & Poderosa
Esqueça as listas fechadas de modelos. O **PryAI Interpreter** permite que você escreva qualquer equação linear ou não-linear.
* **Suporte Nativo:** Schumacher-Hall, Spurr, Hipsométricos, Polinomiais.
* **Sintaxe Livre:** Escreva `ln(Y) = b0 + b1*ln(DAP)` ou `Y = b0 + b1*(DAP**2)` e o motor OLS resolve.
* **Biblioteca Inteligente:** Salve suas equações favoritas na memória da sessão para uso recorrente.

### 2. Diagnóstico Visual Interativo
Gráficos que contam a história dos dados, não apenas plotam pontos.
* **Interatividade Total:** Passe o mouse para ver ID, Talhão e erro de cada árvore.
* **Análise de Resíduos:** Linha zero destacada e dispersão para identificar tendenciosidades.
* **Curvas Suaves (Loess):** Visualização clara da tendência biológica sobre os dados reais.

### 3. Métricas de Engenharia Florestal
Cálculo automático dos indicadores que realmente importam para o inventário:
* ✅ **R² Ajustado:** Explicação da variância.
* ✅ **Syx %:** O Erro Padrão da Estimativa em porcentagem (o "selo de qualidade" do modelo).
* ✅ **Fator de Meyer:** Correção automática de viés para modelos logarítmicos.
* ✅ **AIC / BIC / Durbin-Watson:** Para seleção fina de modelos e análise de autocorrelação.

### 4. Report One-Click
Gera um **Relatório Técnico em PDF** com design minimalista e profissional, contendo:
* Resumo do Projeto e Equação Ajustada.
* Tabela de Métricas formatada (padrão ABNT/Acadêmico).
* Gráficos de Alta Resolução.

---

## 🛠️ Instalação e Uso

### 🌐 Opção 1: Acesso Imediato (Cloud)
Utilize a versão estável hospedada na nuvem:
👉 **[Acessar PryAI Canopy Online](SEU_LINK_DO_STREAMLIT_AQUI)**

### 💻 Opção 2: Execução Local
Para desenvolvedores ou processamento offline:

```bash
# 1. Clone o repositório
git clone [https://github.com/PryAI/PryAI-Canopy.git](https://github.com/PryAI/PryAI-Canopy.git)
cd PryAI-Canopy

# 2. Instale as dependências (Recomendado usar venv)
pip install -r requirements.txt

# 3. Execute a aplicação
streamlit run app.py
