class Patato:
    def __init__(self):             # 快捷键CTRL+E可以查看原来的.py文件
        self.cook_time = 0          # refactor里面有rename操作
        self.static = '生的'
        self.condiments = []

    def cook(self, time):
        self.cook_time += time
        if 0 <= self.cook_time < 3:
            self.static = '生的'
        elif 3 >= self.cook_time < 5:
            self.static = '半生半熟'
        elif 5 <= self.cook_time > 8:
            self.static = '熟的'
        else:
            self.static = '烤糊了'

    def add_condiments(self, condiments):
        self.condiments.append(condiments)

    def __str__(self):
        return f'这个地瓜烤了{self.cook_time}分钟,当前状态为{self.static},往里' \
               f'面加了{self.condiments}'


# 快捷键 Ctrl + Shift +J  可以使多行变成一行
patato = Patato()
patato.cook(2)
print(patato)
patato.add_condiments('酱油')
print(patato)
patato.add_condiments('生抽')