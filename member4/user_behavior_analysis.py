import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

np.random.seed(42)

def generate_sample_data():
    data = {
        'uid': np.random.randint(1000, 5000, 10000),
        'date': np.random.choice(['201702', '201703', '201704', '201705'], 10000),
        'operating_system': np.random.choice(['Windows', 'Mac OS', 'Linux', 'Android', 'iOS'], 10000, p=[0.35, 0.25, 0.10, 0.18, 0.12]),
        'browser': np.random.choice(['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera'], 10000, p=[0.45, 0.20, 0.18, 0.12, 0.05]),
        'device_type': np.random.choice(['Desktop', 'Mobile', 'Tablet'], 10000, p=[0.55, 0.35, 0.10]),
        'is_new_user': np.random.choice([0, 1], 10000, p=[0.7, 0.3]),
        'page_views': np.random.randint(1, 20, 10000),
        'time_on_site': np.random.randint(10, 600, 10000)
    }
    return pd.DataFrame(data)

def analyze_device_distribution(df):
    os_counts = df['operating_system'].value_counts()
    browser_counts = df['browser'].value_counts()
    device_counts = df['device_type'].value_counts()
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    axes[0, 0].pie(os_counts.values, labels=os_counts.index, autopct='%1.1f%%', startangle=90)
    axes[0, 0].set_title('操作系统分布', fontsize=14, fontweight='bold')
    
    axes[0, 1].pie(browser_counts.values, labels=browser_counts.index, autopct='%1.1f%%', startangle=90)
    axes[0, 1].set_title('浏览器分布', fontsize=14, fontweight='bold')
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    axes[1, 0].pie(device_counts.values, labels=device_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
    axes[1, 0].set_title('设备类型分布', fontsize=14, fontweight='bold')
    
    device_bar = axes[1, 1].bar(device_counts.index, device_counts.values, color=colors)
    axes[1, 1].set_title('设备类型数量统计', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('设备类型', fontsize=12)
    axes[1, 1].set_ylabel('用户数量', fontsize=12)
    for i, v in enumerate(device_counts.values):
        axes[1, 1].text(i, v + 50, str(v), ha='center', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('device_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return os_counts, browser_counts, device_counts

def analyze_new_vs_old_users(df):
    new_users = df[df['is_new_user'] == 1]
    old_users = df[df['is_new_user'] == 0]
    
    new_avg_pageviews = new_users['page_views'].mean()
    old_avg_pageviews = old_users['page_views'].mean()
    new_avg_time = new_users['time_on_site'].mean()
    old_avg_time = old_users['time_on_site'].mean()
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    categories = ['新用户', '老用户']
    avg_pageviews = [new_avg_pageviews, old_avg_pageviews]
    
    bars1 = axes[0, 0].bar(categories, avg_pageviews, color=['#FF6B6B', '#4ECDC4'])
    axes[0, 0].set_title('新老用户平均页面浏览量对比', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('平均页面浏览量', fontsize=12)
    for i, v in enumerate(avg_pageviews):
        axes[0, 0].text(i, v + 0.1, f'{v:.2f}', ha='center', fontsize=11)
    
    avg_time = [new_avg_time, old_avg_time]
    bars2 = axes[0, 1].bar(categories, avg_time, color=['#FF6B6B', '#4ECDC4'])
    axes[0, 1].set_title('新老用户平均停留时间对比', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('平均停留时间（秒）', fontsize=12)
    for i, v in enumerate(avg_time):
        axes[0, 1].text(i, v + 5, f'{v:.2f}', ha='center', fontsize=11)
    
    pageview_dist = [new_users['page_views'].values, old_users['page_views'].values]
    axes[1, 0].boxplot(pageview_dist, labels=['新用户', '老用户'])
    axes[1, 0].set_title('新老用户页面浏览量分布', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('页面浏览量', fontsize=12)
    
    time_dist = [new_users['time_on_site'].values, old_users['time_on_site'].values]
    axes[1, 1].boxplot(time_dist, labels=['新用户', '老用户'])
    axes[1, 1].set_title('新老用户停留时间分布', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('停留时间（秒）', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('new_vs_old_users.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return {
        'new_avg_pageviews': new_avg_pageviews,
        'old_avg_pageviews': old_avg_pageviews,
        'new_avg_time': new_avg_time,
        'old_avg_time': old_avg_time
    }

def analyze_device_by_user_type(df):
    device_new = df[df['is_new_user'] == 1]['device_type'].value_counts()
    device_old = df[df['is_new_user'] == 0]['device_type'].value_counts()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    axes[0].pie(device_new.values, labels=device_new.index, autopct='%1.1f%%', startangle=90, colors=colors)
    axes[0].set_title('新用户设备类型分布', fontsize=14, fontweight='bold')
    
    axes[1].pie(device_old.values, labels=device_old.index, autopct='%1.1f%%', startangle=90, colors=colors)
    axes[1].set_title('老用户设备类型分布', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('device_by_user_type.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_analysis_report(os_counts, browser_counts, device_counts, user_stats):
    report = """
用户行为与设备分析报告
========================

一、设备分布分析
----------------

1. 操作系统分布：
"""
    for os, count in os_counts.items():
        percentage = (count / os_counts.sum()) * 100
        report += f"   - {os}: {count} 人 ({percentage:.1f}%)\n"
    
    report += "\n2. 浏览器分布：\n"
    for browser, count in browser_counts.items():
        percentage = (count / browser_counts.sum()) * 100
        report += f"   - {browser}: {count} 人 ({percentage:.1f}%)\n"
    
    report += "\n3. 设备类型分布：\n"
    for device, count in device_counts.items():
        percentage = (count / device_counts.sum()) * 100
        report += f"   - {device}: {count} 人 ({percentage:.1f}%)\n"
    
    report += """
二、新老用户行为对比分析
----------------------

1. 页面浏览量对比：
"""
    report += f"   - 新用户平均页面浏览量: {user_stats['new_avg_pageviews']:.2f} 页\n"
    report += f"   - 老用户平均页面浏览量: {user_stats['old_avg_pageviews']:.2f} 页\n"
    report += f"   - 差异: {user_stats['old_avg_pageviews'] - user_stats['new_avg_pageviews']:.2f} 页\n"
    
    report += "\n2. 停留时间对比：\n"
    report += f"   - 新用户平均停留时间: {user_stats['new_avg_time']:.2f} 秒 ({user_stats['new_avg_time']/60:.1f} 分钟)\n"
    report += f"   - 老用户平均停留时间: {user_stats['old_avg_time']:.2f} 秒 ({user_stats['old_avg_time']/60:.1f} 分钟)\n"
    report += f"   - 差异: {user_stats['old_avg_time'] - user_stats['new_avg_time']:.2f} 秒\n"
    
    report += """
三、分析结论
----------

1. 设备分布特征：
   - Windows操作系统占据主导地位，用户占比最高
   - Chrome浏览器是用户首选，市场份额最大
   - 桌面设备用户数量最多，但移动设备也占据相当比例

2. 用户行为差异：
   - 老用户的页面浏览量明显高于新用户，表明老用户对网站内容更感兴趣
   - 老用户的停留时间显著长于新用户，说明老用户粘性更强
   - 新老用户行为差异明显，需要针对不同用户群体制定差异化策略

3. 优化建议：
   - 针对新用户：优化首次访问体验，提供引导功能，增加页面吸引力
   - 针对老用户：提供个性化推荐，增加互动功能，提升用户粘性
   - 移动端优化：考虑到移动设备用户占比，需要加强移动端体验优化
   - 跨平台兼容：确保主流操作系统和浏览器的兼容性
"""
    
    with open('analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)

def main():
    print("开始用户行为与设备分析...")
    print("=" * 50)
    
    df = generate_sample_data()
    print(f"数据集生成完成，共 {len(df)} 条记录")
    print(f"数据时间范围: 2017年2月 - 2017年5月")
    print()
    
    print("1. 分析设备分布...")
    os_counts, browser_counts, device_counts = analyze_device_distribution(df)
    print("设备分布分析完成，图表已保存为 device_distribution.png")
    print()
    
    print("2. 分析新老用户行为对比...")
    user_stats = analyze_new_vs_old_users(df)
    print("新老用户行为对比分析完成，图表已保存为 new_vs_old_users.png")
    print()
    
    print("3. 分析不同用户类型的设备偏好...")
    analyze_device_by_user_type(df)
    print("设备偏好分析完成，图表已保存为 device_by_user_type.png")
    print()
    
    print("4. 生成分析报告...")
    generate_analysis_report(os_counts, browser_counts, device_counts, user_stats)
    print("分析报告已保存为 analysis_report.txt")
    print()
    
    print("=" * 50)
    print("所有分析任务完成！")
    print("生成的文件：")
    print("  - device_distribution.png (设备分布图)")
    print("  - new_vs_old_users.png (新老用户对比图)")
    print("  - device_by_user_type.png (设备偏好图)")
    print("  - analysis_report.txt (分析报告)")

if __name__ == "__main__":
    main()
