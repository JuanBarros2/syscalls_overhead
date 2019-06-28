import os
import process_data as pr
import numpy as np
import matplotlib.pyplot as plt

def process_hip1():
    perfPath = "reports/hip1/perf"
    perfChildPaths = os.listdir(perfPath)
    stracePath = "reports/hip1/strace"
    straceChildPaths = os.listdir(stracePath)
    df = { 'time' : [], 'syscall': [], 'tool': [], 'depth': []}
    for syscall in perfChildPaths:
        fileNames = os.listdir(perfPath + "/" + syscall)
        for fileName in fileNames:
            pr.getResultPerf(df, perfPath + "/" + syscall + "/"+ fileName, syscall)
            df['depth'].append(fileName.split(".txt")[0])

    for syscall in straceChildPaths:
        fileNames = os.listdir(stracePath + "/" + syscall)
        for fileName in fileNames:
            pr.getResultStrace(df, stracePath + "/" + syscall + "/"+ fileName, syscall)
            df['depth'].append(fileName.split(".txt")[0])
    return df

def make_chart_hip1(df):
    tools = np.unique(df['tool']) 
    depths = np.unique(df['depth']) 
    
    ind = np.arange(len(np.unique(df['syscall']) ))
    barWidth = 0.30
    palette = plt.get_cmap('Set1')
    num = 1

    for tool in tools:
        plt.subplot(1, len(tools), num)
        color_id = 0
        width = 0
        syscalls = []
        for dep in depths:
            df_filtered = df.loc[(df.depth == dep) & (df.tool == tool)]
            syscalls = df_filtered.syscall
            plt.bar(
            [x + width for x in ind],
            df_filtered.time,
            width=barWidth,
            color=palette(color_id),
            edgecolor='white',
            label=dep+ " níveis de pilha")
            width += 0.30
            color_id += 1
        plt.xlabel('Resultado com ' + tool, fontweight='bold')
        plt.xticks([r + (barWidth/2) for r in range(len(syscalls))], syscalls)
        num += 1
    plt.legend()
    plt.savefig('reports/hip1/chart.png', dpi = 1200)