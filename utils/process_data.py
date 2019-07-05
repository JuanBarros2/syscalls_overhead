import re

def getTimeFromTextStrace(lines, syscall):
    if syscall == "fork":
        for line in lines:
            if re.search("child_stack=NULL, flags=CLONE_CHILD_CLEARTID\|CLONE_CHILD_SETTID\|SIGCHLD", line) is not None:
                return float(re.findall("<\d+\.\d+>", line)[0][1:-1])
    elif syscall == "execvp" or syscall == "execv":
        time = 0
        for line in lines:
            if re.search('execve\("/', line) is not None:
                time += float(re.findall("<\d+\.\d+>", line)[0][1:-1])
        return time
    elif syscall == "clone":
        time = 0
        for line in lines:
            if re.search('clone resumed> child_stack=.*, flags=CLONE_VFORK\)', line) is not None:
                return float(re.findall("<\d+\.\d+>", line)[0][1:-1])
        return time
    elif syscall == "posix_spawn" or syscall == "posix_spawnp":
        time = 0
        for line in lines:
            #if re.search('clone resumed> child_stack=.*, flags=CLONE_VM', line) is not None 
            #    time += float(re.findall("<\d+\.\d+>", line)[0][1:-1])
            if re.search('execve\("/.*<\d+\.\d+>', line) is not None or re.search(' execve resumed>', line) is not None:
                time += float(re.findall("<\d+\.\d+>", line)[0][1:-1])
        return time


def getTimeFromTextPerf(lines, syscall):
    if syscall == "fork":
        for line in lines:
            if re.search("clone\(.*: 18874385, .*:", line) is not None:
                return float(re.findall("m \d+\.\d+ ms", line)[0][2:-3])* 10**-3
    elif syscall == "execvp" or syscall == "execv":
        time = 0
        for line in lines:
            if re.search('execve\(.*: ', line) is not None:
                time += float(re.findall("( \d+\.\d+ ms)", line)[0][2:-3])* 10**-3
        return time
    elif syscall == "clone":
        for line in lines:
            if re.search('clone\(.*: 16384, ', line) is not None:
                return float(re.findall("m \d+\.\d+ ms", line)[0][2:-3])* 10**-3
    elif syscall == "posix_spawn" or syscall == "posix_spawnp":
        time = 0
        for line in lines:
            if re.search('clone\(.*: 16657, ', line):
                time += float(re.findall("m \d+\.\d+ ms", line)[0][2:-3])* 10**-3
            if re.search('execve\(.*: ', line):
                if not re.search('sleep', line):
                    time += float(re.findall("( \d+\.\d+ ms)", line)[0][2:-3])* 10**-3
        return time
