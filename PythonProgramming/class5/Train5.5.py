'''
有三个圆柱A、B、C，初始时A上有N个圆盘，N由用户输入给出，最终移动到圆柱C上。‪‬‪‬‪‬‪‬‪‬‮‬‪‬‮‬‪‬‪‬‪‬‪‬‪‬‮‬‫‬‫‬‪‬‪‬‪‬‪‬‪‬‮‬‭‬‫‬‪‬‪‬‪‬‪‬‪‬‮‬‪‬‮‬‪‬‪‬‪‬‪‬‪‬‮‬‭‬‪‬‪‬‪‬‪‬‪‬‪‬‮‬‪‬‮‬
每次移动步骤的表达方式示例如下：[STEP  10] A->C。其中，STEP是步骤序号，宽度为4个字符，右对齐。
'''
steps = 0
def hanoi(src, des, mid, n):
    global steps
    if n == 1:
        steps+=1
        print("[STEP{:>4}] {}->{}".format(steps, src, des))
    else:
        hanoi(src,mid,des,n-1)
        steps+=1
        print("[STEP{:>4}] {}->{}".format(steps, src, des))
        hanoi(mid,des,src,n-1)
N = eval(input())
hanoi("A", "C", "B", N)