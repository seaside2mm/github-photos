import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 生成示例数据（可用实际数据替换）
np.random.seed(42)
data = pd.DataFrame({
    'X': np.random.normal(50, 15, 100),
    'Y': np.random.normal(50, 10, 100),
    'Category': np.random.choice(['A', 'B'], 100)
})

# 设置Excel风格参数
plt.style.use('seaborn-whitegrid')  # 最接近Excel的基础样式

# 创建画布和坐标轴
fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

# 绘制散点图（模拟Excel默认颜色）
colors = {'A': '#4472C4', 'B': '#ED7D31'}  # Excel默认蓝色和橙色
for category, group in data.groupby('Category'):
    ax.scatter(
        x=group['X'],
        y=group['Y'],
        s=40,  # 点大小
        edgecolors=colors[category],  # 点边框颜色
        facecolors='white',  # 点填充色
        linewidths=1.5,  # 边框粗细
        label=category,
        alpha=0.8
    )

# 设置图表元素样式
# 标题
ax.set_title('Sales Analysis', 
            fontsize=14, 
            fontweight='bold', 
            pad=20,
            family='Arial')

# 坐标轴
ax.set_xlabel('X Values', 
             fontsize=10, 
             labelpad=10,
             family='Arial')
ax.set_ylabel('Y Values', 
             fontsize=10, 
             labelpad=10,
             family='Arial')

# 网格线
ax.grid(True, 
        linestyle='--', 
        linewidth=0.5, 
        color='#D9D9D9', 
        alpha=0.8)

# 坐标轴范围
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# 刻度标签
ax.tick_params(axis='both', 
               which='major', 
               labelsize=9,
               colors='#404040')

# 图例
legend = ax.legend(
    title='Category',
    bbox_to_anchor=(1, 0.5),  # 右侧显示
    frameon=True,
    edgecolor='#BFBFBF',
    facecolor='white',
    title_fontsize=10,
    fontsize=9
)
legend.get_frame().set_linewidth(0.5)

# 边框样式
for spine in ax.spines.values():
    spine.set_color('#808080')
    spine.set_linewidth(0.7)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()

# 保存图表（可选）
# fig.savefig('excel_style_scatter.png', bbox_inches='tight', dpi=300)
