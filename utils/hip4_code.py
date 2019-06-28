import os
import process_data as pr
import numpy as np
import matplotlib.pyplot as plt


def process_hip4():
    perfPath = "reports/hip4/perf"
    perfChildPaths = os.listdir(perfPath)
    perfChildPaths.sort()
    stracePath = "reports/hip4/strace"
    straceChildPaths = os.listdir(stracePath)
    straceChildPaths.sort()
    df = { 'time' : [], 'syscall': [], 'tool': []}
    for syscall in perfChildPaths:
        pr.getResultPerf(df, perfPath + "/" + syscall, syscall[:-4])

    for syscall in straceChildPaths:
        pr.getResultStrace(df, stracePath + "/" + syscall, syscall[:-4])
    return df

def make_chart_hip4(df):
    tools = np.unique(df['tool']) 
    ind = np.arange(len(np.unique(df['syscall']) ))
    barWidth = 0.30
    palette = plt.get_cmap('Set1')
    syscalls = []
    color_id = 0
    width = 0
    for tool in tools:
        df_filtered = df.loc[(df.tool == tool)]
        syscalls = df_filtered.syscall
        plt.bar([x + width for x in ind], df_filtered.time, width=barWidth, color=palette(color_id), edgecolor='white', label=tool)
        width += 0.30
        color_id += 1
    plt.xlabel('Resultado com as ferramentas', fontweight='bold')
    plt.xticks([r + (barWidth/2) for r in range(len(syscalls))], syscalls)
    plt.legend()
    plt.savefig('reports/hip4/chart.png', dpi = 1200)