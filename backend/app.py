import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho do arquivo no Docker
file_path = 'data/escolas_selecionadas.CSV'

# Dicionário para mapear códigos de estado
estado_mapping = {
    12: "AC - Acre", 27: "AL - Alagoas", 13: "AM - Amazonas", 16: "AP - Amapá", 29: "BA - Bahia",
    23: "CE - Ceará", 53: "DF - Distrito Federal", 32: "ES - Espírito Santo", 52: "GO - Goiás",
    21: "MA - Maranhão", 51: "MT - Mato Grosso", 50: "MS - Mato Grosso do Sul", 31: "MG - Minas Gerais",
    15: "PA - Pará", 25: "PB - Paraíba", 26: "PE - Pernambuco", 22: "PI - Piauí", 41: "PR - Paraná",
    33: "RJ - Rio de Janeiro", 24: "RN - Rio Grande do Norte", 43: "RS - Rio Grande do Sul", 11: "RO - Rondônia",
    14: "RR - Roraima", 42: "SC - Santa Catarina", 35: "SP - São Paulo", 28: "SE - Sergipe", 17: "TO - Tocantins"
}

# Leitura do CSV
if os.path.exists(file_path):
    df = pd.read_csv(file_path, sep=",", encoding="latin1", low_memory=False)
    df["Estado"] = df["CO_UF"].map(estado_mapping)
    print(df.head())
else:
    print(f"Erro: Arquivo não encontrado em: {file_path}")
    exit()

# Preparação do ambiente de gráficos
plt.rcParams["figure.figsize"] = (10, 5)

def salvar_grafico(fig, nome):
    fig.savefig(f"output/{nome}.png", bbox_inches="tight")

os.makedirs("output", exist_ok=True)

# Gráfico 1
fig1 = plt.figure()
sns.countplot(x=df['TP_DEPENDENCIA'])
plt.title("Distribuição das escolas por dependência administrativa")
salvar_grafico(fig1, "dependencia")

# Gráfico 2
fig2 = plt.figure()
df["Estado"].value_counts().sort_index().plot(kind='bar', color='skyblue')
plt.title("Quantidade de escolas por estado")
salvar_grafico(fig2, "escolas_por_estado")

# Gráfico 3
fig3 = plt.figure()
df['TP_SITUACAO_FUNCIONAMENTO'].value_counts().plot(kind='bar', color='orange')
plt.title("Situação de funcionamento das escolas")
salvar_grafico(fig3, "situacao_funcionamento")

# Gráfico 4
fig4 = plt.figure()
df['IN_PROFISSIONALIZANTE'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['red', 'green'])
plt.title("Escolas que oferecem ensino profissionalizante")
plt.ylabel("")
salvar_grafico(fig4, "ensino_profissionalizante")

# Gráfico 5
fig5 = plt.figure()
top_municipios = df['CO_MUNICIPIO'].value_counts().nlargest(10).index
df_top_municipios = df[df['CO_MUNICIPIO'].isin(top_municipios)]
municipios_estados = df_top_municipios.groupby(['CO_MUNICIPIO', 'Estado']).size().reset_index(name='Quantidade')
municipios_estados['Label'] = municipios_estados['CO_MUNICIPIO'].astype(str) + " - " + municipios_estados['Estado']
plt.bar(municipios_estados['Label'], municipios_estados['Quantidade'], color='purple')
plt.title("Top 10 municípios com mais escolas")
plt.xticks(rotation=90)
salvar_grafico(fig5, "top_municipios")

# Gráfico 6
fig6 = plt.figure()
sns.barplot(x=df['TP_DEPENDENCIA'].value_counts().index, y=df['TP_DEPENDENCIA'].value_counts().values, palette='coolwarm')
plt.title("Quantidade de escolas por tipo de dependência administrativa")
salvar_grafico(fig6, "dependencia_barplot")

# Gráfico 7
fig7 = plt.figure()
df.groupby("Estado")["IN_PROFISSIONALIZANTE"].sum().sort_index().plot(kind='bar', color='teal')
plt.title("Quantidade de escolas profissionais por estado")
plt.xticks(rotation=90)
salvar_grafico(fig7, "escolas_profissionais_por_estado")

# Gráfico 8
fig8 = plt.figure()
estados_profissionalizantes = df[df['IN_PROFISSIONALIZANTE'] == 1]['Estado'].value_counts()
estados_profissionalizantes.plot(kind='bar', color='darkblue')
plt.title("Estados com mais escolas de ensino profissionalizante")
plt.xticks(rotation=90)
salvar_grafico(fig8, "mais_profissionalizantes")
