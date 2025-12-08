import matplotlib.pyplot as plt
import numpy as np

# --- 1. 核心修复：设置支持中文的字体 ---
# 优先使用 Times New Roman，找不到字符时回退到 SimSun (宋体)
# 注意：列表顺序很重要，排在前面的优先
# plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['Times New Roman', 'SimSun'] 
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS'] 

# mac 用户如果没装 SimSun，可以使用 'Arial Unicode MS' 或 'Songti SC'
# plt.rcParams['font.serif'] = ['Times New Roman', 'Arial Unicode MS'] 

plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def plot_accuracy_bar_chinese():
    # --- 2. 数据准备 (这里我把标签改成了中文演示) ---
    categories = ['空闲', 'SQLite', 'OpenCV', 'YOLO', 'TinyLlama', '7zip']
    
    # HPRO (ResSnap) 数据
    acc_hpro = [100, 85.5, 96.1, 91.2, 92.5, 89.9]
    # LRU 数据
    acc_lru = [100, 78.5, 93.4, 91.2, 86.7, 84.0]

    x = np.arange(len(categories))
    width = 0.3

    # --- 3. 绘图 ---
    fig, ax = plt.subplots(figsize=(8, 5))

    color_hpro = '#2ca02c' 
    color_lru = '#1f77b4'

    # 绘制柱状图
    rects1 = ax.bar(x - width/2, acc_hpro, width, label='HPRO', 
                    color='white', edgecolor=color_hpro, hatch='////', linewidth=1.5)
    
    rects2 = ax.bar(x + width/2, acc_lru, width, label='LRU', 
                    color='white', edgecolor=color_lru, hatch='...', linewidth=1.5)

    # --- 4. 细节调整 ---
    ax.set_ylabel('工作集识别准确率 (%)', fontsize=16) # 中文标签
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=14)
    
    ax.set_ylim(50, 105)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # 图例
    ax.legend(loc='upper right', frameon=True, edgecolor='black', fancybox=False, fontsize=12, ncol=2)

    plt.tight_layout()
    
    # 保存图片
    plt.savefig('acc.pdf', format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_accuracy_bar_chinese()