import pickle
import pandas
import matplotlib.pyplot as plt


def filter_outliers(df, col):
    vals = df[col].dropna()
    mean_val = vals.mean()
    mad = (vals - mean_val).abs().mean()  # Mean absolute deviation
    threshold = 2 * mad
    rolling_median = df[col].rolling(window=5, center=True).median()
    diff = (df[col] - rolling_median).abs()  # Absolute deviation from rolling mean

    return df[diff < threshold]


def main():
    # Load data
    with open("rocket_data.pickle", "rb") as f:
        data = pickle.load(f)
    df = pandas.DataFrame(data)
    df.to_csv("output.csv", index=False)

    filtered_stage1_alts = filter_outliers(df, "stage1_alt")
    filtered_stage1_vels = filter_outliers(df, "stage1_vel")

    fig, ax1 = plt.subplots(figsize=(8, 4))

    ax1.plot(filtered_stage1_alts["time"], filtered_stage1_alts["stage1_alt"], label="Stage 1 Altitude")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Stage 1 Altitude (m)")

    ax2 = ax1.twinx()
    ax2.plot(filtered_stage1_vels["time"], filtered_stage1_vels["stage1_vel"], label="Stage 1 Velocity")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Stage 1 Velocity (m/s)")
    plt.show()

if __name__ == "__main__":
    main()
