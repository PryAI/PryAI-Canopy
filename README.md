# 🌲 PryAI Canopy

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.42-red)
![Status](https://img.shields.io/badge/Status-Production-success)
![License](https://img.shields.io/badge/License-MIT-green)

> **Inteligência Computacional e Blindagem de Dados para Modelagem Biométrica Florestal.**

O **PryAI Canopy** é um ecossistema robusto desenvolvido para transformar dados brutos de campo (muitas vezes inconsistentes) em modelos matemáticos precisos e relatórios de nível de consultoria.

Diferente de softwares tradicionais que travam com erros de digitação ou formatação, o Canopy implementa o **PryAI Shield™**, um motor de blindagem que detecta, isola e neutraliza falhas antes que elas afetem a estatística.

---

## 🌐 Acesso Imediato

Utilize a versão estável hospedada na nuvem:

👉 **[Acessar PryAI Canopy Online](https://pryai-canopy.streamlit.app/)**

---

## 🛡️ O Diferencial: PryAI Shield™

A verdadeira inteligência do Canopy está no que você não vê. O módulo de processamento (`src/parser.py`) atua como um "firewall" estatístico:

* **Detecção Universal de Decimais:** O sistema identifica automaticamente se a planilha está no padrão brasileiro (vírgula) ou americano (ponto) e normaliza os dados sem intervenção do usuário.
* **Limpeza Semântica:** Textos acidentais em colunas numéricas (ex: "Vinte", "Erro", "S/D") são detectados, convertidos para nulo e filtrados automaticamente, garantindo que apenas dados válidos entrem no cálculo.
* **Proteção Matemática:** Bloqueio proativo de operações ilegais (como `ln(0)` ou números negativos em transformações logarítmicas), garantindo a integridade matemática do ajuste OLS.

---

## ⚡ Funcionalidades Principais

### 1. Modelagem Flexível & Biblioteca Inteligente
Esqueça as listas fechadas. O **PryAI Interpreter** permite liberdade total:
* **Sintaxe Livre:** Escreva `ln(Y) = b0 + b1*ln(DAP)` ou `Y = b0 + b1*(DAP**2)`. O motor entende.
* **Biblioteca de Equações:** Salve seus modelos favoritos (Spurr, Schumacher, Hipsométricos) na memória da sessão para reutilização instantânea.

### 2. Diagnóstico Visual Interativo
Gráficos que contam a história dos dados:
* **Interatividade:** Passe o mouse para ver o ID, Talhão e erro exato de cada árvore.
* **Controle Total:** Botão de "Restaurar Visão" caso você se perca no zoom.
* **Análise de Resíduos:** Linha zero destacada em vermelho para identificação imediata de tendências.
* **Curvas Suaves (Loess):** Visualização clara da tendência biológica sobre os dados reais.

### 3. Métricas de Engenharia
Cálculo automático dos indicadores vitais para o inventário florestal:
* **R² Ajustado:** Explicação da variância.
* **Syx %:** O Erro Padrão da Estimativa em porcentagem (o selo de qualidade do modelo).
* **Fator de Meyer:** Correção automática de viés para modelos logarítmicos.
* **AIC / BIC / Durbin-Watson:** Critérios avançados para seleção de modelos e análise de autocorrelação.

### 4. Report One-Click
Gera um **Relatório Técnico em PDF** com design minimalista e alto contraste, contendo:
* Resumo do Projeto e Equação Ajustada.
* Tabela de Métricas formatada.
* Gráficos de Alta Resolução alinhados.

---

## 🛠️ Instalação Local (Para Desenvolvedores)

Se preferir rodar a aplicação na sua máquina:

```bash
# 1. Clone o repositório
git clone [https://github.com/PryAI/PryAI-Canopy.git](https://github.com/PryAI/PryAI-Canopy.git)
cd PryAI-Canopy

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a aplicação
streamlit run app.py
