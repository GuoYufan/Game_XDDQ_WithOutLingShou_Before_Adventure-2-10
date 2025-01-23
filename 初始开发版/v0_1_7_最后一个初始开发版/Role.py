from Stat import *

# --- 角色类 ---
class Role():
    def __init__(self,基础属性列表,名称):
        self._基础属性列表=基础属性列表
        self.血,self.攻,self.防,self.敏=self._基础属性列表
        self._剩余血量=self.血
        self.已掉血量=self.血-self._剩余血量
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
        self.强制连击率吗=False
        self.整场有多少回合强制连击率=6
        self.强制连击率之第一回合是否可连击=True
        self.本次回血=self.本次伤害=0 
        self._青龙灵脉=0
        self.暴伤系数=2
        self.每次暴击后暴伤系数递增=(7+5*self.青龙灵脉)/100 if self.青龙灵脉 else 0
        self.战斗属性之暴击=0
        self.战斗抗性之抗暴=0
        self.战斗属性之有效暴击率=0
        self.记者=Stat()
        self.最近一场结束时将敌人压到血线多少=0
        self.需要失去几次行动=0
        self.可行动=True
    
    @property
    def 需要失去几次行动(self):return self._需要失去几次行动
    
    @需要失去几次行动.setter
    def 需要失去几次行动(self,value):
        self._需要失去几次行动=value
        if self.需要失去几次行动==0:self.可行动=True
        else:self.可行动=False
    
    @property
    def 青龙灵脉(self):
        return self._青龙灵脉
        
    @青龙灵脉.setter
    def 青龙灵脉(self,value):
        self._青龙灵脉=value
        self.每次暴击后暴伤系数递增=(7+5*self._青龙灵脉)/100 if self.青龙灵脉 else 0
 
    @property
    def 基础属性列表(self):
        return self._基础属性列表
   
    @基础属性列表.setter
    def 基础属性列表(self,value):
        if not isinstance(value,list):
            raise TypeError("基础属性列表必须是list对象")
        self._基础属性列表=value
        self.血,self.攻,self.防,self.敏=self._基础属性列表
        self.剩余血量=self.血

    @property
    def 剩余血量(self):
        return self._剩余血量
    
    @剩余血量.setter
    def 剩余血量(self,value):
        self._剩余血量=value
        self.已掉血量=self.血-self._剩余血量
       
    def 触发了暴击(self):
        self.暴伤系数+=self.每次暴击后暴伤系数递增
        self.记者.累计触发暴击+=1
        
    def 设置战斗属性(self, 均属, 高属名="", 高属=-1):
        self.战斗属性之吸血=self.战斗属性之连击=self.战斗属性之暴击=均属
        if 高属名:exec(f"self.战斗属性之{高属名}={高属}")
    
    def 设置战斗抗性(self, 均抗, 高抗名="", 高抗=-1):
        self.战斗抗性之抗吸=self.战斗抗性之抗连=self.战斗抗性之抗暴=均抗
        if 高抗名:exec(f"self.战斗抗性之{高抗名}={高抗}")
    
    def 使双方战斗属性与抗性完全相等(self):
        self.对手.战斗属性之吸血=self.战斗属性之吸血
        self.对手.战斗属性之连击=self.战斗属性之连击
        self.对手.战斗属性之暴击=self.战斗属性之暴击
        self.对手.战斗抗性之抗吸=self.战斗抗性之抗吸
        self.对手.战斗抗性之抗连=self.战斗抗性之抗连
        self.对手.战斗抗性之抗暴=self.战斗抗性之抗暴

if __name__=="__main__":
    a=Role([240,2400,40,500],"我")
    print(Role.__dict__)
    print()
    print(a.__dict__)
