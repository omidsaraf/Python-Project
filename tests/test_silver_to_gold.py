import pandas as pd
from src.silver_to_gold import aggregate_data

def test_aggregate_data():
    df = pd.DataFrame({"category": ["A", "A", "B"], "amount": [10, 20, 30]})
    gold_df = aggregate_data(df)
    assert len(gold_df) == 2
    assert set(gold_df["category"]) == {"A", "B"}
