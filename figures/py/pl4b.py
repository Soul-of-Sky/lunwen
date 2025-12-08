import matplotlib.pyplot as plt
import numpy as np

# --- 1. 样式设置 (学术风格 + 中文支持) ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def plot_performance_loss_pl4b():
    # --- 2. 数据准备 ---
    categories = ['SQLite', '7zip', 'OpenCV', 'YOLO']
    
    # Updated data provided
    pre_copy = [24.1, 38.5, 15.5, 6.7]
    mlls = [17.8, 19.1, 11.3, 6.1]
    flic = [19.5, 22.1, 12.3, 7.2]
    ressnap = [12.3, 13.4, 12.0, 5.9]

    # --- 3. 绘图参数 ---
    x = np.arange(len(categories))
    width = 0.18
    
    fig, ax = plt.subplots(figsize=(12, 5))

    # 学术配色 (Tab10)
    c_qemu = '#2ca02c'  # Green
    c_mlls = '#1f77b4'  # Blue
    c_flic = '#d62728'  # Red
    c_ress = '#ff7f0e'  # Orange

    # --- 4. 绘制柱状图 ---
    ax.bar(x - 1.5 * width, pre_copy, width, label='QEMU', 
           color='white', edgecolor=c_qemu, hatch='////', linewidth=1.5)
    
    ax.bar(x - 0.5 * width, mlls, width, label='MLLS', 
           color='white', edgecolor=c_mlls, hatch='...', linewidth=1.5)
    
    ax.bar(x + 0.5 * width, flic, width, label='FLIC-DRAM', 
           color='white', edgecolor=c_flic, hatch='xx', linewidth=1.5)
    
    ax.bar(x + 1.5 * width, ressnap, width, label='ResSnap', 
           color='white', edgecolor=c_ress, hatch='++', linewidth=1.5)

    # --- 5. 细节调整 ---
    # Y轴标签
    ax.set_ylabel('虚拟机性能损失 (%)', fontsize=16)
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=14)
    
    # 设置Y轴范围 
    # 数据最大值 38.5，设置上限为 45
    ax.set_ylim(0, 45) 
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # 图例设置 (ncol=2, 带边框)
    ax.legend(loc='upper right', frameon=True, edgecolor='black', 
              fancybox=False, fontsize=12, ncol=2)

    plt.tight_layout()

    # --- 6. 保存图片 ---
    plt.savefig('pl4b.pdf', format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_performance_loss_pl4b()