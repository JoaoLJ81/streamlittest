import pandas as pd
import streamlit as st
import plotly.express as px
import sys

# Set the pageview in streamlit to wide
st.set_page_config(layout="wide")

# Import from the CSV to the dataframe, using pandas
df = pd.read_csv("report.csv", sep=",")


# Change the type of object of the dates to date, and sort the dataframe by dates
# The function to_datetime needs the dayfirst = True, because the default is False.
# We do that to change the convention to D/M/Y.
df["Data de Venda"] = pd.to_datetime(df["Data de Venda"], dayfirst=True)
df = df.sort_values("Data de Venda")


# Creates a month variable so we can separate by month
df["Month"] = df["Data de Venda"].apply(lambda x: str(x.year) + "-" + str(x.month))


# Sidebar to act as filter for data
# month = st.sidebar.selectbox("Mês", df["Month"].unique())
month = st.sidebar.multiselect("Mês", df["Month"].unique(), placeholder="Por favor, selecione os meses para análise.")

if len(month) > 1:
    df_filtered = df
elif len(month) == 1:
    df_filtered = df[df["Month"] == month[0]]
else:
    st.write("Please choose a month to analize")
    sys.exit(1)

# First graph: Vendas por data, por produto

# Histogram allows me to use the count versions of the data. Just don't use a y axis, but set the color  
# Barmode = group stop the stacking of the bars

fig1 = px.histogram(df_filtered,
                x="Data de Venda",
                color="Nome do Produto",
                title="Vendas por dia",
                barmode="group")

# Updating the layout to set the gap between bars. In different datas and in different products on the same day.

fig1.update_layout(bargap=0.2, 
                   bargroupgap = 0.2)


# Formatting the x axis. Formatting the day format and setting the dtick to have one every day.

fig1.update_xaxes(type="date",
                  tickformat = '%d-%b',
                  dtick=86400000.0)

# Changing the title of the y axis.

fig1.update_yaxes(title_text="Produtos Vendidos")


# Second graph: Número de compradores por produto.

total_buyer = df_filtered.groupby("Nome do Produto")["Comprador"].count().reset_index()

fig2 = px.bar(total_buyer,
                x="Nome do Produto",
                y="Comprador",
                title="Compradores por produto")
    

# Organizing the plotly page.

# Create columns
col1, col2 = st.columns([0.8, 0.2])
col5, col6 = st.columns(2)
col3, col4 = st.columns([0.6, 0.4], gap="large")

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.write("Esse gráfico é uma relação de produtos vendidos por dia. A Mentoria Apollo 11 teve um bom rendimento no final do mês de maio, decaindo no dia 31/05, mas atinge um ápice no dia 02/06. Em junho as vendas estabilizam. Provavelmente houve um investimento para vendas do produto no final do mês de maio. As vendas do Manual para conquistar a Lua variam muito com o tempo, não havendo um padrão aparente, com alguns picos no começo de Junho. Esse padrão talvez seja explicado pelo próximo gráfico.")

with col5:
    st.write(" ")
    st.write(" ")
    st.write(" ")

with col3:
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    st.write("Aqui podemos ver o número de compradores de cada produto. Nos dados recebidos, temos 248 compradores, sendo assim, todos eles compraram a Mentoria Apollo 11 e alguns também compraram o Manual. Isso pode indicar que a Mentoria é o principal produto e o Manual é um produto complementar. Assim, isso explica as vendas dispersas no período de tempo analisado. Com apenas 41,5% dos compradores da Mentoria comprando também o Manual, é preciso fazer uma análise de investimento para saber se a produção do Manual para conquistar a Lua está se justificando.") 