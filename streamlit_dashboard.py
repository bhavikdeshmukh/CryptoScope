import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="CryptoScope",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: center;
    }
    .metric-value { font-size: 28px; font-weight: 700; color: #212529; }
    .metric-label { font-size: 12px; color: #6c757d; margin-top: 4px; }
    .metric-delta { font-size: 13px; color: #198754; margin-top: 2px; }
    .metric-delta.negative { color: #dc3545; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cryptoscope_cleaned.csv")
        return df
    except FileNotFoundError:
        st.error("cryptoscope_cleaned.csv not found. Run section1 and section2 notebooks first.")
        st.stop()


df = load_data()

SIGNAL_COLORS = {
    "Bullish": "#2ecc71",
    "Neutral": "#3498db",
    "Bearish": "#e67e22",
    "Strong Bear": "#e74c3c",
    "Unknown": "#95a5a6"
}

st.sidebar.title("CryptoScope")
st.sidebar.markdown("Crypto Market Intelligence Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Market Overview", "EDA Explorer", "Coin Lookup", "ML Prediction"],
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.sidebar.caption(f"Total coins: {len(df):,}")

if "fear_greed_score" in df.columns:
    fg_score = int(df["fear_greed_score"].iloc[0])
    fg_label = df["fear_greed_label"].iloc[0] if "fear_greed_label" in df.columns else ""
    st.sidebar.metric("Fear and Greed Index", fg_score, fg_label)

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")
selected_signals = st.sidebar.multiselect(
    "Market Signal",
    options=df["market_signal"].unique().tolist(),
    default=df["market_signal"].unique().tolist()
)

risk_tiers = st.sidebar.multiselect(
    "Risk Tier",
    options=["Mega", "Large", "Mid", "Small"],
    default=["Mega", "Large", "Mid", "Small"]
)

price_min = float(df["price_usd"].min())
price_max = float(df["price_usd"].quantile(0.95))
price_range = st.sidebar.slider(
    "Price Range (USD)",
    min_value=0.0,
    max_value=price_max,
    value=(0.0, price_max),
    format="%.2f"
)

df_filtered = df[
    (df["market_signal"].isin(selected_signals)) &
    (df["risk_tier"].isin(risk_tiers)) &
    (df["price_usd"] >= price_range[0]) &
    (df["price_usd"] <= price_range[1])
].copy()


if page == "Market Overview":

    st.title("CryptoScope - Market Overview")
    st.caption("Real-time crypto market intelligence. Use the sidebar filters to explore the data.")
    st.markdown("---")

    col1, col2, col3, col4, col5 = st.columns(5)

    total_mcap = df_filtered["market_cap_usd"].sum()
    total_vol = df_filtered["volume_24h_usd"].sum()
    avg_change_24h = df_filtered["price_change_pct_24h"].mean()
    pct_bullish = (df_filtered["market_signal"] == "Bullish").mean() * 100
    avg_volatility = df_filtered["volatility_24h_pct"].mean()

    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">${total_mcap/1e12:.2f}T</div>
            <div class="metric-label">Total Market Cap</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">${total_vol/1e9:.1f}B</div>
            <div class="metric-label">24h Trading Volume</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        delta_class = "negative" if avg_change_24h < 0 else ""
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{avg_change_24h:+.2f}%</div>
            <div class="metric-label">Avg 24h Change</div>
            <div class="metric-delta {delta_class}">{"Declining" if avg_change_24h < 0 else "Rising"}</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{pct_bullish:.1f}%</div>
            <div class="metric-label">Bullish Coins (30d)</div>
        </div>""", unsafe_allow_html=True)

    with col5:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{avg_volatility:.1f}%</div>
            <div class="metric-label">Avg 24h Volatility</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        signal_counts = df_filtered["market_signal"].value_counts().reset_index()
        signal_counts.columns = ["Signal", "Count"]
        fig_pie = px.pie(
            signal_counts, names="Signal", values="Count",
            color="Signal",
            color_discrete_map=SIGNAL_COLORS,
            title="Market Signal Distribution"
        )
        fig_pie.update_layout(margin=dict(t=40, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        tier_signal = df_filtered.groupby(["risk_tier", "market_signal"]).size().reset_index(name="count")
        tier_order_list = ["Mega", "Large", "Mid", "Small"]
        fig_bar = px.bar(
            tier_signal, x="risk_tier", y="count", color="market_signal",
            color_discrete_map=SIGNAL_COLORS,
            title="Market Signal by Risk Tier",
            category_orders={"risk_tier": tier_order_list}
        )
        fig_bar.update_layout(margin=dict(t=40, b=10))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Top 20 Coins by Market Cap")
    top20 = df_filtered.nlargest(20, "market_cap_usd")[
        ["name", "symbol", "price_usd", "market_cap_usd",
         "volume_24h_usd", "price_change_pct_24h", "market_signal", "risk_tier"]
    ].copy()
    top20["market_cap_usd"] = top20["market_cap_usd"].apply(lambda x: f"${x/1e9:.2f}B")
    top20["volume_24h_usd"] = top20["volume_24h_usd"].apply(lambda x: f"${x/1e9:.2f}B")
    top20["price_usd"] = top20["price_usd"].apply(lambda x: f"${x:,.4f}")
    top20["price_change_pct_24h"] = top20["price_change_pct_24h"].apply(lambda x: f"{x:+.2f}%")
    top20.columns = ["Name", "Symbol", "Price", "Market Cap", "Volume 24h", "Change 24h", "Signal", "Tier"]
    st.dataframe(top20, use_container_width=True, hide_index=True)


elif page == "EDA Explorer":

    st.title("Exploratory Data Analysis")
    st.caption("Interactive charts exploring price behavior, volatility, and market structure.")
    st.markdown("---")

    chart_choice = st.selectbox(
        "Select Analysis View",
        [
            "Price Change Distribution",
            "Market Cap vs Volume",
            "Momentum Map (7d vs 30d)",
            "Volatility Analysis",
            "Fear and Greed Trend",
            "ATH Recovery Analysis",
            "Correlation Heatmap"
        ]
    )

    if chart_choice == "Price Change Distribution":
        fig = px.histogram(
            df_filtered, x="price_change_pct_24h",
            nbins=80, color="market_signal",
            color_discrete_map=SIGNAL_COLORS,
            title="24h Price Change Distribution by Signal",
            labels={"price_change_pct_24h": "24h Price Change (%)"}
        )
        fig.update_layout(bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"Mean 24h change: {df_filtered['price_change_pct_24h'].mean():.2f}% | "
                f"Std Dev: {df_filtered['price_change_pct_24h'].std():.2f}%")

    elif chart_choice == "Market Cap vs Volume":
        fig = px.scatter(
            df_filtered, x="log_market_cap", y="log_volume",
            color="market_signal", hover_name="name",
            color_discrete_map=SIGNAL_COLORS,
            title="Log Market Cap vs Log Volume",
            labels={"log_market_cap": "Log Market Cap", "log_volume": "Log Volume 24h"}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("Strong positive correlation confirms larger coins attract more trading activity.")

    elif chart_choice == "Momentum Map (7d vs 30d)":
        fig = px.scatter(
            df_filtered,
            x=df_filtered["price_change_pct_7d"].clip(-50, 50),
            y=df_filtered["price_change_pct_30d"].clip(-80, 80),
            color="market_signal", hover_name="name",
            color_discrete_map=SIGNAL_COLORS,
            title="Momentum Map: 7d vs 30d Price Change",
            labels={"x": "7-Day Change (%)", "y": "30-Day Change (%)"}
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
        fig.add_vline(x=0, line_dash="dash", line_color="gray", line_width=1)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_choice == "Volatility Analysis":
        col1, col2 = st.columns(2)
        with col1:
            vol_counts = df_filtered["volatility_category"].value_counts().reset_index()
            vol_counts.columns = ["Category", "Count"]
            fig = px.pie(vol_counts, names="Category", values="Count",
                         title="Volatility Category Distribution",
                         color_discrete_sequence=px.colors.sequential.RdYlGn_r)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            top_vol = df_filtered[df_filtered["is_stablecoin"] == 0].nlargest(15, "volatility_24h_pct")
            fig = px.bar(
                top_vol, x="volatility_24h_pct", y="name",
                orientation="h", title="Top 15 Most Volatile Coins",
                color="volatility_24h_pct", color_continuous_scale="Reds",
                labels={"volatility_24h_pct": "24h Volatility (%)", "name": ""}
            )
            st.plotly_chart(fig, use_container_width=True)

    elif chart_choice == "Fear and Greed Trend":
        try:
            df_fg = pd.read_csv("fear_greed.csv")
            df_fg["fg_date"] = pd.to_datetime(df_fg["fg_date"])
            df_fg = df_fg.sort_values("fg_date")
            fig = px.line(
                df_fg, x="fg_date", y="fear_greed_score",
                title="Fear and Greed Index - Last 30 Days",
                labels={"fg_date": "Date", "fear_greed_score": "Score (0=Fear, 100=Greed)"}
            )
            fig.add_hline(y=50, line_dash="dash", line_color="gray")
            fig.add_hrect(y0=0, y1=25, fillcolor="red", opacity=0.08, annotation_text="Extreme Fear")
            fig.add_hrect(y0=75, y1=100, fillcolor="green", opacity=0.08, annotation_text="Extreme Greed")
            st.plotly_chart(fig, use_container_width=True)
        except FileNotFoundError:
            st.warning("fear_greed.csv not found. Run the data collection notebook first.")

    elif chart_choice == "ATH Recovery Analysis":
        fig = px.box(
            df_filtered, x="risk_tier", y="pct_below_ath",
            color="risk_tier", title="ATH Recovery by Risk Tier",
            category_orders={"risk_tier": ["Mega", "Large", "Mid", "Small"]},
            labels={"pct_below_ath": "% Below ATH", "risk_tier": "Risk Tier"}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("Negative values indicate how far below the all-time high each coin is currently trading.")

    elif chart_choice == "Correlation Heatmap":
        corr_cols = [
            "price_change_pct_24h", "price_change_pct_30d",
            "volatility_24h_pct", "log_market_cap", "log_volume",
            "momentum_score", "volume_to_mcap_ratio",
            "price_to_ath_ratio", "fear_greed_score"
        ]
        available_cols = [c for c in corr_cols if c in df_filtered.columns]
        corr_matrix = df_filtered[available_cols].corr().round(2)

        fig = px.imshow(
            corr_matrix, text_auto=True, color_continuous_scale="RdBu",
            zmin=-1, zmax=1, aspect="auto",
            title="Feature Correlation Heatmap"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)


elif page == "Coin Lookup":

    st.title("Coin Lookup")
    st.caption("Search for any coin and view detailed metrics.")
    st.markdown("---")

    search = st.text_input("Search by coin name or symbol", placeholder="e.g. Bitcoin or BTC")

    if search:
        results = df[
            (df["name"].str.lower().str.contains(search.lower())) |
            (df["symbol"].str.lower().str.contains(search.lower()))
        ]
    else:
        results = df.nlargest(50, "market_cap_usd")

    st.caption(f"Showing {len(results)} coins")

    if len(results) > 0:
        selected_coin = st.selectbox(
            "Select a coin to view details",
            options=results["name"].tolist()
        )

        coin_data = df[df["name"] == selected_coin].iloc[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"${coin_data['price_usd']:,.6f}",
                      f"{coin_data['price_change_pct_24h']:+.2f}% (24h)")
        with col2:
            st.metric("Market Cap", f"${coin_data['market_cap_usd']/1e6:,.1f}M")
        with col3:
            st.metric("24h Volume", f"${coin_data['volume_24h_usd']/1e6:,.1f}M")

        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("7-Day Change", f"{coin_data['price_change_pct_7d']:+.2f}%")
        with col5:
            st.metric("30-Day Change", f"{coin_data['price_change_pct_30d']:+.2f}%")
        with col6:
            st.metric("% Below ATH", f"{coin_data['pct_below_ath']:.1f}%")

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Classification**")
            st.write(f"Market Signal: `{coin_data['market_signal']}`")
            st.write(f"Risk Tier: `{coin_data['risk_tier']}`")
            st.write(f"Volatility Category: `{coin_data['volatility_category']}`")
            st.write(f"Stablecoin: `{'Yes' if coin_data['is_stablecoin'] == 1 else 'No'}`")

        with col_b:
            st.write("**Engineered Features**")
            st.write(f"Momentum Score: `{coin_data['momentum_score']:.3f}`")
            st.write(f"Volume/MCap Ratio: `{coin_data['volume_to_mcap_ratio']:.4f}`")
            st.write(f"Price to ATH Ratio: `{coin_data['price_to_ath_ratio']:.4f}`")
            if "news_mentions" in coin_data:
                st.write(f"News Mentions: `{int(coin_data['news_mentions'])}`")

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=coin_data["price_to_ath_ratio"] * 100 if pd.notna(coin_data["price_to_ath_ratio"]) else 0,
            title={"text": "Price as % of ATH"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#3498db"},
                "steps": [
                    {"range": [0, 30], "color": "#fadbd8"},
                    {"range": [30, 70], "color": "#fdebd0"},
                    {"range": [70, 100], "color": "#d5f5e3"}
                ]
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)


elif page == "ML Prediction":

    st.title("ML Prediction - Will This Coin Have a Positive Week?")
    st.caption("Enter coin market data to predict whether the 7-day return will be positive.")
    st.markdown("---")

    st.info("This model uses Random Forest trained on 1000 coins. Input values to get a live prediction.")

    col1, col2, col3 = st.columns(3)

    with col1:
        inp_change_24h = st.number_input("24h Price Change (%)", value=0.0, step=0.1, format="%.2f")
        inp_change_30d = st.number_input("30d Price Change (%)", value=0.0, step=1.0, format="%.2f")
        inp_volatility = st.number_input("24h Volatility (%)", value=3.0, min_value=0.0, step=0.5)
        inp_volume = st.number_input("24h Volume (USD millions)", value=100.0, min_value=0.1, step=10.0)
        inp_mcap = st.number_input("Market Cap (USD millions)", value=1000.0, min_value=0.1, step=100.0)

    with col2:
        inp_fg = st.slider("Fear and Greed Score", 0, 100, 50)
        inp_fg_avg = st.slider("Fear and Greed 7d Avg", 0, 100, 50)
        inp_shift = st.slider("Sentiment Shift (vs 7d ago)", -50, 50, 0)
        inp_news = st.number_input("News Mentions", value=0, min_value=0, step=1)
        inp_pct_ath = st.number_input("% Below ATH (negative value)", value=-40.0, step=1.0)

    with col3:
        inp_momentum = st.number_input("Momentum Score", value=0.0, step=0.5, format="%.2f")
        inp_vol_mcap = st.number_input("Volume/MCap Ratio", value=0.05, min_value=0.0, step=0.01, format="%.4f")
        inp_price_ath = st.number_input("Price/ATH Ratio", value=0.5, min_value=0.0, max_value=1.0, step=0.01)
        inp_supply = st.number_input("Supply Utilization (0-1)", value=0.7, min_value=0.0, max_value=1.0, step=0.01)
        inp_spread = st.number_input("MCap-Volume Spread (log)", value=5.0, step=0.5)

    if st.button("Run Prediction", type="primary"):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler

        feature_cols_model = [
            "price_change_pct_24h", "price_change_pct_30d", "volatility_24h_pct",
            "log_volume", "log_market_cap", "fear_greed_score", "fear_greed_7d_avg",
            "sentiment_shift", "news_mentions", "pct_below_ath", "momentum_score",
            "volume_to_mcap_ratio", "price_to_ath_ratio", "supply_utilization", "mcap_volume_spread"
        ]

        train_df = df.dropna(subset=feature_cols_model + ["target"])
        X_train_full = train_df[feature_cols_model]
        y_train_full = train_df["target"]

        sc = StandardScaler()
        X_train_sc = sc.fit_transform(X_train_full)

        model_live = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced")
        model_live.fit(X_train_sc, y_train_full)

        user_input = np.array([[
            inp_change_24h, inp_change_30d, inp_volatility,
            np.log1p(inp_volume * 1e6), np.log1p(inp_mcap * 1e6),
            inp_fg, inp_fg_avg, inp_shift,
            inp_news, inp_pct_ath, inp_momentum,
            inp_vol_mcap, inp_price_ath, inp_supply, inp_spread
        ]])

        user_input_sc = sc.transform(user_input)
        prediction = model_live.predict(user_input_sc)[0]
        probability = model_live.predict_proba(user_input_sc)[0]

        st.markdown("---")
        st.subheader("Prediction Result")

        col_res1, col_res2 = st.columns(2)
        with col_res1:
            if prediction == 1:
                st.success(f"POSITIVE WEEK PREDICTED")
                st.metric("Confidence", f"{probability[1]*100:.1f}%")
            else:
                st.error(f"NEGATIVE WEEK PREDICTED")
                st.metric("Confidence", f"{probability[0]*100:.1f}%")

        with col_res2:
            fig_prob = go.Figure(go.Bar(
                x=["Negative Week", "Positive Week"],
                y=[probability[0]*100, probability[1]*100],
                marker_color=["#e74c3c", "#2ecc71"]
            ))
            fig_prob.update_layout(
                title="Prediction Probability (%)",
                yaxis=dict(range=[0, 100]),
                height=280, margin=dict(t=40, b=20)
            )
            st.plotly_chart(fig_prob, use_container_width=True)

        st.caption("Note: This model is trained on a snapshot of 1000 coins. Crypto markets are highly unpredictable. This is for educational purposes only, not financial advice.")
