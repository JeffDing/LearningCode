#PythonDraw.py
import turtle as tu
tu.setup(650,350,200,200)
tu.penup()
tu.fd(-250)
tu.pendown()
tu.pensize("35")
tu.pencolor("purple")
tu.seth(-40)
for i in range(4):
    tu.circle(40,80)
    tu.circle(-40,80)
tu.circle(40,80/2)
tu.fd(50)
tu.circle(25, 180)
tu.fd(40*2/3)
tu.done()
