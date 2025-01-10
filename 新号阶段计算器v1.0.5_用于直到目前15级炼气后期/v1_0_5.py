'''
import sys
sys.path.append(
	"/sdcard/[GuoYufan]/[Python]/XDDQ/寻道大千_新号无灵兽阶段计算器/")
del sys
from v1_0_5 import *
'''


'''
import os

here=__file__
#当设置为1 为回退到最底层目录
回退到上几级目录=4
for i in range(回退到上几级目录):
    here=os.path.dirname(here)
del 回退到上几级目录,i
#input(here)

import sys
sys.path.append(
	here+
 os.sep.join("/[GuoYufan]/[Python]/XDDQ/寻道大千_新号无灵兽阶段计算器/".split("/"))
)
del sys,os

from v1_0_5 import *
'''



	
import math,random

# --- 角色类 ---
class Role():
    def __init__(self,基础属性列表,名称):
        self._基础属性列表=基础属性列表
        self.血,self.攻,self.防,self.敏=self._基础属性列表
        self._剩余血量=self.血
        self.已掉血量=self.血-self.剩余血量
        self.名称=名称
        self.有视防御伤=0
        self.打对方回合数_白板=0
        self.打对方实际回合数_白板=0
        self.有视防御伤百分比=0
        self.战斗属性之吸血=0
        self.战斗抗性之抗吸=0
        self.战斗属性之有效吸血率=0
        self.吸血回血量=0
        self.战斗属性之连击=0
        self.战斗抗性之抗连=0
        self.战斗属性之有效连击率=0     
        self.限定连击吗=False
        self.整场连击限定回合数=6
        self.限定连击之第一回合是否可连击=True
        self.本次回血=self.本次伤害=0 
        self.青龙灵脉=4
        self.暴伤系数=2
        self.每次暴击后暴伤系数递增=(7+5*self.青龙灵脉)/100 if self.青龙灵脉 else 0
        self.战斗属性之暴击=0
        self.战斗抗性之抗暴=0
        self.战斗属性之有效暴击率=0
        self.记者=Stat()
        self.本场结束时将敌人压到血线多少=0
        
    @property
    def 基础属性列表(self):
        return self._基础属性列表
   
    @基础属性列表.setter
    def 基础属性列表(self,value):
        if not isinstance(value,list):
            raise TypeError("基础属性列表必须是list对象")
        self._基础属性列表=value
        self.血,self.攻,self.防,self.敏=self._基础属性列表
  
    @property
    def 剩余血量(self):
        return self._剩余血量
    
    @剩余血量.setter
    def 剩余血量(self,value):
        self._剩余血量=value
        self.已掉血量=self.血-self.剩余血量
        
    def 触发了暴击(self):
        self.暴伤系数+=self.每次暴击后暴伤系数递增
        self.记者.累计触发暴击+=1

# --- 战斗类 ---
class Fight():
    def __init__(self,我方,对方):
        self.我方=我方
        self.对方=对方
        self.先手方=self.后手方=None
        self.谁胜=str()
        self.本场结束时进行到第几回合=0
        self.易得=False
        self.去除连击暴击=False
    
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
        此方.战斗属性之有效连击率=(此方.战斗属性之连击-彼方.战斗抗性之抗连)*3.5/100
        此方.吸血回血量=0 if 此方.战斗属性之有效吸血率<=0 else int(此方.有视防御伤*此方.战斗属性之有效吸血率)
      

    def 模糊战况报告(self):
        self.计算双方()
        print(f"我打敌多少回合：{self.我方.打对方回合数_白板}——{self.我方.打对方实际回合数_白板}回合")
        print(f"敌打我多少回合：{self.对方.打对方回合数_白板}——{self.对方.打对方实际回合数_白板}回合")
        print(f"我打敌一下掉血百分比：{round(self.我方.有视防御伤百分比*100,2)}%——{math.ceil(1/self.我方.有视防御伤百分比)}回合")
        print(f"敌打我一下掉血百分比：{round(self.对方.有视防御伤百分比*100,2)}%——{math.ceil(1/self.对方.有视防御伤百分比)}回合")
        print(f"我打敌一下有视防御伤：{self.我方.有视防御伤}")
        print(f"敌打我一下有视防御伤：{self.对方.有视防御伤}")
        print(f"我打敌一下吸血回血量：{self.我方.吸血回血量}")
        print(f"敌打我一下吸血回血量：{self.对方.吸血回血量}")
        print(f"先手方：{self.先手方.名称}")
        print(f"谁胜：{self.谁胜}")
        对策_需要进行多少次连击=(\
1-self.我方.有视防御伤百分比*(self.对方.打对方实际回合数_白板-1 if self.先手方==self.对方 else self.对方.打对方实际回合数_白板))/self.我方.有视防御伤百分比
        print(f"对策：需要进行{对策_需要进行多少次连击}次连击")
        print(f"对策：平均每回合进行{对策_需要进行多少次连击/self.对方.打对方实际回合数_白板}次连击)")
    
    # --- 准确战况 ---
    
    def 获取彼方(self,此方):
        return self.后手方 if 此方==self.先手方 else self.先手方   
        
    def 造成本次伤害(self,此方,彼方):
        彼方.剩余血量-=此方.本次伤害
        self.造成本次治疗(此方)
        
    def 每次轮序数据重置(self,此方,彼方):
        此方.本次回血=彼方.本次回血=此方.本次伤害=彼方.本次伤害=0
    
    # --- 同一对手连续打多场存档 ---
    def 重新雇佣记者(self):
        self.我方.记者.__init__()
        self.我方.记者.名称="我"
        self.对方.记者.__init__()
        self.对方.记者.名称="敌"
    
    # --- 每到下一场刷新删档 ---
    def 整场数据重置(self,此方):
        此方.剩余血量=此方.血
        此方.暴伤系数=2
        此方.记者.最近一场有效吸血率历史记录.clear()
        此方.记者.最近一场有效连击率历史记录.clear()
        此方.记者.最近一场有效暴击率历史记录.clear()
        
        
    def 造成本次治疗(self,此方):
        此方.吸血回血量=0 if 此方.战斗属性之有效吸血率<=0 else int(此方.本次伤害*此方.战斗属性之有效吸血率)
        此方.本次回血=此方.吸血回血量 if 此方.已掉血量>=此方.吸血回血量 else 此方.已掉血量
        此方.剩余血量+=此方.本次回血
        self.治疗溢出修正(此方)
        
    def 治疗溢出修正(self,此方):
        if 此方.剩余血量>此方.血:此方.剩余血量=此方.血
    
    def 每次轮序必要的计算(self,此方,彼方):
        此方.有视防御伤=此方.攻-彼方.防
        此方.战斗属性之有效吸血率=(此方.战斗属性之吸血-彼方.战斗抗性之抗吸)/100
        if not 此方.限定连击吗:此方.战斗属性之有效连击率=(此方.战斗属性之连击-彼方.战斗抗性之抗连)*1.5/100
        此方.战斗属性之有效暴击率=(此方.战斗属性之暴击-彼方.战斗抗性之抗暴)*2/100
        
        此方.记者.最近一场有效吸血率历史记录.append(f"{round(此方.战斗属性之有效吸血率*100,2)}%")
        此方.记者.最近一场有效连击率历史记录.append(f"{round(此方.战斗属性之有效连击率*100,2)}%")
        此方.记者.最近一场有效暴击率历史记录.append(f"{round(此方.战斗属性之有效暴击率*100,2)}%")
 
    def 每次轮序相应面板报告(self):
        print("\n(除了吸血以外，原始率与有效率的倍数关系为3倍）")
        print(f"我打敌的有效吸血率：{self.我方.战斗属性之有效吸血率*100}%")
        print(f"我打敌的有效连击率：{self.我方.战斗属性之有效连击率*100}%")
        print(f"我打敌的有效暴击率：{self.我方.战斗属性之有效暴击率*100}%")

    
    def 轮序到人物(self,此方):
        彼方=self.获取彼方(此方)
        self.每次轮序数据重置(此方,彼方)
        self.每次轮序必要的计算(此方,彼方)
        #self.每次轮序相应面板报告()
        #input(此方.__dict__)
        #input(彼方.__dict__)
        此方.本次伤害=此方.有视防御伤

        if self.去除连击暴击:
            self.造成本次伤害(此方,彼方)
            return
            
        if random.randint(1,100)<=此方.战斗属性之有效暴击率*100:
            此方.本次伤害*=此方.暴伤系数
            if not self.易得:print(f"❗️触发暴击,暴伤系数{此方.暴伤系数}")
            此方.触发了暴击()      
        
        if random.randint(1,100)<=此方.战斗属性之有效连击率*100:
            本次轮序连击几次=1
            if not self.易得:print(f"❗️触发连击{本次轮序连击几次}次")
            for i in range(本次轮序连击几次):
                此方.记者.累计触发连击+=1
                if random.randint(1,100)<=此方.战斗属性之有效暴击率*100:
                    if not self.易得:print(f"❗️触发暴击,暴伤系数{此方.暴伤系数}")
                    此方.本次伤害+=此方.有视防御伤*此方.暴伤系数
                    此方.触发了暴击()
                else:此方.本次伤害+=此方.有视防御伤
                
        self.造成本次伤害(此方,彼方)
                
    
    def 分出胜负(self):
        if self.先手方.剩余血量<=0:
            self.谁胜=self.后手方.名称
            return True
        elif self.后手方.剩余血量<=0:
            self.谁胜=self.先手方.名称
            return True
        return False
        
    def 记者的变化(self,此方):
        彼方=self.获取彼方(此方)
        此方.本场结束时将敌人压到血线多少=彼方.已掉血量/彼方.血
        if self.谁胜==此方.名称:
            此方.记者.获胜次数+=1
        此方.记者.参赛次数+=1
        此方.记者.历史将敌人压到最低血线=此方.本场结束时将敌人压到血线多少 if 此方.本场结束时将敌人压到血线多少>此方.记者.历史将敌人压到最低血线 else 此方.记者.历史将敌人压到最低血线

            	
    def 准确战况报告(self):
        [self.整场数据重置(i) for i in (self.我方,self.对方)]
        #print(f"第{self.我方.记者.参赛次数+1}场")
        if not self.易得:print("双方初始基础属性:\n{0} PK {1}".format(self.我方.基础属性列表,self.对方.基础属性列表))
        for 第几回合 in range(1,15+1):
            if self.我方.限定连击吗:
                if i<=self.我方.整场连击限定回合数:
                    if 第几回合==1:
                        if self.我方.限定连击之第一回合是否可连击:
                            self.我方.战斗属性之有效连击率=100/100
                        else:self.我方.战斗属性之有效连击率=0
                    else:self.我方.战斗属性之有效连击率=100/100
                else:self.我方.战斗属性之有效连击率=0
            if not self.易得:print(f"\n第{第几回合}回合:")
            for 此方 in (self.先手方,self.后手方):
                if not self.易得:print(f"{此方.名称}行动",end="\t")
                self.轮序到人物(此方)
                if not self.易得:print("{0}(+{3:.2%}|{2:.2%})  {1}(+{5:.2%}|{4:.2%})".\
format(self.我方.剩余血量,self.对方.剩余血量,self.我方.已掉血量/self.我方.血,\
 	self.我方.本次回血/self.我方.血,self.对方.已掉血量/self.对方.血,	self.对方.本次回血/self.对方.血))
                if self.分出胜负():
                    if not self.易得:print(f"谁胜:{self.谁胜}")
                    self.本场结束时进行到第几回合=第几回合
                    
                    self.记者的变化(self.我方)
                    self.记者的变化(self.对方)
                    break
            else:continue
            break
            
            
    def 记者召开发布会(self,第几场):
        print("\033[32;40m",end="")
        print(f"\n---《针对{第几场}记者召开发布会》---")
        print("\033[0m",end="")
        
        print("\033[1;34m")
        self.我方.记者.发布会()
        print("\x1b[31m")
        self.对方.记者.发布会()
        print("\033[0m")
    
    def 直到第一百场(self):
        print("\033[32;40m",end="")
        print("\n---《继续进行九十八场（火力全开）》---")
        print("\033[0m")
        
        self.易得=True
        self.去除连击暴击=False
        for 场次 in range(98):self.准确战况报告()
        input()
        self.记者召开发布会("这一百场")
        input()
        
    def 第二场(self):
        print("\033[32;40m",end="")
        print("\n---《继续进行第二场（火力全开）》---")
        print("\033[0m")
        
        self.去除连击暴击=False
        self.准确战况报告()
        input()
        self.记者召开发布会("第二场")
        input()
        
        
    def 第一场(self):
        print("\033[32;40m",end="")
        print("\n---《进行第一场（去除连击暴击）》---")
        print("\033[0m")
        
        self.易得=False
        self.去除连击暴击=True
        self.准确战况报告()
        input()
        self.记者召开发布会("第一场")
        input()


# --- 统计类 ---
class Stat():
    def __init__(self):
        self.累计触发连击=0
        self.累计触发暴击=0
        self.获胜次数=0
        self.参赛次数=0
        self._胜率=0
        self.名称=str()
        self.最近一场有效吸血率历史记录=list()        
        self.最近一场有效连击率历史记录=list()
        self.最近一场有效暴击率历史记录=list()
        self.历史将敌人压到最低血线=0
        
    @property    	
    def 胜率(self):
        if (self.参赛次数==0):
            raise ZeroDivisionError("除数不能为0")
        return self.获胜次数/self.参赛次数
    
    def 发布会(self):
        print(f"{self.名称}参赛{self.参赛次数}次")
        print(f"{self.名称}累计触发连击{self.累计触发连击}次")
        print(f"{self.名称}累计触发暴击{self.累计触发暴击}次")
        print(f"{self.名称}最近一场有效吸血率历史记录:{self.最近一场有效吸血率历史记录}")
        print(f"{self.名称}最近一场有效连击率历史记录:{self.最近一场有效连击率历史记录}")
        print(f"{self.名称}最近一场有效暴击率历史记录:{self.最近一场有效暴击率历史记录}")
        print(f"{self.名称}历史将敌人压到最低血线:{round(self.历史将敌人压到最低血线*100,2)}%")
        print(f"{self.名称}获胜{self.获胜次数}次")
        print(f"{self.名称}胜率{self.胜率*100}%")



    
def main():
    
    # 怪：《冒险1-10》
    # 8回合暴击1次反击2次
    #敌=Role([5135,740,148,300])

    # 怪：《冒险小村庄2-6》
    # 胜率：61.3%（6回合连击一次暴击两次）
    # 对我=Role([7312,1104,179,299],"我")
    #敌=Role([6854,1475,246,292],"敌")
    
    # 怪：《冒险小村庄2-7》
    # 胜率：75%（6回合连击一次暴击两次闪避一次）
    # 对我=Role([7671,1150,187,323],"我")
    #敌=Role([7025,1511,252,301],"敌")
    
    # 胜率：75%（6回合一连一暴）
    # 对我=我=Role([7918,1193,194,347],"我")
    #敌=Role([7194,1547,258,309],"敌")
    
    敌=Role([9861,1421,284,359],"敌")
    
    # 斗法
    # （两次没打过）
    #敌=Role([15947,2357,390,653],"敌")
    #敌=Role([8339,1258,203,384],"敌")
    
    # 旧我
    旧我=Role([7671,1150,187,323],"我")
    # 新我
    我=Role([8036,1212,197,355],"我")
    
    # 让新敌与旧敌分高下
    #我=Role([4880,1048,175,354],"我")
    
    # 我vs敌 吸血
    #我.战斗属性之吸血=3.4
    我.战斗属性之吸血=0
    敌.战斗抗性之抗吸=1.7
    
    # 敌vs我 吸血
    敌.战斗属性之吸血=0.6
    我.战斗抗性之抗吸=0
    
    #，我vs敌 连击
    我.战斗属性之连击=13
    敌.战斗抗性之抗连=1.7
    
    #，敌vs我 连击
    敌.战斗属性之连击=1.9
    我.战斗抗性之抗连=0
    
    # 我vs敌 暴击
    我.战斗属性之暴击=8.8
    敌.战斗抗性之抗暴=13.7
    
    # 敌vs我 暴击
    敌.战斗属性之暴击=0.6
    我.战斗抗性之抗暴=0
    
    战场=Fight(我,敌)
    print(f"旧我基础属性:{旧我.基础属性列表}")
    print(f"新我基础属性:{我.基础属性列表}")
    print("新我是旧我的几倍：%s"%("~".join([str(a/b) for a,b in zip(我.基础属性列表,旧我.基础属性列表)])))
    
    print("\x1b[7m",end="")
    print("\n\t《战场：模糊战况报告》\t",end="")
    print("\033[0m")
    战场.模糊战况报告()
    
    print("\x1b[7m",end="")
    print("\n\t《战场：准确战况报告》\t",end="")
    print("\033[0m")
    战场.重新雇佣记者()
    
    # 这个开关最关键，要关闭时只要调一个就好了，其他不用管
    #战场.我方.限定连击吗=False
    #战场.我方.整场连击限定回合数=6
    #战场.我方.限定连击之第一回合是否可连击=True
   
    战场.第一场()
    战场.第二场()
    战场.直到第一百场()

                
if __name__=="__main__":
    main()