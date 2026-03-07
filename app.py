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
# CSS — clean white professional UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"], .stApp {
    font-family: 'Sora', sans-serif !important;
    background-color: #f8f9fb !important;
    color: #1a1d23 !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e8eaf0 !important;
    padding: 0 !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
section[data-testid="stSidebar"] > div {
    padding: 24px 16px !important;
}

/* ── Sidebar header ── */
.sidebar-header {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9ca3b0;
    padding: 0 4px 16px 4px;
    border-bottom: 1px solid #f0f1f5;
    margin-bottom: 20px;
}

/* ── Filter section label ── */
.filter-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 600;
    color: #4b5563;
    margin: 20px 0 10px 0;
    letter-spacing: 0.3px;
}
.filter-label svg { width: 14px; height: 14px; }

/* ── Checkboxes ── */
.stCheckbox > label {
    font-size: 13px !important;
    color: #374151 !important;
    gap: 8px !important;
}
.stCheckbox > label > span:first-child {
    border-color: #d1d5db !important;
    border-radius: 4px !important;
}

/* ── Apply button ── */
.stButton > button {
    width: 100% !important;
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
    cursor: pointer !important;
    transition: background 0.2s !important;
    margin-top: 8px !important;
}
.stButton > button:hover {
    background: #1d4ed8 !important;
}

/* ── Main content area ── */
.main-content {
    padding: 32px 36px;
    background: #f8f9fb;
    min-height: 100vh;
}

/* ── Page title ── */
.page-title {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}

/* ── Breadcrumb ── */
.breadcrumb {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.breadcrumb a { color: #2563eb; text-decoration: none; }
.breadcrumb span { color: #9ca3b0; }

/* ── Metric cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.metric-card {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 12px;
    padding: 20px 24px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
}
.metric-card-left {}
.metric-card-label {
    font-size: 12px;
    color: #6b7280;
    font-weight: 500;
    margin-bottom: 8px;
    letter-spacing: 0.2px;
}
.metric-card-value {
    font-size: 30px;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -1px;
    line-height: 1;
    margin-bottom: 6px;
}
.metric-card-sub {
    font-size: 11px;
    color: #9ca3b0;
}
.metric-card-icon {
    width: 36px;
    height: 36px;
    background: #eff6ff;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #2563eb;
    font-size: 16px;
}

/* ── Table container ── */
.table-container {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 12px;
    overflow: hidden;
}

/* ── Table tabs ── */
.table-tabs {
    display: flex;
    align-items: center;
    padding: 0 24px;
    border-bottom: 1px solid #f0f1f5;
    gap: 0;
}
.table-tab {
    padding: 16px 4px;
    margin-right: 28px;
    font-size: 13px;
    font-weight: 500;
    color: #6b7280;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}
.table-tab.active {
    color: #2563eb;
    border-bottom-color: #2563eb;
    font-weight: 600;
}
.table-update {
    margin-left: auto;
    font-size: 11px;
    color: #9ca3b0;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Fund table header ── */
.fund-table-header {
    display: grid;
    grid-template-columns: 80px 1fr 140px 120px 100px 100px;
    padding: 10px 24px;
    background: #f8f9fb;
    border-bottom: 1px solid #f0f1f5;
}
.fund-table-header span {
    font-size: 11px;
    font-weight: 600;
    color: #9ca3b0;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Fund row ── */
.fund-row {
    display: grid;
    grid-template-columns: 80px 1fr 140px 120px 100px 100px;
    padding: 16px 24px;
    border-bottom: 1px solid #f8f9fb;
    align-items: center;
    transition: background 0.15s;
}
.fund-row:hover { background: #fafbff; }
.fund-row:last-child { border-bottom: none; }

/* ── Rank number ── */
.rank-num {
    font-size: 16px;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 8px;
}
.rank-trend-up { color: #10b981; font-size: 14px; }
.rank-trend-down { color: #ef4444; font-size: 14px; }
.rank-trend-flat { color: #9ca3b0; font-size: 14px; }

/* ── Fund name ── */
.fund-name-cell {}
.fund-name-main {
    font-size: 14px;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 2px;
}
.fund-name-code {
    font-size: 11px;
    color: #9ca3b0;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Stars ── */
.stars-cell { color: #f59e0b; font-size: 16px; letter-spacing: 1px; }
.stars-empty { color: #e5e7eb; }

/* ── Asset class badge ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.badge-equity   { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.badge-debt     { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
.badge-hybrid   { background: #fdf4ff; color: #9333ea; border: 1px solid #e9d5ff; }
.badge-other    { background: #f9fafb; color: #6b7280; border: 1px solid #e5e7eb; }

/* ── Return value ── */
.return-pos { color: #10b981; font-weight: 600; font-size: 13px; }
.return-neg { color: #ef4444; font-weight: 600; font-size: 13px; }
.return-neu { color: #6b7280; font-weight: 600; font-size: 13px; }

/* ── Score value ── */
.score-val {
    font-size: 13px;
    font-weight: 500;
    color: #374151;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Pagination ── */
.pagination {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    border-top: 1px solid #f0f1f5;
}
.page-info { font-size: 12px; color: #6b7280; }
.page-info b { color: #0f172a; }
.page-btns { display: flex; gap: 6px; align-items: center; }
.page-btn {
    width: 32px; height: 32px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    border: 1px solid #e8eaf0;
    background: #fff;
    color: #374151;
}
.page-btn.active { background: #2563eb; color: #fff; border-color: #2563eb; }
.page-btn.arrow { color: #6b7280; }

/* ── Sort button ── */
.sort-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    border: 1px solid #e8eaf0;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 500;
    color: #374151;
    background: #fff;
    cursor: pointer;
}

/* ── Streamlit overrides ── */
.stSelectbox > div > div {
    background: #fff !important;
    border-color: #e8eaf0 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}
.stMultiSelect > div > div {
    background: #fff !important;
    border-color: #e8eaf0 !important;
    border-radius: 8px !important;
}
div[data-testid="stHorizontalBlock"] { gap: 16px; }

/* ── Download button ── */
.stDownloadButton > button {
    background: #fff !important;
    color: #2563eb !important;
    border: 1px solid #2563eb !important;
    border-radius: 8px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
}

/* ── Spinner ── */
.stSpinner { color: #2563eb !important; }

/* ── Info box ── */
.stAlert {
    border-radius: 10px !important;
    border: 1px solid #bfdbfe !important;
    background: #eff6ff !important;
    color: #1d4ed8 !important;
}

hr { border-color: #f0f1f5 !important; margin: 20px 0 !important; }

/* ── Tabs (Charts / Raw Scores) ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid #f0f1f5;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #6b7280 !important;
    padding: 12px 20px !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #2563eb !important;
    border-bottom-color: #2563eb !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# COLUMN MAPPING — hardcoded by position
# ─────────────────────────────────────────────
COLUMNS = [
    'Scheme Code', 'Scheme Name', 'Asset Class', 'Category', 'Scheme AUM',
    'Total Equity Stocks Count', 'Top 5 Stocks (%)', 'Total Sector Count',
    'Turnover Ratio (%)', 'Std. Deviation', 'Beta', 'Sharpe Ratio',
    'Jensen Alpha', 'Sortino', 'Up/Down Capture Ratio',
    '3YR_1D', '3YR_1M', '3YR_1Y',
    '5Y_1D', '5Y_1M', '5Y_1Y',
    '10Y_1D', '10Y_1M', '10Y_1Y',
    'Information Ratio', 'Age (From Incept Date)', 'Exit Load',
    '1YEAR_CAGR', '3YEAR_CAGR', '5YEAR_CAGR', '10YEAR_CAGR'
]


def load_and_fix(df):
    df = df.iloc[:, :len(COLUMNS)].copy()
    df.columns = COLUMNS
    for col in COLUMNS:
        if col not in ['Scheme Code', 'Scheme Name', 'Asset Class', 'Category', 'Exit Load']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def make_stars(x):
    try:
        n = int(x)
        if n < 1 or n > 5:
            return '—'
        return '★' * n + '☆' * (5 - n)
    except:
        return '—'


def badge_class(asset):
    a = str(asset).lower()
    if 'equity' in a: return 'badge-equity'
    if 'debt' in a or 'fixed' in a or 'income' in a: return 'badge-debt'
    if 'hybrid' in a or 'multi' in a: return 'badge-hybrid'
    return 'badge-other'


# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_from_drive(gdrive_url):
    try:
        file_id = gdrive_url.split("/d/")[1].split("/")[0]
        direct = f"https://drive.google.com/uc?export=download&id={file_id}"
        df = pd.read_excel(direct, engine="openpyxl", header=0)
        df = load_and_fix(df)
        return df
    except Exception as e:
        st.error(f"Could not load from Google Drive: {e}")
        return None


# ─────────────────────────────────────────────
# RATING ENGINE
# ─────────────────────────────────────────────
def percentile_score(series, weights):
    ranks = series.rank(ascending=False, method='min')
    n = len(series)
    scores = pd.Series(index=series.index, dtype=float)
    for idx in series.index:
        pct = ranks[idx] / n
        if pct <= 0.25:   scores[idx] = weights[0]
        elif pct <= 0.50: scores[idx] = weights[1]
        elif pct <= 0.75: scores[idx] = weights[2]
        else:             scores[idx] = weights[3]
    return scores / 100


def compute_ratings(df_raw):
    df = df_raw.copy()
    df = df[pd.to_numeric(df['Age (From Incept Date)'], errors='coerce') >= 5].copy()
    df = df.reset_index(drop=True)

    if df.empty:
        st.error("No funds with Age >= 5 years found.")
        st.stop()

    cat_avg_cols = [
        'Std. Deviation', 'Beta', 'Jensen Alpha', 'Sharpe Ratio', 'Sortino',
        'Information Ratio', 'Up/Down Capture Ratio', 'Top 5 Stocks (%)',
        '3YR_1D', '3YR_1M', '3YR_1Y', '5Y_1D', '5Y_1M', '5Y_1Y',
        '10Y_1D', '10Y_1M', '10Y_1Y',
        '1YEAR_CAGR', '3YEAR_CAGR', '5YEAR_CAGR', '10YEAR_CAGR',
        'Scheme AUM', 'Total Equity Stocks Count', 'Total Sector Count', 'Turnover Ratio (%)'
    ]
    cat_avgs = df.groupby('Category')[cat_avg_cols].transform('mean')

    df['s_StdDev'] = np.where(df['Std. Deviation'] < cat_avgs['Std. Deviation'], 0.025, 0.005)
    df['s_Beta']   = np.where(df['Beta'] < cat_avgs['Beta'], 0.025, 0.005)

    for col, sname, w in [
        ('Jensen Alpha',          's_JAlpha',  [10, 7, 4, 2]),
        ('Sharpe Ratio',          's_Sharpe',  [10, 7, 4, 2]),
        ('Sortino',               's_Sortino', [10, 7, 4, 2]),
        ('Up/Down Capture Ratio', 's_UpDown',  [10, 7, 4, 2]),
    ]:
        diff = df[col] - cat_avgs[col]
        df[sname] = diff.groupby(df['Category']).transform(lambda x: percentile_score(x, w))

    df['s_IR'] = np.where(
        df['Information Ratio'] > cat_avgs['Information Ratio'] * 1.70, 0.02,
        np.where(df['Information Ratio'] > cat_avgs['Information Ratio'] * 1.50, 0.01,
        np.where(df['Information Ratio'] > cat_avgs['Information Ratio'] * 1.30, 0.005, 0))
    )
    df['s_Top5'] = np.where(df['Top 5 Stocks (%)'] < 35, 0.02, -0.02)

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

    df['s_1YCAGR']  = np.where(df['1YEAR_CAGR']  > cat_avgs['1YEAR_CAGR'],  0.02, 0)
    df['s_3YCAGR']  = np.where(df['3YEAR_CAGR']  > cat_avgs['3YEAR_CAGR'],  0.02, 0)
    df['s_5YCAGR']  = np.where(df['5YEAR_CAGR']  > cat_avgs['5YEAR_CAGR'],  0.03, 0)
    df['s_10YCAGR'] = np.where(df['10YEAR_CAGR'] > cat_avgs['10YEAR_CAGR'], 0.03, 0)

    quant_cols = [
        's_StdDev','s_Beta','s_JAlpha','s_Sharpe','s_Sortino','s_IR','s_UpDown','s_Top5',
        's_3YR_1D','s_3YR_1M','s_3YR_1Y','s_5Y_1D','s_5Y_1M','s_5Y_1Y',
        's_10Y_1D','s_10Y_1M','s_10Y_1Y','s_1YCAGR','s_3YCAGR','s_5YCAGR','s_10YCAGR'
    ]
    df['QUANT'] = df[quant_cols].sum(axis=1) / 2

    df['s_AUM']       = np.where(df['Scheme AUM'] > cat_avgs['Scheme AUM'], 0.10, 0.05)
    df['s_ExitLoad']  = np.where(df['Exit Load'].astype(str).str.strip().str.lower().isin(['yes','1','y']), -0.10, 0.05)
    df['s_StockCnt']  = np.where(df['Total Equity Stocks Count'] > cat_avgs['Total Equity Stocks Count'], 0.10, 0.05)
    df['s_SectorCnt'] = np.where(df['Total Sector Count'] > cat_avgs['Total Sector Count'], 0.10, 0.05)
    df['s_Turnover']  = np.where(df['Turnover Ratio (%)'] < cat_avgs['Turnover Ratio (%)'], 0.10, 0.05)
    df['QUAL'] = df[['s_AUM','s_ExitLoad','s_StockCnt','s_SectorCnt','s_Turnover']].sum(axis=1)

    df['TOTAL_SCORE'] = df['QUANT'] + df['QUAL']
    df['Rank'] = df.groupby('Category')['TOTAL_SCORE'].rank(ascending=False, method='min').astype(int)

    def assign_stars(group):
        n = len(group)
        stars = pd.Series(index=group.index, dtype=float)
        for idx in group.index:
            pct = group.loc[idx, 'Rank'] / n
            if pct <= 0.25:   stars[idx] = 5
            elif pct <= 0.50: stars[idx] = 4
            elif pct <= 0.75: stars[idx] = 3
            else:             stars[idx] = 2
        return stars

    df['Stars'] = df.groupby('Category', group_keys=False).apply(assign_stars)
    df['Stars'] = pd.to_numeric(df['Stars'], errors='coerce').fillna(0).astype(int)
    return df


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-header">Market Filters</div>', unsafe_allow_html=True)

    data_source = st.radio("Load data from", ["Google Drive", "Upload Excel"],
                           index=0, label_visibility="collapsed")

    df_raw = None

    if data_source == "Google Drive":
        gdrive_url = st.text_input("Google Drive link",
                                   placeholder="https://drive.google.com/file/d/...",
                                   label_visibility="collapsed")
        if gdrive_url:
            with st.spinner("Loading..."):
                df_raw = load_from_drive(gdrive_url)
            if df_raw is not None:
                st.success(f"✅ {len(df_raw)} funds loaded")

    if data_source == "Upload Excel":
        uploaded = st.file_uploader("Upload Excel", type=["xlsx","xls"], label_visibility="collapsed")
        if uploaded:
            df_raw = pd.read_excel(uploaded, engine="openpyxl", header=0)
            df_raw = load_and_fix(df_raw)
            st.success(f"✅ {len(df_raw)} funds loaded")

    # ── Filters ──
    if df_raw is not None:
        st.markdown("""
        <div class="filter-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
            </svg>
            Asset Class
        </div>
        """, unsafe_allow_html=True)

        all_assets = sorted(df_raw['Asset Class'].dropna().unique().tolist())
        sel_assets = []
        for ac in all_assets:
            count = len(df_raw[df_raw['Asset Class'] == ac])
            checked = st.checkbox(f"{ac}  **{count}**", value=True, key=f"ac_{ac}")
            if checked:
                sel_assets.append(ac)
        if not sel_assets:
            sel_assets = all_assets

        st.markdown("""
        <div class="filter-label" style="margin-top:20px;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18M7 12h10M11 18h2"/>
            </svg>
            Sub Category
        </div>
        """, unsafe_allow_html=True)

        filtered_by_asset = df_raw[df_raw['Asset Class'].isin(sel_assets)]
        all_cats = sorted(filtered_by_asset['Category'].dropna().unique().tolist())
        sel_cats = []
        for cat in all_cats:
            count = len(filtered_by_asset[filtered_by_asset['Category'] == cat])
            checked = st.checkbox(f"{cat}  **{count}**", value=True, key=f"cat_{cat}")
            if checked:
                sel_cats.append(cat)
        if not sel_cats:
            sel_cats = all_cats

        st.markdown("""
        <div class="filter-label" style="margin-top:20px;">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>
            </svg>
            Ratings
        </div>
        """, unsafe_allow_html=True)

        star_options = {5: "★★★★★", 4: "★★★★☆", 3: "★★★☆☆", 2: "★★☆☆☆"}
        sel_stars = []
        for s, label in star_options.items():
            checked = st.checkbox(label, value=True, key=f"star_{s}")
            if checked:
                sel_stars.append(s)
        if not sel_stars:
            sel_stars = [5, 4, 3, 2]

        st.markdown("<br>", unsafe_allow_html=True)
        apply = st.button("Apply Filters", use_container_width=True)

        st.markdown(
            '<div style="text-align:center;margin-top:10px;font-size:12px;color:#9ca3b0;cursor:pointer;">Reset All</div>',
            unsafe_allow_html=True
        )

    else:
        sel_assets = []
        sel_cats   = []
        sel_stars  = [5, 4, 3, 2]


# ─────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if df_raw is None:
    st.markdown("""
    <div style="text-align:center; padding: 80px 40px;">
        <div style="font-size:48px; margin-bottom:16px;">📊</div>
        <h2 style="font-size:22px; font-weight:700; color:#0f172a; margin-bottom:8px;">
            Mutual Fund Rating System
        </h2>
        <p style="color:#6b7280; font-size:14px; max-width:400px; margin:0 auto 24px;">
            Load your data from Google Drive or upload an Excel file using the sidebar to get started.
        </p>
        <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; padding:16px 24px; display:inline-block; text-align:left; max-width:420px;">
            <p style="font-size:13px; color:#1d4ed8; font-weight:600; margin:0 0 8px;">How to connect Google Drive:</p>
            <p style="font-size:12px; color:#3b82f6; margin:0; line-height:1.8;">
                1. Open your Excel in Google Drive<br>
                2. Share → Anyone with link → Viewer<br>
                3. Paste the link in the sidebar
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Compute ratings
with st.spinner("Computing ratings..."):
    try:
        df = compute_ratings(df_raw)
    except Exception as e:
        st.error(f"Error: {e}")
        st.exception(e)
        st.stop()

# Apply filters
dff = df.copy()
if sel_assets:
    dff = dff[dff['Asset Class'].isin(sel_assets)]
if sel_cats:
    dff = dff[dff['Category'].isin(sel_cats)]
dff = dff[dff['Stars'].isin(sel_stars)]
dff = dff.sort_values(['Category', 'Rank']).reset_index(drop=True)

# ── Page header ──────────────────────────────
# Determine title from filters
if len(sel_cats) == 1:
    page_title = sel_cats[0]
elif len(sel_assets) == 1:
    page_title = f"{sel_assets[0]} Funds"
else:
    page_title = "Mutual Fund Market"

cat_crumb = " › ".join(sel_cats[:3]) if sel_cats else "All Categories"

col_title, col_sort = st.columns([5, 1])
with col_title:
    st.markdown(f"""
    <h1 class="page-title">{page_title}</h1>
    <div class="breadcrumb">
        <a href="#">All Funds</a>
        <span>›</span>
        <span>{" › ".join(sel_assets) if sel_assets else "All Asset Classes"}</span>
        <span>›</span>
        <span>{cat_crumb}</span>
    </div>
    """, unsafe_allow_html=True)
with col_sort:
    sort_by = st.selectbox("Sort", ["Rank", "Total Score", "1Y CAGR", "Scheme AUM"],
                           label_visibility="collapsed")

# ── Metric cards ──────────────────────────────
avg_score = dff['TOTAL_SCORE'].mean() * 100 if len(dff) else 0
avg_cagr  = dff['1YEAR_CAGR'].mean() if len(dff) and '1YEAR_CAGR' in dff.columns else 0

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-card-left">
            <div class="metric-card-label">Total Funds</div>
            <div class="metric-card-value">{len(dff):,}</div>
            <div class="metric-card-sub">{dff['Category'].nunique()} categories</div>
        </div>
        <div class="metric-card-icon">⊞</div>
    </div>
    <div class="metric-card">
        <div class="metric-card-left">
            <div class="metric-card-label">Avg Score</div>
            <div class="metric-card-value">{avg_score:.1f}</div>
            <div class="metric-card-sub">{len(dff[dff['Stars']==5])} five-star funds</div>
        </div>
        <div class="metric-card-icon">📈</div>
    </div>
    <div class="metric-card">
        <div class="metric-card-left">
            <div class="metric-card-label">Avg 1Y Return</div>
            <div class="metric-card-value">{avg_cagr:.1f}%</div>
            <div class="metric-card-sub">Category average</div>
        </div>
        <div class="metric-card-icon">↗</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Apply sort ────────────────────────────────
if sort_by == "Total Score":
    dff = dff.sort_values('TOTAL_SCORE', ascending=False).reset_index(drop=True)
elif sort_by == "1Y CAGR":
    dff = dff.sort_values('1YEAR_CAGR', ascending=False).reset_index(drop=True)
elif sort_by == "Scheme AUM":
    dff = dff.sort_values('Scheme AUM', ascending=False).reset_index(drop=True)

# ── Pagination ────────────────────────────────
PAGE_SIZE = 10
total_funds = len(dff)
total_pages = max(1, (total_funds + PAGE_SIZE - 1) // PAGE_SIZE)

if 'page' not in st.session_state:
    st.session_state.page = 1
st.session_state.page = min(st.session_state.page, total_pages)

page_start = (st.session_state.page - 1) * PAGE_SIZE
page_end   = min(page_start + PAGE_SIZE, total_funds)
page_df    = dff.iloc[page_start:page_end]

# ── Table ─────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Fund Performance", "Charts", "Detailed Scoring"])

with tab1:
    # Header
    st.markdown("""
    <div class="table-container">
        <div class="fund-table-header">
            <span>Rank</span>
            <span>Fund Details</span>
            <span>Star Rating</span>
            <span>Asset Class</span>
            <span>1Y Return</span>
            <span>Total Score</span>
        </div>
    """, unsafe_allow_html=True)

    # Rows
    rows_html = ""
    for _, row in page_df.iterrows():
        stars_n   = int(row['Stars'])
        stars_str = '★' * stars_n + '<span class="stars-empty">' + '☆' * (5 - stars_n) + '</span>'
        badge_cls = badge_class(row['Asset Class'])
        cagr_1y   = row.get('1YEAR_CAGR', np.nan)

        if pd.notna(cagr_1y):
            ret_cls = 'return-pos' if cagr_1y > 0 else 'return-neg'
            ret_str = f"{'+'if cagr_1y>0 else ''}{cagr_1y:.1f}%"
        else:
            ret_cls = 'return-neu'
            ret_str = '—'

        score_str = f"{row['TOTAL_SCORE']:.4f}"
        rank_val  = int(row['Rank'])

        rows_html += f"""
        <div class="fund-row">
            <div class="rank-num">{rank_val}</div>
            <div class="fund-name-cell">
                <div class="fund-name-main">{row['Scheme Name']}</div>
                <div class="fund-name-code">{row['Category']}</div>
            </div>
            <div class="stars-cell">{stars_str}</div>
            <div><span class="badge {badge_cls}">{row['Asset Class']}</span></div>
            <div class="{ret_cls}">{ret_str}</div>
            <div class="score-val">{score_str}</div>
        </div>
        """

    st.markdown(rows_html, unsafe_allow_html=True)

    # Pagination row
    page_nums_html = ""
    pages_to_show = []
    if total_pages <= 7:
        pages_to_show = list(range(1, total_pages + 1))
    else:
        pages_to_show = [1, 2, 3, '...', total_pages]

    for p in pages_to_show:
        if p == '...':
            page_nums_html += '<span class="page-btn" style="border:none;color:#9ca3b0;">…</span>'
        else:
            active = 'active' if p == st.session_state.page else ''
            page_nums_html += f'<span class="page-btn {active}">{p}</span>'

    st.markdown(f"""
    <div class="pagination">
        <span class="page-info">Showing <b>{page_start+1}–{page_end}</b> of <b>{total_funds:,}</b> funds</span>
        <div class="page-btns">
            <span class="page-btn arrow">‹</span>
            {page_nums_html}
            <span class="page-btn arrow">›</span>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Pagination controls
    pcol1, pcol2, pcol3, pcol4, pcol5 = st.columns([2, 1, 1, 1, 2])
    with pcol2:
        if st.button("← Prev", disabled=st.session_state.page <= 1, use_container_width=True):
            st.session_state.page -= 1
            st.rerun()
    with pcol3:
        st.markdown(f'<div style="text-align:center;padding:8px;font-size:13px;color:#374151;font-weight:600;">{st.session_state.page} / {total_pages}</div>', unsafe_allow_html=True)
    with pcol4:
        if st.button("Next →", disabled=st.session_state.page >= total_pages, use_container_width=True):
            st.session_state.page += 1
            st.rerun()

    # Download
    st.markdown("<br>", unsafe_allow_html=True)
    dl_df = dff[['Rank', 'Stars', 'Scheme Name', 'Asset Class', 'Category',
                  'QUANT', 'QUAL', 'TOTAL_SCORE', 'Age (From Incept Date)', 'Scheme AUM']].copy()
    dl_df['Rating'] = dl_df['Stars'].apply(make_stars)
    csv = dl_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Full Ratings CSV", csv, "mf_ratings.csv", "text/csv")

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Star Distribution")
        star_counts = dff['Stars'].value_counts().sort_index(ascending=False)
        fig = px.bar(
            x=star_counts.index.astype(str) + ' ★', y=star_counts.values,
            color=star_counts.values, color_continuous_scale='Blues',
            labels={'x': 'Stars', 'y': 'Funds'}
        )
        fig.update_layout(paper_bgcolor='#fff', plot_bgcolor='#f8f9fb',
                          font_color='#374151', showlegend=False,
                          coloraxis_showscale=False, margin=dict(t=20, b=20))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Funds per Category")
        cat_counts = dff['Category'].value_counts().head(15)
        fig2 = px.bar(
            x=cat_counts.values, y=cat_counts.index, orientation='h',
            color=cat_counts.values, color_continuous_scale='Blues',
            labels={'x': 'Count', 'y': ''}
        )
        fig2.update_layout(paper_bgcolor='#fff', plot_bgcolor='#f8f9fb',
                           font_color='#374151', showlegend=False,
                           coloraxis_showscale=False, height=400,
                           margin=dict(t=20, b=20))
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Quant vs Qual Score")
    scatter_df = dff[['Scheme Name', 'Category', 'QUANT', 'QUAL', 'Stars', 'TOTAL_SCORE']].dropna()
    if len(scatter_df) > 0:
        fig3 = px.scatter(
            scatter_df, x='QUANT', y='QUAL', color='Stars',
            hover_name='Scheme Name', hover_data=['Category', 'TOTAL_SCORE'],
            color_continuous_scale='RdYlGn',
            labels={'QUANT': 'Quantitative Score', 'QUAL': 'Qualitative Score'}
        )
        fig3.update_layout(paper_bgcolor='#fff', plot_bgcolor='#f8f9fb',
                           font_color='#374151', height=400,
                           margin=dict(t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True)

with tab3:
    score_cols = [
        'Scheme Name', 'Category', 'Stars', 'Rank',
        's_StdDev','s_Beta','s_JAlpha','s_Sharpe','s_Sortino',
        's_IR','s_UpDown','s_Top5',
        's_3YR_1D','s_3YR_1M','s_3YR_1Y',
        's_5Y_1D','s_5Y_1M','s_5Y_1Y',
        's_10Y_1D','s_10Y_1M','s_10Y_1Y',
        's_1YCAGR','s_3YCAGR','s_5YCAGR','s_10YCAGR','QUANT',
        's_AUM','s_ExitLoad','s_StockCnt','s_SectorCnt','s_Turnover',
        'QUAL','TOTAL_SCORE'
    ]
    available = [c for c in score_cols if c in dff.columns]
    st.dataframe(
        dff[available].sort_values(['Category','Rank']).round(4),
        use_container_width=True, hide_index=True
    )

st.markdown('</div>', unsafe_allow_html=True)
