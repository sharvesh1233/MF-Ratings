import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MF Rating System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0d1117; color: #e6edf3; }
h1, h2, h3 { font-family: 'DM Serif Display', serif; }
.main { background-color: #0d1117; }
section[data-testid="stSidebar"] { background: #161b22; border-right: 1px solid #30363d; }
.page-header { background: linear-gradient(90deg, #161b22 0%, #1c2128 100%); border: 1px solid #30363d; border-radius: 14px; padding: 28px 32px; margin-bottom: 24px; }
.stars { color: #f0b429; font-size: 20px; }
.stars-grey { color: #3d444d; font-size: 20px; }
hr { border-color: #30363d; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_from_drive(gdrive_url):
    try:
        file_id = gdrive_url.split("/d/")[1].split("/")[0]
        direct = f"https://drive.google.com/uc?export=download&id={file_id}"
        df = pd.read_excel(direct, engine="openpyxl")
        df.columns = df.columns.str.strip()  # remove hidden spaces
        return df
    except Exception as e:
        st.error(f"Could not load from Google Drive: {e}")
        return None


# ─────────────────────────────────────────────
# RATING ENGINE
# ─────────────────────────────────────────────
def percentile_score(series, weights):
    """Assigns score based on quartile rank. Higher value = better."""
    ranks = series.rank(ascending=False, method='min')
    n = len(series)
    scores = pd.Series(index=series.index, dtype=float)
    for idx in series.index:
        pct = ranks[idx] / n
        if pct <= 0.25:
            scores[idx] = weights[0]
        elif pct <= 0.50:
            scores[idx] = weights[1]
        elif pct <= 0.75:
            scores[idx] = weights[2]
        else:
            scores[idx] = weights[3]
    return scores / 100


def compute_ratings(df_raw):
    df = df_raw.copy()
    df.columns = df.columns.str.strip()

    # Exclude funds younger than 5 years
    df = df[pd.to_numeric(df['Age (From Incept Date)'], errors='coerce') >= 5].copy()

    if df.empty:
        st.error("No funds with Age >= 5 years found. Check your 'Age (From Incept Date)' column.")
        st.stop()

    # Category averages
    cat_avg_cols = [
        'Std. Deviation', 'Beta', 'Jensen Alpha', 'Sharpe Ratio', 'Sortino',
        'Information Ratio', 'Up/Down Capture Ratio', 'Top 5 Stocks (%)',
        '3YR_1D', '3YR_1M', '3YR_1Y', '5Y_1D', '5Y_1M', '5Y_1Y',
        '10Y_1D', '10Y_1M', '10Y_1Y',
        '1YEAR_CAGR', '3YEAR_CAGR', '5YEAR_CAGR', '10YEAR_CAGR',
        'Scheme AUM', 'Total Equity Stocks Count', 'Total Sector Count', 'Turnover Ratio (%)'
    ]
    existing = [c for c in cat_avg_cols if c in df.columns]
    cat_avgs = df.groupby('Category')[existing].transform('mean')

    # ── QUANTITATIVE ──────────────────────────────────────────────

    # Std Deviation & Beta: lower = better
    df['s_StdDev'] = np.where(df['Std. Deviation'] < cat_avgs['Std. Deviation'], 0.025, 0.005)
    df['s_Beta']   = np.where(df['Beta'] < cat_avgs['Beta'], 0.025, 0.005)

    # Percentile-based metrics
    for col, sname, w in [
        ('Jensen Alpha',          's_JAlpha',  [10, 7, 4, 2]),
        ('Sharpe Ratio',          's_Sharpe',  [10, 7, 4, 2]),
        ('Sortino',               's_Sortino', [10, 7, 4, 2]),
        ('Up/Down Capture Ratio', 's_UpDown',  [10, 7, 4, 2]),
    ]:
        diff = df[col] - cat_avgs[col]
        df[sname] = diff.groupby(df['Category']).transform(
            lambda x: percentile_score(x, w)
        )

    # Information Ratio
    df['s_IR'] = np.where(df['Information Ratio'] > cat_avgs['Information Ratio'] * 1.70, 0.02,
                 np.where(df['Information Ratio'] > cat_avgs['Information Ratio'] * 1.50, 0.01,
                 np.where(df['Information Ratio'] > cat_avgs['Information Ratio'] * 1.30, 0.005, 0)))

    # Top 5 Stocks concentration
    df['s_Top5'] = np.where(df['Top 5 Stocks (%)'] < 35, 0.02, -0.02)

    # Rolling return scores
    def rolling_score(col, w):
        diff = df[col] - cat_avgs[col]
        return diff.groupby(df['Category']).transform(lambda x: percentile_score(x, w))

    df['s_3YR_1D'] = rolling_score('3YR_1D', [5, 3, 2, 0])
    df['s_3YR_1M'] = rolling_score('3YR_1M', [6, 4, 2, 0])
    df['s_3YR_1Y'] = rolling_score('3YR_1Y', [5, 3, 2, 0])
    df['s_5Y_1D']  = rolling_score('5Y_1D',  [4, 2, 1, 0])
    df['s_5Y_1M']  = rolling_score('5Y_1M',  [4, 2, 1, 0])
    df['s_5Y_1Y']  = rolling_score('5Y_1Y',  [4, 2, 1, 0])
    df['s_10Y_1D'] = rolling_score('10Y_1D', [4, 2, 1, 0])
    df['s_10Y_1M'] = rolling_score('10Y_1M', [4, 2, 1, 0])
    df['s_10Y_1Y'] = rolling_score('10Y_1Y', [4, 2, 1, 0])

    # CAGR
    df['s_1YCAGR']  = np.where(df['1YEAR_CAGR']  > cat_avgs['1YEAR_CAGR'],  0.02, 0)
    df['s_3YCAGR']  = np.where(df['3YEAR_CAGR']  > cat_avgs['3YEAR_CAGR'],  0.02, 0)
    df['s_5YCAGR']  = np.where(df['5YEAR_CAGR']  > cat_avgs['5YEAR_CAGR'],  0.03, 0)
    df['s_10YCAGR'] = np.where(df['10YEAR_CAGR'] > cat_avgs['10YEAR_CAGR'], 0.03, 0)

    quant_cols = [
        's_StdDev', 's_Beta', 's_JAlpha', 's_Sharpe', 's_Sortino',
        's_IR', 's_UpDown', 's_Top5',
        's_3YR_1D', 's_3YR_1M', 's_3YR_1Y',
        's_5Y_1D', 's_5Y_1M', 's_5Y_1Y',
        's_10Y_1D', 's_10Y_1M', 's_10Y_1Y',
        's_1YCAGR', 's_3YCAGR', 's_5YCAGR', 's_10YCAGR'
    ]
    df['QUANT'] = df[quant_cols].sum(axis=1) / 2

    # ── QUALITATIVE ───────────────────────────────────────────────
    df['s_AUM']       = np.where(df['Scheme AUM'] > cat_avgs['Scheme AUM'], 0.10, 0.05)
    df['s_ExitLoad']  = np.where(df['Exit Load'].astype(str).str.strip().str.lower().isin(['yes', '1', 'y']), -0.10, 0.05)
    df['s_StockCnt']  = np.where(df['Total Equity Stocks Count'] > cat_avgs['Total Equity Stocks Count'], 0.10, 0.05)
    df['s_SectorCnt'] = np.where(df['Total Sector Count'] > cat_avgs['Total Sector Count'], 0.10, 0.05)
    df['s_Turnover']  = np.where(df['Turnover Ratio (%)'] < cat_avgs['Turnover Ratio (%)'], 0.10, 0.05)

    df['QUAL'] = df[['s_AUM', 's_ExitLoad', 's_StockCnt', 's_SectorCnt', 's_Turnover']].sum(axis=1)

    # ── TOTAL SCORE, RANK, STARS ──────────────────────────────────
    df['TOTAL_SCORE'] = df['QUANT'] + df['QUAL']
    df['Rank'] = df.groupby('Category')['TOTAL_SCORE'].rank(ascending=False, method='min').astype(int)

    def assign_stars(group):
        n = len(group)
        stars = pd.Series(index=group.index, dtype=int)
        for idx in group.index:
            pct = group.loc[idx, 'Rank'] / n
            stars[idx] = 5 if pct <= 0.25 else 4 if pct <= 0.50 else 3 if pct <= 0.75 else 2
        return stars

    df['Stars'] = df.groupby('Category', group_keys=False).apply(assign_stars)

    return df


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Data Source")
    data_source = st.radio("Load data from", ["Google Drive", "Upload Excel"], index=0)

    df_raw = None

    if data_source == "Google Drive":
        gdrive_url = st.text_input(
            "Paste your Google Drive share link",
            placeholder="https://drive.google.com/file/d/..."
        )
        if gdrive_url:
            with st.spinner("Fetching data..."):
                df_raw = load_from_drive(gdrive_url)
            if df_raw is not None:
                st.success(f"✅ Loaded {len(df_raw)} funds")
    else:
        uploaded = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
        if uploaded:
            df_raw = pd.read_excel(uploaded, engine="openpyxl")
            df_raw.columns = df_raw.columns.str.strip()
            st.success(f"✅ Loaded {len(df_raw)} funds")

    st.divider()

    # Filters — only show after data is loaded
    if df_raw is not None:
     st.write("DEBUG - Column names:", df_raw.columns.tolist())
     st.markdown("## 🔍 Filters")
     asset_classes = ['All'] + sorted(df_raw['Asset Class'].dropna().unique().tolist())
        sel_asset = st.selectbox("Asset Class", asset_classes)

        if sel_asset != 'All':
            cats = sorted(df_raw[df_raw['Asset Class'] == sel_asset]['Category'].dropna().unique().tolist())
        else:
            cats = sorted(df_raw['Category'].dropna().unique().tolist())
        sel_category = st.selectbox("Category", ['All'] + cats)

        star_filter = st.multiselect("Star Rating", [5, 4, 3, 2], default=[5, 4, 3, 2])
    else:
        sel_asset    = 'All'
        sel_category = 'All'
        star_filter  = [5, 4, 3, 2]

    st.divider()
    st.markdown("### 📌 About")
    st.caption("Proprietary Mutual Fund Rating System. Not investment advice.")


# ─────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1 style="margin:0; font-size:2rem;">📊 Mutual Fund Rating System</h1>
    <p style="margin:6px 0 0; color:#8b949e; font-size:14px;">
        Quantitative + Qualitative scoring across Equity · Debt · Hybrid
    </p>
</div>
""", unsafe_allow_html=True)

if df_raw is None:
    st.info("👈 Load your data from the sidebar to get started.")
    st.markdown("""
    **How to connect your Google Drive file:**
    1. Open your Excel file in Google Drive
    2. Click **Share** → **Anyone with the link can view**
    3. Copy the link and paste it in the sidebar
    """)
    st.stop()

# Compute ratings
with st.spinner("Computing ratings..."):
    try:
        df = compute_ratings(df_raw)
    except Exception as e:
        st.error(f"Error computing ratings: {e}")
        st.exception(e)
        st.stop()

# Apply filters
dff = df.copy()
if sel_asset != 'All':
    dff = dff[dff['Asset Class'] == sel_asset]
if sel_category != 'All':
    dff = dff[dff['Category'] == sel_category]
dff = dff[dff['Stars'].isin(star_filter)]

# ── Summary metrics ────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Funds Rated", len(dff))
c2.metric("5★ Funds", len(dff[dff['Stars'] == 5]))
c3.metric("Avg Score", f"{dff['TOTAL_SCORE'].mean():.3f}" if len(dff) else "—")
c4.metric("Categories", dff['Category'].nunique())

st.divider()

# ── Tabs ───────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏆 Rankings", "📈 Charts", "🔢 Raw Scores"])

with tab1:
    view_df = dff[['Rank', 'Stars', 'Scheme Name', 'Asset Class', 'Category',
                   'QUANT', 'QUAL', 'TOTAL_SCORE', 'Age (From Incept Date)', 'Scheme AUM']].copy()
    view_df['Rating'] = view_df['Stars'].apply(lambda x: '★' * x + '☆' * (5 - x))
    view_df = view_df[['Rank', 'Rating', 'Scheme Name', 'Asset Class', 'Category',
                        'QUANT', 'QUAL', 'TOTAL_SCORE', 'Age (From Incept Date)', 'Scheme AUM']]
    view_df = view_df.sort_values(['Category', 'Rank']).round(4)

    st.dataframe(
        view_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Rating": st.column_config.TextColumn("⭐ Rating", width="medium"),
            "Scheme Name": st.column_config.TextColumn("Fund Name", width="large"),
            "TOTAL_SCORE": st.column_config.ProgressColumn("Total Score", min_value=0, max_value=1, format="%.4f"),
            "Scheme AUM": st.column_config.NumberColumn("AUM (Cr)", format="₹%.0f"),
        }
    )
    csv = view_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Ratings CSV", csv, "mf_ratings.csv", "text/csv")

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Star Distribution")
        star_counts = dff['Stars'].value_counts().sort_index(ascending=False)
        fig = px.bar(x=star_counts.index.astype(str) + ' ★', y=star_counts.values,
                     color=star_counts.values, color_continuous_scale='Oranges')
        fig.update_layout(paper_bgcolor='#161b22', plot_bgcolor='#161b22',
                          font_color='#e6edf3', showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Funds per Category")
        cat_counts = dff['Category'].value_counts().head(15)
        fig2 = px.bar(x=cat_counts.values, y=cat_counts.index, orientation='h',
                      color=cat_counts.values, color_continuous_scale='Blues')
        fig2.update_layout(paper_bgcolor='#161b22', plot_bgcolor='#161b22',
                           font_color='#e6edf3', showlegend=False, coloraxis_showscale=False, height=400)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Quant vs Qual Score")
    scatter_df = dff[['Scheme Name', 'Category', 'QUANT', 'QUAL', 'Stars', 'TOTAL_SCORE']].dropna()
    if len(scatter_df) > 0:
        fig3 = px.scatter(scatter_df, x='QUANT', y='QUAL', color='Stars',
                          hover_name='Scheme Name', hover_data=['Category', 'TOTAL_SCORE'],
                          color_continuous_scale='YlOrRd')
        fig3.update_layout(paper_bgcolor='#161b22', plot_bgcolor='#161b22',
                           font_color='#e6edf3', height=420)
        st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.markdown("#### Detailed Score Breakdown")
    score_cols = ['Scheme Name', 'Category', 'Stars', 'Rank',
                  's_StdDev', 's_Beta', 's_JAlpha', 's_Sharpe', 's_Sortino',
                  's_IR', 's_UpDown', 's_Top5',
                  's_3YR_1D', 's_3YR_1M', 's_3YR_1Y',
                  's_5Y_1D', 's_5Y_1M', 's_5Y_1Y',
                  's_10Y_1D', 's_10Y_1M', 's_10Y_1Y',
                  's_1YCAGR', 's_3YCAGR', 's_5YCAGR', 's_10YCAGR', 'QUANT',
                  's_AUM', 's_ExitLoad', 's_StockCnt', 's_SectorCnt', 's_Turnover',
                  'QUAL', 'TOTAL_SCORE']
    available = [c for c in score_cols if c in dff.columns]
    st.dataframe(dff[available].sort_values(['Category', 'Rank']).round(4),
                 use_container_width=True, hide_index=True)
