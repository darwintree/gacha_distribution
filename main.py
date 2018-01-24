import random
P_ORI_TABLE = [0.01, 0.99]
P_NAME = ['SSR', 'NOT SSR']

GACHA_COUNT = 480
SIM_TIME = 10000
MAX_DISPLAY = 20
DESIRED_ITEM = 0

P_DISTRIBUTE_TABLE = []
for i in range(len(P_ORI_TABLE)):
    if i == 0:
        P_DISTRIBUTE_TABLE.append(P_ORI_TABLE[0])
    else:
        P_DISTRIBUTE_TABLE.append(P_ORI_TABLE[i - 1] + P_ORI_TABLE[i])
if P_DISTRIBUTE_TABLE[-1] != 1:
    P_DISTRIBUTE_TABLE.append(1)
    P_NAME.append("SOMETHING WRONG")


def gacha_once(distribute_table):
    r = random.random()
    for j in range(len(distribute_table)):
        if r < distribute_table[j]:
            return j


# select desired item to return
def continuous_gacha(try_count: int, desired_item: int) -> int:
    result = 0
    for j in range(try_count):
        if gacha_once(P_DISTRIBUTE_TABLE) == desired_item:
            result += 1
    return result


def display_sim_result(sim_result: dict):
    try:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import sys
        mpl.rcParams["font.family"] = "sans-serif"
        mpl.rcParams["font.sans-serif"] = u'SimHei'

        # init a height tuple
        height_list = []
        left_list = []

        for j in range(MAX_DISPLAY):
            left_list.append(j)
            if j in sim_result:
                height_list.append(sim_result[j]*100)
            else:
                height_list.append(0)

        # 绘制垂直条形图
        rect = plt.bar(left=tuple(left_list), height=tuple(height_list), width=0.8, align="center")
        plt.ylabel('人数比例/%')
        plt.xlabel('数量')
        plt.xticks(tuple(left_list), tuple(left_list))
        plt.legend((rect,), ("%d抽获得SSR数量的人数分布"%GACHA_COUNT,))
        # 显示绘制图片
        plt.show()
    except Exception as e:
        print(e)
        for j in sim_result:
            print("%d次："%j, end="")
            print(sim_result[j], end="人\n")


def main():
    sim_result = {}
    for j in range(SIM_TIME):
        result = continuous_gacha(GACHA_COUNT, DESIRED_ITEM)
        if result in sim_result:
            sim_result[result] += 1
        else:
            sim_result[result] = 1
    for item in sim_result:
        sim_result[item] /= SIM_TIME
    display_sim_result(sim_result)


main()