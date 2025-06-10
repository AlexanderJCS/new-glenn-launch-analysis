

def smooth_outliers(df, col):
    vals = df[col].dropna()
    mean_val = vals.mean()
    mad = (vals - mean_val).abs().mean()  # Mean absolute deviation
    threshold = 2 * mad
    rolling_median = df[col].rolling(window=5, center=True).median()
    diff = (df[col] - rolling_median).abs()  # Absolute deviation from rolling mean

    return df[diff < threshold]

