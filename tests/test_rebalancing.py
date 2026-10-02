import pandas as pd
from fleetpulse.services.rebalancing import recommend_rebalancing

def test_rebalancing_returns_expected_columns():
    df = pd.DataFrame([
        {"vehicle_id":"LFP-1","latitude":50.11,"longitude":8.68,"trips_24h":20,"battery_pct":80},
        {"vehicle_id":"LFP-2","latitude":50.11,"longitude":8.68,"trips_24h":20,"battery_pct":80},
    ])
    result = recommend_rebalancing(df)
    assert {"zone_id","available_vehicles","estimated_demand","demand_gap","action","priority"} <= set(result.columns)
    assert len(result) == 1
