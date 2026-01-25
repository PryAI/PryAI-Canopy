# 🌲 PryAI Canopy

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.42-red)
![Status](https://img.shields.io/badge/Status-Production-success)
![License](https://img.shields.io/badge/License-MIT-green)

> **Modelagem Biométrica Florestal de Alta Precisão com Flexibilidade Total.**

O **PryAI Canopy** é uma ferramenta desenvolvida para trazer segurança, agilidade e precisão ao processamento de inventários florestais. O software transforma dados brutos de campo em modelos matemáticos confiáveis, oferecendo controle total ao engenheiro sobre o ajuste e a validação das equações.

---

## 🌐 Acesso Imediato

Utilize a versão estável hospedada na nuvem:

👉 **[Acessar PryAI Canopy Online](https://pryai-canopy.streamlit.app/)**

---

## ⚡ Funcionalidades Principais

### 1. Modelagem Flexível & Dualidade de Ajuste
O sistema oferece total liberdade através do **PryAI Interpreter**, permitindo que o usuário decida como o modelo deve ser construído:
* **Sintaxe Livre:** Suporte para equações lineares e não-lineares personalizadas. Ex: `ln(Y) = b0 + b1*ln(DAP)`.
* **Ajuste Automático (OLS):** O motor estatístico analisa sua base de dados e gera instantaneamente os melhores coeficientes.
* **Ajuste Manual:** O usuário tem a opção de inserir manualmente seus próprios coeficientes (b0, b1, b2...). Ideal para testar equações de literatura ou validar modelos pré-existentes sobre novos dados de campo.
* **Biblioteca de Equações:** Salve e carregue modelos recorrentes (Spurr, Schumacher, Hipsométricos) para agilizar o fluxo de trabalho.

### 2. Diagnóstico Visual Interativo
Visualização de dados reativa para uma auditoria completa do comportamento do modelo:
* **Interatividade:** Gráficos dinâmicos com *tooltips* detalhados (ID, Talhão, Erro) ao passar o mouse.
* **Análise de Resíduos:** Ferramentas visuais para identificação de tendenciosidades, com destaque para a linha zero e análise de dispersão.
* **Curvas Suaves (Loess):** Plotagem de tendências biológicas sobrepostas aos dados reais.

### 3. Métricas de Engenharia e Precisão
Cálculo automático dos indicadores vitais para o rigor técnico do setor florestal:
* **R² Ajustado:** Coeficiente de determinação para explicação da variância.
* **Syx %:** Erro Padrão da Estimativa em porcentagem.
* **Fator de Meyer:** Correção de viés para transformações logarítmicas.
* **Critérios de Seleção:** AIC, BIC e Teste de Durbin-Watson para análise de autocorrelação.

### 4. Relatórios Técnicos (Laudo em PDF)
Geração instantânea de um documento profissional pronto para entrega:
* Resumo estatístico do projeto e metadados.
* Equação ajustada e coeficientes (gerados ou inseridos).
* Tabela de métricas formatada e gráficos de diagnóstico em alta resolução.

---

## 🛡️ Camada de Resiliência: PryAI Shield™

Para garantir a fluidez do uso, o sistema conta com o módulo **PryAI Shield™**, que trata inconsistências comuns de dados:
* **Normalização de Decimais:** Identifica automaticamente se a planilha utiliza vírgula (BR) ou ponto (US).
* **Limpeza Semântica:** Detecta textos acidentais em colunas numéricas (ex: "Vinte", "Erro"), filtrando-os para evitar travamentos.
* **Segurança Matemática:** Bloqueio proativo de cálculos inválidos (como logaritmos de zero ou negativos).

---

## 🛠️ Instalação Local (Para Desenvolvedores)

```bash
# 1. Clone o repositório
git clone [https://github.com/PryAI/PryAI-Canopy.git](https://github.com/PryAI/PryAI-Canopy.git)
cd PryAI-Canopy

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a aplicação
streamlit run app.py
```

---

🎓 Sobre
O PryAI Canopy foi desenvolvido por Pedro, graduando em Engenharia Florestal pela Universidade Federal do Paraná (UFPR).

Este software faz parte do ecossistema PryAI, uma iniciativa focada em unir inteligência computacional, automação e ciência de dados para elevar o nível técnico e a eficiência do setor florestal brasileiro.

Licença MIT - Open Source Software
