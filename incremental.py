import streamlit as st

st.set_page_config(page_title="Ecosystem – Concession Coverage", layout="wide")

st.write("### Ecosystem Banking – Concession vs Ecosystem Coverage")

# ====================================================
# TOP: CONCESSION SLIDER
# ====================================================

top_left, top_right = st.columns([2, 3])

with top_left:
    concession_bps = st.slider(
        "🎯 Concession requested (bps on base lending rate)",
        min_value=0, max_value=300, value=150, step=10,
    )
concession_pct = concession_bps / 10000.0

with top_right:
    st.caption(
        "Choose the concession in bps. The model shows how much is funded by the "
        "current ecosystem, how much extra ecosystem is needed, and whether it is feasible."
    )

# ====================================================
# INPUTS – 3 BLOCKS: CREDIT, ECOSYSTEM %, ECONOMICS
# ====================================================

col_credit, col_ecosystem, col_econ = st.columns(3)

# ---------- CREDIT BLOCK ----------
with col_credit:
    st.subheader("💳 Credit")
    anchor_loan_cr = st.number_input(
        "Corporate limit (₹ crore)",
        min_value=0.0, max_value=1_000_000.0,
        value=200.0, step=10.0, format="%.1f",
    )
    base_rate = st.number_input(
        "Base lending rate p.a.",
        min_value=0.00, max_value=0.20,
        value=0.09, step=0.005, format="%.3f",
    )
    processing_fee_pct = st.number_input(
        "Processing fee (%) – upfront",
        min_value=0.00, max_value=0.05,
        value=0.005, step=0.001, format="%.3f",
    )
    fee_amort_years = st.number_input(
        "Fee amortisation (years)",
        min_value=1, max_value=10,
        value=3, step=1,
    )

# ---------- ECOSYSTEM CURRENT vs MAX ----------
with col_ecosystem:
    st.subheader("🌐 Ecosystem – Current vs Max (%)")

    st.caption("Salary / CASA")
    salary_cur = st.slider("Current Salary a/c penetration", 0, 100, 60, 5) / 100.0
    salary_max = st.slider("Max Salary a/c penetration", 0, 100, 90, 5) / 100.0

    st.caption("Retail Loans")
    retail_cur = st.slider("Current Retail loan take-up", 0, 100, 10, 5) / 100.0
    retail_max = st.slider("Max Retail loan take-up", 0, 100, 25, 5) / 100.0

    st.caption("Insurance")
    ins_cur = st.slider("Current Insurance penetration", 0, 100, 8, 2) / 100.0
    ins_max = st.slider("Max Insurance penetration", 0, 100, 30, 5) / 100.0

    st.caption("Wealth")
    wealth_cur = st.slider("Current Wealth penetration", 0, 100, 5, 1) / 100.0
    wealth_max = st.slider("Max Wealth penetration", 0, 100, 20, 5) / 100.0

# ---------- ECONOMICS ----------
with col_econ:
    st.subheader("⚙️ Economics (per employee / per product)")
    employees = st.number_input(
        "No. of employees (ecosystem size)",
        min_value=0, max_value=1_000_000,
        value=8000, step=100,
    )

    st.caption("CASA")
    avg_balance = st.number_input(
        "Avg salary balance per employee (₹)",
        min_value=0.0, max_value=10_000_000.0,
        value=20000.0, step=1000.0, format="%.0f",
    )
    casa_spread = st.number_input(
        "CASA net spread p.a.",
        min_value=0.0, max_value=0.20,
        value=0.045, step=0.005, format="%.3f",
    )

    st.caption("Retail Loans")
    retail_amount = st.number_input(
        "Avg retail loan per employee (₹)",
        min_value=0.0, max_value=10_000_000.0,
        value=400000.0, step=10000.0, format="%.0f",
    )
    retail_yield = st.number_input(
        "Retail yield p.a.",
        min_value=0.0, max_value=0.30,
        value=0.11, step=0.005, format="%.3f",
    )
    retail_cost = st.number_input(
        "Retail cost of funds p.a.",
        min_value=0.0, max_value=0.20,
        value=0.04, step=0.005, format="%.3f",
    )
    retail_fee_pct = st.number_input(
        "Retail processing fee (%)",
        min_value=0.0, max_value=0.10,
        value=0.01, step=0.002, format="%.3f",
    )

    st.caption("Insurance / Wealth / CMS")
    ins_income_per_emp = st.number_input(
        "Insurance income / employee (₹ p.a.)",
        min_value=0.0, max_value=10_000_000.0,
        value=1200.0, step=100.0, format="%.0f",
    )
    wealth_income_per_emp = st.number_input(
        "Wealth income / employee (₹ p.a.)",
        min_value=0.0, max_value=10_000_000.0,
        value=1500.0, step=100.0, format="%.0f",
    )
    cms_income_cr = st.number_input(
        "CMS + Cards + APIs income (₹ crore p.a.)",
        min_value=0.0, max_value=10_000.0,
        value=1.30, step=0.10, format="%.2f",
    )

# ====================================================
# CALCULATIONS – CREDIT & ECOSYSTEM
# ====================================================

# Base credit income (no concession)
credit_nii_cr = anchor_loan_cr * base_rate
credit_fee_cr = anchor_loan_cr * processing_fee_pct / fee_amort_years
base_credit_income_cr = credit_nii_cr + credit_fee_cr

# Concession revenue loss (₹ cr)
revenue_loss_cr = anchor_loan_cr * concession_pct
new_rate = base_rate - concession_pct

# Helper: ecosystem income for given penetrations
def eco_income(p_salary, p_retail, p_ins, p_wealth):
    # CASA
    emp_salary = employees * p_salary
    casa_bal_cr = emp_salary * avg_balance / 1e7  # ₹ → ₹ crore
    casa_nii = casa_bal_cr * casa_spread

    # Retail
    emp_retail = employees * p_retail
    retail_book_cr = emp_retail * retail_amount / 1e7
    retail_nii = retail_book_cr * (retail_yield - retail_cost)
    retail_fee = retail_book_cr * retail_fee_pct

    # Insurance & Wealth
    ins_fee = employees * p_ins * ins_income_per_emp / 1e7
    wealth_fee = employees * p_wealth * wealth_income_per_emp / 1e7

    return casa_nii + retail_nii + retail_fee + ins_fee + wealth_fee

# Ecosystem income at current and max
eco_current_cr = eco_income(salary_cur, retail_cur, ins_cur, wealth_cur) + cms_income_cr
eco_max_cr = eco_income(salary_max, retail_max, ins_max, wealth_max) + cms_income_cr

# How much concession is funded in ₹-terms
concession_covered_by_current = min(revenue_loss_cr, eco_current_cr)
shortfall_cr = max(0.0, revenue_loss_cr - eco_current_cr)

incremental_potential_cr = max(0.0, eco_max_cr - eco_current_cr)

if incremental_potential_cr > 0:
    extra_share = shortfall_cr / incremental_potential_cr
else:
    extra_share = 0.0

# Clamp for required % calculation
extra_share_clamped = max(0.0, min(extra_share, 1.0))

# Required penetrations
req_salary = salary_cur + (salary_max - salary_cur) * extra_share_clamped
req_retail = retail_cur + (retail_max - retail_cur) * extra_share_clamped
req_ins = ins_cur + (ins_max - ins_cur) * extra_share_clamped
req_wealth = wealth_cur + (wealth_max - wealth_cur) * extra_share_clamped

# bps that current and max ecosystem can support
if anchor_loan_cr > 0:
    eco_current_supported_bps = eco_current_cr / anchor_loan_cr * 10000
    eco_max_supported_bps = eco_max_cr / anchor_loan_cr * 10000
else:
    eco_current_supported_bps = 0.0
    eco_max_supported_bps = 0.0

max_concession_bps = eco_max_supported_bps  # break-even if full ecosystem given

# Traffic light logic
if concession_bps <= eco_current_supported_bps + 1e-6:
    status = "GREEN"
    status_emoji = "🟢"
    status_msg = "Fully covered by current ecosystem"
    feasible = True
    # no extra ecosystem really needed
    req_salary = salary_cur
    req_retail = retail_cur
    req_ins = ins_cur
    req_wealth = wealth_cur
elif concession_bps <= eco_max_supported_bps + 1e-6:
    status = "AMBER"
    status_emoji = "🟡"
    status_msg = "Needs additional ecosystem commitment"
    feasible = True
else:
    status = "RED"
    status_emoji = "🔴"
    status_msg = "Not feasible even at max ecosystem"
    feasible = False
    # even pushing all levers to max won't fully cover
    req_salary = salary_max
    req_retail = retail_max
    req_ins = ins_max
    req_wealth = wealth_max

# Scenario 2 income if we actually grant the requested concession
eco_used_cr = eco_current_cr + incremental_potential_cr * min(extra_share, 1.0)
scenario2_income_cr = base_credit_income_cr - revenue_loss_cr + eco_used_cr

# ====================================================
# SUMMARY KPIs (INCLUDING BREAK-EVEN & TRAFFIC LIGHT)
# ====================================================

st.markdown("---")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Base credit income (₹ cr p.a.)", f"{base_credit_income_cr:,.2f}")

with k2:
    pct_covered_now = (concession_covered_by_current / revenue_loss_cr * 100) if revenue_loss_cr > 0 else 0
    st.metric(
        "Covered by current ecosystem",
        f"₹{concession_covered_by_current:,.2f} cr",
        help=f"{pct_covered_now:.1f}% of requested concession",
    )

with k3:
    st.metric(
        "Break-even concession (max bps)",
        f"{max_concession_bps:,.0f} bps",
        help="Maximum concession the full ecosystem (current + headroom) can support",
    )

with k4:
    if feasible:
        if status == "GREEN":
            delta_text = "No extra ecosystem needed"
        else:
            # how much of headroom used
            headroom_used_pct = extra_share_clamped * 100
            delta_text = f"Use {headroom_used_pct:.1f}% of remaining ecosystem headroom"
        st.metric(
            "Feasibility",
            f"{status_emoji} {status}",
            delta=delta_text,
        )
    else:
        st.metric(
            "Feasibility",
            f"{status_emoji} {status}",
            delta=f"Max support only ~{max_concession_bps:,.0f} bps",
        )

# ====================================================
# REQUIRED PENETRATIONS (CURRENT vs REQUIRED vs MAX)
# ====================================================

st.markdown("#### Ecosystem – Current vs Required vs Max")

c1, c2, c3, c4 = st.columns(4)

def penetration_block(col, name, cur, req, max_):
    with col:
        st.markdown(f"**{name}**")
        st.write(f"Current: **{cur*100:.1f}%**")
        st.write(f"Required: **{req*100:.1f}%**")
        st.write(f"Max: **{max_*100:.1f}%**")
        delta_pp = (req - cur) * 100
        if feasible:
            if delta_pp > 0.05:
                st.write(f"Extra commitment: **+{delta_pp:.1f} p.p.**")
            else:
                st.write("No additional commitment needed.")
        else:
            st.write("Even max is insufficient for this concession.")

penetration_block(c1, "🏦 Salary / CASA", salary_cur, req_salary, salary_max)
penetration_block(c2, "🏠 Retail Loans", retail_cur, req_retail, retail_max)
penetration_block(c3, "🛡 Insurance", ins_cur, req_ins, ins_max)
penetration_block(c4, "📈 Wealth", wealth_cur, req_wealth, wealth_max)
