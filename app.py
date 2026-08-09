import streamlit as st
import pandas as pd
import joblib


# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="Predição dos Níveis de Obesidade",
    page_icon="🏥",
    layout="wide"
)


# =====================================================
# CARREGANDO O MODELO
# =====================================================

modelo = joblib.load("modelo_obesidade.pkl")
scaler = joblib.load("scaler.pkl")
colunas_modelo = joblib.load("colunas_modelo.pkl")


# =====================================================
# TÍTULO
# =====================================================

st.title("🏥 Predição dos Níveis de Obesidade")

st.markdown("""
Esta aplicação utiliza um modelo de **Machine Learning (Random Forest)**
para estimar o nível de obesidade com base em características físicas
e hábitos de vida.

Preencha as informações abaixo para realizar uma previsão.
""")

st.info(
    "💡 Esta ferramenta possui finalidade exclusivamente acadêmica "
    "e não substitui uma avaliação realizada por um profissional de saúde."
)


# =====================================================
# DADOS PESSOAIS
# =====================================================

st.header("👤 Informações pessoais")

col1, col2 = st.columns(2)

with col1:

    gender_label = st.selectbox(
        "Sexo",
        ["Feminino", "Masculino"]
    )

    age = st.number_input(
        "Idade",
        min_value=10,
        max_value=100,
        value=25,
        step=1
    )


with col2:

    height = st.number_input(
        "Altura (metros)",
        min_value=1.20,
        max_value=2.30,
        value=1.70,
        step=0.01
    )

    weight = st.number_input(
        "Peso (kg)",
        min_value=30.0,
        max_value=250.0,
        value=70.0,
        step=0.1
    )


# Conversão para os valores originais do dataset

gender = {
    "Feminino": "Female",
    "Masculino": "Male"
}[gender_label]


# =====================================================
# HISTÓRICO FAMILIAR
# =====================================================

with st.expander("🧬 Histórico familiar", expanded=True):

    family_history_label = st.radio(
        "Existe histórico familiar de obesidade?",
        ["Não", "Sim"],
        horizontal=True
    )

    family_history = {
        "Não": "no",
        "Sim": "yes"
    }[family_history_label]


# =====================================================
# ALIMENTAÇÃO
# =====================================================

with st.expander("🍎 Alimentação", expanded=True):

    col1, col2 = st.columns(2)

    with col1:

        favc_label = st.radio(
            "Você costuma consumir alimentos altamente calóricos?",
            ["Não", "Sim"],
            horizontal=True
        )

        favc = {
            "Não": "no",
            "Sim": "yes"
        }[favc_label]


        # Consumo de vegetais

        fcvc_label = st.radio(
            "🥦 Com que frequência você consome vegetais?",
            [
                "Raramente",
                "Às vezes",
                "Frequentemente"
            ],
            index=1,
            help="Escolha a opção que melhor representa seu consumo habitual."
        )

        fcvc = {
            "Raramente": 1.0,
            "Às vezes": 2.0,
            "Frequentemente": 3.0
        }[fcvc_label]


        # Número de refeições

        ncp = st.number_input(
            "🍽️ Quantas refeições principais você faz por dia?",
            min_value=1,
            max_value=4,
            value=3,
            step=1
        )


    with col2:

        # Alimentação entre refeições

        caec_label = st.selectbox(
            "🍪 Com que frequência você come entre as refeições?",
            [
                "Nunca",
                "Às vezes",
                "Frequentemente",
                "Sempre"
            ]
        )

        caec = {
            "Nunca": "no",
            "Às vezes": "Sometimes",
            "Frequentemente": "Frequently",
            "Sempre": "Always"
        }[caec_label]


        # Consumo de água

        ch2o_label = st.radio(
            "💧 Como você avalia seu consumo diário de água?",
            [
                "Baixo",
                "Moderado",
                "Alto"
            ],
            index=1,
            help="Indique como você considera seu consumo habitual de água."
        )

        ch2o = {
            "Baixo": 1.0,
            "Moderado": 2.0,
            "Alto": 3.0
        }[ch2o_label]


        # Monitoramento de calorias

        scc_label = st.radio(
            "📊 Você monitora o consumo de calorias?",
            ["Não", "Sim"],
            horizontal=True
        )

        scc = {
            "Não": "no",
            "Sim": "yes"
        }[scc_label]


# =====================================================
# ATIVIDADE FÍSICA
# =====================================================

with st.expander("🏃 Atividade física", expanded=True):

    col1, col2 = st.columns(2)

    with col1:

        faf_label = st.radio(
            "🏋️ Com que frequência você pratica atividade física?",
            [
                "Nunca ou quase nunca",
                "Poucas vezes",
                "Frequentemente",
                "Muito frequentemente"
            ],
            index=1
        )

        faf = {
            "Nunca ou quase nunca": 0.0,
            "Poucas vezes": 1.0,
            "Frequentemente": 2.0,
            "Muito frequentemente": 3.0
        }[faf_label]


    with col2:

        tue_label = st.radio(
            "📱 Quanto tempo você passa utilizando dispositivos tecnológicos?",
            [
                "Pouco",
                "Moderado",
                "Muito"
            ],
            index=1
        )

        tue = {
            "Pouco": 0.0,
            "Moderado": 1.0,
            "Muito": 2.0
        }[tue_label]


# =====================================================
# HÁBITOS E ESTILO DE VIDA
# =====================================================

with st.expander("🚬 Hábitos e estilo de vida", expanded=True):

    col1, col2 = st.columns(2)

    with col1:

        smoke_label = st.radio(
            "Você fuma?",
            ["Não", "Sim"],
            horizontal=True
        )

        smoke = {
            "Não": "no",
            "Sim": "yes"
        }[smoke_label]


    with col2:

        calc_label = st.selectbox(
            "🍷 Com que frequência você consome bebidas alcoólicas?",
            [
                "Não",
                "Às vezes",
                "Frequentemente",
                "Sempre"
            ]
        )

        calc = {
            "Não": "no",
            "Às vezes": "Sometimes",
            "Frequentemente": "Frequently",
            "Sempre": "Always"
        }[calc_label]


# =====================================================
# TRANSPORTE
# =====================================================

with st.expander("🚗 Transporte", expanded=True):

    mtrans_label = st.selectbox(
        "Qual é o seu principal meio de transporte?",
        [
            "Automóvel",
            "Motocicleta",
            "Bicicleta",
            "Transporte público",
            "A pé"
        ]
    )

    mtrans = {
        "Automóvel": "Automobile",
        "Motocicleta": "Motorbike",
        "Bicicleta": "Bike",
        "Transporte público": "Public_Transportation",
        "A pé": "Walking"
    }[mtrans_label]


# =====================================================
# PREVISÃO
# =====================================================

st.divider()

if st.button(
    "🔍 Realizar previsão",
    type="primary",
    use_container_width=True
):

    # =================================================
    # CALCULA O IMC
    # =================================================

    bmi = weight / (height ** 2)


    # =================================================
    # CRIA O DATAFRAME
    # =================================================

    dados = pd.DataFrame({
        "Gender": [gender],
        "Age": [age],
        "Height": [height],
        "Weight": [weight],
        "family_history": [family_history],
        "FAVC": [favc],
        "FCVC": [fcvc],
        "NCP": [ncp],
        "CAEC": [caec],
        "SMOKE": [smoke],
        "CH2O": [ch2o],
        "SCC": [scc],
        "FAF": [faf],
        "TUE": [tue],
        "CALC": [calc],
        "MTRANS": [mtrans],
        "BMI": [bmi]
    })


    # =================================================
    # PRÉ-PROCESSAMENTO
    # =================================================

    dados = pd.get_dummies(dados)


    # Garante que todas as colunas do treinamento existam

    for coluna in colunas_modelo:
        if coluna not in dados.columns:
            dados[coluna] = 0


    # Mantém exatamente a mesma ordem das colunas utilizadas
    # durante o treinamento

    dados = dados[colunas_modelo]


    # Aplica a padronização

    dados = scaler.transform(dados)


    # =================================================
    # REALIZA A PREVISÃO
    # =================================================

    previsao = modelo.predict(dados)[0]


    # =================================================
    # RESULTADO
    # =================================================

    st.divider()

    st.header("🎯 Resultado da previsão")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "IMC calculado",
            f"{bmi:.1f}"
        )

    with col2:

        st.success(
            f"**Nível previsto:**\n\n### {previsao}"
        )


    st.warning("""
    ⚠️ **Importante**

    Esta previsão foi gerada por um modelo de Machine Learning
    treinado com a base **Obesity Levels Dataset**.

    O resultado possui finalidade exclusivamente acadêmica e
    não substitui avaliação ou diagnóstico realizado por um
    profissional de saúde.
    """)


# =====================================================
# INFORMAÇÕES SOBRE O MODELO
# =====================================================

st.divider()

st.header("📊 Sobre o modelo")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    **Algoritmo:** Random Forest

    **Métricas obtidas no treinamento:**

    - 🎯 Acurácia: **98,80%**
    - Precision: **98,81%**
    - Recall: **98,80%**
    - F1-Score: **98,80%**
    """)


with col2:

    st.markdown("""
    **Projeto:** Tech Challenge – Fase 4

    **Curso:** Pós-graduação em Data Analytics

    **Tecnologias utilizadas:**

    - Python
    - Streamlit
    - Scikit-Learn
    - Pandas
    - Random Forest
    """)


# =====================================================
# RODAPÉ
# =====================================================

st.divider()

st.caption(
    "Projeto desenvolvido para o Tech Challenge - "
    "Pós-graduação em Data Analytics."
)