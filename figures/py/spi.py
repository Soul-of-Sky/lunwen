import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 设置中文字体 ---
# 根据你的系统环境选择合适的字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

# 设置全局字体大小和线宽
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.5

def generate_and_plot_sampled():
    # --- 1. 数据模拟 (采样周期 200ms) ---
    dt = 0.2  # 采样周期 200ms
    t = np.arange(0, 60 + dt, dt)
    
    # 初始化数组
    spi = np.zeros_like(t)
    lat_aggressive = np.zeros_like(t)
    lat_conservative = np.zeros_like(t)
    lat_hpro = np.zeros_like(t)
    
    # 设置随机种子保证结果可复现
    np.random.seed(42)
    noise_spi = np.random.normal(0, 0.02, size=len(t))
    noise_lat = np.random.normal(0, 0.01, size=len(t))

    for i, time in enumerate(t):
        # 1.1 模拟 SPI 系统压力指数
        if time < 20:
            base_spi = 0.2  # 低负载
        elif time < 40:
            base_spi = 0.85 # 高负载激增
        else:
            base_spi = 0.55 # 回落至标准区间
        spi[i] = base_spi + noise_spi[i]
        
        # 1.2 模拟 激进策略 (Aggressive)
        if 20 <= time < 40:
            # 模拟负载飙升导致的延迟增加 (先升后降的梯形)
            if time < 30:
                # 线性上升至 4.5
                val = 1.0 + (3.5 * (time - 20) / 10)
            else:
                # 线性下降
                val = 4.5 - (3.5 * (time - 30) / 10)
            lat_aggressive[i] = val
        else:
            lat_aggressive[i] = 1.0
        # 确保基准值不低于1.0
        lat_aggressive[i] = max(lat_aggressive[i], 1.0) + noise_lat[i]
        
        # 1.3 模拟 保守策略 (Conservative)
        # 始终保持低延迟 (牺牲了吞吐，但延迟低)
        lat_conservative[i] = 1.0 + noise_lat[i]
        
        # 1.4 模拟 HPRO (本文策略)
        # 在高负载区间(20-40s)切换模式，延迟略有波动但被压制
        if 20 <= time < 40:
             # 模拟受控的轻微波动
             lat_hpro[i] = 1.0 + 0.15 * np.exp(-0.5 * ((time - 30) / 5)**2)
        else:
             lat_hpro[i] = 1.0
        lat_hpro[i] += noise_lat[i]

    # --- 2. 保存数据到文件 ---
    df = pd.DataFrame({
        'time': t,
        'spi': spi,
        'latency_aggressive': lat_aggressive,
        'latency_conservative': lat_conservative,
        'latency_hpro': lat_hpro
    })
    filename = 'spi_latency_sampled_data_200ms.csv'
    df.to_csv(filename, index=False)
    print(f"模拟数据已生成并保存至: {filename}")

    # --- 3. 绘图 (关键：使用 step 函数) ---
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 定义颜色
    color_agg = '#d62728' # 红
    color_con = '#1f77b4' # 蓝
    color_hpro = '#2ca02c' # 绿
    color_spi = 'gray'

    # 关键：使用 step(where='post') 绘制阶梯状采样线
    # where='post' 表示在采样点之后发生跳变，符合数字系统的零阶保持特性
    l1, = ax1.step(t, lat_aggressive, where='post', color=color_agg, linestyle='-', linewidth=1, label='激进策略')
    l2, = ax1.step(t, lat_conservative, where='post', color=color_con, linestyle='-', linewidth=1, label='保守策略')
    l3, = ax1.step(t, lat_hpro, where='post', color=color_hpro, linestyle='-', linewidth=2, label='HPRO')

    ax1.set_xlabel('时间 (s)', fontsize=14)
    ax1.set_ylabel('归一化 99% 尾延迟', fontsize=14)
    ax1.set_ylim(0.5, 5.0)
    ax1.tick_params(axis='y', labelsize=12)
    ax1.grid(True, linestyle='--', alpha=0.3)

    # --- 右轴：SPI 指数 ---
    ax2 = ax1.twinx()
    # SPI 也使用 step 绘制
    l4, = ax2.step(t, spi, where='post', color=color_spi, linestyle='-', linewidth=1.5, alpha=0.4, label='SPI')
    
    ax2.set_ylabel('SPI 值', fontsize=14, color='dimgray')
    ax2.set_ylim(0, 1.1)
    ax2.tick_params(axis='y', labelcolor='dimgray')

    # --- 阈值线标注 ---
    ax2.axhline(y=0.8, color='black', linestyle='-.', linewidth=1, alpha=0.5)
    ax2.text(61, 0.8 + 0.01, '高阈值 (0.8)',
            ha='left', va='bottom', fontsize=10, color='black')

    ax2.axhline(y=0.3, color='black', linestyle='-.', linewidth=1, alpha=0.5)
    ax2.text(61, 0.3 + 0.01, '低阈值 (0.3)',
            ha='left', va='bottom', fontsize=10, color='black')



    # --- 模式背景区域标注 ---
    # 低压模式
    ax1.axvspan(0, 20, color='green', alpha=0.05)
    ax1.text(10, 4.6, '低压模式\n(全速传输)', ha='center', va='center', fontsize=11, fontweight='bold', color='darkgreen')

    # 高压模式
    ax1.axvspan(20, 40, color='red', alpha=0.05)
    ax1.text(30, 4.6, '高压模式\n(最小干扰)', ha='center', va='center', fontsize=11, fontweight='bold', color='darkred')
    
    # 箭头注释
    # ax1.annotate('延迟飙升 (4.5x)', xy=(30, 4.5), xytext=(36, 3.8),
    #              arrowprops=dict(facecolor='black', shrink=0.05), fontsize=10)
    
    # ax1.annotate('HPRO 压制效果 (<1.15x)', xy=(30, 1.15), xytext=(36, 1.8),
    #              arrowprops=dict(facecolor='darkgreen', shrink=0.05), fontsize=10, color='darkgreen')

    # 标准模式
    ax1.axvspan(40, 60, color='blue', alpha=0.05)
    ax1.text(50, 4.6, '标准模式\n(均衡调度)', ha='center', va='center', fontsize=11, fontweight='bold', color='navy')

    # --- 图例 ---
    lines = [l1, l2, l3, l4]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, fancybox=True, shadow=True, fontsize=10)

    plt.tight_layout()
    
    # 保存为 PDF
    plt.savefig('spi.pdf')
    plt.show()

if __name__ == "__main__":
    generate_and_plot_sampled()