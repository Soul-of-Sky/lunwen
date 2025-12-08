import matplotlib.pyplot as plt
import numpy as np

# --- 1. 样式设置 (支持中文 & 学术风格) ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def plot_downtime_bar_chinese_style():
    # --- 2. 数据准备 (保持数据不变) ---
    # 为了满足“中文”要求，将 Idle 翻译为 空闲，其他专有名词保留英文
    categories = ['空闲', 'SQLite', 'OpenCV', 'YOLO', 'TinyLlama', '7zip']
    
    # Updated data provided by user
    pre_copy = [39, 367, 911, 914, 808, 489]
    mlls = [44, 252, 766, 782, 728, 295]
    flic = [42, 463, 773, 754, 682, 500]
    ressnap = [40, 398, 634, 660, 578, 442]

    # --- 3. 绘图参数 ---
    x = np.arange(len(categories))
    width = 0.18 # 调整宽度以适配
    
    fig, ax = plt.subplots(figsize=(12, 5))

    # 学术配色 (对应 Green, Blue, Red, Orange)
    c_qemu = '#2ca02c'
    c_mlls = '#1f77b4'
    c_flic = '#d62728'
    c_ress = '#ff7f0e'

    # --- 4. 绘制柱状图 (白底 + 彩色边框 + 纹理) ---
    # QEMU
    ax.bar(x - 1.5 * width, pre_copy, width, label='QEMU', 
           color='white', edgecolor=c_qemu, hatch='////', linewidth=1.5)
    
    # MLLS
    ax.bar(x - 0.5 * width, mlls, width, label='MLLS', 
           color='white', edgecolor=c_mlls, hatch='...', linewidth=1.5)
    
    # FLIC-DRAM
    ax.bar(x + 0.5 * width, flic, width, label='FLIC-DRAM', 
           color='white', edgecolor=c_flic, hatch='xx', linewidth=1.5)
    
    # ResSnap
    ax.bar(x + 1.5 * width, ressnap, width, label='HPRO', 
           color='white', edgecolor=c_ress, hatch='++', linewidth=1.5)

    # --- 5. 细节调整 ---
    # 设置中文标签
    ax.set_ylabel('虚拟机停机时间 (ms)', fontsize=16)
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=14)
    
    # 设置Y轴网格和范围 (根据数据最大值914，设置为1000合适)
    ax.set_ylim(0, 1000) 
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # 图例设置 (带边框，横向排列)
    ax.legend(loc='upper left', frameon=True, edgecolor='black', 
              fancybox=False, fontsize=12, ncol=2)

    plt.tight_layout()

    # --- 6. 保存图片 ---
    # 按照要求保存为 dt4b.pdf
    plt.savefig('dt4b.pdf', format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_downtime_bar_chinese_style()