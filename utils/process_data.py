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