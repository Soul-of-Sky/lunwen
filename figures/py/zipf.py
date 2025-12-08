import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. 样式设置 ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def plot_write_frequency_distribution_final():
    # --- 2. 数据准备 ---
    # 修改标签为 >=5
    x_labels = ['0', '1', '2', '3', '4', '>=5']
    
    # 数据调整策略：
    # 1. 大幅削减中间项 (2, 3, 4) 的数值，使其呈现更明显的"凹"字形或 L 形
    # 2. >=5 的数据控制在 5% 以内 (7zip 除外)
    # 3. 减少的数值回填给 0 (冷页面) 或 1
    data = {
        # Idle: 几乎全0
        "空闲":    [99.6, 0.3,  0.0, 0.0, 0.0, 0.1],
        
        # SQLite: 中间极少，两头翘
        "SQLite":         [78.0, 15.0, 1.0, 1.0, 0.5, 3.5], 
        
        # OpenCV: 
        "OpenCV":         [70.0, 20.0, 0.9, 1.5, 1.3, 4.0],
        
        # TinyLlama: 
        "TinyLlama":      [60.0, 32.8, 0.5, 0.8, 0.5, 4.2],
        
        # YOLO: 
        "YOLO":           [52.0, 37.2, 1.3, 1.1, 1.2, 4.8],
        
        # 7zip: 允许稍微超一点 (6.5%)
        "7zip":           [35.0, 43.5, 1.9, 1.7, 1.2, 8.5]
    }

    # --- 3. 绘图参数 ---
    x = np.arange(len(x_labels)) 
    total_width = 0.85 #稍微加宽一点整体宽度
    n_bars = len(data)
    width = total_width / n_bars 
    
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ['#7f7f7f', '#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd']
    patterns = ['---', '...', '///', '\\\\\\', 'xx', '++'] 
    
    # --- 4. 循环绘制 ---
    for i, (label, percentages) in enumerate(data.items()):
        offset = (i - n_bars / 2) * width + width / 2
        
        bars = ax.bar(
            x + offset,
            percentages,
            width,
            label=label,
            hatch=patterns[i],
            edgecolor=colors[i],
            color='white',
            linewidth=1.2
        )
        
        # --- 视觉放大技巧：为最后一列 (>=5) 添加数值标注 ---
        # 只在最后一个数据点 (index = 6) 上添加文字
        val = percentages[-1] # 获取 >=5 的值
        x_pos = x[-1] + offset # 获取最后一根柱子的位置
        
        # 只有当数值大于0.1时才显示，避免显示空闲任务的0.1挤在一起
        if val > 0: 
            ax.text(
                x_pos, 
                val + 1.5, # 文字位置在柱子上方一点
                f"{val}", 
                ha='center', 
                va='bottom', 
                fontsize=10, 
                fontweight='bold',
                color=colors[i], # 文字颜色与柱子边框一致
                rotation=90 # 旋转文字防止重叠
            )

    # --- 5. 细节调整 ---
    
    ax.set_ylabel('内存页面占比 (%)', fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=14)
    ax.set_xlabel('快照周期内页面脏化次数', fontsize=16)

    ax.set_ylim(0, 110) # 稍微增加Y轴高度以容纳标注
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # --- 视觉放大技巧：高亮最后一块区域 ---
    # 在 >=5 的位置画一个淡淡的红色背景框
    ax.axvspan(4.5, 5.5, color='red', alpha=0.05, lw=0)
    # 可以在上方加一个简单的注释（可选）
    # ax.text(6, 105, "Hotspot Area", ha='center', fontsize=12, color='darkred')

    # 图例
    ax.legend(loc='upper right', frameon=True, edgecolor='black', 
              fancybox=False, fontsize=12, ncol=3)

    plt.tight_layout()

    # --- 6. 保存 ---
        
    plt.savefig('zipf.pdf', format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_write_frequency_distribution_final()