import streamlit as st

st.set_page_config(page_title="Ecosystem Simulator", layout="wide")

st.markdown("### Ecosystem Banking – Anchor Simulation")

# ====================================================
# TOP: PLACEHOLDER FOR OUTPUTS (ALWAYS VISIBLE)
# ====================================================

results_placeholder = st.container()

st.markdown("---")

# ====================================================
# INPUTS – SINGLE ROW, 4 SECTIONS (CREDIT / CASA / RETAIL / WEALTH)
# ====================================================

col_credit, col_casa, col_retail, col_wealth = st.columns(4)

# ---------- CREDIT ----------
with col_credit:
    st.markdown("**Credit**")
    anchor_loan_cr = st.number_input(
        "Limit (₹ cr)",
        min_value=0.0, value=200.0, step=10.0, format="%.1f"
    )
    lending_rate = st.number_input(
        "Interest rate p.a.",
        min_value=0.00, max_value=0.20,
        value=0.09, step=0.005, format="%.3f"
    )
    processing_fee_pct = st.number_input(
        "Processing fee (%) – upfront",
        min_value=0.00, max_value=0.05,
        value=0.005, step=0.001, format="%.3f"
    )
    fee_amort_years = st.number_input(
        "Fee amortisation (years)",
        min_value=1, max_value=10, value=3, step=1
    )

# ---------- CASA ----------
with col_casa:
    st.markdown("**CASA (Salary)**")
    employees = st.number_input(
        "No. of employees",
        min_value=0, value=8000, step=100
    )
    salary_penetration = st.slider(
        "Salary account penetration (%)",
        min_value=0, max_value=100,
        value=70, step=5
    ) / 100.0
    avg_balance = st.number_input(
        "Avg balance per employee (₹)",
        min_value=0.0, value=20000.0,
        step=1000.0, format="%.0f"
    )
    casa_spread = st.number_input(
        "CASA spread (net p.a.)",
        min_value=0.0, max_value=0.15,
        value=0.045, step=0.005, format="%.3f"
    )

# ---------- RETAIL LOANS ----------
with col_retail:
    st.markdown("**Retail Loans to Employees**")
    retail_take_up = st.slider(
        "Retail loan take-up (% of employees)",
        min_value=0, max_value=100,
        value=15, step=5
    ) / 100.0
    retail_amount = st.number_input(
        "Avg retail loan per employee (₹)",
        min_value=0.0, value=400000.0,
        step=10000.0, format="%.0f"
    )
    retail_yield = st.number_input(
        "Retail yield p.a.",
        min_value=0.0, max_value=0.30,
        value=0.11, step=0.005, format="%.3f"
    )
    retail_cost = st.number_input(
        "Retail cost of funds p.a.",
        min_value=0.0, max_value=0.20,
        value=0.04, step=0.005, format="%.3f"
    )
    retail_fee_pct = st.number_input(
        "Retail processing fee (%)",
        min_value=0.0, max_value=0.10,
        value=0.01, step=0.002, format="%.3f"
    )

# ---------- WEALTH / INSURANCE / CMS ----------
with col_wealth:
    st.markdown("**Wealth, Insurance & CMS/APIs**")
    ins_penetration = st.slider(
        "Insurance penetration (% of employees)",
        min_value=0, max_value=100,
        value=20, step=5
    ) / 100.0
    ins_income_per_emp = st.number_input(
        "Insurance income / employee (₹ p.a.)",
        min_value=0.0, value=1200.0,
        step=100.0, format="%.0f"
    )
    wealth_penetration = st.slider(
        "Wealth penetration (% of employees)",
        min_value=0, max_value=100,
        value=10, step=5
    ) / 100.0
    wealth_income_per_emp = st.number_input(
        "Wealth income / employee (₹ p.a.)",
        min_value=0.0, value=1500.0,
        step=100.0, format="%.0f"
    )
    cms_income_cr = st.number_input(
        "CMS + Cards + APIs income (₹ crore p.a.)",
        min_value=0.0, value=1.30, step=0.10, format="%.2f"
    )

# ====================================================
# CALCULATIONS
# ====================================================

# Scenario 1 – Credit only
corporate_interest_income_cr = anchor_loan_cr * lending_rate
corporate_fee_income_cr = anchor_loan_cr * processing_fee_pct / fee_amort_years
scenario1_revenue_cr = corporate_interest_income_cr + corporate_fee_income_cr

# Scenario 2 – Ecosystem (credit + CASA + retail + wealth/insurance + CMS)
scenario2_corp_income_cr = corporate_interest_income_cr + corporate_fee_income_cr

# CASA
employees_on_us = employees * salary_penetration
casa_balance_cr = employees_on_us * avg_balance / 1e7  # ₹ → ₹ crore
casa_nii_cr = casa_balance_cr * casa_spread

# Retail
retail_customers = employees * retail_take_up
retail_book_cr = retail_customers * retail_amount / 1e7  # ₹ → ₹ crore
retail_nii_cr = retail_book_cr * (retail_yield - retail_cost)
retail_fee_cr = retail_book_cr * retail_fee_pct

# Wealth & Insurance
insurance_income_cr = employees * ins_penetration * ins_income_per_emp / 1e7
wealth_income_cr = employees * wealth_penetration * wealth_income_per_emp / 1e7

# Total Scenario 2 revenue
scenario2_revenue_cr = (
    scenario2_corp_income_cr
    + casa_nii_cr
    + retail_nii_cr
    + retail_fee_cr
    + insurance_income_cr
    + wealth_income_cr
    + cms_income_cr
)

incremental_revenue_cr = scenario2_revenue_cr - scenario1_revenue_cr

if anchor_loan_cr > 0:
    concession_pct = incremental_revenue_cr / anchor_loan_cr
else:
    concession_pct = 0.0

concession_bps = concession_pct * 10000
new_rate = max(lending_rate - concession_pct, 0)

# ====================================================
# FILL THE TOP RESULTS PLACEHOLDER
# ====================================================

with results_placeholder:
    r1, r2, r3, r4 = st.columns(4)

    with r1:
        st.markdown("**Scenario 1 – Credit Only**")
        st.metric(
            "Revenue (₹ cr p.a.)",
            f"{scenario1_revenue_cr:,.2f}"
        )
        st.caption(
            f"NII: ₹{corporate_interest_income_cr:,.2f} | "
            f"Fee: ₹{corporate_fee_income_cr:,.2f}"
        )

    with r2:
        st.markdown("**Scenario 2 – Ecosystem**")
        st.metric(
            "Revenue (₹ cr p.a.)",
            f"{scenario2_revenue_cr:,.2f}",
            delta=f"{incremental_revenue_cr:,.2f} cr"
        )
        st.caption(
            f"CASA NII: ₹{casa_nii_cr:,.2f} | Retail NII: ₹{retail_nii_cr:,.2f}"
        )

    with r3:
        st.markdown("**Fee & Non-Interest**")
        total_fee_other = retail_fee_cr + insurance_income_cr + wealth_income_cr + cms_income_cr
        st.metric(
            "Fee & other (₹ cr p.a.)",
            f"{total_fee_other:,.2f}"
        )
        st.caption(
            f"Retail fee: ₹{retail_fee_cr:,.2f} | "
            f"Ins+Wealth: ₹{(insurance_income_cr+wealth_income_cr):,.2f} | "
            f"CMS: ₹{cms_income_cr:,.2f}"
        )

    with r4:
        st.markdown("**Concession Capacity**")
        st.metric(
            "Max concession (bps)",
            f"{concession_bps:,.0f} bps"
        )
        st.caption(
            f"{lending_rate*100:.2f}% → {new_rate*100:.2f}% "
            f"(Δ {concession_pct*100:.2f}%)"
        )
