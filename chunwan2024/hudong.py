from collections import deque
import random
 
def auto():
    pokers=[]
    poker=[]
    for i in ['♥','♠','♦','♣']:
        for j in ['A','2','3','4','5','6','7','8','9','10','J','Q','K']:
            poker.append(i)
            poker.append(j)
            pokers.append(poker)
            poker=[]
    pokers.append('Joker')
    pokers.append('joker')
    return pokers
                        
def get_input(prompt_message, expected_type=int, min_val=None, max_val=None):
    while True:
        user_input = input(prompt_message)
        try:
            value = expected_type(user_input)
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                print(f"Error: Please enter a value between {min_val} and {max_val}.")
            else:
                return value
        except ValueError:
            print(f"输入类型或范围错误，请重新输入。")
 
# 获取名字字数，地域，性别
cardn = get_input("输入初始抽取卡牌数量（3-54）：", int, 1, 54)
name = get_input("请输入名字字数，范围（2-7）：", int, 2, 7)
location = get_input("南方人请输入1，北方人请输入2，不确定请输入3：", int, 1, 3)
sexe = get_input("男生请输入1，女生请输入2：", int, 1, 2)
 
def simulate_magic(cards, cardn, name, location, sexe):
    # 洗牌
    random.shuffle(cards)
 
    # 随机选择四张，对折撕开
    selected_values = random.sample(cards, cardn)
    selceted_cards = deque(selected_values * 2)
    print(f"抽出的牌：{selceted_cards}")
    
    # 1. 根据名字有几个字，将前n张牌移到最后
    print("根据名字有几个字，将前n张牌移到最后")
    selceted_cards.rotate(-name)
    print(f"此时的顺序：{selceted_cards}")
    print()
 
    # 2. 取出前三张牌并随机插入剩余牌中，不能插在第一张和最后一张
    print("取出前三张牌并随机插入剩余牌中，不能插在第一张和最后一张")
    first_three = [selceted_cards.popleft() for _ in range(3)]
 
    for card in first_three:    
        insert_position = random.randint(1, len(selceted_cards) - 2)
        selceted_cards.insert(insert_position, card)
    print(f"此时的顺序：{selceted_cards}")
    print()
 
    # 3. 把最上面的牌放到一边
    print("把最上面的牌放到一边")
    remembered_card = selceted_cards.popleft()
    print(f"取出的初始的牌：{remembered_card}")
    print()
 
    # 4. 南方人取1张，北方人取2张，无法确定取3张，将这些牌随机插入剩下的牌中
    print("南方人取1张，北方人取2张，无法确定取3张，将这些牌随机插入剩下的牌中")
    first_a = [selceted_cards.popleft() for _ in range(location)]
    print(f"取出的牌：{first_a}")
    print()
 
    for card in first_a:
        if len(selceted_cards) > 2:
            insert_position = random.randint(1, len(selceted_cards) - 2)
        else:
            insert_position = 0
        selceted_cards.insert(insert_position, card)
        print(f"此时的顺序：{selceted_cards}")
    print()
 
    # 5. 男生取1张，女生取2张，将这些牌扔掉
    print("男生取1张，女生取2张，将这些牌扔掉")
    for _ in range(sexe):
        print(f"扔掉的牌：{selceted_cards.popleft()}")
        print(f"此时的顺序：{selceted_cards}")
    print()
 
    # 6. 见证奇迹的时刻
    print("见证奇迹的时刻")
    selceted_cards.rotate(-7)
    print(f"此时的顺序：{selceted_cards}")
 
    # 7. 好运留下来，烦恼丢出去！
    while len(selceted_cards) > 1:
        print("好运留下来，烦恼丢出去！")
        selceted_cards.append(selceted_cards.popleft())  # 第一张牌移到最后
        print(f"第一张牌移到最后：{selceted_cards}")
        selceted_cards.popleft()  # 删除现在的第一张牌
        print(f"删除现在的第一张牌后的顺序：{selceted_cards}")
 
    # 返回手里剩下的牌和放在一边的牌
    return selceted_cards[0], remembered_card
    print(f"返回手里剩下的牌：{selceted_cards[0]}")
    print(f"放在一边的牌：{remembered_card}")
    print()

poker=auto()
print(f"扑克牌：{poker}")
print()
final_card, remebered_card = simulate_magic(poker,cardn, name, location, sexe) 
print(f"初始牌：{remebered_card}, 剩下的牌：{final_card}")
print(f"初始牌和手里的牌是否相同：{remebered_card == final_card}")
print()
print("祝大家龙年大吉！龙行龘龘！")
