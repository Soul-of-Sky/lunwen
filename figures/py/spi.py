import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- 设置中文字体 ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS', 'sans-serif'] 
plt.rcParams['axes.unicode_minus'] = False 

# 设置全局字体大小和线宽
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.5

def generate_and_plot_sampled_v4():
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
    noise_lat_base = np.random.normal(0, 0.01, size=len(t))
    noise_lat_agg_burst = np.random.normal(0, 0.5, size=len(t)) 
    noise_lat_agg_mid = np.random.normal(0, 0.2, size=len(t)) 
    # HPRO 专用微小波动
    noise_lat_hpro_small = np.random.normal(0, 0.05, size=len(t)) 

    for i, time in enumerate(t):
        # 1.1 模拟 SPI 系统压力指数
        if time < 20:
            base_spi = 0.2
        elif time < 40:
            base_spi = 0.88
        else:
            base_spi = 0.55
        spi[i] = base_spi + noise_spi[i]
        
        # --- 1.2 模拟 激进策略 (Aggressive) ---
        if time < 20:
            # 低负载：基准延迟
            val = 1.0
            current_noise = noise_lat_base[i]
        elif time < 40:
            # 高负载激增：延迟立刻到高位(4.0)，并叠加大幅度波动噪声
            val = 4.0 
            current_noise = noise_lat_base[i] + noise_lat_agg_burst[i] 
        else:
            # 标准模式（40s 之后）：延迟立刻下降到中等水平 (2.0)，并保持中等波动
            val = 2.0
            current_noise = noise_lat_base[i] + noise_lat_agg_mid[i]
            
        lat_aggressive[i] = max(val, 1.0) + current_noise
        
        # --- 1.3 模拟 保守策略 (Conservative) ---
        lat_conservative[i] = 1.0 + noise_lat_base[i]
        
        # --- 1.4 模拟 HPRO (本文策略) ---
        if 20 <= time < 40:
            # 模式：高压模式
            # 延迟上升到一个被压制的值 (例如 1.2)，并保持微小波动
            
            # 模拟：20s 时有一个短暂的切换尖峰 (20s-20.4s)，然后回撤到稳定高值 (1.2)
            if time < 20.4:
                 # 尖峰：从 1.0 迅速升至 1.3
                 rise_factor = (time - 20) / 0.4 
                 base_hpro = 1.0 + 0.3 * rise_factor
            elif time < 21:
                 # 回撤：从 1.3 迅速降至受控高值 1.2
                 fall_factor = (time - 20.4) / 0.6
                 base_hpro = 1.3 - 0.1 * fall_factor
            else:
                 # 稳定受控高值：持续保持在 1.2
                 base_hpro = 1.2
                 
            # 叠加微小波动噪声
            lat_hpro[i] = base_hpro + noise_lat_hpro_small[i]
            
        else:
             # 低压/标准模式：基准延迟 1.0
             lat_hpro[i] = 1.0 + noise_lat_base[i]
             
        lat_hpro[i] = max(lat_hpro[i], 1.0) # 确保不低于基准线

    # --- 2. 保存数据到文件 ---
    df = pd.DataFrame({
        'time': t,
        'spi': spi,
        'latency_aggressive': lat_aggressive,
        'latency_conservative': lat_conservative,
        'latency_hpro': lat_hpro
    })
    filename = 'spi_latency_sampled_data.csv'
    df.to_csv(filename, index=False)
    print(f"模拟数据已生成并保存至: {filename}")

    # --- 3. 绘图 ---
    fig, ax1 = plt.subplots(figsize=(10, 6))
    

    # 定义颜色
    color_agg = '#d62728' 
    color_con = '#1f77b4' 
    color_hpro = '#2ca02c' 
    color_spi = 'gray'

    # 绘制阶梯状采样线
    l1, = ax1.step(t, lat_aggressive, where='post', color=color_agg, linestyle='-', linewidth=1, label='激进策略')
    l2, = ax1.step(t, lat_conservative, where='post', color=color_con, linestyle='-', linewidth=1, label='保守策略')
    l3, = ax1.step(t, lat_hpro, where='post', color=color_hpro, linestyle='-', linewidth=2, label='HPRO')

    ax1.set_xlabel('时间 (s)', fontsize=14)
    ax1.set_ylabel('归一化 99% 尾延迟', fontsize=14)
    ax1.set_ylim(0.5, 6.0) 
    ax1.tick_params(axis='y', labelsize=12)
    ax1.grid(True, linestyle='--', alpha=0.3)

    # --- 右轴：SPI 指数 ---
    ax2 = ax1.twinx()
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
    ax1.axvspan(0, 20, color='green', alpha=0.05)
    ax1.text(10, 5.5, '低压模式\n(全速保存)', ha='center', va='center', fontsize=11, fontweight='bold', color='darkgreen')

    ax1.axvspan(20, 40, color='red', alpha=0.05)
    ax1.text(30, 5.5, '高压模式\n(最小干扰)', ha='center', va='center', fontsize=11, fontweight='bold', color='darkred')
    
    ax1.axvspan(40, 60, color='blue', alpha=0.05)
    ax1.text(50, 5.5, '标准模式\n(均衡调度)', ha='center', va='center', fontsize=11, fontweight='bold', color='navy')

    # --- 图例 ---
    lines = [l1, l2, l3, l4]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, fancybox=True, shadow=True, fontsize=10)

    plt.tight_layout()
    
    # 保存为 PDF
    plt.savefig('spi.pdf')
    plt.show()

if __name__ == "__main__":
    generate_and_plot_sampled_v4()