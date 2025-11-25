
import streamlit as st

st.set_page_config(page_title="Ecosystem Simulator", layout="wide")

# ------------------ GLOBAL STYLES ------------------ #
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* PAGE & TITLES */
        .block-container {
            padding-top: 2.2rem !important;
            padding-bottom: 0.5rem !important;
            max-width: 1400px !important;
        }

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }

        body {
            background: #f8fafc;
        }

        .main .block-container {
            background: transparent;
        }

        /* Add subtle background to main content area */
        .main {
            background: #f8fafc;
        }

        /* HEADER STYLING */
        h3 {
            font-weight: 700 !important;
            font-size: 1.5rem !important;
            margin-bottom: 0.25rem !important;
            margin-top: 0.5rem !important;
            color: #1e293b !important;
        }

        .section-title {
            font-weight: 600;
            font-size: 0.95rem;
            color: #1e293b;
            margin-bottom: 0.4rem;
            padding-bottom: 0.4rem;
            border-bottom: 2px solid #e2e8f0;
        }


        label {
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            color: #475569 !important;
        }

        /* Ensure all text is visible */
        .stSlider label {
            color: #475569 !important;
        }

        /* Slider value display */
        .stSlider > div > div > div > div + div {
            color: #1e293b !important;
        }

        /* CARD LOOK APPLIED TO EACH COLUMN */
        div[data-testid="column"] > div {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 12px;
            padding: 0.8rem 0.75rem 0.6rem 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: all 0.3s ease;
        }

        div[data-testid="column"] > div:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transform: translateY(-2px);
            border-color: #cbd5e1;
        }

        /* INPUT STYLING */
        .stNumberInput > div > div > input {
            background-color: #ffffff;
            border: 1.5px solid #e2e8f0;
            border-radius: 8px;
            padding: 0.5rem 0.75rem;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .stNumberInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            outline: none;
        }

        .stSlider > div > div > div {
            background-color: #e2e8f0;
        }

        .stSlider > div > div > div > div {
            background: #3b82f6;
        }

        /* METRIC STYLING */
        [data-testid="stMetricValue"] {
            color: #1e293b !important;
            font-size: 1.3rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #475569 !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
        }

        [data-testid="stMetricDelta"] {
            background-color: #e0f2fe !important;
            color: #0369a1 !important;
            border-radius: 6px !important;
            padding: 0.25rem 0.5rem !important;
            font-weight: 600 !important;
        }

        /* CAPTION STYLING */
        .stCaption {
            color: #64748b !important;
            font-size: 0.7rem !important;
        }

        /* Regular text styling */
        p, div, span {
            color: #1e293b !important;
        }

        /* Input value text */
        .stNumberInput input {
            color: #1e293b !important;
        }

        /* HIDE STREAMLIT BRANDING */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /*header {visibility: hidden;}*/

        /* SCROLLBAR STYLING */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }

        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }

    </style>
""", unsafe_allow_html=True)

# ====================================================
# HEADER TITLE
# ====================================================
st.markdown("### 🌐 Ecosystem Banking – Anchor Simulation")

# ====================================================
# KPI PLACEHOLDERS (Will be filled after calculations)
# ====================================================
kpi_placeholder = st.empty()

# ====================================================
# INPUTS – 4 CARDS
# ====================================================
st.markdown("### 📋 Input Parameters")
col_credit, col_casa, col_retail, col_wealth = st.columns(4)

# ---------- CREDIT ----------
with col_credit:
    st.markdown('<div class="section-title">💳 <strong>Credit</strong></div>', unsafe_allow_html=True)
    anchor_loan_cr = st.number_input("Limit (₹ crore)", 0.0, 9999.0, 200.0, 10.0, format="%.1f", key="credit_limit")
    lending_rate = st.number_input("Interest rate p.a.", 0.00, 0.20, 0.09, 0.005, format="%.3f", key="lending_rate")
    processing_fee_pct = st.number_input("Processing fee (%) – upfront", 0.00, 0.05, 0.005, 0.001, format="%.3f", key="processing_fee")
    fee_amort_years = st.number_input("Fee amortisation (years)", 1, 10, 3, 1, key="fee_amort")

# ---------- CASA ----------
with col_casa:
    st.markdown('<div class="section-title">🏦 <strong>CASA (Salary)</strong></div>', unsafe_allow_html=True)
    employees = st.number_input("No. of employees", 0, 1000000, 5000, 100, key="employees")
    salary_penetration = st.slider("Salary account penetration (%)", 0, 100, 0, 5, key="salary_pen") / 100.0
    avg_balance = st.number_input("Avg balance per employee (₹)", 0.0, 9999999.0, 50000.0, 1000.0, format="%.0f", key="avg_balance")
    casa_spread = st.number_input("CASA spread (net p.a.)", 0.0, 0.15, 0.045, 0.005, format="%.3f", key="casa_spread")

# ---------- RETAIL LOANS ----------
with col_retail:
    st.markdown('<div class="section-title">🏠 <strong>Retail Loans</strong></div>', unsafe_allow_html=True)
    retail_take_up = st.slider("Retail loan take-up (% of employees)", 0, 100, 0, 5, key="retail_takeup") / 100.0
    retail_amount = st.number_input("Avg retail loan per employee (₹)", 0.0, 9999999.0, 400000.0, 10000.0, format="%.0f", key="retail_amount")
    retail_yield = st.number_input("Retail yield p.a.", 0.0, 0.30, 0.11, 0.005, format="%.3f", key="retail_yield")
    retail_cost = st.number_input("Retail cost of funds p.a.", 0.0, 0.20, 0.04, 0.005, format="%.3f", key="retail_cost")
    retail_fee_pct = st.number_input("Retail processing fee (%)", 0.0, 0.10, 0.01, 0.002, format="%.3f", key="retail_fee")

# ---------- WEALTH / INSURANCE / CMS ----------
with col_wealth:
    st.markdown('<div class="section-title">📈 <strong>Wealth, Insurance & CMS/APIs</strong></div>', unsafe_allow_html=True)
    ins_penetration = st.slider("Insurance penetration (% of employees)", 0, 100, 0, 5, key="ins_pen") / 100.0
    ins_income_per_emp = st.number_input("Insurance income / employee (₹ p.a.)", 0.0, 9999999.0, 1200.0, 100.0, format="%.0f", key="ins_income")
    wealth_penetration = st.slider("Wealth penetration (% of employees)", 0, 100, 0, 5, key="wealth_pen") / 100.0
    wealth_income_per_emp = st.number_input("Wealth income / employee (₹ p.a.)", 0.0, 9999999.0, 1500.0, 100.0, format="%.0f", key="wealth_income")
    cms_income_cr = st.number_input("CMS + Cards + APIs income (₹ crore p.a.)", 0.0, 999.0, 0.0, 0.10, format="%.2f", key="cms_income")

# ====================================================
# CALCULATIONS
# ====================================================
corporate_interest_income_cr = anchor_loan_cr * lending_rate
corporate_fee_income_cr = anchor_loan_cr * processing_fee_pct / fee_amort_years
scenario1_revenue_cr = corporate_interest_income_cr + corporate_fee_income_cr

employees_on_us = employees * salary_penetration
casa_balance_cr = employees_on_us * avg_balance / 1e7
casa_nii_cr = casa_balance_cr * casa_spread

retail_customers = employees * retail_take_up
retail_book_cr = retail_customers * retail_amount / 1e7
retail_nii_cr = retail_book_cr * (retail_yield - retail_cost)
retail_fee_cr = retail_book_cr * retail_fee_pct

insurance_income_cr = employees * ins_penetration * ins_income_per_emp / 1e7
wealth_income_cr = employees * wealth_penetration * wealth_income_per_emp / 1e7

scenario2_revenue_cr = (
    scenario1_revenue_cr
    + casa_nii_cr
    + retail_nii_cr
    + retail_fee_cr
    + insurance_income_cr
    + wealth_income_cr
    + cms_income_cr
)
subsidy_share = st.slider("Useable ecosystem income (%)", 10, 80, 35, 5) / 100.0
incremental_revenue_cr = scenario2_revenue_cr - scenario1_revenue_cr
concession_pct = (incremental_revenue_cr * subsidy_share / anchor_loan_cr) if anchor_loan_cr > 0 else 0
concession_bps = concession_pct * 10000
new_rate = max(lending_rate - concession_pct, 0)
total_fee_other = retail_fee_cr + insurance_income_cr + wealth_income_cr + cms_income_cr

# ====================================================
# UPDATE KPI DISPLAY (At the top)
# ====================================================
with kpi_placeholder.container():
    k1, k2, k3, k4 = st.columns(4)
    with k1: 
        st.metric("📊 Scenario 1 – Credit Only", f"₹{scenario1_revenue_cr:,.2f} cr")
    with k2: 
        st.metric("🚀 Scenario 2 – Ecosystem", f"₹{scenario2_revenue_cr:,.2f} cr", delta=f"+₹{incremental_revenue_cr:,.2f} cr")
    with k3: 
        st.metric("💰 Fee & Non-interest", f"₹{total_fee_other:,.2f} cr")
    with k4:
        st.metric("📉 Max concession", f"{concession_bps:,.0f} bps")
        st.caption(f"Rate: {lending_rate*100:.2f}% → {new_rate*100:.2f}%")
=======
import streamlit as st

st.set_page_config(page_title="Ecosystem Simulator", layout="wide")

# ------------------ GLOBAL STYLES ------------------ #
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* PAGE & TITLES */
        .block-container {
            padding-top: 2.2rem !important;
            padding-bottom: 0.5rem !important;
            max-width: 1400px !important;
        }

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }

        body {
            background: #f8fafc;
        }

        .main .block-container {
            background: transparent;
        }

        /* Add subtle background to main content area */
        .main {
            background: #f8fafc;
        }

        /* HEADER STYLING */
        h3 {
            font-weight: 700 !important;
            font-size: 1.5rem !important;
            margin-bottom: 0.25rem !important;
            margin-top: 0.5rem !important;
            color: #1e293b !important;
        }

        .section-title {
            font-weight: 600;
            font-size: 0.95rem;
            color: #1e293b;
            margin-bottom: 0.4rem;
            padding-bottom: 0.4rem;
            border-bottom: 2px solid #e2e8f0;
        }


        label {
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            color: #475569 !important;
        }

        /* Ensure all text is visible */
        .stSlider label {
            color: #475569 !important;
        }

        /* Slider value display */
        .stSlider > div > div > div > div + div {
            color: #1e293b !important;
        }

        /* CARD LOOK APPLIED TO EACH COLUMN */
        div[data-testid="column"] > div {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 12px;
            padding: 0.8rem 0.75rem 0.6rem 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: all 0.3s ease;
        }

        div[data-testid="column"] > div:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            transform: translateY(-2px);
            border-color: #cbd5e1;
        }

        /* INPUT STYLING */
        .stNumberInput > div > div > input {
            background-color: #ffffff;
            border: 1.5px solid #e2e8f0;
            border-radius: 8px;
            padding: 0.5rem 0.75rem;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .stNumberInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            outline: none;
        }

        .stSlider > div > div > div {
            background-color: #e2e8f0;
        }

        .stSlider > div > div > div > div {
            background: #3b82f6;
        }

        /* METRIC STYLING */
        [data-testid="stMetricValue"] {
            color: #1e293b !important;
            font-size: 1.3rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #475569 !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
        }

        [data-testid="stMetricDelta"] {
            background-color: #e0f2fe !important;
            color: #0369a1 !important;
            border-radius: 6px !important;
            padding: 0.25rem 0.5rem !important;
            font-weight: 600 !important;
        }

        /* CAPTION STYLING */
        .stCaption {
            color: #64748b !important;
            font-size: 0.7rem !important;
        }

        /* Regular text styling */
        p, div, span {
            color: #1e293b !important;
        }

        /* Input value text */
        .stNumberInput input {
            color: #1e293b !important;
        }

        /* HIDE STREAMLIT BRANDING */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /*header {visibility: hidden;}*/

        /* SCROLLBAR STYLING */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }

        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }

    </style>
""", unsafe_allow_html=True)

# ====================================================
# HEADER TITLE
# ====================================================
st.markdown("### 🌐 Ecosystem Banking – Anchor Simulation")

# ====================================================
# KPI PLACEHOLDERS (Will be filled after calculations)
# ====================================================
kpi_placeholder = st.empty()

# ====================================================
# INPUTS – 4 CARDS
# ====================================================
st.markdown("### 📋 Input Parameters")
col_credit, col_casa, col_retail, col_wealth = st.columns(4)

# ---------- CREDIT ----------
with col_credit:
    st.markdown('<div class="section-title">💳 <strong>Credit</strong></div>', unsafe_allow_html=True)
    anchor_loan_cr = st.number_input("Limit (₹ crore)", 0.0, 9999.0, 200.0, 10.0, format="%.1f", key="credit_limit")
    lending_rate = st.number_input("Interest rate p.a.", 0.00, 0.20, 0.09, 0.005, format="%.3f", key="lending_rate")
    processing_fee_pct = st.number_input("Processing fee (%) – upfront", 0.00, 0.05, 0.005, 0.001, format="%.3f", key="processing_fee")
    fee_amort_years = st.number_input("Fee amortisation (years)", 1, 10, 3, 1, key="fee_amort")

# ---------- CASA ----------
with col_casa:
    st.markdown('<div class="section-title">🏦 <strong>CASA (Salary)</strong></div>', unsafe_allow_html=True)
    employees = st.number_input("No. of employees", 0, 1000000, 5000, 100, key="employees")
    salary_penetration = st.slider("Salary account penetration (%)", 0, 100, 0, 5, key="salary_pen") / 100.0
    avg_balance = st.number_input("Avg balance per employee (₹)", 0.0, 9999999.0, 50000.0, 1000.0, format="%.0f", key="avg_balance")
    casa_spread = st.number_input("CASA spread (net p.a.)", 0.0, 0.15, 0.045, 0.005, format="%.3f", key="casa_spread")

# ---------- RETAIL LOANS ----------
with col_retail:
    st.markdown('<div class="section-title">🏠 <strong>Retail Loans</strong></div>', unsafe_allow_html=True)
    retail_take_up = st.slider("Retail loan take-up (% of employees)", 0, 100, 0, 5, key="retail_takeup") / 100.0
    retail_amount = st.number_input("Avg retail loan per employee (₹)", 0.0, 9999999.0, 400000.0, 10000.0, format="%.0f", key="retail_amount")
    retail_yield = st.number_input("Retail yield p.a.", 0.0, 0.30, 0.11, 0.005, format="%.3f", key="retail_yield")
    retail_cost = st.number_input("Retail cost of funds p.a.", 0.0, 0.20, 0.04, 0.005, format="%.3f", key="retail_cost")
    retail_fee_pct = st.number_input("Retail processing fee (%)", 0.0, 0.10, 0.01, 0.002, format="%.3f", key="retail_fee")

# ---------- WEALTH / INSURANCE / CMS ----------
with col_wealth:
    st.markdown('<div class="section-title">📈 <strong>Wealth, Insurance & CMS/APIs</strong></div>', unsafe_allow_html=True)
    ins_penetration = st.slider("Insurance penetration (% of employees)", 0, 100, 0, 5, key="ins_pen") / 100.0
    ins_income_per_emp = st.number_input("Insurance income / employee (₹ p.a.)", 0.0, 9999999.0, 1200.0, 100.0, format="%.0f", key="ins_income")
    wealth_penetration = st.slider("Wealth penetration (% of employees)", 0, 100, 0, 5, key="wealth_pen") / 100.0
    wealth_income_per_emp = st.number_input("Wealth income / employee (₹ p.a.)", 0.0, 9999999.0, 1500.0, 100.0, format="%.0f", key="wealth_income")
    cms_income_cr = st.number_input("CMS + Cards + APIs income (₹ crore p.a.)", 0.0, 999.0, 0.0, 0.10, format="%.2f", key="cms_income")

# ====================================================
# CALCULATIONS
# ====================================================
corporate_interest_income_cr = anchor_loan_cr * lending_rate
corporate_fee_income_cr = anchor_loan_cr * processing_fee_pct / fee_amort_years
scenario1_revenue_cr = corporate_interest_income_cr + corporate_fee_income_cr

employees_on_us = employees * salary_penetration
casa_balance_cr = employees_on_us * avg_balance / 1e7
casa_nii_cr = casa_balance_cr * casa_spread

retail_customers = employees * retail_take_up
retail_book_cr = retail_customers * retail_amount / 1e7
retail_nii_cr = retail_book_cr * (retail_yield - retail_cost)
retail_fee_cr = retail_book_cr * retail_fee_pct

insurance_income_cr = employees * ins_penetration * ins_income_per_emp / 1e7
wealth_income_cr = employees * wealth_penetration * wealth_income_per_emp / 1e7

scenario2_revenue_cr = (
    scenario1_revenue_cr
    + casa_nii_cr
    + retail_nii_cr
    + retail_fee_cr
    + insurance_income_cr
    + wealth_income_cr
    + cms_income_cr
)
subsidy_share = st.slider("Useable ecosystem income (%)", 10, 80, 35, 5) / 100.0
incremental_revenue_cr = scenario2_revenue_cr - scenario1_revenue_cr
concession_pct = (incremental_revenue_cr * subsidy_share / anchor_loan_cr) if anchor_loan_cr > 0 else 0
concession_bps = concession_pct * 10000
new_rate = max(lending_rate - concession_pct, 0)
total_fee_other = retail_fee_cr + insurance_income_cr + wealth_income_cr + cms_income_cr

# ====================================================
# UPDATE KPI DISPLAY (At the top)
# ====================================================
with kpi_placeholder.container():
    k1, k2, k3, k4 = st.columns(4)
    with k1: 
        st.metric("📊 Scenario 1 – Credit Only", f"₹{scenario1_revenue_cr:,.2f} cr")
    with k2: 
        st.metric("🚀 Scenario 2 – Ecosystem", f"₹{scenario2_revenue_cr:,.2f} cr", delta=f"+₹{incremental_revenue_cr:,.2f} cr")
    with k3: 
        st.metric("💰 Fee & Non-interest", f"₹{total_fee_other:,.2f} cr")
    with k4:
        st.metric("📉 Max concession", f"{concession_bps:,.0f} bps")
        st.caption(f"Rate: {lending_rate*100:.2f}% → {new_rate*100:.2f}%")

