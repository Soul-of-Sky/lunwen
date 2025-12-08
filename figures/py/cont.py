import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np

# --- 1. 字体与风格设置 ---
# 优先使用黑体/宋体显示中文，Times New Roman 显示数字/英文
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def plot_continuous_snapshot_cn():
    # --- 2. 数据准备 ---
    # 将分类标签改为 TinyLlama 负载占比%
    categories = ['0', '10', '20', '50', '100']
    
    # 原始数据 (数据不动)
    availability_raw = [0.3, 1.7, 5.6, 22.3, 100] 
    
    # 计算批处理大小
    packed_size = [100 / x for x in availability_raw]

    # --- 数据转换 ---
    # 1. 可用性指数 (取对数)
    log_availability = [np.log10(x) for x in availability_raw]
    
    # 2. 平均批处理粒度 (取 log2)
    log2_packed_size = [np.log2(x) for x in packed_size]

    # --- 3. 绘图 ---
    x = np.arange(len(categories))
    width = 0.45 

    fig, ax1 = plt.subplots(figsize=(8, 5))

    # --- 柱状图 (左轴：可用性指数) ---
    # 标签改为中文
    rects = ax1.bar(x, log_availability, width, label='可用性指数', 
                    hatch='////', edgecolor='#1f77b4', color='white', linewidth=1.5)

    # --- 折线图 (右轴：批处理粒度) ---
    ax2 = ax1.twinx()
    # 标签改为中文
    line, = ax2.plot(x, log2_packed_size, color='#d62728', marker='o', linestyle='-', 
                     label='平均批处理粒度 ($\log_2$)', markersize=8, markerfacecolor='white', markeredgewidth=1.5)

    # --- 4. 轴标签与刻度 (全部中文) ---
    ax1.set_ylabel('可用性指数 ($\log_{10}$)', fontsize=16)
    ax2.set_ylabel('平均批处理粒度 ($\log_2$ 页)', fontsize=16)
    
    # 修改横坐标标题
    ax1.set_xlabel('TinyLlama 负载占比 (%)', fontsize=16)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=14)

    # 设置 Y 轴范围
    ax1.set_ylim(-1.0, 2.5)
    ax1.set_yticks([-1, 0, 1, 2])
    
    ax2.set_ylim(-1, 12)

    # 添加基准线 (y=0)
    ax1.axhline(0, color='black', linewidth=1, linestyle='-')

    # 网格线
    ax1.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax1.set_axisbelow(True)

    # --- 5. 图例合并 (中文) ---
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    
    # 图例字体设置
    font_prop = font_manager.FontProperties(family=['SimHei', 'SimSun'], size=12)
    
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', 
               prop=font_prop, frameon=True, edgecolor='black', fancybox=False, ncol=2)

    plt.tight_layout()
    plt.savefig('cont.pdf', format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_continuous_snapshot_cn()