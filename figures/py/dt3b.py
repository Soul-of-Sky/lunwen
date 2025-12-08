import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. 样式设置 (复用参考代码的风格) ---
# 字体设置：优先使用 SimHei/SimSun 以支持可能出现的中文，同时兼顾英文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['font.family'] = 'sans-serif' # 确保生效
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def plot_downtime_bar():
    # --- 2. 数据准备 (保持原数据不变) ---
    categories = ['空闲', 'SQLite', 'OpenCV', 'MQTT', 'Lighttpd', '7zip']
    
    # 原始数据
    pre_copy_raw = [288, 1383, 2798, 1857, 732, 1779]
    mlls_raw = [319, 1099, 2184, 1408, 599, 1422]
    flic_raw = [327, 1262, 2395, 1799, 773, 1404]
    ressnap_raw = [310, 1050, 1988, 1606, 703, 1302]

    # 【核心修改】：将所有数据除以 2.3
    # 使用 np.array 直接进行向量化运算
    pre_copy = np.array(pre_copy_raw) / 2.3
    mlls = np.array(mlls_raw) / 2.3
    flic = np.array(flic_raw) / 2.3
    ressnap = np.array(ressnap_raw) / 2.3

    # --- 3. 绘图参数计算 ---
    x = np.arange(len(categories))
    width = 0.18 # 稍微调整宽度以容纳4根柱子
    
    fig, ax = plt.subplots(figsize=(12, 5))

    # 定义颜色 (对应 Green, Blue, Red, Orange 的学术配色)
    c_qemu = '#2ca02c'  # Green
    c_mlls = '#1f77b4'  # Blue
    c_flic = '#d62728'  # Red
    c_ress = '#ff7f0e'  # Orange

    # --- 4. 绘制柱状图 (风格：白底 + 彩色边框 + 纹理) ---
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

    # --- 5. 细节调整 (复用参考代码的 Grid 和 Label 风格) ---
    ax.set_ylabel('虚拟机停机时间 (ms)', fontsize=16) # 增加单位通常更严谨
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=14)
    
    # 设置Y轴网格
    ax.set_ylim(0, 1400)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True) # 确保网格在柱子下方

    # 图例设置 (带黑色边框，无圆角)
    ax.legend(loc='upper left', frameon=True, edgecolor='black', 
              fancybox=False, fontsize=12, ncol=2) # ncol=4 让图例横向排列，更美观

    plt.tight_layout()

    # 保存图片
    plt.savefig('dt3b.pdf', format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_downtime_bar()