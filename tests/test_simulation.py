import numpy as np
import pandas as pd
from simulation import retirement_simulation, compute_income

def test_retirement_simulation_columns():
    df = retirement_simulation(
        start_age=30,
        end_age=30,
        current_income=60000,
        income_increase_rate=0.02,
        current_spending=40000,
        inflation_rate=0.02,
        initial_net_worth=100000,
        investment_return_rate=0.05,
        retirement_age=65,
        investment_tax_rate=0.3,
        state_pension=0,
        state_retirement_age=67,
        wealth_tax_rate=0,
        wealth_tax_threshold=0
    )
    expected_columns = ["Age", "Income", "Spending", "Net Worth", "Delta Net Worth", "Net Worth (euros constants)"]
    assert all(col in df.columns for col in expected_columns)

def test_retirement_simulation_initial_values():
    df = retirement_simulation(
        start_age=30,
        end_age=30,
        current_income=60000,
        income_increase_rate=0.02,
        current_spending=40000,
        inflation_rate=0.02,
        initial_net_worth=100000,
        investment_return_rate=0.05,
        retirement_age=65,
        investment_tax_rate=0.3,
        state_pension=0,
        state_retirement_age=67,
        wealth_tax_rate=0,
        wealth_tax_threshold=0
    )
    assert df.iloc[0]["Age"] == 30
    assert df.iloc[0]["Income"] == 60000
    assert df.iloc[0]["Spending"] == 40000
    assert df.iloc[0]["Net Worth"] == 100000

def test_compute_income_before_retirement():
    income = compute_income(60000, 40, 65, 67, 20000)
    assert income == 60000

def test_compute_income_after_retirement():
    income = compute_income(0, 66, 65, 67, 20000)
    assert income == 0

def test_compute_income_after_state_retirement():
    income = compute_income(0, 68, 65, 67, 20000)
    assert income == 20000
