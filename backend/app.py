from flask import Flask, render_template, send_from_directory
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__, static_url_path='/static')

def gerar_graficos():
    file_path = 'data/escolas_selecionadas.CSV'

    estado_mapping = {
        12: "AC - Acre", 27: "AL - Alagoas", 13: "AM - Amazonas", 16: "AP - Amapá", 29: "BA - Bahia",
        23: "CE - Ceará", 53: "DF - Distrito Federal", 32: "ES - Espírito Santo", 52: "GO - Goiás",
        21: "MA - Maranhão", 51: "MT - Mato Grosso", 50: "MS - Mato Grosso do Sul", 31: "MG - Minas Gerais",
        15: "PA - Pará", 25: "PB - Paraíba", 26: "PE - Pernambuco", 22: "PI - Piauí", 41: "PR - Paraná",
        33: "RJ - Rio de Janeiro", 24: "RN - Rio Grande do Norte", 43: "RS - Rio Grande do Sul", 11: "RO - Rondônia",
        14: "RR - Roraima", 42: "SC - Santa Catarina", 35: "SP - São Paulo", 28: "SE - Sergipe", 17: "TO - Tocantins"
    }

    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        return

    df = pd.read_csv(file_path, sep=",", encoding="latin1", low_memory=False)
    df["Estado"] = df["CO_UF"].map(estado_mapping)

    plt.rcParams["figure.figsize"] = (10, 5)
    output_dir = "static/output"
    os.makedirs(output_dir, exist_ok=True)

    def salvar(fig, nome):
        caminho = f"{output_dir}/{nome}.png"
        fig.savefig(caminho, bbox_inches="tight")
        print(f"Salvo: {caminho}")
        plt.close(fig)

    # Geração dos gráficos
    fig = plt.figure()
    sns.countplot(x=df['TP_DEPENDENCIA'])
    plt.title("Distribuição das escolas por dependência administrativa")
    salvar(fig, "dependencia")

    fig = plt.figure()
    df["Estado"].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title("Quantidade de escolas por estado")
    salvar(fig, "escolas_por_estado")

    fig = plt.figure()
    df['TP_SITUACAO_FUNCIONAMENTO'].value_counts().plot(kind='bar', color='orange')
    plt.title("Situação de funcionamento das escolas")
    salvar(fig, "situacao_funcionamento")

    fig = plt.figure()
    df['IN_PROFISSIONALIZANTE'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['red', 'green'])
    plt.title("Escolas que oferecem ensino profissionalizante")
    plt.ylabel("")
    salvar(fig, "ensino_profissionalizante")

    fig = plt.figure()
    top_municipios = df['CO_MUNICIPIO'].value_counts().nlargest(10).index
    df_top = df[df['CO_MUNICIPIO'].isin(top_municipios)]
    municipios_estados = df_top.groupby(['CO_MUNICIPIO', 'Estado']).size().reset_index(name='Quantidade')
    municipios_estados['Label'] = municipios_estados['CO_MUNICIPIO'].astype(str) + " - " + municipios_estados['Estado']
    plt.bar(municipios_estados['Label'], municipios_estados['Quantidade'], color='purple')
    plt.title("Top 10 municípios com mais escolas")
    plt.xticks(rotation=90)
    salvar(fig, "top_municipios")

    fig = plt.figure()
    sns.barplot(x=df['TP_DEPENDENCIA'].value_counts().index, y=df['TP_DEPENDENCIA'].value_counts().values, palette='coolwarm')
    plt.title("Quantidade de escolas por tipo de dependência administrativa")
    salvar(fig, "dependencia_barplot")

    fig = plt.figure()
    df.groupby("Estado")["IN_PROFISSIONALIZANTE"].sum().sort_index().plot(kind='bar', color='teal')
    plt.title("Quantidade de escolas profissionais por estado")
    plt.xticks(rotation=90)
    salvar(fig, "escolas_profissionais_por_estado")

    fig = plt.figure()
    estados_prof = df[df['IN_PROFISSIONALIZANTE'] == 1]['Estado'].value_counts()
    estados_prof.plot(kind='bar', color='darkblue')
    plt.title("Estados com mais escolas de ensino profissionalizante")
    plt.xticks(rotation=90)
    salvar(fig, "mais_profissionalizantes")


@app.route("/")
def index():
    imagens = [
        "escolas_por_estado",
        "situacao_funcionamento",
        "ensino_profissionalizante",
        "top_municipios",
        "dependencia_barplot",
        "escolas_profissionais_por_estado",
        "mais_profissionalizantes"
    ]
    return render_template("grafico.html", imagens=imagens)


if __name__ == "__main__":
    gerar_graficos()
    app.run(host="0.0.0.0", port=5000, debug=True)
