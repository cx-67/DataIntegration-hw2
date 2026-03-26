# 商品与用户购买分析 - 完成报告

**项目成员**: Member 5  
**完成日期**: 2026年  
**数据源**: E:\数据集成\cleaned (Google Analytics真实数据)

---

## 一、项目概述

本项目对Google Analytics电商数据进行深入分析，重点关注：
- 🛍️ **商品分析**: 销售额/销量Top 10分析
- 👥 **用户分析**: 消费金额/消费行为分析
- 📊 **相关性分析**: 销售额与销量的关系
- 💰 **用户分层**: VIP用户识别与分析

---

## 二、关键数据指标

### 2.1 基础统计
| 指标 | 数值 |
|-----|------|
| 总交易记录 | 2,161 笔 |
| 消费用户数 | 1,031 人 |
| 不同商品数 | 599 种 |
| 总消费金额 | ¥160,910 元 |

### 2.2 商品分析

**Top 10销售额商品** (占总销售额 23.80%)
1. YouTube Hard Cover Journal - ¥5,559
2. Google Hard Cover Journal - ¥5,134
3. Google Spiral Journal with Pen - ¥4,941
4. Leatherette Journal - ¥4,661
5. Google 22 oz Water Bottle - ¥3,994
6. Sport Bag - ¥3,184
7. Recycled Paper Journal Set - ¥2,961
8. Google Men's 100% Cotton Short Sleeve Hero Tee Black - ¥2,894
9. YouTube Twill Cap - ¥2,489
10. Google Twill Cap - ¥2,474

**Top 10销量商品** (累计销量 7,172件)
1. Google 22 oz Water Bottle - 1,358件
2. Recycled Paper Journal Set - 830件
3. Google Kick Ball - 761件
4. Google Spiral Journal with Pen - 719件
5. SPF-15 Slim & Slender Lip Balm - 678件
6. Sport Bag - 652件
7. Leatherette Journal - 622件
8. Foam Can and Bottle Cooler - 578件
9. Spiral Notebook and Pen Set - 524件
10. Google Sunglasses - 450件

### 2.3 用户分析

**Top 10消费用户** (累计消费 ¥55,612,占34.56%)
- 人均消费: ¥5,561
- Top 1用户消费额: ¥25,255
- 平均交易次数: 1.6次

**用户分层统计**
| 用户层级 | 用户数 | 消费额(¥) | 占比 | 人均消费(¥) |
|--------|-------|---------|------|----------|
| VIP用户 | 258 | 128,307 | 79.74% | 497.31 |
| 高价值用户 | 257 | 17,929 | 11.14% | 69.76 |
| 中等用户 | 257 | 9,680 | 6.01% | 37.66 |
| 基础用户 | 259 | 4,994 | 3.10% | 19.28 |

---

## 三、核心发现

### 3.1 商品维度洞察
- **销售额与销量强正相关** (相关系数 0.9222)
  - 说明销量大的商品通常销售额也大
  - 高价格+高销量的商品才能驱动业绩
  
- **商品集中度中等**
  - Top 10商品销售额占比仅23.8%
  - 意味着商品组合相对均衡，长尾效应明显

- **品类多元化**
  - 599种商品实现了¥160,910销售额
  - 平均单品销售额 ¥269
  - 建议优化品类结构，重点推广高ROI商品

### 3.2 用户维度洞察
- **用户消费高度集中**
  - Top 10用户贡献34.56%销售额
  - VIP用户(25%人口)贡献79.74%销售额
  - 帕累托原则(80/20法则)明显

- **用户金字塔健康**
  - 基础用户占25% (入门新客)
  - VIP用户占25% (核心客户)
  - 中间层级均衡分布

- **VIP用户价值显著**
  - VIP平均消费 ¥497/人
  - 基础用户平均消费 ¥19/人
  - 转化倍数 ~26倍

### 3.3 结构性洞察
- **销售结构健康**
  - 销售额与销量保持同向变化
  - 无明显的"低价大销"或"高价滞销"异常
  - 定价策略合理

---

## 四、建议与对策

### 4.1 商品策略
1. **强化Top 10商品**
  - 加大Top 10商品的库存和推广投入
  - 这10件商品已证明市场认可

2. **优化产品组合**
  - 分析599种商品中的高毛利品种
  - 建立分级管理体系（星级商品）

3. **长尾商品管理**
  - 评估低销量商品的库存成本
  - 考虑下架或促销处理

### 4.2 用户运营
1. **VIP用户维护**
  - 258个VIP用户贡献79.74%销售额
  - 建立专属权益和增值服务体系
  - 实现VIP用户的复购和口碑传播

2. **分层营销策略**
  - 基础用户: 优惠吸引，降低转化成本
  - 中等用户: 挖掘需求，拉升客单价
  - 高价值用户: 保留和升级到VIP
  - VIP用户: 增值服务，提升粘性

3. **用户转化路径**
  - 建立清晰的升级路径：基础→中等→高价值→VIP
  - 设定阶段性消费目标和激励

### 4.3 数据应用
1. 建立定期监控机制，跟踪关键指标变化
2. 按月度/季度生成对标分析，评估策略效果
3. 通过A/B测试验证新的商品/营销策略

---

## 五、交付件清单

### 5.1 分析报告
✅ analysis_summary.txt - 数据总结报告  
✅ product_user_purchase_analysis.ipynb - 完整分析代码和执行结果

### 5.2 可视化图表 (6张)
✅ top10_products_by_revenue.png - Top 10销售额商品  
✅ top10_products_by_volume.png - Top 10销量商品  
✅ products_revenue_vs_volume_comparison.png - 销售额vs销量对比  
✅ top10_users_by_spending.png - Top 10消费用户  
✅ user_spending_tier_distribution.png - 用户分层分布  
✅ revenue_vs_volume_correlation.png - 销售额与销量相关性  

### 5.3 数据导出 (3份CSV)
✅ top10_products_by_revenue.csv - Top 10销售额商品数据  
✅ top10_products_by_volume.csv - Top 10销量商品数据  
✅ top10_users_by_spending.csv - Top 10消费用户数据  

### 5.4 辅助代码
✅ data_processor.py - 数据处理模块（可复用）  
✅ inspect_data.py - 数据探索脚本

---

## 六、技术细节

### 6.1 数据处理
- **数据源**: Google Analytics原始CSV导出
- **数据量**: 324,096条GA_HIT记录，71,812条GA_TOTAL记录
- **有效交易**: 2,161笔(JSON字段解析后)
- **数据清洗**: JSON嵌套字段展平，金额单位转换(微元→元)

### 6.2 分析方法
- Pandas数据聚合和分组统计
- 相关性分析 (Pearson correlation)
- 用户分层 (四分位数分割)
- Matplotlib/Seaborn可视化

### 6.3 环境
- Python 3.13
- 核心库: pandas, numpy, matplotlib, seaborn
- Jupyter Notebook交互式分析

---

## 七、结语

本次分析成功从实际Google Analytics数据中提取了商品和用户的关键洞察，为后续的商业决策提供了量化的依据。

**核心成果:**
- 📊 清晰的商品排名和销售贡献度分析
- 👥 精准的用户分层和VIP识别
- 💡 可行的优化建议和运营方向

建议定期（如月度）重复执行本分析，监控指标变化趋势，并根据结果优化运营策略。

---

**联系信息**: Member 5  
**报告生成**: 2026年
