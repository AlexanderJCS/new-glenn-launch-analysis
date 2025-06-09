import pickle
import numpy as np
import pandas
import matplotlib.pyplot as plt

def main():
    # Load data
    with open("rocket_data.pickle", "rb") as f:
        data = pickle.load(f)
    df = pandas.DataFrame(data)
    df.to_csv("output.csv", index=False)

    # 1. Drop NaNs in altitude
    alts = df["stage1_alt"].dropna()

    # 2. Compute the mean absolute deviation (MAD)
    mean_alt = alts.mean()
    mad = (alts - mean_alt).abs().mean()

    # 3. Build threshold (e.g. 3 × MAD)
    threshold = 2 * mad

    # 4. Compute rolling median for local context
    rolling_median = df["stage1_alt"].rolling(window=5, center=True).median()

    # 5. Compute absolute deviation from rolling median
    diff = (df["stage1_alt"] - rolling_median).abs()

    # 6. Filter out outliers
    filtered = df[diff < threshold]

    # 7. Extract the time and altitude of the filtered points
    time = filtered["time"]
    alt = filtered["stage1_alt"]

    # 8. Plot raw vs filtered for comparison
    plt.figure(figsize=(8, 5))
    plt.plot(time, alt, linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Stage 1 Altitude (m)")
    plt.title("Stage 1 Altitude vs Time (Filtered)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
