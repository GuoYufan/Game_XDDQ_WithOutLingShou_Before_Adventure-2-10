import math
class Role():
    def __init__(self,基础属性列表):
        self.基础属性列表=基础属性列表
        self.基础属性=dict(zip(("hp","atk","def","spd"),self.基础属性列表))
        self.打对方回合数=0
        self.打对方实际回合数=0
        self.对方被打一下掉血量=0
    def 设置基础属性(self):
       self.基础属性=dict(zip(("hp","atk","def","spd"),self.基础属性列表))
    
    def 计算一切(self,对方):
        self.打对方回合数=对方.基础属性["hp"]/(self.基础属性["atk"]-对方.基础属性["def"])
        self.打对方实际回合数=math.ceil(self.打对方回合数)
        self.对方被打一下掉血量=1/self.打对方回合数

class Fight():
    def __init__(self,我方,对方):
        self.我方=我方
        self.对方=对方
        self.先手方=str()
        self.谁胜=str()
    def 设置双方(self,我方,对方):
        self.我方=我方
        self.对方=对方
    
    def 我是先手方吗(self):
        return self.我方.基础属性["spd"]>self.对方.基础属性["spd"]
    
    def 我胜吗(self):
        if self.先手方=="我":
            if self.我方.打对方实际回合数<=self.对方.打对方实际回合数:return True
        else:
            if self.我方.打对方实际回合数<self.对方.打对方实际回合:return True
        return False
    
    def 计算一切(self):
        self.先手方="我" if  self.我是先手方吗() else "敌"
        self.谁胜="我" if self.我胜吗() else "敌"

敌=Role([2306,811,108,263])
我=Role([3485,509,81,270])
# 假设被暴击一下
#敌.基础属性["hp"]-=(我.基础属性["atk"]-敌.基础属性["def"])
我.计算一切(敌)
敌.计算一切(我)
战场=Fight(我,敌)
战场.计算一切()
print(f"我打敌：{我.打对方回合数}——{我.打对方实际回合数}")
print(f"敌打我：{敌.打对方回合数}——{敌.打对方实际回合数}")
print(f"我打敌一下掉血量：{round(我.对方被打一下掉血量*100,2)}%——{math.ceil(1/我.对方被打一下掉血量)}")
print(f"敌打我一下掉血量：{round(敌.对方被打一下掉血量*100,2)}%——{math.ceil(1/敌.对方被打一下掉血量)}")
print(f"先手方：{战场.先手方}")
print(f"谁胜：{战场.谁胜}")
for i in range(1,11):
    print()
    multi=1+i*0.1
    我.基础属性列表=[int(i*multi) for i in 我.基础属性列表[:-1]]+[我.基础属性列表[-1]]
    我.设置基础属性()
    我.计算一切(敌)
    敌.计算一切(我)
    
    战场.设置双方(我,敌)
    战场.计算一切()
    print(f"把我变至几倍：{multi}倍 {我.基础属性列表}")
    print(f"我打敌：{我.打对方回合数}——{我.打对方实际回合数}")
    print(f"敌打我：{敌.打对方回合数}——{敌.打对方实际回合数}")
    print(f"我打敌一下掉血量：{round(我.对方被打一下掉血量*100,2)}%——{math.ceil(1/我.对方被打一下掉血量)}")
    print(f"敌打我一下掉血量：{round(敌.对方被打一下掉血量*100,2)}%——{math.ceil(1/敌.对方被打一下掉血量)}")
    print(f"谁胜：{战场.谁胜}")
    
    if 战场.谁胜=="我":break