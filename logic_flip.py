import streamlit as st

st.set_page_config(page_title="Ecosystem Concession Simulator", layout="wide")

# ------------------ GLOBAL STYLES ------------------ #
st.markdown("""
    <style>
        .block-container {
            padding-top: 1.6rem !important;
            padding-bottom: 0.5rem !important;
        }

        body {
            background-color: #f5f7fb;
        }

        .section-title {
            font-weight: 600;
            font-size: 0.9rem;
            color: #334155;
            margin-bottom: 0.25rem;
        }

        .header-line {
            border-bottom: 1px solid #e2e8f0;
            margin-top: 0.2rem;
            margin-bottom: 0.4rem;
        }

        label {
            font-size: 0.82rem !important;
        }

        /* Card look for input columns */
        div[data-testid="column"] > div {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.6rem;
            padding: 0.6rem 0.75rem 0.5rem 0.75rem;
        }

        /* Sticky header (title + slider + KPIs) */
        .sticky-kpi {
            position: sticky;
            top: 0;
            z-index: 999;
            background-color: #f5f7fb;
            padding-top: 0.4rem;
            padding-bottom: 0.4rem;
        }
    </style>
""", unsafe_allow_html=True)

# ====================================================
# STICKY HEADER CONTAINER (WE'LL FILL IT IN TWO STEPS)
# ====================================================

sticky_header = st.container()

# ====================================================
# 1) FIRST PART OF STICKY HEADER: TITLE + SLIDER
#    (we also read concession here so we can use it below)
# ====================================================

with sticky_header:
    st.markdown('<div class="sticky-kpi">', unsafe_allow_html=True)

    # Title
    st.markdown("### 🌐 Ecosystem Banking – Concession-led Simulation")
    st.markdown('<div class="header-line"></div>', unsafe_allow_html=True)

    # Slider row
    top_left, top_right = st.columns([2, 2])
    with top_left:
        concession_bps_input = st.slider(
            "🎯 Concession requested (bps on base rate)",
            min_value=0, max_value=300, value=150, step=10, key="concession_slider"
        )
    with top_right:
        st.caption("Move the slider to see what level of CASA, Retail, Insurance and Wealth is needed to fund this concession.")

# convert concession slider to percentage
concession_pct = concession_bps_input / 10000.0

# ====================================================
# INPUTS – CREDIT + ASSUMPTIONS + ECONOMICS (4 CARDS BELOW)
# ====================================================

col_credit, col_assump, col_casa_retail, col_fee = st.columns(4)

# ---------- CREDIT ----------
with col_credit:
    st.markdown('<div class="section-title">💳 Credit</div>', unsafe_allow_html=True)
    anchor_loan_cr = st.number_input(
        "Corporate limit (₹ crore)",
        min_value=0.0, max_value=1_000_000.0,
        value=200.0, step=10.0, format="%.1f"
    )
    base_rate = st.number_input(
        "Base lending rate p.a.",
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
        min_value=1, max_value=10,
        value=3, step=1
    )

# ---------- STRUCTURAL ASSUMPTIONS ----------
with col_assump:
    st.markdown('<div class="section-title">⚙️ Structural Assumptions</div>', unsafe_allow_html=True)
    employees = st.number_input(
        "No. of employees (ecosystem size)",
        min_value=0, max_value=1_000_000,
        value=8000, step=100
    )

    st.caption("Max achievable penetration (if everything goes very well):")
    max_salary_pen = st.slider(
        "Max Salary account penetration (%)",
        min_value=0, max_value=100, value=90, step=5
    ) / 100.0
    max_retail_take = st.slider(
        "Max Retail loan take-up (% of employees)",
        min_value=0, max_value=100, value=25, step=5
    ) / 100.0
    max_ins_pen = st.slider(
        "Max Insurance penetration (% of employees)",
        min_value=0, max_value=100, value=30, step=5
    ) / 100.0
    max_wealth_pen = st.slider(
        "Max Wealth penetration (% of employees)",
        min_value=0, max_value=100, value=20, step=5
    ) / 100.0

# ---------- CASA & RETAIL ECONOMICS ----------
with col_casa_retail:
    st.markdown('<div class="section-title">🏦 CASA & 🏠 Retail Economics</div>', unsafe_allow_html=True)
    avg_balance = st.number_input(
        "Avg salary balance per employee (₹)",
        min_value=0.0, max_value=10_000_000.0,
        value=20000.0, step=1000.0, format="%.0f"
    )
    casa_spread = st.number_input(
        "CASA net spread p.a.",
        min_value=0.0, max_value=0.15,
        value=0.045, step=0.005, format="%.3f"
    )

    retail_amount = st.number_input(
        "Avg retail loan per employee (₹)",
        min_value=0.0, max_value=10_000_000.0,
        value=400000.0, step=10000.0, format="%.0f"
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

# ---------- FEE: WEALTH / INSURANCE / CMS ----------
with col_fee:
    st.markdown('<div class="section-title">📈 Fee – Wealth / Insurance / CMS</div>', unsafe_allow_html=True)
    ins_income_per_emp = st.number_input(
        "Insurance income / employee (₹ p.a.)",
        min_value=0.0, max_value=10_000_000.0,
        value=1200.0, step=100.0, format="%.0f"
    )
    wealth_income_per_emp = st.number_input(
        "Wealth income / employee (₹ p.a.)",
        min_value=0.0, max_value=10_000_000.0,
        value=1500.0, step=100.0, format="%.0f"
    )
    cms_income_cr = st.number_input(
        "CMS + Cards + APIs income (₹ crore p.a.)",
        min_value=0.0, max_value=10_000.0,
        value=1.30, step=0.10, format="%.2f"
    )

# ====================================================
# CALCULATIONS – BASE & MAX ECOSYSTEM
# ====================================================

# Base credit income
corporate_interest_income_cr = anchor_loan_cr * base_rate
corporate_fee_income_cr = anchor_loan_cr * processing_fee_pct / fee_amort_years
scenario1_revenue_cr = corporate_interest_income_cr + corporate_fee_income_cr

# Revenue loss from concession
revenue_loss_cr = anchor_loan_cr * concession_pct
new_rate = base_rate - concession_pct

# Max ecosystem potential (if all levers max)
# CASA max
employees_on_us_max = employees * max_salary_pen
casa_balance_cr_max = employees_on_us_max * avg_balance / 1e7
casa_nii_cr_max = casa_balance_cr_max * casa_spread

# Retail max
retail_customers_max = employees * max_retail_take
retail_book_cr_max = retail_customers_max * retail_amount / 1e7
retail_nii_cr_max = retail_book_cr_max * (retail_yield - retail_cost)
retail_fee_cr_max = retail_book_cr_max * retail_fee_pct

# Insurance + Wealth max
insurance_income_cr_max = employees * max_ins_pen * ins_income_per_emp / 1e7
wealth_income_cr_max = employees * max_wealth_pen * wealth_income_per_emp / 1e7

incremental_ecosystem_max_cr = (
    casa_nii_cr_max
    + retail_nii_cr_max
    + retail_fee_cr_max
    + insurance_income_cr_max
    + wealth_income_cr_max
    + cms_income_cr
)

# Required scale factor s
if incremental_ecosystem_max_cr > 0:
    scale_s = revenue_loss_cr / incremental_ecosystem_max_cr
else:
    scale_s = 0.0

feasible = scale_s <= 1.0
scale_s_display = max(0.0, min(scale_s, 2.0))

# Required penetrations (scaled)
required_salary_pen = max_salary_pen * scale_s_display
required_retail_take = max_retail_take * scale_s_display
required_ins_pen = max_ins_pen * scale_s_display
required_wealth_pen = max_wealth_pen * scale_s_display

incremental_ecosystem_used_cr = incremental_ecosystem_max_cr * min(scale_s, 1.0)
scenario2_revenue_cr = scenario1_revenue_cr - revenue_loss_cr + incremental_ecosystem_used_cr

# ====================================================
# 2) SECOND PART OF STICKY HEADER: KPIs
#    (appended AFTER slider, still inside sticky div)
# ====================================================

with sticky_header:
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "Base credit income (₹ cr p.a.)",
            f"{scenario1_revenue_cr:,.2f}"
        )

    with k2:
        st.metric(
            "Concession requested",
            f"{concession_bps_input} bps",
            delta=f"-₹{revenue_loss_cr:,.2f} cr"
        )

    with k3:
        if feasible:
            st.metric(
                "Ecosystem potential used",
                f"{scale_s*100:,.1f}% of max"
            )
        else:
            st.metric(
                "Ecosystem potential used",
                "100%+",
                delta="Not enough"
            )

    with k4:
        if feasible:
            st.metric(
                "New lending rate",
                f"{new_rate*100:.2f} %",
                delta=f"-{concession_bps_input} bps"
            )
        else:
            st.metric(
                "New lending rate (requested)",
                f"{new_rate*100:.2f} %",
                delta="Not fully covered"
            )

    # close sticky wrapper
    st.markdown("</div>", unsafe_allow_html=True)

# ====================================================
# REQUIRED PENETRATIONS SUMMARY
# ====================================================

st.markdown("#### Required Ecosystem Penetration to Support Requested Concession")

col_req1, col_req2, col_req3, col_req4 = st.columns(4)

with col_req1:
    st.markdown("**🏦 Salary / CASA**")
    st.write(f"Max Salary penetration: **{max_salary_pen*100:.1f}%**")
    if feasible:
        st.write(f"Required Salary penetration: **{required_salary_pen*100:.1f}%**")
    else:
        st.write(f"Even **{max_salary_pen*100:.1f}%** is not enough.")

with col_req2:
    st.markdown("**🏠 Retail Loans**")
    st.write(f"Max Retail take-up: **{max_retail_take*100:.1f}%**")
    if feasible:
        st.write(f"Required Retail take-up: **{required_retail_take*100:.1f}%**")
    else:
        st.write(f"Even **{max_retail_take*100:.1f}%** is not enough.")

with col_req3:
    st.markdown("**🛡 Insurance**")
    st.write(f"Max Insurance penetration: **{max_ins_pen*100:.1f}%**")
    if feasible:
        st.write(f"Required Insurance penetration: **{required_ins_pen*100:.1f}%**")
    else:
        st.write(f"Even **{max_ins_pen*100:.1f}%** is not enough.")

with col_req4:
    st.markdown("**📈 Wealth**")
    st.write(f"Max Wealth penetration: **{max_wealth_pen*100:.1f}%**")
    if feasible:
        st.write(f"Required Wealth penetration: **{required_wealth_pen*100:.1f}%**")
    else:
        st.write(f"Even **{max_wealth_pen*100:.1f}%** is not enough.")

if not feasible:
    st.warning(
        "With the current assumptions, the requested concession cannot be fully "
        "funded even if CASA, Retail, Insurance and Wealth all reach their maximum penetration."
    )
