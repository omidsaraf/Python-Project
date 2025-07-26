from src.visualization import generate_plot
import pandas as pd

def test_generate_plot(tmp_path):
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    output_path = tmp_path / "test_plot.png"
    generate_plot(df, x_col="x", y_col="y", output_file=str(output_path))
    assert output_path.exists()
