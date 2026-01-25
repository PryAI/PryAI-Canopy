# 🌲 PryAI Canopy

**Ferramenta Avançada de Modelagem Biométrica e Volumétrica**

O **PryAI Canopy** é uma aplicação web desenvolvida para processamento estatístico de dados florestais. O diferencial desta ferramenta é o seu sistema de **"Blindagem de Dados"** (*PryAI Shield*), que detecta e neutraliza erros comuns de campo (como erros de digitação, unidades incorretas e outliers físicos) antes do ajuste dos modelos, garantindo a integridade das análises.

## 🚀 Funcionalidades Principais

* **🛡️ Blindagem de Dados:** Algoritmos de limpeza que impedem travamentos por erros de tipagem (ex: texto em coluna numérica) e filtram inconsistências físicas (DAP negativo, altura zero).
* **📐 Regressão Flexível:** Ajuste robusto de modelos clássicos (Schumacher-Hall, Spurr, Hipsométricos) e suporte para equações personalizadas via *PryAI Interpreter*.
* **📊 Estatísticas de Precisão:** Cálculo automático de métricas vitais para a engenharia florestal:
    * R² Ajustado
    * Syx% (Erro Padrão da Estimativa)
    * Fator de Correção de Meyer (para modelos logarítmicos)
    * AIC e BIC
    * Teste de Durbin-Watson
* **📄 Relatórios Profissionais:** Geração automática de relatórios em PDF com as equações ajustadas, coeficientes e gráficos de resíduos.

## 🛠️ Instalação e Uso

### Opção 1: Acesso Online
Acesse a versão hospedada no Streamlit Cloud: [Cole o Link do seu App Aqui depois de subir]

### Opção 2: Execução Local

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/pryai-canopy.git](https://github.com/SEU_USUARIO/pryai-canopy.git)
    cd pryai-canopy
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```

## 📂 Estrutura do Projeto

* `app.py`: Interface principal (Frontend) e orquestrador da aplicação.
* `src/parser.py`: Módulo responsável pela limpeza profunda e tipagem dos dados brutos.
* `src/external_model.py`: Motor matemático para ajustes OLS, tratamentos estatísticos e validação de fórmulas.
* `src/plots.py`: Biblioteca de visualização gráfica (Resíduos x Preditos, Dispersão).
* `src/report_export.py`: Motor de geração de relatórios técnicos em PDF.

## 🎓 Sobre o Autor

Desenvolvido por **Pedro** (Graduando em Engenharia Florestal - UFPR) como parte do ecossistema **PryAI**, focado em trazer inteligência computacional e automação para o setor florestal.

---
*Licença MIT - Open Source*
