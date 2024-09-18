import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Définition des fonctions pour les calculs
def update_income(current_income, rate_increase, age, retirement_age, state_retirement_age, state_pension):
    income = 0
    if age >= state_retirement_age:
        income += state_pension

    if age >= retirement_age:
        return income  # Pas de revenu du travail après la retraite
    else:
        return current_income * (1 + rate_increase) + income

def update_spending(current_spending, inflation_rate):
    return current_spending * (1 + inflation_rate)

def update_net_worth(net_worth, income, spending, return_rate, age, retirement_age, investment_tax_rate):
    if age > retirement_age:
        spending = spending/(1 - investment_tax_rate)
    new_worth = net_worth * (1 + return_rate) + income - spending
    return max(new_worth, 0)

# Création de la fonction principale pour gérer la simulation
def retirement_simulation(start_age, end_age, current_income, income_increase_rate,
                          current_spending, inflation_rate, initial_net_worth, investment_return_rate, retirement_age, investment_tax_rate, state_pension, state_retirement_age):

    years = end_age - start_age
    age_range = range(start_age, end_age + 1)
    data = {
        "Age": age_range,
        "Income": [],
        "Spending": [],
        "Net Worth": [],
        "Delta Net Worth": []
    }

    net_worth = initial_net_worth
    for age in age_range:
        if age > start_age:
            state_pension = state_pension*(1+inflation_rate)
            current_income = update_income(current_income, income_increase_rate, age, retirement_age, state_retirement_age, state_pension)
            current_spending = update_spending(current_spending, inflation_rate)

        new_net_worth = update_net_worth(net_worth, current_income, current_spending, investment_return_rate, age, retirement_age, investment_tax_rate)

        # Enregistre les données pour l'année
        data["Income"].append(current_income)
        data["Spending"].append(current_spending)
        data["Net Worth"].append(new_net_worth)
        data["Delta Net Worth"].append(new_net_worth - net_worth)

        # Mise à jour du patrimoine net pour l'année suivante
        net_worth = new_net_worth

    df = pd.DataFrame(data)
    return df

# Configuration de l'interface Streamlit
st.title("Calculateur de rente avancé")

INIT_AGE = 41
RETIREMENT_AGE = 45
CURRENT_INCOME = 48_000
INCOME_INCREASE_RATE = 0.022
CURRENT_SPENDING = 45_000
INFLATION = 0.04
INIT_NET_WORTH = 1_300_000
RETURN_RATE = 0.06
INVESTMENT_TAX_RATE = 0.3
STATE_PENSION = 8900
STATE_RETIREMENT_AGE = 66

# Configuration des entrées utilisateur
percent_format = "%.3f"
start_age = st.number_input("Age initial", min_value=18, max_value=100, value=INIT_AGE)
end_age = st.number_input("Age final de la simulation", min_value=18, max_value=150, value=100)
retirement_age = st.number_input("Age de départ à la retraite", min_value=18, max_value=100, value=RETIREMENT_AGE)
current_income = st.number_input("Revenu annuel initial (net net)", min_value=0, value=CURRENT_INCOME)
income_increase_rate = st.number_input("Taux de réévaluation annuel du revenu", min_value=0.0, max_value=1.0, format=percent_format, value=INCOME_INCREASE_RATE)
current_spending = st.number_input("Dépenses annuelles", min_value=0, value=CURRENT_SPENDING)
inflation_rate = st.number_input("Taux d'inflation", min_value=0.0, max_value=1.0, format=percent_format, value=INFLATION)
initial_net_worth = st.number_input("Patrimoine initial", min_value=0, value=INIT_NET_WORTH)
investment_return_rate = st.number_input("Taux de rendement des placements", format=percent_format, min_value=-1.0, max_value=1.0, value=RETURN_RATE)
investment_tax_rate = st.number_input("Taxe sur les plus values réalisées", format=percent_format, min_value=0.0, max_value = 1.0, value = 0.3)

is_pension = st.checkbox("Retraite de l'état", value = False)

state_retirement_age =  STATE_RETIREMENT_AGE
if is_pension:
    state_pension = st.number_input("Retraite de l'état", min_value = 0, step=500, value = STATE_PENSION)
    state_retirement_age = st.number_input("Age de départ à la retraite officiel (pour la pension de l'état)", min_value = 64, step = 1, value=STATE_RETIREMENT_AGE)
else:
    state_pension = 0

# Calcul et affichage des résultats
if st.button("Calculer la rente"):
    df = retirement_simulation(start_age, end_age, current_income, income_increase_rate,
                               current_spending, inflation_rate, initial_net_worth, investment_return_rate, retirement_age, investment_tax_rate,
                               state_pension, state_retirement_age)
    
    st.write("Résultats de la simulation")
    st.dataframe(df)
    
    # Graphique de l'évolution du patrimoine
    fig, ax = plt.subplots()
    ax.bar(df["Age"], df["Net Worth"], color='blue')
    ax.set_xlabel("Age")
    ax.set_ylabel("Patrimoine")
    ax.set_title("Évolution du patrimoine par âge")
    st.pyplot(fig)

    # Graphique du delta de patrimoine
    fig, ax = plt.subplots()
    colors = ['green' if x > 0 else 'red' for x in df["Delta Net Worth"]]
    ax.bar(df["Age"], df["Delta Net Worth"], color=colors)
    ax.set_xlabel("Age")
    ax.set_ylabel("Delta de Patrimoine")
    ax.set_title("Delta de Patrimoine par âge")
    st.pyplot(fig)

    # Graphique de l'évolution du patrimoine à euros constants
    df["Net Worth (euros constants)"] = df["Net Worth"]/(1+inflation_rate)**(df["Age"]-start_age)
    fig, ax = plt.subplots()
    ax.bar(df["Age"],df["Net Worth (euros constants)"] , color='blue')
    ax.set_xlabel("Age")
    ax.set_ylabel("Patrimoine")
    ax.set_title("Évolution du patrimoine à euros constants")
    st.pyplot(fig)


