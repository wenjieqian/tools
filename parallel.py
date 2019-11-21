# -*- coding:utf-8 -*- 
# Author : Wenjie Qian
# Email  : wenjieqian@foxmail.com
# Desc   : 利用并行计算提高密集型程序执行效率

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 多线程
executor = ThreadPoolExecutor(max_workers=100)
# 多进程【慎用】
# executor = ProcessPoolExecutor(max_workers=100)

def func(id):
    '''对每个子任务进行处理，并返回处理结果'''
    # do something
    res = id
    return res
    
if __name__ == "__main__":
    ids = [1,2,3,4] # 待处理输入列表
    res = list(executor.map(func, ids)) # 并行处理
    print(list(zip(ids,res))) # 将输入输出分组打印
