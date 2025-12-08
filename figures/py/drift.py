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

def plot_organic_sparks_drift():
    # --- 2. 数据模拟 (采用随机游走算法) ---
    time_steps = 100
    memory_space = 200
    
    # 初始化背景 (极低噪音，几乎全白)
    np.random.seed(42) 
    data = np.random.exponential(scale=0.1, size=(memory_space, time_steps))

    # --- 核心算法：模拟一个随机漂移的热点群 ---
    def add_wandering_hotspot(data_matrix, start_addr, t_start, t_end, 
                              drift_speed=2.0, spread=5.0, intensity=25):
        """
        创建一个随时间随机上下漂移的热点群
        start_addr: 初始中心地址
        drift_speed: 漂移速度 (越大越剧烈)
        spread: 离散程度 (越大火花越散)
        """
        current_center = start_addr
        
        for t in range(t_start, t_end):
            # 1. 中心漂移：下一时刻的中心 = 当前中心 + 随机波动
            # 使用 float 保证平滑，取整时再转 int
            movement = np.random.normal(0, drift_speed)
            current_center += movement
            
            # 边界保护
            current_center = np.clip(current_center, 10, memory_space - 10)
            
            # 2. 撒点：在当前中心周围生成 N 个火花
            # 模拟访问的突发性：有时候访问多，有时候少
            num_sparks = np.random.randint(5, 25) 
            
            # 生成火花的地址 (正态分布：中心密集，边缘稀疏)
            spark_addrs = np.random.normal(loc=current_center, scale=spread, size=num_sparks).astype(int)
            spark_addrs = np.clip(spark_addrs, 0, memory_space - 1)
            
            # 3. 写入数据
            spark_values = np.random.normal(loc=intensity, scale=5, size=num_sparks)
            np.add.at(data_matrix[:, t], spark_addrs, spark_values)

    # --- 场景构建：模拟真实的复杂应用 ---

    # 热点 A (主工作区，如 Heap): 从低地址开始，缓慢向高地址漂移，比较松散
    add_wandering_hotspot(data, start_addr=40, t_start=0, t_end=100, 
                          drift_speed=1.5, spread=8.0, intensity=20)

    # 热点 B (临时缓冲区，如 Buffer): 在中间某段时间突然出现，快速移动，然后消失
    add_wandering_hotspot(data, start_addr=120, t_start=30, t_end=80, 
                          drift_speed=3.0, spread=4.0, intensity=28)
    
    # 热点 C (系统/栈区，如 Stack): 始终在低地址徘徊，非常稳定，范围小
    add_wandering_hotspot(data, start_addr=10, t_start=0, t_end=100, 
                          drift_speed=0.2, spread=2.0, intensity=15)

    # 热点 D (突发的大范围扫描): 也就是你说的“星星之火”，全图随机闪现
    # 模拟偶尔的 GC (垃圾回收) 或 全局搜索
    random_noise_t = np.random.randint(0, 100, 300) # 300个随机时刻
    random_noise_addr = np.random.randint(0, 200, 300) # 300个随机地址
    random_noise_val = np.random.normal(15, 5, 300)
    np.add.at(data, (random_noise_addr, random_noise_t), random_noise_val)

    # 截断数据，美化视觉
    data = np.clip(data, 0, 40)

    # --- 3. 绘图 ---
    fig, ax = plt.subplots(figsize=(10, 5))

    # 使用 OrRd，这种色谱最适合表现“火花”
    cmap = plt.cm.get_cmap('OrRd')
    
    # interpolation='none' 是关键！这能保留像素的颗粒感，不让它模糊成一团
    im = ax.imshow(data, cmap=cmap, aspect='auto', origin='lower', 
                   extent=[0, 100, 0, 200], vmin=0.5, vmax=35, 
                   interpolation='none') 

    # --- 4. 细节调整 ---
    ax.set_xlabel('执行时间 (归一化)', fontsize=16)
    ax.set_ylabel('内存地址空间 (PFN)', fontsize=16)
    
    # 移除垂直网格线，让视觉更自然
    # ax.grid(False) 

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('写入强度', rotation=270, labelpad=20, fontsize=14)
    cbar.outline.set_linewidth(1)

    plt.tight_layout()

    # --- 5. 保存 ---
    plt.savefig('drift.pdf', format='pdf', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    plot_organic_sparks_drift()