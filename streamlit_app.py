import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from simulation import retirement_simulation

today = datetime.today().strftime('%Y-%m-%d')
st.set_page_config(
    page_title="Simulateur du rentier",
)

# Configuration de l'interface Streamlit
st.title("Calculateur de rente avancé")

# --- Initial Values ---
INIT_AGE = 41
RETIREMENT_AGE = 44
CURRENT_INCOME = 48_000
INCOME_INCREASE_RATE = 0.022
CURRENT_SPENDING = 45_000
INFLATION = 0.03
INIT_NET_WORTH = 1_300_000
RETURN_RATE = 0.07
INVESTMENT_TAX_RATE = 0.33
STATE_PENSION = 8900
STATE_RETIREMENT_AGE = 66
percent_format = "%.3f" 

with st.expander("Paramètres de la simulation", expanded=True):
    # --- Simulation Parameters ---
    st.header("Paramètres de la simulation")
    start_age = st.number_input("Age initial", min_value=18, max_value=100, value=INIT_AGE)
    end_age = st.number_input("Age final de la simulation", min_value=18, value=100)
    retirement_age = st.number_input("Age ciblé pour l'arrêt d'activité", min_value=18, max_value=100, value=RETIREMENT_AGE)

    # --- Income and Spending ---
    st.header(f"Revenus et dépenses au {today}")
    current_income = st.number_input(f"Revenu annuel (net net)", min_value=0, value=CURRENT_INCOME)
    current_spending = st.number_input("Dépenses annuelles", min_value=0, value=CURRENT_SPENDING)

    # --- State Pension ---
    is_pension = st.checkbox("Pension, retraite de l'état", value = False)
    state_retirement_age =  STATE_RETIREMENT_AGE
    if is_pension:
        state_pension = st.number_input("Retraite de l'état", min_value = 0, step=500, value = STATE_PENSION)
        state_retirement_age = st.number_input("Age de départ à la retraite", min_value = 55, step = 1, value=STATE_RETIREMENT_AGE)
    else:
        state_pension = 0

    # --- Evolution Rates ---
    st.header("Evolution")
    income_increase_rate = st.number_input("Taux de réévaluation annuel du revenu", min_value=0.0, max_value=1.0, format=percent_format, value=INCOME_INCREASE_RATE)
    inflation_rate = st.number_input("Taux d'inflation", min_value=0.0, max_value=1.0, format=percent_format, value=INFLATION)

    # --- Investments ---
    st.header("Placements")
    initial_net_worth = st.number_input("Patrimoine", min_value=0, value=INIT_NET_WORTH)
    investment_return_rate = st.number_input("Taux de rendement des placements", format=percent_format, min_value=-1.0, max_value=1.0, value=RETURN_RATE)

    # --- Taxes ---
    st.header("Taxes")
    investment_tax_rate = st.number_input("Taxe sur les plus values réalisées", format=percent_format, min_value=0.0, max_value = 1.0, value = INVESTMENT_TAX_RATE)
    is_wealth_tax = st.checkbox("ISF", value = False)
    wealth_tax_rate = 0
    wealth_tax_threshold = 0
    if is_wealth_tax:
        wealth_tax_rate = st.number_input("ISF", format=percent_format, min_value = 0., max_value = 1., value = 0.)
        wealth_tax_threshold = st.number_input("seuil ISF", min_value = 0, step= 100000, value = 1_000_000)

# --- Simulation and Results ---
if st.button("Calculer la rente"):
    df = retirement_simulation(start_age, end_age, current_income, income_increase_rate,
                               current_spending, inflation_rate, initial_net_worth,
                               investment_return_rate, retirement_age, investment_tax_rate,
                               state_pension, state_retirement_age, wealth_tax_rate, wealth_tax_threshold)
    
    st.write("Résultats de la simulation")
    
    # --- Charts ---
    st.header("Patrimoine")
    fig, ax = plt.subplots()
    ax.bar(df["Age"], df["Net Worth"], color='blue')
    ax.set_xlabel("Age")
    ax.set_ylabel("Patrimoine")
    ax.set_title("Évolution du patrimoine par âge")
    st.pyplot(fig)

    ruined = df[df["Net Worth"] == 0]["Age"]
    if len(ruined) > 0:
        st.warning(f"Attention, vous serez ruiné vers {ruined.iloc[0]} ans!")

    st.header("Variations du patrimoine")
    fig, ax = plt.subplots()
    colors = ['green' if x > 0 else 'red' for x in df["Delta Net Worth"]]
    ax.bar(df["Age"], df["Delta Net Worth"], color=colors)
    ax.set_xlabel("Age")
    ax.set_ylabel("Delta de Patrimoine")
    ax.set_title("Delta de Patrimoine par âge")
    st.pyplot(fig)

    st.header("Patrimoine à euros constants")
    fig, ax = plt.subplots()
    ax.bar(df["Age"],df["Net Worth (euros constants)"] , color='blue')
    ax.set_xlabel("Age")
    ax.set_ylabel("Patrimoine")
    ax.set_title("Évolution du patrimoine à euros constants")
    st.pyplot(fig)

    vals = df["Net Worth (euros constants)"].values
    if vals[-1] < vals[-2] or vals[-1] == 0:
        st.warning("Attention, vous ne maintiendrez pas votre pouvoir d'achat!")

    # --- Data Table ---
    st.header("Données de la simulation")
    st.dataframe(df.set_index("Age"))
