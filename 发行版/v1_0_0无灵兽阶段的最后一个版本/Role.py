import random, math
from Stat import Stat
from Fight import Fight, FightEnd


class Role():
    def __init__(self,基础属性列表,名称):
        # --- 基 础 属 性 ---
        self.血,self.攻,self.防,self.敏=基础属性列表
        self._剩余血量=self.血
        self.已掉血量=self.血-self._剩余血量
        self.剩余血量百分比=0
        self.已掉血量百分比=0
        self.名称=名称
        self.对手=None
        
        # --- 宣 布 本 场 战 斗 结 束 ---
        self.已死亡=False
        
        # --- 妖 气 与 神 通 ---
        self.现阶段="筑基"
        self.神通功能开启=False
        self.妖气=0
        self.携带神通=[]
        self._时刻=str()
        self.已完成补气=False
        
        # --- 复 活 相 关 ---
        self.复活未起身=False
        self.可复活次数=0
        
        # --- 战 斗 属 性 相 关 ---
        self.吸=self.连=self.暴=0
        self.抗吸=self.抗连=self.抗暴=0
        self.触发了连击=self.触发了暴击=False
        self.暴伤系数=2
        self.青龙灵脉=0
        self.每次暴击后暴伤系数递增=(7+5*self.青龙灵脉)/100 if self.青龙灵脉 else 0
    
    
        # --- 媒 体 活 动 与 记 者 ---
        self.记者=Stat()
        self.记者.选手=self
        
        # --- 战 场 ---
        self.战场=None
       
        # --- 模 糊 战 报 之 面 板 计 算---
        self.面板_有视防御伤=0
        self.面板_打对方回合数=0
        self.面板_打对方实际回合数=0
        self.面板_有视防御伤百分比=0
        self.面板_吸血回血量=0
        self.哪一方=""
       
        # --- 状 态 ---
        self.需要失去几次行动=0
        
    
    @property
    def 剩余血量(self):
        return self._剩余血量
    
    @剩余血量.setter
    def 剩余血量(self,value):
        if value>self.血:value=self.血
        self._剩余血量=value
        self.已掉血量=self.血-self._剩余血量
        self.剩余血量百分比=self.剩余血量/self.血*100
        self.已掉血量百分比=self.已掉血量/self.血*100        
        if self.已掉血量百分比 > self.对手.记者.历史将敌人压到最低血线:
            self.对手.记者.历史将敌人压到最低血线=self.已掉血量百分比
        self.已死亡=self.剩余血量<=0
        if self.已死亡:self.检查复活()
        
    @property
    def 时刻(self):return self._时刻
    
    @时刻.setter
    def 时刻(self,value):
        self._时刻=value
        if self._时刻 in ("掉血之未回妖气","普攻后之未回妖气","受到蚀魂咒"):
            if self.神通功能开启:self.妖气变化()
        elif self._时刻=="普攻后之未发动神通":
            if self.神通功能开启:self.神通跟随()
            
    def 妖气变化(self):
        if self.时刻=="释放道法后":
            self.妖气=0
            self.已完成补气=False
            if "七十二变" in self.携带神通:
                self.妖气+=3000
            return
        if self.时刻=="掉血之未回妖气":
            self.妖气+=self.本次受伤量/self.血*5000
        elif self.时刻=="普攻后之未回妖气":
            self.妖气+=2000
        elif self.时刻=="受到蚀魂咒":
            self.妖气-=800
            
        if self.妖气>=10000:
            self.妖气=10000
            self.已完成补气=True
        elif self.妖气<0:
            self.妖气=0
    
    def 神通跟随(self):
        if self.时刻=="普攻后之未发动神通":
            if "蚀魂咒" in self.携带神通:
                print(f"❗️{self.名称}的神识神通蚀魂咒发动,{self.对手.名称}此前妖气{self.对手.妖气:g},",end="")
                self.对手.时刻="受到蚀魂咒"
                print(f"目前妖气{self.对手.妖气:g}")
    
    def 计算本次伤害出发(self,伤害种类):
        if 伤害种类=="有视防御伤":
            self.本次伤害出发=self.攻-self.对手.防
            if self.触发了暴击:
                self.本次伤害出发=(self.攻-self.对手.防)*self.暴伤系数
                self.暴伤系数+=self.每次暴击后暴伤系数递增
                self.记者.累计触发暴击+=1
                self.触发了暴击=False
            return

                
    def 计算本次伤害受到(self):
        self.本次伤害受到=self.对手.本次伤害出发
        if not self.战场.关闭战报:print(f"{self.名称}受到伤害:{self.本次伤害受到:g} 掉血百分比:{self.本次伤害受到/self.血*100:.2f}%")
    
    def 检查复活(self):
        self.已死亡=self.剩余血量<=0
        左=self.战场.左
        
        if self.已死亡:
            if not self.战场.关闭战报:print("（目前剩余血量：%s%g(%.2f%%) VS %s%g(%.2f%%)）"%(\
                 左.名称, 左.剩余血量, 左.已掉血量百分比,
                 左.对手.名称, 左.对手.剩余血量, 左.对手.已掉血量百分比))
            if 左.神通功能开启 and not self.战场关闭战报:
                print("（目前妖气：%s%g VS %s%g）"%(\
                    左.名称,左.妖气,\
                    左.对手.名称,左.对手.妖气))
            if not (self.复活未起身 or self.可复活次数>0):
                if not self.战场.关闭战报:
                    print(f"（{self.名称}已死，无复活）")
                    print(f"\n📖\n（{self.名称}告负）")
                self.战场.谁胜=self.对手
                raise FightEnd()
            if not self.战场.关闭战报:print(f"（{self.名称}已死，有复活）")
            self.复活未起身=True
    
    def 掉血之血条变化(self):
        self.剩余血量-=self.本次伤害受到
    
    def 连击暴击判定(self):
        if 1 <= random.randint(1,100) <= self.连-self.对手.抗连:
            self.触发了连击=True
            if not self.战场.关闭战报:print(f"❗️{self.名称}触发了连击")
        else:self.触发了连击=False
        
        if 1 <= random.randint(1,100) <= self.暴-self.对手.抗暴:
            self.触发了暴击=True
            if not self.战场.关闭战报:print(f"❗️{self.名称}触发了暴击")
        else:self.触发了暴击=False
   
    def 释放道法(self):
        print("❗️释放道法")
        self.时刻="释放道法后"
        
        
    def 进行普攻(self):
        self.时刻="普攻后之未回妖气"
        while True:
            self.连击暴击判定()
            self.计算本次伤害出发("有视防御伤")
            self.对手.计算本次伤害受到()
            self.进行吸血()
            self.对手.时刻=="掉血之未回妖气"
            self.时刻="普攻后之未发动神通"
            self.对手.掉血之血条变化()   
            if self.触发了连击:
                self.记者.累计触发连击+=1
                self.触发了连击=False
                continue
            break

    def 每次轮序数据重置(self):
        self.本次回血=self.对手.本次回血=self.本次伤害=self.对手.本次伤害=0
        
    def 轮序到人物(self):
        if not self.战场.关闭战报:print(f"【{self.名称}行动】")
        if self.复活未起身:
            self.可复活次数-=1
            self.复活未起身=False
            self.剩余血量=self.血*0.12
        if not self.对手.复活未起身:
            if self.已完成补气:self.释放道法()
            else:self.进行普攻()
            
    def 计算单方面板(self):
        self.面板_有视防御伤=self.攻-self.对手.防
        self.面板_打对方回合数=self.对手.血/self.面板_有视防御伤
        self.面板_打对方实际回合数=math.ceil(self.面板_打对方回合数)
        self.面板_有视防御伤百分比=1/self.面板_打对方回合数
        self.面板_吸血回血量=0 if self.吸-self.对手.抗吸<=0 else int(self.面板_有视防御伤*(self.吸-self.对手.抗吸)/100)

    def 为了专用于新号而开始(self):
        if self.现阶段 in ("筑基"):
            self.神通功能开启=False

             
    def 进行吸血(self):
        self.吸血回血量=int(self.对手.本次伤害受到*(self.吸-self.对手.抗吸)/100) if self.吸>self.对手.抗吸 else 0
        if not self.战场.关闭战报:print(f"{self.名称}吸血回血量:{self.吸血回血量} 治疗百分比:{self.吸血回血量/self.血*100:.2f}%")
        self.剩余血量+=self.吸血回血量
        
    def 设置战斗属性(self, 均属, 高属名="", 高属=-1):
        self.吸=self.连=self.暴=均属
        if 高属名:exec(f"self.{高属名}={高属}")
    
    def 设置战斗抗性(self, 均抗, 高抗名="", 高抗=-1):
        self.抗吸=self.抗连=self.抗暴=均抗
        if 高抗名:exec(f"self.{高抗名}={高抗}")
    
    def 使双方战斗属性与抗性完全相等(self):
        pass
            
    def 记者的变化(self):
        if self.战场.谁胜==self.记者.选手:
            self.记者.获胜次数+=1
        self.记者.参赛次数+=1
    

    