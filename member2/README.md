# member2 — 地域与交易额分析

本目录对应《作业2分工》中的“2. 地域与交易额分析负责人”。

## 产出物

- `run_region_revenue_analysis.py`：一键生成汇总结果与图表
- `outputs/`：聚合后的 CSV / 运行元信息
- `figures/`：柱状图 PNG + 世界地图 HTML（并尝试导出 PNG）
- `region_revenue_analysis.ipynb`：用于提交的 Notebook（可复现生成过程）

## 数据位置

脚本默认读取仓库根目录下的：

- `as2_data/cleaned/ga_session.csv`
- `as2_data/cleaned/ga_total.csv`
- `as2_data/cleaned/ga_geo_network.csv`

（按 `uid` 进行 session 级别 join）

## 运行方式

在仓库根目录下执行（Windows / PowerShell）：

```powershell
# 安装依赖（可选：如果你已安装过可跳过）
d:/study/computer/dataIntegration/.venv/Scripts/python.exe -m pip install -r DataIntegration-hw2/member2/requirements.txt

# 生成图表与汇总结果
d:/study/computer/dataIntegration/.venv/Scripts/python.exe DataIntegration-hw2/member2/run_region_revenue_analysis.py
```

运行完成后可在 `DataIntegration-hw2/member2/figures/` 和 `DataIntegration-hw2/member2/outputs/` 查看结果。

## 口径说明

- 交易额字段使用 `ga_total.total_transaction_revenue`
- 根据作业说明示例（28990000 -> $28.99），将其按 GA 常见口径视为 micros，换算为：`revenue_usd = total_transaction_revenue / 1e6`
- 地域维度来自 `ga_geo_network`（country/continent/sub_continent 等）
