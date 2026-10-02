from pathlib import Path
import pandas as pd
import streamlit as st
from fleetpulse.services.anomaly_detection import score_anomalies
from fleetpulse.services.rebalancing import recommend_rebalancing
from fleetpulse.services.telemetry import generate_telemetry

st.set_page_config(page_title="FleetPulse AI", page_icon="🚲", layout="wide")
st.title("FleetPulse AI")
st.caption("Micromobility fleet operations control room — synthetic demo data")

@st.cache_data
def load_data():
    path = Path("data/generated/telemetry.csv")
    return pd.read_csv(path) if path.exists() else generate_telemetry()

df = load_data()
latest = df.sort_values("timestamp").groupby("vehicle_id").tail(1)
anomalies = score_anomalies(latest)
recs = recommend_rebalancing(latest)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Vehicles", len(latest))
c2.metric("Low battery", int((latest.battery_pct < 15).sum()))
c3.metric("High/Critical alerts", int(anomalies.severity.isin(["high","critical"]).sum()))
c4.metric("Zones needing action", int((recs.action != "hold").sum()))

st.subheader("Live fleet map")
st.map(latest[["latitude", "longitude"]].dropna(), size=8)

left, right = st.columns(2)

with left:
    st.subheader("Priority anomalies")
    display = anomalies.head(12).copy()
    display["reasons"] = display["reasons"].apply(lambda x: ", ".join(x))
    st.dataframe(display, use_container_width=True, hide_index=True)

with right:
    st.subheader("Rebalancing recommendations")
    st.dataframe(recs.head(12), use_container_width=True, hide_index=True)

st.subheader("Battery distribution")
st.bar_chart(latest["battery_pct"].round(-1).value_counts().sort_index())
