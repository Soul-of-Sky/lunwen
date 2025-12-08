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

def plot_duration_bar_du3b():
    # --- 2. 数据准备 ---
    # 类别：Idle -> 空闲，其他保持英文
    categories = ['空闲', 'SQLite', 'OpenCV', 'MQTT', 'Lighttpd', '7zip']
    
    # 原始数据 (ms)
    pre_copy_raw = [11352, 119795, 40568, 18671, 17967, 79004]
    mlls_raw = [11853, 40433, 35442, 16895, 16695, 32894]
    flic_raw = [12046, 34911, 37048, 18323, 17000, 36197]
    ressnap_raw = [11777, 31759, 29299, 17777, 15913, 32084]

    # 【单位转换】 将数据除以 1000，转换为秒 (s)
    pre_copy = np.array(pre_copy_raw) / 1000.0 / 1.8
    mlls = np.array(mlls_raw) / 1000.0 / 1.8
    flic = np.array(flic_raw) / 1000.0 / 1.8
    ressnap = np.array(ressnap_raw) / 1000.0 / 1.8

    # --- 3. 绘图参数 ---
    x = np.arange(len(categories))
    width = 0.18
    
    fig, ax = plt.subplots(figsize=(12, 5))

    # 学术配色 (Tab10: Green, Blue, Red, Orange)
    c_qemu = '#2ca02c'
    c_mlls = '#1f77b4'
    c_flic = '#d62728'
    c_ress = '#ff7f0e'

    # --- 4. 绘制柱状图 ---
    ax.bar(x - 1.5 * width, pre_copy, width, label='QEMU', 
           color='white', edgecolor=c_qemu, hatch='////', linewidth=1.5)
    
    ax.bar(x - 0.5 * width, mlls, width, label='MLLS', 
           color='white', edgecolor=c_mlls, hatch='...', linewidth=1.5)
    
    ax.bar(x + 0.5 * width, flic, width, label='FLIC-DRAM', 
           color='white', edgecolor=c_flic, hatch='xx', linewidth=1.5)
    
    ax.bar(x + 1.5 * width, ressnap, width, label='HPRO', 
           color='white', edgecolor=c_ress, hatch='++', linewidth=1.5)

    # --- 5. 细节调整 ---
    # Y轴标签
    ax.set_ylabel('总迁移时间 (s)', fontsize=16)
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=14)
    
    # 设置Y轴范围 
    # 数据最大值约 119.8s (SQLite)，设置上限为 140 比较合适
    ax.set_ylim(0, 80) 
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # 图例设置 (横向排列)
    ax.legend(loc='upper right', frameon=True, edgecolor='black', 
              fancybox=False, fontsize=12, ncol=2)

    plt.tight_layout()

    # --- 6. 保存图片 ---
    plt.savefig('du3b.pdf', format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_duration_bar_du3b()