import math

class Role():
    def __init__(self,基础属性列表):
        self.基础属性列表=基础属性列表
        self.基础属性=dict(zip(("hp","atk","def","spd"),self.基础属性列表))
        self.有视防御伤=0
        self.打对方回合数=0
        self.打对方实际回合数=0
        self.有视防御伤百分比=0
        self.敌血倍=0
        self.战斗属性={"吸血":0}
        self.战斗抗性={"抗吸":0}
        self.吸血回血量=0
        self.先手方=str()
        
    def 设置基础属性(self):
       self.基础属性=dict(zip(("hp","atk","def","spd"),self.基础属性列表))
    
    def 我是先手方吗(self,对方):
        return self.基础属性["spd"]>对方.基础属性["spd"]

        
    def 计算一切(self,对方):
        self.有视防御伤=self.基础属性["atk"]-对方.基础属性["def"]
        self.打对方回合数=对方.基础属性["hp"]/self.有视防御伤
        self.打对方实际回合数=math.ceil(self.打对方回合数)
        self.有视防御伤百分比=1/self.打对方回合数
        self.敌血倍=对方.基础属性["hp"]/self.基础属性["hp"]
        self.吸血回血量=self.有视防御伤百分比*(self.战斗属性["吸血"]-对方.战斗抗性["抗吸"])*对方.基础属性["hp"]
        self.先手方="我" if  self.我是先手方吗(对方) else "敌"

class Fight():
    def __init__(self,我方,对方):
        self.我方=我方
        self.对方=对方
        self.我方.计算一切(对方)
        self.对方.计算一切(我方)
        self.先手方=我方.先手方
        self.谁胜=str()
        self.胜方回合数=0
        self.计算一切()

    def 设置双方(self,我方,对方):
        self.我方=我方
        self.对方=对方
        self.我方.计算一切(对方)
        self.对方.计算一切(我方)
        self.先手方=我方.先手方
        self.计算一切()
        
        
    def 我胜吗(self):
        if self.我方.先手方=="我":
            if self.我方.打对方实际回合数<=self.对方.打对方实际回合数:return True
        else:
            if self.我方.打对方实际回合数<self.对方.打对方实际回合数:return True
        return False
    
    def 计算一切(self):
        self.谁胜="我" if self.我胜吗() else "敌"
        self.胜方回合数=self.我方.打对方实际回合数 if self.谁胜=="我" else self.对方.打对方实际回合数            	

    def 战况报告(self):
        print(f"我打敌多少回合：{self.我方.打对方回合数}——{self.我方.打对方实际回合数}回合")
        print(f"敌打我多少回合：{self.对方.打对方回合数}——{self.对方.打对方实际回合数}回合")
        print(f"我打敌一下掉血量：{round(self.我方.有视防御伤百分比*100,2)}%——{math.ceil(1/self.我方.有视防御伤百分比)}回合")
        print(f"敌打我一下掉血量：{round(self.对方.有视防御伤百分比*100,2)}%——{math.ceil(1/self.对方.有视防御伤百分比)}回合")
        print(f"我打敌一下有视防御伤：{self.我方.有视防御伤}")
        print(f"我打敌一下吸血回血量：{self.我方.吸血回血量}")
        print(f"先手方：{self.先手方}")
        print(f"谁胜：{self.谁胜}")
            	

# 旧怪：《冒险1-10》
# 8回合暴击1次反击2次
旧敌=Role([5135,740,148,300])
# 新怪：《冒险2-2》
敌=Role([4663,1000,167,333])
# 斗法
#敌=Role([4635,691,111,287])


旧我=Role([4461,683,106,289])
我=Role([4729,710,114,297])
# 让新敌与旧敌分高下
#我=Role([5135,740,148,300])


我.战斗属性["吸血"]=3.4/100
# 怪
敌.战斗抗性["抗吸"]=1/100
# 斗法
#敌.战斗抗性["抗吸"]=0/100


# 假设对方被连击几下
#'''
#for i in range(3+1):
#    敌.基础属性["hp"]-=我.有视防御伤
#'''

print(f"新我的基础属性：{我.基础属性列表}")
print("新我是旧我的几倍：%f~%f~%f"%(我.基础属性["hp"]/旧我.基础属性["hp"],我.基础属性["atk"]/旧我.基础属性["atk"],我.基础属性["def"]/旧我.基础属性["def"]))

战场=Fight(我,敌)

# 假设吸血7个回合
#'''
吸血触发回合数=战场.胜方回合数-(1 if 战场.先手方=="我" else 0)
print(f"吸血触发：{吸血触发回合数}回合")
我.基础属性列表[0]+=我.吸血回血量*吸血触发回合数
我.设置基础属性()

战场.设置双方(我,敌)
#'''
战场.战况报告()





for i in range(10):
    if 战场.谁胜=="我":break
    print()
    multi=1+0.05*(i+1)
    我.基础属性列表=[int(i*multi) for i in 我.基础属性列表[:-1]]+[我.基础属性列表[-1]]
    我.设置基础属性()
    战场.设置双方(我,敌)
    
    print(f"把我变至几倍：{multi}倍")
    print(f"我的属性更新为：{我.基础属性列表}")
    战场.战况报告()

    