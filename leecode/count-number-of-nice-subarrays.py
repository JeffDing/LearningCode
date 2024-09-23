'''1248. 统计「优美子数组」
给你一个整数数组 nums 和一个整数 k。
如果某个 连续 子数组中恰好有 k 个奇数数字，我们就认为这个子数组是「优美子数组」。
请返回这个数组中「优美子数组」的数目。
示例：
输入：nums = [1,1,2,1,1], k = 3
输出：2
解释：包含 3 个奇数的子数组是 [1,1,2,1] 和 [1,2,1,1] 。
'''
class Solution:
    def numberOfSubarrays(nums, k):
        tmp = [] # 存连续偶数个数的子序列
        n = 1 # 从1开始计数，将来计算的时候就不用加1了
        for i in nums:
            if i % 2 == 0:
                n += 1
            else: # 发现一个奇数就存入连续偶数的个数
                tmp.append(n)
                n = 1
        tmp.append(n) # 循环结束后还要把最后一个n加进来
        if len(tmp) < k+1: # k个奇数，tmp里至少要有k+1个元素
            return 0 # 凑不够k个奇数返回0
        res = 0
        for i in range(k, len(tmp)): # 将k个奇数两侧的偶数数量相乘，加在一起
            res += tmp[i] * tmp[i-k]
        return res

    nums=[]
    k=eval(input("请输入k的值："))
    nums=input("请输入数组（逗号分隔）：").split(',')
    print(numberOfSubarrays([1,1,2,1,1],k))