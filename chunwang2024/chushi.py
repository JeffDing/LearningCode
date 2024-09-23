import random
 
def magic_proof():
    # 初始牌组
    cards = ['A', 'B', 'C', 'D'] * 2
 
    # 1. 根据名字有几个字(随机选择2-7之间的整数)，将前n张牌移到最后
    n = random.randint(2, 7)
    cards = cards[n:] + cards[:n]
 
    # 2. 取出前三张牌并随机插入剩余牌中，不能插在第一张和最后一张
    first_three = cards[:3]
    cards = cards[3:]
    for card in first_three:
        insert_position = random.randint(1, len(cards) - 2)
        cards.insert(insert_position, card)
 
    # 3. 把最上面的牌放到一边
    remembered_card = cards.pop(0)
 
    # 4. 从最上面取牌，南方人取1张，北方人取2张，无法确定取3张，将这些牌随机插入剩下的牌中
    a = random.randint(1, 3)
    first_a = cards[:a]
    cards = cards[a:]
    for card in first_a:
 
        insert_position = random.randint(1, len(cards) - 2) 
        cards.insert(insert_position, card)
 
    # 5. 从最上面取牌，男生取1张，女生取2张，将这些牌扔掉
    b = random.randint(1, 2)
    cards = cards[b:]
 
    # 6. 见证奇迹的时刻：每次将第一张牌移到最后，重复7次
    for _ in range(7):
        cards.append(cards.pop(0))
 
    # 7. 好运留下来，烦恼丢出去：交替进行将第一张牌移到最后和删除，直到剩一张牌
    while len(cards) > 1:
        cards.append(cards.pop(0))  # 第一张牌移到最后
        cards.pop(0)  # 删除现在的第一张牌
 
    # 返回最后剩下的牌和之前放在一边的牌
    return cards[0], remembered_card
 
# 重新进行多次模拟并计算匹配的频率
correct_match_nb = 0
for _ in range(10000):
    final_card, remembered_card = magic_proof()
    if final_card == remembered_card:
        correct_match_nb += 1
 
match_rate = correct_match_nb / 10000
print(match_rate)
