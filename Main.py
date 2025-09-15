import os
import time
import multiprocessing as mp

# 根目录,这个目录下放着的是DRIAMS打头的文件夹
rootDir = "D:/Work/PythonProject/FilesOperator/DatasTestCopy"
# 最多并发线程数，留一个逻辑核心给系统，避免windows卡顿
processesCount = max(1, mp.cpu_count() - 1)
# 开启单进程模式
isSingleProcess = False
# 开启计时器 可以拿来看看单进程和多进程的性能开销区别
isTimerEnable = True

def ProcessFile(path, mode):
    # 利用with这个上下文管理器来自动管理f的生命周期
    # f的类是TextIOWrapper，它是实现了__enter__和__exit__方法的
    # 用with会比手动open和close更简洁，也更不容易犯错

    # 我看最大的文件也不超过800KB，直接整个一次性读进来就可以
    # 如果说单个文件超过了1MB，那应该优先考虑流式读写，免得内存爆了
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 标题处理部分
    # 标题要么是直接开标题，要么先两行带#的，再开标题，所以是1~3行
    # 让程序自己去识别好了
    header, dataStart = [], 0
    if lines and lines[0].startswith("#"):
        header.append(lines[0])
        if len(lines) > 1 and lines[1].startswith("#"):
            header.append(lines[1])
            if len(lines) > 2:
                header.append(lines[2]); dataStart = 3
        else:
            if len(lines) > 1:
                header.append(lines[1]); dataStart = 2
    else:
        if lines: header.append(lines[0]); dataStart = 1

    newLines = []
    # 先收集第二列的所有 float 值，用于计算 min/max
    dataCols = []
    for line in lines[dataStart:]:
        if not line.strip():
            continue
        cols = line.strip().split()
        if len(cols) < 2:
            continue
        dataCols.append(float(cols[1]))
    if dataCols:
        yMin, yMax = min(dataCols), max(dataCols)
        yRange = yMax - yMin if yMax != yMin else 1.0  # 避免除以 0
    else:
        yMin, yRange = 0.0, 1.0

    # 再生成新行
    for line in lines[dataStart:]:
        if not line.strip():
            newLines.append(line)
            continue
        cols = line.strip().split()
        if len(cols) < 2:
            newLines.append(line)
            continue
        x, y = cols[0], cols[1]
        try:
            yFloat = float(y)
        except:
            newLines.append(line)
            continue
        # 第一列处理
        if mode == "binned":
            col1 = str(int(float(x)))
        else:
            col1 = f"{float(x):.2f}"
        # 第二列归一化到 0~9999
        col2 = str(int((yFloat - yMin) / yRange * 9999))
        newLines.append(col1 + " " + col2 + "\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(header + newLines)

#在根目录下遍历子目录，查找出需要用的文件，并标记成对应格式
def CollectFiles():
    tasks = []

    #在根目录下找出以DRIAMS开头的文件夹
    #listdir:把指定目录下所有子文件和子文件夹的名字str以迭代器的方式返回
    for dname in os.listdir(rootDir):
        #os.path.join:用于在不同的系统下正确的拼接路径
        dpath = os.path.join(rootDir, dname)
        #isdir：看看指定的路径是不是文件夹
        if not os.path.isdir(dpath) or not dname.upper().startswith("DRIAMS"):
            continue

        #在DRIAMS下找到指定文件名的文件夹，打标记做成元组，然后装进tasks列表里返回
        for mode, sub in [("binned", "binned_6000"),
                          ("preprocessed", "preprocessed"),
                          ("raw", "raw")]:
            subdir = os.path.join(dpath, sub)
            #os.walk:遍历目录下所有子目录和文件，是树状遍历，深度优先
            #每次迭代返回一个三元组：(dirpath, dirnames, filenames)，都是str
            #这里用_抛弃掉dirnames，剩下俩要用来接着找
            for dp, _, files in os.walk(subdir):
                #files是每一个文件的文件名组成的列表
                for fn in files:
                    if fn.endswith(".txt"):
                        tasks.append((os.path.join(dp, fn), mode))
    return tasks

if __name__ == "__main__":
    if(isTimerEnable):
        start_time = time.time()

    files = CollectFiles()
    if (isSingleProcess):
        # 跑一个分支，如果是单进程模式，就用迭代器顺次执行
        for path, mode in files:
            ProcessFile(path, mode)
    else:
        #否则调用进程池来并发，避免1核有难31核围观
        with mp.Pool(processesCount) as pool:
            #第一个参数是目标方法，第二个参数是一个迭代器，是目标方法的参数列表
            #这里ProcessFile的参数列表恰好能对应上files的元组，可以自动依次匹配地传参
            pool.starmap(ProcessFile, files)

    if(isTimerEnable):
        end_time = time.time()
        print(f"程序运行耗时: {(end_time - start_time):.4f} 秒")
