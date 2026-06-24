"""Conversion funnel ETL — session-level dataset + download analytics."""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt


PRODUCT_MAPPING = {
    "TKT01": "Ticket Hub Account",
    "AUD01": "Audio Library",
    "MUS01": "Music Subscription",
    "VID01": "Video Stream",
    "POD01": "Podcast Library",
    "PS01": "Ticket Hub Account",
    "PS02": "Audio Library",
    "FIT01": "Music Subscription",
    "SDR01": "Video Stream",
    "PFG01": "Digital Studio Access",
}


def classify_device(user_agent: str) -> str:
    if pd.isna(user_agent):
        return "Other/Bot"
    ua = str(user_agent).lower()
    if "windows nt" in ua:
        return "Windows"
    if "macintosh" in ua:
        return "MacOs"
    if "ipad" in ua or "iphone" in ua:
        return "iOS Mobile"
    if "android" in ua:
        return "Android Mobile"
    return "Other/Bot"


def build_download_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily downloads by product and cookie type with 7-day rolling average."""
    data = df.copy()
    data["is_new_cookie"] = data["cookie_id"].apply(lambda x: "new" in str(x).lower())
    data["date"] = pd.to_datetime(data["timestamp"]).dt.date
    data["product_name"] = data["sub_product_code"].map(PRODUCT_MAPPING)

    downloads = data[data["log_type"] == "download"]
    agg = (
        downloads.groupby(["date", "sub_product_code", "is_new_cookie"])["cookie_id"]
        .nunique()
        .reset_index(name="unique_cloudid_count")
    )
    agg = agg.sort_values("date")
    agg["rolling_avg"] = agg.groupby(["sub_product_code", "is_new_cookie"])["unique_cloudid_count"].transform(
        lambda x: x.rolling(window=7, min_periods=1).mean()
    )
    return agg


def plot_rolling_trends(agg: pd.DataFrame, save_path: str | None = None) -> None:
    """Plot 7-day rolling download trends per digital product."""
    products = agg["sub_product_code"].unique()
    fig, axes = plt.subplots(len(products), 1, figsize=(10, 5 * len(products)), sharex=True)
    if len(products) == 1:
        axes = [axes]

    for ax, code in zip(axes, products):
        subset = agg[agg["sub_product_code"] == code]
        new = subset[subset["is_new_cookie"]]
        existing = subset[~subset["is_new_cookie"]]
        ax.plot(new["date"], new["rolling_avg"], label="New Cookie", linestyle="--", marker="o")
        ax.plot(existing["date"], existing["rolling_avg"], label="Existing Cookie", linestyle="-", marker="x")
        ax.set_title(f"{PRODUCT_MAPPING.get(code, code)} — 7-Day Rolling Average")
        ax.set_ylabel("Unique CloudID Count")
        ax.legend()
        ax.grid(True)

    plt.xlabel("Date")
    plt.suptitle("Download Trends by Product and Cookie Type", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    if save_path:
        plt.savefig(save_path, dpi=120)
    else:
        plt.show()


def sample_events() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2025-10-01", periods=200, freq="6h"),
            "log_type": ["download", "view", "download", "stream"] * 50,
            "event": ["open_app", "play_audio", "add_to_library", "close_app"] * 50,
            "cookie_id": ["cookie_new1", "cookie_new2", "cookie_exist1", "cookie_exist2"] * 50,
            "route": ["/music", "/video", "/podcast", "/ticket"] * 50,
            "sub_product_code": ["AUD01", "VID01", "POD01", "TKT01"] * 50,
        }
    )


if __name__ == "__main__":
    agg = build_download_trends(sample_events())
    print(agg.head())
    plot_rolling_trends(agg)
