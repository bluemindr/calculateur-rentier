import pandas as pd
from typing import Dict, Any

def compute_income(current_income: float, age: int, retirement_age: int, state_retirement_age: int, state_pension: float) -> float:
    """
    Computes the income for a given age.
    """
    income = 0.0
    if age >= state_retirement_age:
        income += state_pension

    if age >= retirement_age:
        return income
    else:
        return current_income + income

def update_income(current_income: float, rate_increase: float, age: int, retirement_age: int) -> float:
    """
    Updates the income based on the annual increase rate.
    """
    if age <= retirement_age:
        return current_income * (1 + rate_increase)
    return 0.0

def update_spending(current_spending: float, inflation_rate: float) -> float:
    """
    Updates the spending based on the inflation rate.
    """
    return current_spending * (1 + inflation_rate)

def update_net_worth(net_worth: float, income: float, spending: float, return_rate: float, age: int, investment_tax_rate: float, wealth_tax_rate: float, wealth_tax_threshold: float) -> float:
    """
    Updates the net worth based on income, spending, and investment returns.
    """
    wealth_tax = 0.0
    if net_worth > wealth_tax_threshold:
        wealth_tax = (net_worth - wealth_tax_threshold) * wealth_tax_rate

    s = spending - income + wealth_tax
    if s > 0:
        s = s / (1 - investment_tax_rate)

    new_worth = net_worth * (1 + return_rate) - s
    return max(new_worth, 0)

def retirement_simulation(start_age: int, end_age: int, current_income: float, income_increase_rate: float,
                          current_spending: float, inflation_rate: float, initial_net_worth: float,
                          investment_return_rate: float, retirement_age: int, investment_tax_rate: float,
                          state_pension: float, state_retirement_age: int, wealth_tax_rate: float, wealth_tax_threshold: float) -> pd.DataFrame:
    """
    Runs the retirement simulation.
    """
    age_range = range(start_age, end_age + 1)
    data: Dict[str, Any] = {
        "Age": age_range,
        "Income": [],
        "Spending": [],
        "Net Worth": [],
        "Delta Net Worth": []
    }

    net_worth = initial_net_worth
    for age in age_range:
        data["Income"].append(current_income)
        data["Spending"].append(current_spending)
        data["Net Worth"].append(net_worth)

        current_income_for_year = compute_income(current_income, age, retirement_age, state_retirement_age, state_pension)
        new_net_worth = update_net_worth(net_worth, current_income_for_year, current_spending, investment_return_rate, age, investment_tax_rate, wealth_tax_rate, wealth_tax_threshold)

        state_pension *= (1 + inflation_rate)
        current_spending = update_spending(current_spending, inflation_rate)
        current_income = update_income(current_income, income_increase_rate, age, retirement_age)
        wealth_tax_threshold *= (1 + inflation_rate)

        data["Delta Net Worth"].append(new_net_worth - net_worth)
        net_worth = new_net_worth

    df = pd.DataFrame(data)
    df["Net Worth (euros constants)"] = df["Net Worth"] / (1 + inflation_rate)**(df["Age"] - start_age)
    return df
