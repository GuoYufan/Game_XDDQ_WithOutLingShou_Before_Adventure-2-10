'''
import sys
sys.path.append(
	"/sdcard/[GuoYufan]/[Python]/")
del sys
from 寻道大千_用于炼气之前_v1.0.3 import *
'''
	
import math
class Role():
    def __init__(self,基础属性列表,名称):
        self._基础属性列表=基础属性列表
        self.血,self.攻,self.防,self.敏=self._基础属性列表
        self.剩余血量=self.血
        self.名称=名称
        self.有视防御伤=0
        self.打对方回合数=0
        self.打对方实际回合数=0
        self.有视防御伤百分比=0
        self.战斗属性之吸血=0
        self.战斗抗性之抗吸=0
        self.战斗属性之有效吸血率=0
        self.吸血回血量=0

    @property
    def 基础属性列表(self):
        return self._基础属性列表
   
    @基础属性列表.setter
    def 基础属性列表(self,value):
        if not isinstance(value,list):
            raise TypeError("基础属性列表必须是list对象")
        self._基础属性列表=value
        self.血,self.攻,self.防,self.敏=self._基础属性列表
  

敌=Role([4663,1000,167,333],"敌")
我=Role([4729,710,114,297],"我")

我.战斗属性之吸血=3.4
敌.战斗抗性之抗吸=1


class Fight():
    def __init__(self,我方,对方):
        self.我方=我方
        self.对方=对方
        self.先手方=self.后手方=None
        self.谁胜=str()
    
    def 分出先后手方(self):
        self.先手方=self.我方 if self.我方.敏>self.对方.敏 else self.对方
        self.后手方=self.我方 if not self.先手方==self.我方 else self.对方
        
    def 我胜吗(self):
        if self.先手方.名称=="我":
            if self.我方.打对方实际回合数_白板<=self.对方.打对方实际回合数_白板:return True
        else:
            if self.我方.打对方实际回合数_白板<self.对方.打对方实际回合数_白板:return True
        return False
    
    def 计算双方(self):
        self.分出先后手方()
        self.计算单方(self.先手方)
        self.计算单方(self.后手方)
        self.谁胜="我" if self.我胜吗() else "敌"

    def 计算单方(self,此方):
        彼方=self.获取彼方(此方)
        
        此方.有视防御伤=此方.攻-彼方.防
        此方.打对方回合数_白板=彼方.血/此方.有视防御伤
        此方.打对方实际回合数_白板=math.ceil(此方.打对方回合数_白板)
        此方.有视防御伤百分比=1/此方.打对方回合数_白板
        此方.战斗属性之有效吸血率=(此方.战斗属性之吸血-彼方.战斗抗性之抗吸)/100
        此方.吸血回血量=此方.有视防御伤*此方.战斗属性之有效吸血率
      

    def 模糊战况报告(self):
        self.计算双方()
        print(f"我打敌多少回合：{self.我方.打对方回合数_白板}——{self.我方.打对方实际回合数_白板}回合")
        print(f"敌打我多少回合：{self.对方.打对方回合数_白板}——{self.对方.打对方实际回合数_白板}回合")
        print(f"我打敌一下掉血百分比：{round(self.我方.有视防御伤百分比*100,2)}%——{math.ceil(1/self.我方.有视防御伤百分比)}回合")
        print(f"敌打我一下掉血百分比：{round(self.对方.有视防御伤百分比*100,2)}%——{math.ceil(1/self.对方.有视防御伤百分比)}回合")
        print(f"我打敌一下有视防御伤：{self.我方.有视防御伤}")
        print(f"我打敌一下吸血回血量：{self.我方.吸血回血量}")
        print(f"先手方：{self.先手方.名称}")
        print(f"谁胜：{self.谁胜}")
    
    def 获取彼方(self,此方):
        return self.后手方 if 此方==self.先手方 else self.先手方
   
    def 计算单方有视防御伤及吸血(self,此方):
        彼方=self.获取彼方(此方)
        此方.有视防御伤=此方.攻-彼方.防
        此方.战斗属性之有效吸血率=(此方.战斗属性之吸血-彼方.战斗抗性之抗吸)/100
        此方.吸血回血量=int(此方.有视防御伤*此方.战斗属性之有效吸血率)
            
    def 轮序到人物(self,此方):
        彼方=self.获取彼方(此方)
        self.计算单方有视防御伤及吸血(此方)
        彼方.剩余血量-=(此方.有视防御伤)
        此方已掉血量=此方.血-此方.剩余血量
        此方本次回血=此方.吸血回血量 if 此方已掉血量>=此方.吸血回血量 else 此方已掉血量
        此方.剩余血量+=此方本次回血
    
    def 分出胜负(self):
        if self.先手方.剩余血量<=0:
            self.谁胜=self.后手方.名称
            return True
        elif self.后手方.剩余血量<=0:
            self.谁胜=self.先手方.名称
            return True
        return False
        
    def 准确战况报告(self):
        for i in range(15):
            print()
            print(f"第{i+1}回合:")
            for 此方 in (self.先手方,self.后手方):
                print(f"{此方.名称}行动",end="\t")
                self.轮序到人物(此方)
                print(f"{此方.吸血回血量}")
                if self.分出胜负():
                    print(f"谁胜:{self.谁胜}")
                    return
            


战场=Fight(我,敌)
战场.模糊战况报告()
input()
战场.准确战况报告()
input()

for i in range(10):
    if 战场.谁胜=="我":break
    print()
    multi=1+0.05*(i+1)
    我.基础属性列表=[int(i*multi) for i in 我.基础属性列表[:-1]]+[我.基础属性列表[-1]]
    print(f"把我变至几倍：{multi}倍")
    print(f"我的属性更新为：{我.基础属性列表}")
    战场.模糊战况报告()
