from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class Paths:
    repo_root: Path
    data_dir: Path
    out_dir: Path
    fig_dir: Path


def _ensure_dirs(*dirs: Path) -> None:
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path, usecols: Iterable[str] | None = None) -> pd.DataFrame:
    return pd.read_csv(path, usecols=list(usecols) if usecols is not None else None)


def load_joined_dataset(data_dir: Path) -> pd.DataFrame:
    """Load cleaned CSVs and join into a session-level dataframe.

    Join key: uid (unique per session).
    """

    geo = _read_csv(
        data_dir / "ga_geo_network.csv",
        usecols=["uid", "continent", "sub_continent", "country", "region", "city"],
    )
    totals = _read_csv(
        data_dir / "ga_total.csv",
        usecols=[
            "uid",
            "visits",
            "transactions",
            "total_transaction_revenue",
            "pageviews",
            "time_on_site",
            "bounces",
        ],
    )
    sessions = _read_csv(
        data_dir / "ga_session.csv",
        usecols=["uid", "full_visitor_id", "date", "channel_grouping"],
    )

    df = sessions.merge(totals, on="uid", how="left").merge(geo, on="uid", how="left")
    return df


def clean_region_revenue(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d", errors="coerce")

    df["total_transaction_revenue"] = pd.to_numeric(
        df["total_transaction_revenue"], errors="coerce"
    )
    df["transactions"] = pd.to_numeric(df["transactions"], errors="coerce")
    df["visits"] = pd.to_numeric(df["visits"], errors="coerce")

    # In GA exports, revenue is typically in micros; the course handout example also matches
    # 28990000 -> $28.99, so divide by 1e6.
    df["revenue_usd"] = df["total_transaction_revenue"] / 1_000_000.0

    # Normalize missing strings
    for col in ["continent", "sub_continent", "country", "region", "city"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df.loc[df[col].isin(["nan", "None", "(not set)"]), col] = pd.NA

    # Some rows use this placeholder string
    placeholder = "not available in demo dataset"
    for col in ["country", "continent", "sub_continent", "region", "city"]:
        if col in df.columns:
            df.loc[df[col] == placeholder, col] = pd.NA

    return df


def summarize_by_region(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (country_summary, continent_summary)."""

    paid = df.loc[df["revenue_usd"].fillna(0) > 0].copy()

    country = (
        paid.groupby(["country"], dropna=True)
        .agg(
            revenue_usd=("revenue_usd", "sum"),
            transactions=("transactions", "sum"),
            sessions=("uid", "count"),
            visitors=("full_visitor_id", pd.Series.nunique),
        )
        .sort_values("revenue_usd", ascending=False)
        .reset_index()
    )

    continent = (
        paid.groupby(["continent"], dropna=True)
        .agg(
            revenue_usd=("revenue_usd", "sum"),
            transactions=("transactions", "sum"),
            sessions=("uid", "count"),
            visitors=("full_visitor_id", pd.Series.nunique),
        )
        .sort_values("revenue_usd", ascending=False)
        .reset_index()
    )

    return country, continent


def save_summaries(country: pd.DataFrame, continent: pd.DataFrame, out_dir: Path) -> None:
    country.to_csv(out_dir / "revenue_by_country.csv", index=False, encoding="utf-8-sig")
    continent.to_csv(out_dir / "revenue_by_continent.csv", index=False, encoding="utf-8-sig")
    country.head(10).to_csv(out_dir / "top10_country_by_revenue.csv", index=False, encoding="utf-8-sig")


def plot_bars(country: pd.DataFrame, continent: pd.DataFrame, fig_dir: Path) -> None:
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_theme(style="whitegrid")

    top10 = country.head(10).copy()
    plt.figure(figsize=(11, 6))
    ax = sns.barplot(data=top10, y="country", x="revenue_usd", color=sns.color_palette()[0])
    ax.set_title("Top 10 Countries by Transaction Revenue (USD)")
    ax.set_xlabel("Revenue (USD)")
    ax.set_ylabel("Country")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)
    plt.tight_layout()
    plt.savefig(fig_dir / "top10_countries_revenue.png", dpi=200)
    plt.close()

    plt.figure(figsize=(9, 5))
    ax = sns.barplot(data=continent, y="continent", x="revenue_usd", color=sns.color_palette()[1])
    ax.set_title("Continents by Transaction Revenue (USD)")
    ax.set_xlabel("Revenue (USD)")
    ax.set_ylabel("Continent")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)
    plt.tight_layout()
    plt.savefig(fig_dir / "continents_revenue.png", dpi=200)
    plt.close()


def plot_world_map(country: pd.DataFrame, fig_dir: Path) -> None:
    import plotly.express as px

    # Plotly expects common country names. Apply a small fixup map for known GA variants.
    name_fix = {
        "United States": "United States",
        "Russia": "Russia",
        "Congo - Kinshasa": "Democratic Republic of the Congo",
        "Congo - Brazzaville": "Republic of the Congo",
        "Ivory Coast": "Cote d'Ivoire",
        "Czech Republic": "Czechia",
        "Venezuela": "Venezuela",
        "Vietnam": "Viet Nam",
        "Laos": "Lao People's Democratic Republic",
        "Bolivia": "Bolivia",
        "Tanzania": "Tanzania",
        "Macedonia (FYROM)": "North Macedonia",
        "Palestine": "Palestine",
    }

    m = country.copy()
    m = m[m["country"].notna()].copy()
    m["country_plot"] = m["country"].map(lambda x: name_fix.get(x, x))

    fig = px.choropleth(
        m,
        locations="country_plot",
        locationmode="country names",
        color="revenue_usd",
        hover_name="country",
        hover_data={"revenue_usd": ":.2f", "transactions": True, "sessions": True},
        color_continuous_scale="Blues",
        title="Transaction Revenue by Country (USD)",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))

    fig.write_html(fig_dir / "country_revenue_world_map.html", include_plotlyjs="cdn")

    # Optional: static export (requires kaleido)
    try:
        fig.write_image(fig_dir / "country_revenue_world_map.png", width=1200, height=650, scale=2)
    except Exception as exc:  # pragma: no cover
        (fig_dir / "country_revenue_world_map_export_failed.txt").write_text(
            f"PNG export failed: {exc}\nHTML version was generated successfully.",
            encoding="utf-8",
        )


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    paths = Paths(
        repo_root=repo_root,
        data_dir=repo_root / "as2_data" / "cleaned",
        out_dir=Path(__file__).resolve().parent / "outputs",
        fig_dir=Path(__file__).resolve().parent / "figures",
    )
    _ensure_dirs(paths.out_dir, paths.fig_dir)

    df = load_joined_dataset(paths.data_dir)
    df = clean_region_revenue(df)

    country, continent = summarize_by_region(df)
    save_summaries(country, continent, paths.out_dir)

    plot_bars(country, continent, paths.fig_dir)
    plot_world_map(country, paths.fig_dir)

    # Write a tiny metadata file for the report
    date_min = df["date"].min()
    date_max = df["date"].max()
    meta = [
        "Regional revenue analysis run metadata",
        f"Rows (sessions): {len(df)}",
        f"Date range: {date_min} ~ {date_max}",
        f"Paid sessions (revenue>0): {(df['revenue_usd'].fillna(0)>0).sum()}",
    ]
    (paths.out_dir / "run_metadata.txt").write_text("\n".join(meta), encoding="utf-8")


if __name__ == "__main__":
    main()
