# 🌲 PryAI Canopy

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.42-red)
![Status](https://img.shields.io/badge/Status-Production-success)
![License](https://img.shields.io/badge/License-MIT-green)

> **Inteligência Computacional e Blindagem de Dados para Modelagem Biométrica Florestal.**

O **PryAI Canopy** é uma ferramenta desenvolvida para trazer segurança e precisão ao processamento de inventários florestais. Seu foco é transformar dados brutos de campo em modelos matemáticos confiáveis e relatórios técnicos padronizados.

Projetado para a realidade do trabalho de campo, o sistema conta com o **PryAI Shield™**, um motor de tratamento de dados que assegura que inconsistências de digitação ou formatação não comprometam a análise estatística.

---

## 🌐 Acesso Imediato

Utilize a versão estável hospedada na nuvem:

👉 **[Acessar PryAI Canopy Online](https://pryai-canopy.streamlit.app/)**

---

## 🛡️ Recurso Exclusivo: PryAI Shield™

Para garantir a integridade dos modelos ajustados, o módulo de processamento (`src/parser.py`) implementa camadas automáticas de validação:

* **Normalização de Decimais:** Identificação e padronização automática de arquivos que utilizam vírgula (padrão BR) ou ponto (padrão US), garantindo a leitura correta dos valores.
* **Limpeza Semântica:** Tratamento inteligente de colunas numéricas. Células contendo textos acidentais (ex: "Vinte", "Erro", "S/D") são identificadas e convertidas para valores nulos, sendo filtradas antes do cálculo para evitar inconsistências.
* **Segurança Matemática:** Verificação prévia de operações (como logaritmos), impedindo o processamento de valores matematicamente inválidos (zeros ou negativos) e garantindo a estabilidade do ajuste OLS.

---

## ⚡ Funcionalidades

### 1. Modelagem Flexível & Biblioteca
O sistema oferece total liberdade para o pesquisador e o engenheiro:
* **Sintaxe Livre:** Suporte para equações lineares e não-lineares personalizadas via **PryAI Interpreter**. Ex: `ln(Y) = b0 + b1*ln(DAP)`.
* **Biblioteca de Equações:** Permite salvar e carregar modelos recorrentes (Spurr, Schumacher, Hipsométricos) diretamente na sessão de uso.

### 2. Diagnóstico Visual Interativo
Visualização de dados focada em clareza:
* **Interatividade:** Gráficos dinâmicos com *tooltips* detalhados (ID, Talhão, Erro) ao passar o mouse.
* **Análise de Resíduos:** Ferramentas visuais para identificação de tendenciosidades, incluindo destaque da linha zero e análise de dispersão.
* **Curvas Suaves (Loess):** Plotagem de tendências biológicas sobrepostas aos dados observados.

### 3. Métricas de Engenharia
Cálculo automático dos principais indicadores de precisão:
* **R² Ajustado:** Coeficiente de determinação.
* **Syx %:** Erro Padrão da Estimativa em porcentagem.
* **Fator de Meyer:** Correção de viés para transformações logarítmicas.
* **Critérios de Seleção:** AIC, BIC e teste de Durbin-Watson para análise de autocorrelação.

### 4. Relatórios Técnicos
Geração instantânea de **Relatório em PDF**, contendo:
* Resumo estatístico do projeto.
* Equação ajustada e coeficientes.
* Tabela de métricas formatada.
* Gráficos de diagnóstico em alta resolução.

---

## 🛠️ Instalação Local (Para Desenvolvedores)

Caso deseje executar a aplicação em ambiente local:

```bash
# 1. Clone o repositório
git clone [https://github.com/PryAI/PryAI-Canopy.git](https://github.com/PryAI/PryAI-Canopy.git)
cd PryAI-Canopy

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a aplicação
streamlit run app.py
