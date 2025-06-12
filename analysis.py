import numpy as np


def smooth_outliers(df, col, threshold_multiplier=2, derivative_smoothing=True):
    vals = df[col].dropna()
    mean_val = vals.mean()
    mad = (vals - mean_val).abs().mean()  # Mean absolute deviation
    threshold = 2 * mad
    rolling_median = df[col].rolling(window=5, center=True).median()
    diff = (df[col] - rolling_median).abs()  # Absolute deviation from rolling mean

    # if the derivative is greater than a threshold, consider it an outlier
    derivative = df[col].diff().abs()

    return df[(diff < threshold) & (derivative < (50 if derivative_smoothing else np.inf))].copy()

