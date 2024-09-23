#turtle风轮绘制
import turtle as t
t.setup(600,400)
t.right(45) #首先让海龟右转45度，以保证四个小风轮都是可以使用循环结构绘制的
t.pensize(5)
for i in range(4): #计算清楚海龟什么时候需要转向，什么时候需要前行，然后使用循环语句即可
    t.left(135)
    t.fd(110)
    t.right(90)
    t.circle(-110,45)
    t.right(90)
    t.fd(110)
t.done()
