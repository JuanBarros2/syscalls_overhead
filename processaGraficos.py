import os
import pandas as pd

def main():
    pd.DataFrame.from_dict(hip1()).to_csv('reports/hip1/result.csv', index=False)
    pd.DataFrame.from_dict(hip4()).to_csv('reports/hip4/result.csv', index=False)

def hip1():
    perfPath = "reports/hip1/perf"
    perfChildPaths = os.listdir(perfPath)
    stracePath = "reports/hip1/strace"
    straceChildPaths = os.listdir(stracePath)
    df = { 'time' : [], 'syscall': [], 'tool': [], 'depth': []}
    for syscall in perfChildPaths:
        fileNames = os.listdir(perfPath + "/" + syscall)
        for fileName in fileNames:
            getResultPerf(df, perfPath + "/" + syscall + "/"+ fileName, syscall)
            df['depth'].append(fileName.split(".txt")[0])

    for syscall in straceChildPaths:
        fileNames = os.listdir(stracePath + "/" + syscall)
        for fileName in fileNames:
            getResultStrace(df, stracePath + "/" + syscall + "/"+ fileName, syscall)
            df['depth'].append(fileName.split(".txt")[0])
    return df

def hip4():
    perfPath = "reports/hip4/perf"
    perfChildPaths = os.listdir(perfPath)
    stracePath = "reports/hip4/strace"
    straceChildPaths = os.listdir(stracePath)
    df = { 'time' : [], 'syscall': [], 'tool': []}
    for syscall in perfChildPaths:
        getResultPerf(df, perfPath + "/" + syscall, syscall[:-4])

    for syscall in straceChildPaths:
        getResultStrace(df, stracePath + "/" + syscall, syscall[:-4])
    return df

def getResultStrace(df, fileName, syscall):
    fileStream = open(fileName, "r")
    line = fileStream.readlines()[-1].split(" ")[4]
    fileStream.close()
    df['time'].append(float(line))
    df['tool'].append('strace')
    df['syscall'].append(syscall)

def getResultPerf(df, fileName, syscall):
    fileStream = open(fileName, "r")
    line = fileStream.readlines()[12].split(" ")[7]
    fileStream.close()
    df['time'].append(float(line))
    df['tool'].append('perf')
    df['syscall'].append(syscall)
    

if __name__ == "__main__":
    main()