import os
import process_data_hip2 as pr
import numpy as np
import matplotlib.pyplot as plt
import re

def process_hip2():
    perfPath = "reports/hip2/perf"
    perfChildPaths = os.listdir(perfPath)
    stracePath = "reports/hip2/strace"
    straceChildPaths = os.listdir(stracePath)
    df = { 'time' : [], 'syscall': [], 'tool': [], 'depth': []}
    for syscall in perfChildPaths:
        fileNames = os.listdir(perfPath + "/" + syscall)
        for fileName in fileNames:
            filePath= perfPath + "/" + syscall + "/" + fileName
            fileStream = open(filePath, "r")
            lines = fileStream.readlines()
            fileStream.close()
            df['time'].append(pr.getTimeFromTextPerf(lines, syscall))
            df['tool'].append('perf')
            df['syscall'].append(syscall)
            df['depth'].append(re.findall("\d+", fileName)[0])

    for syscall in straceChildPaths:
        fileNames = os.listdir(stracePath + "/" + syscall)
        for fileName in fileNames:
            filePath= stracePath + "/" + syscall + "/" + fileName
            fileStream = open(filePath, "r")
            lines = fileStream.readlines()
            fileStream.close()
            time = pr.getTimeFromTextStrace(lines, syscall)
            df['time'].append(time)
            df['tool'].append('strace')
            df['syscall'].append(syscall)
            df['depth'].append(re.findall("\d+", fileName)[0])
    return df

def make_chart_hip2(df):
    tools = np.unique(df['tool']) 
    syscalls = ['clone', 'execvp', 'fork', 'posix_spawnp']
    depths = np.unique(df['depth'])

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    width = np.arange(4)
    offset = 0.2
    count = 0.0

    for dep in depths:
        data = df.loc[(df['depth'] == dep) & (df['tool'] == 'strace')].time
        ax[0].bar(width + count, data, offset, label=dep)
        count += offset
        
    ax[0].legend()
    ax[0].set_title('Strace')
    ax[0].set_xticks(width + offset + 0.1 / 4)
    ax[0].set_xticklabels(syscalls)

    width = np.arange(3)

    for dep in depths:
        data = df.loc[(df['depth'] == dep) & (df['tool'] == 'perf') & (df['syscall'] != 'clone')].time
        ax[1].bar(width + count, data, offset, label=dep)
        count += offset
        
    ax[1].legend()
    ax[1].set_title('Perf')
    ax[1].set_xticks(width + offset + 1.8 / 3)
    ax[1].set_xticklabels(syscalls[1:])

    plt.savefig('reports/hip2/chart.png', dpi = 300)

def make_boxplot_hip2(data, tool):
    pltdata = {}

    i = 10
    for syscall in np.unique(data.syscall):
        pltdata[syscall] = []
        for depth in np.unique(data.depth):
            pltdata[syscall].append(data.loc[(data['depth'] == depth) & (data['tool'] == tool) & (data['syscall'] == syscall)].time)
            i *= 10
            
    fig, axs = plt.subplots(2, 2, figsize=(8, 8), sharex=True)
    axs[0][0].set_title('clone')
    axs[0][0].boxplot(pltdata['clone'], labels=np.unique(data.depth), showfliers=False)
    axs[0][1].set_title('execvp')
    axs[0][1].boxplot(pltdata['execvp'], labels=np.unique(data.depth), showfliers=False)
    axs[1][0].set_title('fork')
    axs[1][0].boxplot(pltdata['fork'], labels=np.unique(data.depth), showfliers=False)
    axs[1][1].set_title('posix_spawnp')
    axs[1][1].boxplot(pltdata['posix_spawnp'], labels=np.unique(data.depth), showfliers=False)

    fig.suptitle("Boxplots da distribuição do tempo de cada\nsyscall de acordo com o número de processos segundo o " + tool)
    plt.savefig('reports/hip2/boxplot-' + tool + '.png', dpi = 300)
