import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    result = df.drop_duplicates()
    logger.debug("remove_duplicates: %d -> %d rows", len(df), len(result))
    return result


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        result = df.dropna(axis=0)
        logger.debug("handle_missing: %d -> %d rows", len(df), len(result))
    elif axis == "columns":
        result = df.dropna(axis=1)
        logger.debug("handle_missing: %d -> %d columns",
                     df.shape[1], result.shape[1])
    else:
        logger.error("Unsupported axis: %s", axis)
        raise ValueError(f"Unsupported axis: {axis}")
    return result


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ("iqr", "zscore"):
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError(f"Unsupported outlier method: {method}")

    for col in columns:
        if col not in df.columns:
            logger.warning("Column not found: %s", col)
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning("Column is not numeric: %s", col)
            continue

        series = df[col]
        if method == "iqr":
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - threshold * iqr, q3 + threshold * iqr
            is_outlier = (series < lower) | (series > upper)
        else:  # zscore
            z = (series - series.mean()) / series.std()
            is_outlier = z.abs() > threshold
            lower = series.mean() - threshold * series.std()
            upper = series.mean() + threshold * series.std()

        removed = int(is_outlier.sum())
        df = df[~is_outlier]
        logger.debug("%s: method=%s, threshold=%s, lower=%.1f, upper=%.1f, removed=%d",
                     col, method, threshold, lower, upper, removed)
    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    settings = config["processing"]

    if settings["remove_duplicates"]:
        df = remove_duplicates(df)

    missing = settings["missing"]
    if missing["enabled"]:
        df = handle_missing(df, axis=missing["axis"])

    outliers = settings["outliers"]
    if outliers["enabled"]:
        df = remove_outliers(df, outliers["columns"],
                             outliers["method"], outliers["threshold"])
    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": df_before.shape[1],
        "columns_after": df_after.shape[1],
        "columns_removed": df_before.shape[1] - df_after.shape[1],
    }