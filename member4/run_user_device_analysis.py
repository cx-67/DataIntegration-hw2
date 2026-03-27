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
    usecols_list = list(usecols) if usecols is not None else None
    dtype = {col: "string" for col in usecols_list} if usecols_list is not None else "string"
    return pd.read_csv(path, usecols=usecols_list, dtype=dtype, low_memory=False)


def load_joined_dataset(data_dir: Path) -> pd.DataFrame:
    device = _read_csv(
        data_dir / "ga_device.csv",
        usecols=["uid", "browser", "device_category", "operating_system"],
    )
    totals = _read_csv(
        data_dir / "ga_total.csv",
        usecols=["uid", "new_visits", "pageviews", "time_on_site", "visits"],
    )
    sessions = _read_csv(
        data_dir / "ga_session.csv",
        usecols=["uid", "full_visitor_id", "date", "channel_grouping"],
    )

    return sessions.merge(totals, on="uid", how="left").merge(device, on="uid", how="left")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()

    d["date"] = pd.to_datetime(d["date"].astype(str), format="%Y%m%d", errors="coerce")

    for c in ["new_visits", "pageviews", "time_on_site", "visits"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")

    # 新用户标识：new_visits==1
    d["user_type"] = d["new_visits"].fillna(0).apply(lambda x: "New Visitor" if x > 0 else "Returning Visitor")

    # 统一缺失/占位值
    missing_tokens = {"nan", "None", "(not set)", "not available in demo dataset", ""}
    for c in ["browser", "device_category", "operating_system"]:
        d[c] = d[c].astype(str).str.strip()
        d.loc[d[c].isin(missing_tokens), c] = pd.NA
        d[c] = d[c].fillna("Unknown")

    return d


def summarize_device_distribution(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    os_dist = (
        df.groupby("operating_system", dropna=False)["uid"]
        .count()
        .rename("sessions")
        .reset_index()
        .sort_values("sessions", ascending=False)
    )
    os_dist["pct"] = os_dist["sessions"] / os_dist["sessions"].sum()

    browser_dist = (
        df.groupby("browser", dropna=False)["uid"]
        .count()
        .rename("sessions")
        .reset_index()
        .sort_values("sessions", ascending=False)
    )
    browser_dist["pct"] = browser_dist["sessions"] / browser_dist["sessions"].sum()

    device_dist = (
        df.groupby("device_category", dropna=False)["uid"]
        .count()
        .rename("sessions")
        .reset_index()
        .sort_values("sessions", ascending=False)
    )
    device_dist["pct"] = device_dist["sessions"] / device_dist["sessions"].sum()

    return os_dist, browser_dist, device_dist


def summarize_new_vs_returning(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("user_type", dropna=False)
        .agg(
            sessions=("uid", "count"),
            users=("full_visitor_id", pd.Series.nunique),
            avg_pageviews=("pageviews", "mean"),
            avg_time_on_site_sec=("time_on_site", "mean"),
            median_pageviews=("pageviews", "median"),
            median_time_on_site_sec=("time_on_site", "median"),
        )
        .reset_index()
    )
    summary["session_pct"] = summary["sessions"] / summary["sessions"].sum()
    return summary


def save_outputs(
    os_dist: pd.DataFrame,
    browser_dist: pd.DataFrame,
    device_dist: pd.DataFrame,
    user_behavior: pd.DataFrame,
    out_dir: Path,
) -> None:
    os_dist.to_csv(out_dir / "os_distribution.csv", index=False, encoding="utf-8-sig")
    browser_dist.to_csv(out_dir / "browser_distribution.csv", index=False, encoding="utf-8-sig")
    device_dist.to_csv(out_dir / "device_distribution.csv", index=False, encoding="utf-8-sig")
    user_behavior.to_csv(out_dir / "new_vs_returning_behavior.csv", index=False, encoding="utf-8-sig")


def plot_charts(
    os_dist: pd.DataFrame,
    browser_dist: pd.DataFrame,
    device_dist: pd.DataFrame,
    user_behavior: pd.DataFrame,
    fig_dir: Path,
) -> None:
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_theme(style="whitegrid")

    # 1) OS 分布（条形图，Top10）
    os_top = os_dist.head(10).copy()
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(data=os_top, x="operating_system", y="sessions", color=sns.color_palette()[0])
    ax.set_title("Top 10 Operating Systems by Sessions")
    ax.set_xlabel("Operating System")
    ax.set_ylabel("Sessions")
    ax.tick_params(axis="x", rotation=30)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=2)
    plt.tight_layout()
    plt.savefig(fig_dir / "os_distribution_bar.png", dpi=220)
    plt.close()

    # 2) 浏览器分布（条形图，Top10）
    browser_top = browser_dist.head(10).copy()
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(data=browser_top, x="browser", y="sessions", color=sns.color_palette()[1])
    ax.set_title("Top 10 Browsers by Sessions")
    ax.set_xlabel("Browser")
    ax.set_ylabel("Sessions")
    ax.tick_params(axis="x", rotation=30)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=2)
    plt.tight_layout()
    plt.savefig(fig_dir / "browser_distribution_bar.png", dpi=220)
    plt.close()

    # 3) 设备类型分布（饼图）
    device_plot = device_dist.copy()
    plt.figure(figsize=(7, 7))
    plt.pie(
        device_plot["sessions"],
        labels=device_plot["device_category"],
        autopct="%1.1f%%",
        startangle=120,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    plt.title("Device Category Distribution")
    plt.tight_layout()
    plt.savefig(fig_dir / "device_distribution_pie.png", dpi=220)
    plt.close()

    # 4) 新老用户：平均页面浏览量对比
    pv_plot = user_behavior.copy()
    plt.figure(figsize=(7, 5))
    ax = sns.barplot(data=pv_plot, x="user_type", y="avg_pageviews", color=sns.color_palette()[2])
    ax.set_title("Average Pageviews: New vs Returning")
    ax.set_xlabel("User Type")
    ax.set_ylabel("Average Pageviews")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", padding=2)
    plt.tight_layout()
    plt.savefig(fig_dir / "new_vs_returning_avg_pageviews.png", dpi=220)
    plt.close()

    # 5) 新老用户：平均停留时间对比
    plt.figure(figsize=(7, 5))
    ax = sns.barplot(data=pv_plot, x="user_type", y="avg_time_on_site_sec", color=sns.color_palette()[3])
    ax.set_title("Average Time on Site (sec): New vs Returning")
    ax.set_xlabel("User Type")
    ax.set_ylabel("Average Time on Site (sec)")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f", padding=2)
    plt.tight_layout()
    plt.savefig(fig_dir / "new_vs_returning_avg_time_on_site.png", dpi=220)
    plt.close()


def write_conclusions(
    os_dist: pd.DataFrame,
    browser_dist: pd.DataFrame,
    device_dist: pd.DataFrame,
    user_behavior: pd.DataFrame,
    out_dir: Path,
) -> None:
    top_os = os_dist.iloc[0]
    top_browser = browser_dist.iloc[0]
    top_device = device_dist.iloc[0]

    new_row = user_behavior.loc[user_behavior["user_type"] == "New Visitor"].iloc[0]
    ret_row = user_behavior.loc[user_behavior["user_type"] == "Returning Visitor"].iloc[0]

    pv_gap = ret_row["avg_pageviews"] - new_row["avg_pageviews"]
    time_gap = ret_row["avg_time_on_site_sec"] - new_row["avg_time_on_site_sec"]

    lines = [
        "# 任务四：用户行为与设备分析结论",
        "",
        "## 1. 设备与浏览环境分布",
        f"- 操作系统占比最高的是 **{top_os['operating_system']}**（{top_os['sessions']} 次会话，占比 {top_os['pct']:.2%}）。",
        f"- 浏览器占比最高的是 **{top_browser['browser']}**（{top_browser['sessions']} 次会话，占比 {top_browser['pct']:.2%}）。",
        f"- 设备类型占比最高的是 **{top_device['device_category']}**（{top_device['sessions']} 次会话，占比 {top_device['pct']:.2%}）。",
        "",
        "## 2. 新老用户行为差异（页面浏览量与停留时间）",
        f"- 新用户平均页面浏览量：**{new_row['avg_pageviews']:.2f}**，老用户平均页面浏览量：**{ret_row['avg_pageviews']:.2f}**。",
        f"- 新用户平均停留时间：**{new_row['avg_time_on_site_sec']:.1f} 秒**，老用户平均停留时间：**{ret_row['avg_time_on_site_sec']:.1f} 秒**。",
        f"- 老用户相对新用户，平均页面浏览量高 **{pv_gap:.2f}**，平均停留时间高 **{time_gap:.1f} 秒**。",
        "",
        "## 3. 分析解读（可用于HW2报告第3–4页、第11页）",
        "- 用户访问设备呈现明显集中趋势，应优先保证主流操作系统与浏览器的兼容性和体验。",
        "- 老用户在深度浏览（页数）与停留时长上通常高于新用户，说明复访用户更容易产生深入行为。",
        "- 建议针对新用户优化落地页引导与关键路径设计，缩短首访用户的决策时间，提高向复访用户转化的概率。",
    ]

    (out_dir / "analysis_conclusions.md").write_text("\n".join(lines), encoding="utf-8")


def resolve_data_dir(repo_root: Path) -> Path:
    candidates = [
        repo_root / "as2_data" / "cleaned",
        repo_root.parent / "更正as2全量同步数据" / "cleaned",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("未找到 cleaned 数据目录。请检查 as2_data/cleaned 或 ../更正as2全量同步数据/cleaned")


def _base_path() -> Path:
    # 在 .py 脚本中可用 __file__；在 Jupyter 中不存在 __file__
    if "__file__" in globals():
        return Path(__file__).resolve().parent
    return Path.cwd()


def main() -> None:
    base_path = _base_path()

    # 若从 member4 目录运行，则 repo_root 是上一级；否则默认当前目录
    repo_root = base_path.parent if base_path.name.lower() == "member4" else base_path
    data_dir = resolve_data_dir(repo_root)

    paths = Paths(
        repo_root=repo_root,
        data_dir=data_dir,
        out_dir=base_path / "outputs",
        fig_dir=base_path / "figures",
    )
    _ensure_dirs(paths.out_dir, paths.fig_dir)

    df = load_joined_dataset(paths.data_dir)
    df = clean_data(df)

    os_dist, browser_dist, device_dist = summarize_device_distribution(df)
    user_behavior = summarize_new_vs_returning(df)

    save_outputs(os_dist, browser_dist, device_dist, user_behavior, paths.out_dir)
    plot_charts(os_dist, browser_dist, device_dist, user_behavior, paths.fig_dir)
    write_conclusions(os_dist, browser_dist, device_dist, user_behavior, paths.out_dir)

    date_min = df["date"].min()
    date_max = df["date"].max()
    metadata = [
        "User/device analysis run metadata",
        f"Data dir: {paths.data_dir}",
        f"Rows (sessions): {len(df)}",
        f"Date range: {date_min} ~ {date_max}",
        f"New sessions: {(df['user_type'] == 'New Visitor').sum()}",
        f"Returning sessions: {(df['user_type'] == 'Returning Visitor').sum()}",
    ]
    (paths.out_dir / "run_metadata.txt").write_text("\n".join(metadata), encoding="utf-8")


if __name__ == "__main__":
    main()
