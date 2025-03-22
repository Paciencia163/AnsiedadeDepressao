import streamlit as st
from fpdf import FPDF
import base64
import os

# Configuração da página
st.set_page_config(page_title="🧠 Diagnóstico de Saúde Mental", page_icon="🧠", layout="wide")

# CSS para estilizar a aplicação
st.markdown("""
    <style>
        .title {
            text-align: center;
            color: #4f8bf9;
            font-size: 32px;
        }
        .stApp {
            background-color: #f5f5f5;
        }
        .centered {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Menu lateral com múltiplas páginas
menu = st.sidebar.radio("📌 Navegação", ["🏠 Início", "📖 Sobre a Depressão", "📄 Relatórios"])

if menu == "🏠 Início":
    # Página Inicial
    st.markdown("<h1 class='title'>🧠 Diagnóstico de Saúde Mental</h1>", unsafe_allow_html=True)
    st.image("C3.jpg", use_container_width=True)

    st.write("Preencha os dados abaixo e veja a análise baseada nos seus sintomas. Esta ferramenta **não substitui um profissional de saúde**.")

    st.divider()

    # Formulário para coletar dados do usuário
    with st.form("user_form"):
        nome = st.text_input("Nome")
        idade = st.number_input("Idade", min_value=10, max_value=100)
        genero = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])
        
        st.subheader("📌 Marque os sintomas que você sente com frequência:")
        tristeza = st.checkbox("Tristeza intensa e persistente")
        falta_prazer = st.checkbox("Perda de interesse em atividades")
        cansaco = st.checkbox("Cansaço constante")
        preocupacao = st.checkbox("Preocupação excessiva")
        palpitacoes = st.checkbox("Palpitações ou crises de pânico")
        insonia = st.checkbox("Dificuldade para dormir")
        mudanca_apetite = st.checkbox("Mudança no apetite")
        dificuldade_concentracao = st.checkbox("Dificuldade em se concentrar")
        isolamento = st.checkbox("Isolamento social")

        submitted = st.form_submit_button("🔍 Analisar")

    if submitted:
        # Contagem de sintomas
        sintomas_depressao = sum([tristeza, falta_prazer, cansaco, insonia, mudanca_apetite, isolamento])
        sintomas_ansiedade = sum([preocupacao, palpitacoes, dificuldade_concentracao, insonia])

        # Diagnóstico baseado na pontuação
        if sintomas_depressao >= 4 and sintomas_ansiedade >= 3:
            resultado = "Possíveis sinais de depressão e ansiedade."
            st.error("⚠️ Indícios de **depressão e ansiedade**. Consulte um especialista.")
        elif sintomas_depressao >= 4:
            resultado = "Possíveis sinais de depressão."
            st.warning("⚠️ Indícios de **depressão**. Procure acompanhamento psicológico.")
        elif sintomas_ansiedade >= 3:
            resultado = "Possíveis sinais de ansiedade."
            st.warning("⚠️ Indícios de **ansiedade**. Considere buscar ajuda especializada.")
        else:
            resultado = "Nenhum sinal preocupante identificado."
            st.success("✅ Nenhum sinal preocupante identificado. Continue cuidando da sua saúde mental! 😊")

        # Geração de relatório em PDF
        def gerar_relatorio(nome, idade, genero, resultado):
            pdf = FPDF()
            pdf.add_page()

            # Adicionando papel timbrado
            pdf.image("papel_timbrado.jpeg", 10, 8, 190)

            # Título
            pdf.set_font("Arial", "B", 16)
            pdf.ln(40)  # Ajuste para papel timbrado
            pdf.cell(200, 10, "Relatório de Saúde Mental", ln=True, align="C")

            # Dados do paciente
            pdf.set_font("Arial", "", 12)
            pdf.ln(10)
            pdf.cell(200, 10, f"Nome: {nome}", ln=True)
            pdf.cell(200, 10, f"Idade: {idade}", ln=True)
            pdf.cell(200, 10, f"Gênero: {genero}", ln=True)

            # Resultado
            pdf.ln(10)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, "Diagnóstico:", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 10, resultado)

            # Salvar relatório
            pdf_path = "relatorio.pdf"
            pdf.output(pdf_path)
            return pdf_path

        # Gerar relatório e exibir botão de download
        pdf_path = gerar_relatorio(nome, idade, genero, resultado)
        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            b64_pdf = base64.b64encode(pdf_bytes).decode()
            pdf_link = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="relatorio_saude_mental.pdf">📄 Baixar Relatório</a>'
            st.markdown(pdf_link, unsafe_allow_html=True)

elif menu == "📖 Sobre a Depressão":
    # Página sobre depressão
    st.markdown("<h1 class='title'>📖 Sobre a Depressão</h1>", unsafe_allow_html=True)
    st.image("https://source.unsplash.com/800x300/?sadness", use_container_width=True)

    st.write("""
    A depressão é um transtorno mental caracterizado por um **estado persistente de tristeza** e **perda de interesse** nas atividades. 
    Pode afetar **pensamentos, emoções e bem-estar físico**.

    🔹 **Sintomas comuns:**  
    - Sensação de tristeza ou vazio  
    - Falta de energia e motivação  
    - Distúrbios do sono e apetite  
    - Pensamentos negativos frequentes  

    🔹 **Tratamentos:**  
    - Psicoterapia  
    - Medicamentos antidepressivos  
    - Mudanças no estilo de vida  

    🔹 **Saiba mais no vídeo abaixo:**  
    """)

    st.video("https://www.youtube.com/watch?v=l16BskCD0cM")  # Link de vídeo sobre depressão

elif menu == "📄 Relatórios":
    st.markdown("<h1 class='title'>📄 Relatórios</h1>", unsafe_allow_html=True)
    st.write("Aqui você pode visualizar e baixar seus relatórios gerados.")

    if os.path.exists("relatorio.pdf"):
        with open("relatorio.pdf", "rb") as pdf_file:
            st.download_button("📥 Baixar Último Relatório", pdf_file, "relatorio_saude_mental.pdf")

