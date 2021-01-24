'''
method: Dynamic Programming
description: 从pdf中找出正文
    暴力 + 哨兵法 + 部分动态规划
    按照从左到右，从上到下的顺序遍历矩阵
    遍历过程中，完成；1.记录到当前元素为止，同行左侧连续1的个数；2.记录当前元素上方含1区域的行的范围（图解看官方），3.计算所有以当前元素为右下角的矩阵的值，并且计算出最大值得，
    时间复杂度为O（m^2*n)
author: jtx
date: 2021_01_20
'''

from bs4 import BeautifulSoup
def maximalSquare(matrix):
    """
    :type matrix: List[List[str]]
    :rtype: int
    """
    if matrix == []: return 0
    M, N = len(matrix), len(matrix[0])
    dp = [[0 for _ in range(N)] for _ in range(M)]
    Max = 0
    for i in range(N):  # dp矩阵初始化
        dp[0][i] = int(matrix[0][i])
        Max = max(dp[0][i], Max)
    for i in range(M):  # dp矩阵初始化
        dp[i][0] = int(matrix[i][0])
        Max = max(dp[i][0], Max)
    for i in range(1, M):
        for j in range(1, N):
            if matrix[i][j] == '0': continue
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
            Max = max(dp[i][j], Max)
    print(dp)
    return Max ** 2

def maximalRectangle(matrix) -> int:
    max_judge = 0
    length_max_judge = 0
    height_max_judge = 0
    length_max = 0
    height_max = 0


    #violence
    #detail matrix is empty, i once forgot
    if not matrix:
        return 0
    row = len(matrix)
    column = len(matrix[0])
    matrix.insert(0,[[0,0,0] for _ in range(column)])
    for i in range(row+1):
        matrix[i].insert(0,[0,0,0])
    row = len(matrix)
    column = len(matrix[0])
    max_ = 0
    temp = matrix.copy()
    for i in range(1,row):
        for j in range(1,column):
            # matrix[i][j] is updated to [left_consecutive_one,upward_one_range,upward_one_minimu_value,value]
            matrix[i][j] = [0,0,int(matrix[i][j])]
            if matrix[i][j][2] != 0:
                matrix[i][j][0] = matrix[i][j-1][0] + 1#left_bounder
                matrix[i][j][1] = matrix[i-1][j][1] + 1#up_bounder
                min_ = matrix[i][j][0]
                min_are = matrix[i][j][0]
                for k in range(i-1,i-matrix[i][j][1],-1):# i once changed the position of (i-1) and i-matrix[i][j][1],be carfully
                    min_ = min(min_,matrix[k][j][0])#I onece replaced min_ with matrix[i][j]
                    length_max_judge = i-k+1
                    height_max_judge = min_
                    min_are = max(min_are,min_*(i-k+1))
                max_ = max(max_,min_are)

                if max_ > max_judge:
                    length_max = length_max_judge
                    height_max = height_max_judge
                    print(length_max)
                    print(height_max)


                    max_judge = max_
        # for i in range...  I once add this line to debug, i changed the value of i, then i debug this for about 30minutes, stupid!
    return max_, length_max, height_max


def maximalRectangle_second(matrix, length_max, height_max, p_all):
    length_max_judge = 0
    height_max_judge = 0
    k = 0
    content_list = []
    sentence_list_judge = []
    sentence_list = []

    #violence
    #detail matrix is empty, i once forgot
    if not matrix:
        return 0
    row = len(matrix)
    column = len(matrix[0])
    matrix.insert(0,[[0,0,0] for _ in range(column)])
    for i in range(row+1):
        matrix[i].insert(0,[0,0,0])
    row = len(matrix)
    column = len(matrix[0])
    max_ = 0
    temp = matrix.copy()
    for i in range(1,row):
        for j in range(1,column):
            # matrix[i][j] is updated to [left_consecutive_one,upward_one_range,upward_one_minimu_value,value]
            matrix[i][j] = [0,0,int(matrix[i][j])]
            if matrix[i][j][2] != 0:
                matrix[i][j][0] = matrix[i][j-1][0] + 1#left_bounder
                matrix[i][j][1] = matrix[i-1][j][1] + 1#up_bounder
                min_ = matrix[i][j][0]
                min_are = matrix[i][j][0]
                for k in range(i-1,i-matrix[i][j][1],-1):# i once changed the position of (i-1) and i-matrix[i][j][1],be carfully
                    min_ = min(min_,matrix[k][j][0])#I onece replaced min_ with matrix[i][j]
                    length_max_judge = i-k+1
                    height_max_judge = min_
                    min_are = max(min_are,min_*(i-k+1))
                max_ = max(max_,min_are)


                if length_max-4 < length_max_judge < length_max+4 and height_max-5 < height_max_judge < height_max+5:
                    for num, p in enumerate(p_all):
                        if '风险提示' in str(p):
                            break
                        p = p.get_text().strip()
                        len_p = len(p)

                        if k-1 <= num <= i-1:
                            if p not in sentence_list_judge:
                                print(p)
                                sentence_list.append(p)
                                sentence_list_judge.append(p)
                    if sentence_list:
                        word_judge = sentence_list[-1]
                        if word_judge.endswith('。'):
                            if sentence_list:
                                print(k - 1)
                                print(i - 1)
                                content_list.append(sentence_list)
                                sentence_list = []

        # for i in range...  I once add this line to debug, i changed the value of i, then i debug this for about 30minutes, stupid!
    return content_list

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        a = f.read()

    soup = BeautifulSoup(a, 'lxml')
    p_all = soup.find_all('p')

    flag_start = 0
    flag_end = 0
    p_pre = ''
    p_sentence = ''
    num = 0
    max_p = 0
    for num, p in enumerate(p_all):
        if '风险提示' in str(p):
            break
        p = p.get_text().strip()

        len_p = len(p)
        max_p = max(max_p, len_p)



    print(max_p)

    len_i = max_p
    len_j = num
    print(len_j)
    dp = [[0 for _ in range(len_i)] for _ in range(len_j)]
    print(dp)
    print(len(dp))
    print(len(dp[0]))

    for num, p in enumerate(p_all):
        if '风险提示' in str(p):
            break
        p = p.get_text().strip()
        print(p)
        len_p = len(p)
        for i in range(len_i):
            # print(num, i)
            if i < len_p:
                dp[num][i] = 1
            else:
                dp[num][i] = 0
    return dp, p_all

dp, p_all = read_file('4.html')

# a = maximalSquare(dp)
# print(a)
a2, length_max, height_max = maximalRectangle(dp)
print('max:', str(a2))
print('length_max:', str(length_max))
print('height_max:', str(height_max))



dp, p_all = read_file('4.html')

content_list = maximalRectangle_second(dp, length_max, height_max, p_all)

print('--------------------------------')

for each in content_list:
    print(each)

