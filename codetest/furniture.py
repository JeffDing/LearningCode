class Furniture:
    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __str__(self):
        return f'家具名称是{self.name},家具占地面积为{self.area}'


furniture1 = Furniture('橱柜', 10)
furniture2 = Furniture('双人床', 20)


class Home:
    def __init__(self, situation, area):
        self.situation = situation
        self.area = area
        self.free_area = area
        self.furniture = []

    def __str__(self):
        return f'房子坐落于{self.situation},面积为{self.area},搬' \
               f'入{self.furniture}后,房屋的剩余面积为{self.free_area}'

    def add_furniture(self, item):
        self.free_area -= item.area
        if self.free_area > 0:
            self.furniture.append(item.name)
        else:
            print('家具占地面积过大，房屋剩余面积不足!请整理房子空间')
            self.free_area +=item.area


home1 = Home('株洲', 180)
home2 = Home('湘潭', 400)    
print(home1)
print(home2)
home2.add_furniture(furniture2)
print(home2)
furniture3 = Furniture('篮球场', 1900)
home2.add_furniture(furniture3)
print(home2)