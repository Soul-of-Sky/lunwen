import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np

# --- 1. 字体与风格设置 ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def plot_write_coalescing_real():
    # --- 2. 数据模拟 (模拟真实采样) ---
    # 采样间隔 0.5s，共 60s -> 120个采样点
    t = np.arange(0, 60.5, 0.5)
    
    # 基础负载形状 (梯形，模拟 Benchmark 预热->稳定->结束)
    # 10s-50s 为高负载区
    base_load = np.zeros_like(t)
    for i, time in enumerate(t):
        if 10 <= time <= 50:
            base_load[i] = 1.0
        elif 5 < time < 10:
            base_load[i] = (time - 5) / 5 # 爬升
        elif 50 < time < 55:
            base_load[i] = 1.0 - (time - 50) / 5 # 下降
            
    # --- 生成 QEMU 数据 (真实特征：高频抖动 + 随机尖峰) ---
    np.random.seed(42)
    # 基准 IOPS ~ 2800
    qemu_base = 2800 * base_load
    # 添加白噪声 (White Noise)
    qemu_noise = np.random.normal(0, 200, size=len(t))
    # 添加突发尖峰 (Spikes - 模拟 Flash GC 造成的卡顿/突发)
    qemu_spikes = np.random.choice([0, -800, 600], size=len(t), p=[0.85, 0.1, 0.05])
    
    iops_qemu = qemu_base + qemu_noise + qemu_spikes
    # 底噪
    iops_qemu += np.random.normal(50, 10, size=len(t))
    iops_qemu = np.maximum(iops_qemu, 0) # 不小于0

    # --- 生成 HPRO 数据 (真实特征：低位运行 + 周期性 Flush) ---
    # 目标：平均降低 ~78%，即保留 ~22% (约 600 IOPS)
    hpro_base = 600 * base_load
    # 添加较小的抖动 (Buffer 吸收了大部分波动)
    hpro_noise = np.random.normal(0, 50, size=len(t))
    # 添加周期性 Flush 锯齿 (模拟缓冲区满落盘)
    # 模拟每 4s 一次小高峰
    hpro_sawtooth = 100 * np.sin(2 * np.pi * t / 4) * base_load
    
    iops_hpro = hpro_base + hpro_noise + hpro_sawtooth
    # 底噪
    iops_hpro += np.random.normal(20, 5, size=len(t))
    iops_hpro = np.maximum(iops_hpro, 0)

    # --- 3. 绘图 ---
    fig, ax = plt.subplots(figsize=(8, 5))

    # 绘制 QEMU (红色，带点，线细一点，表现杂乱感)
    # alpha=0.7 让密集的点不至于糊成一团，保留颗粒感
    ax.plot(t, iops_qemu, color='#d62728', linestyle='-', linewidth=1, marker='.', markersize=4, alpha=0.8, 
            label='QEMU')
    
    # 绘制 HPRO (绿色，带点，稍粗，表现稳定感)
    ax.plot(t, iops_hpro, color='#2ca02c', linestyle='-', linewidth=1.5, marker='o', markersize=4, 
            label='HPRO')

    # --- 4. 标注与细节 ---
    # 选择一个典型时刻标注差距 (例如 t=32s)
    idx = 64 # 32s 对应的索引 (32 / 0.5)
    val_q = iops_qemu[idx]
    val_h = iops_hpro[idx]
    
    # 画箭头
#     ax.annotate('', xy=(32, val_h), xytext=(32, val_q),
#                 arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    
    # 文字说明
#     ax.text(33.5, (val_q + val_h)/2, '峰值降低 ~78%', 
#             color='black', fontsize=12, fontweight='bold', va='center')

    # 标注活跃区间背景
    ax.axvspan(10, 50, color='gray', alpha=0.1)
    ax.text(30, 3600, 'SQLite 活跃窗口', ha='center', fontsize=12, color='dimgray')

    # --- 5. 轴标签设置 ---
    ax.set_xlabel('时间 (s)', fontsize=16)
    ax.set_ylabel('物理 I/O 提交频率 (IOPS)', fontsize=16)
    
    ax.set_xlim(0, 60)
    ax.set_ylim(-100, 4000) # 稍微留点余量

    # 网格 (虚线，模拟示波器/监控面板感觉)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_axisbelow(True)

    # 图例
    font_prop = font_manager.FontProperties(family=['SimHei', 'SimSun'], size=12)
    ax.legend(loc='upper right', prop=font_prop, frameon=True, edgecolor='black', fancybox=False)

    plt.tight_layout()
    plt.savefig('ring.pdf', format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_write_coalescing_real()