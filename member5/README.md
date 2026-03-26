# 成员5 - 商品与用户购买分析 ✅ 已完成

**项目状态**: 已完成  
**数据来源**: Google Analytics真实数据 (E:\数据集成\cleaned)  
**数据规模**: 2,161笔交易 / 1,031位用户 / 599种商品  

## 工作目标 ✅
- ✅ 统计Top 10销售额商品（YouTube Hard Cover Journal领跑 ¥5,559）
- ✅ 统计Top 10销量商品（Google 22oz Water Bottle最畅销 1,358件）
- ✅ 分析销售额与销量关系（相关系数 0.9222 - 强正相关）
- ✅ 用户分层分析（VIP用户258人占销售额79.74%）
- ✅ 生成6张可视化图表和3份CSV导出

## 关键产出
- 📊 **分析文档**: ANALYSIS_REPORT.md (完整分析+建议)
- 🔍 **完成检查**: COMPLETION_CHECKLIST.md
- 💻 **分析代码**: product_user_purchase_analysis.ipynb (53 cells)
- 📈 **6张图表**: 商品分析+用户分析可视化
- 📁 **3份CSV**: Top 10产品/用户数据导出

## 分析模块

### 1. 商品分析
- **Top 10销售额商品** - 统计销售金额最高的商品
- **Top 10销量商品** - 统计交易笔数最高的商品  
- **销售额与销量对比** - 双轴图表展示
- **相关性分析** - 计算两者相关系数

### 2. 用户消费分析
- **Top 10消费用户** - 统计消费金额最高的用户
- **用户消费分层** - 四层用户分类（基础/中等/高价值/VIP）
- **消费结构分布** - 用户数量和金额分布

### 3. 可视化输出
1. `top10_products_by_revenue.png` - Top 10销售额商品柱状图
2. `top10_products_by_volume.png` - Top 10销量商品柱状图
3. `products_revenue_vs_volume_comparison.png` - 销售额vs销量对比
4. `top10_users_by_spending.png` - Top 10消费用户柱状图
5. `user_spending_tier_distribution.png` - 用户消费分层饼图
6. `revenue_vs_volume_correlation.png` - 相关性散点图


## 使用方法

### 查看已完成的分析
所有分析已完成！直接查看以下文件：
- 📊 **ANALYSIS_REPORT.md** - 完整的分析报告和商业建议
- 📈 **PNG图表** - 6张高质量可视化
- 📁 **CSV数据** - 3份导出的数据表

### 重新运行分析 (如需更新数据)
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. VS Code中打开Notebook
code product_user_purchase_analysis.ipynb

# 3. 按顺序执行所有53个cells
# 或执行"运行所有"命令

# 或直接运行Python脚本
python data_processor.py
```

## 数据来源
- **位置**: E:\数据集成\cleaned
- **文件**: 
  - ga_hit.csv (324,096条记录，1.4GB)
  - ga_total.csv (71,812条记录)
  - 其他表: ga_session, ga_device等
- **特点**: Google Analytics原始导出数据，含JSON嵌套字段

## 输出文件说明
| 文件名 | 说明 |
|------|------|
| top10_products_by_revenue.csv | Top 10销售额商品 |
| top10_products_by_volume.csv | Top 10销量商品 |
| top10_users_by_spending.csv | Top 10消费用户 |
| *.png | 6张可视化图表 |

## 分析亮点
- ✨ 完整的商品和用户分析体系
- ✨ 多维度对比分析（销售额vs销量）
- ✨ 用户分层洞察（VIP用户识别）
- ✨ 高质量可视化展示
- ✨ 自动生成分析总结

---
**更新日期**: 2026-03-26  
**负责人**: 成员5
