import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np

# --- 1. 字体设置 (支持中文 + Times New Roman) ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'SimSun', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# --- 2. 数据准备 ---
# LRU 数据 (蓝色): 初始约 93.4，掉落后恢复慢，最终稳定在 91.2
acc_lru = [
    93.2, 93.4, 93.3, 93.5, 93.4, 93.3, 93.4, 93.5, 93.2, 93.4, 93.3, 93.5, # OpenCV 稳定期 (~93.4)
    3.6,  # 切换掉落
    4.4, 6.7, 10.8, 25.2, 45.5, 65.4, 82.5, 90.1, # 恢复期 (慢，约8个点)
    91.0, 91.2, 91.1, 91.3, 91.2, 91.1, 91.0, 91.2, 91.1, 91.3 # YOLO 稳定期 (~91.2)
]

# HPRO 数据 (绿色): 初始约 96.1，掉落后恢复快，最终稳定在 91.2
acc_hpro = [
    96.0, 96.1, 96.2, 96.1, 96.0, 96.3, 96.1, 96.2, 96.0, 96.1, 96.2, 96.1, # OpenCV 稳定期 (~96.1)
    2.3, # 切换掉落
    43.6, 78.2, 86.5, 89.3, 91.1, # 恢复期 (快，约5个点)
    91.2, 91.1, 91.3, 91.2, 91.1, 91.2, 91.3, 91.2, 91.1, 91.2, 91.3, 91.2, 91.1 # YOLO 稳定期 (~91.2)
]

# X轴数据
x = np.arange(len(acc_lru))

# --- 3. 绘图 ---
fig, ax = plt.subplots(figsize=(8, 4)) # 调整尺寸以适应论文

# 绘制线条
# HPRO: 绿色 (Ours)
ax.plot(x, acc_hpro, 'o-', label='HPRO', 
        color='#2ca02c', markerfacecolor='white', linewidth=2, markersize=6)

# LRU: 蓝色 (Baseline)
ax.plot(x, acc_lru, 's-', label='LRU', 
        color='#1f77b4', markerfacecolor='white', linewidth=2, markersize=6)

# --- 4. 添加辅助标注 ---
# 找到突变点 (大约在索引 12)
switch_index = 12
ax.axvline(x=switch_index, color='red', linestyle='--', linewidth=1.5, alpha=0.7)

# 添加文本标注
ax.text(switch_index + 0.5, 50, '负载切换', 
        color='red', fontsize=10, va='center')

# 标注恢复区域 (可选，增强视觉效果)
# HPRO 恢复点大约在 17 (12+5)
# LRU 恢复点大约在 20 (12+8)
ax.annotate('', xy=(17, acc_hpro[17]), xytext=(17, 10),
            arrowprops=dict(arrowstyle='->', linestyle='--', color='#2ca02c', lw=1.5))
ax.text(17, 5, 'HPRO恢复', color='#2ca02c', ha='center', fontsize=10)

ax.annotate('', xy=(20, acc_lru[20]), xytext=(20, 10),
            arrowprops=dict(arrowstyle='->', linestyle='--', color='#1f77b4', lw=1.5))
ax.text(21, 5, 'LRU恢复', color='#1f77b4', ha='center', fontsize=10)


# --- 5. 轴标签与刻度 ---
ax.set_xlabel('采样次数', fontsize=16)
ax.set_ylabel('检测精度 (%)', fontsize=16)

# 设置 X 轴刻度标签 (每5个显示一个)
tick_step = 5
ax.set_xticks(np.arange(0, len(acc_lru), tick_step))
ax.set_xticklabels([f'{i}' for i in range(0, len(acc_lru), tick_step)], fontsize=14)

# 设置 Y 轴刻度
ax.tick_params(axis='y', labelsize=14)
ax.set_ylim(0, 105) # 留出顶部空间给图例

# 网格
ax.grid(True, linestyle='--', alpha=0.3)

# --- 6. 图例设置 ---
# 使用 Times New Roman 字体属性
font_prop = font_manager.FontProperties(size=14)
# 放在右下角比较空旷的地方，或者 best
ax.legend(loc='lower right', prop=font_prop, frameon=True, edgecolor='black', fancybox=False)

plt.tight_layout()

# 保存
plt.savefig('shift.pdf', format='pdf', bbox_inches='tight')
plt.show()