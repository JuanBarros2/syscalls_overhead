import os
import process_data as pr
import numpy as np
import matplotlib.pyplot as plt


def process_hip3():
    perfPath = "reports/hip3/perf"
    perfChildPaths = os.listdir(perfPath)
    perfChildPaths.sort()
    stracePath = "reports/hip3/strace"
    straceChildPaths = os.listdir(stracePath)
    straceChildPaths.sort()
    df = { 'time' : [], 'syscall': [], 'tool': []}
    for syscall in perfChildPaths:
        filePath= perfPath + "/" + syscall
        fileStream = open(filePath, "r")
        lines = fileStream.readlines()
        fileStream.close()
        syscallName = syscall.split("-")[0]
        df['time'].append(pr.getTimeFromTextPerf(lines, syscallName))
        df['tool'].append('perf')
        df['syscall'].append(syscallName)

    for syscall in straceChildPaths:
        filePath= stracePath + "/" + syscall
        fileStream = open(filePath, "r")
        lines = fileStream.readlines()
        fileStream.close()
        syscallName = syscall.split("-")[0]
        time = pr.getTimeFromTextStrace(lines, syscallName)
        df['time'].append(time)
        df['tool'].append('strace')
        df['syscall'].append(syscallName)
    return df

def make_chart_hip3(df):
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
    plt.savefig('reports/hip3/chart.png', dpi = 1200)