
# StreamHub 2024 — Public Streaming Analytics Dashboard (CSV-based)
# Author: Deepa Mallipeddi (@mdeepa12)
# Deploy on Streamlit Cloud: https://share.streamlit.io/

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="StreamHub 2024 — Retention & Revenue", page_icon="🎬", layout="wide")

DATA_DIR = Path(".")
REGION_COORDS = {"US":{"lat":37.0902,"lon":-95.7129},"IN":{"lat":20.5937,"lon":78.9629},"GB":{"lat":55.3781,"lon":-3.4360},"CA":{"lat":56.1304,"lon":-106.3468},"AU":{"lat":-25.2744,"lon":133.7751}}

@st.cache_data
def load_csvs(retention_path: str, arpu_path: str):
    r = pd.read_csv(retention_path)
    a = pd.read_csv(arpu_path)
    r["cohort_month"] = pd.to_datetime(r["cohort_month"])
    a["cohort_month"] = pd.to_datetime(a["cohort_month"])
    if "retention_pct" not in r.columns and "retention" in r.columns:
        r = r.rename(columns={"retention": "retention_pct"})
    return r, a

def kpi_card(label, value, help_text=""):
    st.markdown(f"""
    <div style="background-color:#0f172a; border:1px solid #1f2937; padding:16px; border-radius:12px;">
        <div style="color:#94a3b8; font-size:14px;">{label}</div>
        <div style="color:white; font-size:28px; font-weight:700; margin-top:4px;">{value}</div>
        <div style="color:#94a3b8; font-size:12px; margin-top:6px;">{help_text}</div>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎬 StreamHub 2024")
    st.caption("Public dashboard — retention & revenue analytics (CSV-based)")
    retention_file = st.file_uploader("Upload retention_by_plan_region.csv", type=["csv"], key="ret_csv")
    arpu_file = st.file_uploader("Upload arpu_by_plan_region.csv", type=["csv"], key="arpu_csv")
    st.divider()
    st.markdown("**Filters**")

ret_path = DATA_DIR / "retention_by_plan_region.csv"
arpu_path = DATA_DIR / "arpu_by_plan_region.csv"

if retention_file and arpu_file:
    retention_df = pd.read_csv(retention_file)
    arpu_df = pd.read_csv(arpu_file)
    retention_df["cohort_month"] = pd.to_datetime(retention_df["cohort_month"])
    arpu_df["cohort_month"] = pd.to_datetime(arpu_df["cohort_month"])
elif ret_path.exists() and arpu_path.exists():
    retention_df, arpu_df = load_csvs(str(ret_path), str(arpu_path))
else:
    st.warning("CSV files not found. Upload: retention_by_plan_region.csv & arpu_by_plan_region.csv")
    st.stop()

with st.sidebar:
    regions = sorted(retention_df["region"].dropna().unique().tolist())
    plans = sorted(retention_df["plan_type"].dropna().unique().tolist())
    sel_regions = st.multiselect("Region", regions, default=regions)
    sel_plans = st.multiselect("Plan Type", plans, default=plans)
    week_max = int(retention_df["week_number"].max())
    sel_weeks = st.slider("Weeks since signup", 0, week_max, (0, min(12, week_max)))

rdf = retention_df.query("region in @sel_regions and plan_type in @sel_plans and @sel_weeks[0] <= week_number <= @sel_weeks[1]")
adf = arpu_df.query("region in @sel_regions and plan_type in @sel_plans")

st.markdown('<h1 style="color:white;margin:0;">StreamHub 2024 — Retention & Revenue Analytics</h1>', unsafe_allow_html=True)
st.caption("Interactive public dashboard powered by CSV exports. Use the sidebar to filter by region and plan.")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
try:
    cohort_sizes = (retention_df[retention_df["week_number"] == 0].groupby(["plan_type","region","cohort_month"])["retention_pct"].count().sum())
except Exception:
    cohort_sizes = np.nan
median_ret = rdf.groupby(["plan_type"])["retention_pct"].mean().mean() if not rdf.empty else 0.0
avg_arpu = adf["arpu_retained_d30"].mean() if "arpu_retained_d30" in adf.columns and not adf.empty else 0.0
total_rev = adf["revenue_from_retained"].sum() if "revenue_from_retained" in adf.columns else np.nan

with kpi_col1: kpi_card("Total Cohort Groups", f"{int(cohort_sizes):,}" if not np.isnan(cohort_sizes) else "—", "Cohorts at week 0 across region × plan")
with kpi_col2: kpi_card("Median Retention (%)", f"{median_ret:,.2f}%", f"Weeks {sel_weeks[0]}–{sel_weeks[1]}")
with kpi_col3: kpi_card("Avg ARPU (D30 Retained)", f"${avg_arpu:,.2f}", "Across selected regions & plans")
with kpi_col4: kpi_card("Revenue (Retained Users)", f"${(total_rev or 0):,.0f}", "Sum of retained-user revenue in selection")

st.divider()

c1, c2 = st.columns((1.1, 1))
with c1:
    st.subheader("Retention Curves by Plan")
    rc = rdf.groupby(["plan_type","week_number"])["retention_pct"].mean().reset_index()
    if rc.empty:
        st.info("No data for the selected filters.")
    else:
        fig = px.line(rc, x="week_number", y="retention_pct", color="plan_type", markers=True,
                      labels={"week_number":"Weeks Since Signup","retention_pct":"Retention (%)","plan_type":"Plan"})
        fig.update_layout(margin=dict(l=0,r=0,t=30,b=0), template="plotly_dark", legend_title_text="Plan")
        st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Cohort Retention Heatmap")
    heat = (rdf.groupby(["cohort_month","week_number"])["retention_pct"].mean()
            .reset_index().pivot(index="cohort_month", columns="week_number", values="retention_pct").sort_index())
    if heat.empty:
        st.info("No data for the selected filters.")
    else:
        fig = px.imshow(heat, color_continuous_scale="Teal", labels=dict(color="Retention %"), aspect="auto")
        fig.update_layout(margin=dict(l=0,r=0,t=30,b=0), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

st.divider()

c3, c4 = st.columns((1, 1.1))
with c3:
    st.subheader("ARPU (D30 Retained) by Plan × Region")
    if "arpu_retained_d30" not in adf.columns or adf.empty:
        st.info("ARPU data not available for current filters.")
    else:
        bar = adf.groupby(["region","plan_type"])["arpu_retained_d30"].mean().reset_index()
        fig = px.bar(bar, x="plan_type", y="arpu_retained_d30", color="region", barmode="group",
                     labels={"plan_type":"Plan","arpu_retained_d30":"ARPU (USD)"})
        fig.update_layout(margin=dict(l=0,r=0,t=30,b=0), template="plotly_dark", legend_title_text="Region")
        st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("User/Revenue Distribution by Region")
    users_region = (rdf[rdf["week_number"] == 0].groupby("region")["retention_pct"].count().rename("cohorts").reset_index())
    rev_region = (adf.groupby("region")["revenue_from_retained"].sum().rename("revenue").reset_index()
                  if "revenue_from_retained" in adf.columns else pd.DataFrame(columns=["region","revenue"]))
    geo = pd.merge(users_region, rev_region, on="region", how="outer").fillna(0)
    if geo.empty:
        st.info("No regional aggregates available for current filters.")
    else:
        geo["lat"] = geo["region"].map(lambda r: REGION_COORDS.get(r, {}).get("lat"))
        geo["lon"] = geo["region"].map(lambda r: REGION_COORDS.get(r, {}).get("lon"))
        fig = px.scatter_geo(geo, lat="lat", lon="lon", hover_name="region",
                             size="cohorts", color="revenue",
                             color_continuous_scale="Teal", projection="natural earth")
        fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Automated Insights")
insights = []
week_8 = rdf[rdf["week_number"] == 8].groupby("plan_type")["retention_pct"].mean().sort_values(ascending=False)
if not week_8.empty:
    top_plan, bottom_plan = week_8.index[0], week_8.index[-1]
    gap = float(week_8.iloc[0] - week_8.iloc[-1])
    insights.append(f"At Week 8, **{top_plan}** retains higher than **{bottom_plan}** by **{gap:.1f} pp**.")
if "arpu_retained_d30" in adf.columns and not adf.empty:
    reg_arpu = adf.groupby("region")["arpu_retained_d30"].mean().sort_values(ascending=False)
    if len(reg_arpu) > 0:
        insights.append(f"**{reg_arpu.index[0]}** shows the highest ARPU among selected regions at **${reg_arpu.iloc[0]:.2f}**.")
cohort_rows = len(rdf[rdf['week_number'] == 0])
insights.append(f"Selection includes **{cohort_rows}** cohort-month groups at Week 0 across {len(sel_regions)} region(s) and {len(sel_plans)} plan(s).")
if insights:
    for i in insights: st.markdown(f"- {i}")
else:
    st.info("Adjust filters to see data-driven insights.")
st.caption("© 2024 StreamHub (Synthetic Data). Built with Streamlit + Plotly.")
