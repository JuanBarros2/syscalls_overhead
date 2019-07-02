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
            if re.search('clone resumed> child_stack=.*, flags=CLONE_VM', line) is not None or re.search('execve\("/.*, NULL.*<\d+\.\d+>', line) is not None or re.search(' execve resumed>', line) is not None:
                time += float(re.findall("<\d+\.\d+>", line)[0][1:-1])
        return time


def getTimeFromTextPerf(text, syscall):
    return 0
