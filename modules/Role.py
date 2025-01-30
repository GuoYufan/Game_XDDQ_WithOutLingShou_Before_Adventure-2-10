import random, math, traceback
from Stat import Stat
from Fight import Fight, FightEnd
from Buff import Buff


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
        	# 筑基阶段：开始有灵兽
        	# 金丹阶段：开始有精怪
        self._现阶段="筑基"
        self.神通功能开启=False
        self.妖气=0
        self.携带神通=[]
        self._时刻=str()
        self.已完成补气=False
        
        # --- 复 活 相 关 ---
        self.复活未起身=False
        self.可复活次数=0
        
        # --- 战 斗 属 性 相 关 ---
        self.吸=self.连=self.暴=self.反=0
        self.抗吸=self.抗连=self.抗暴=self.抗反=0
        self._触发了连击=self._触发了暴击=self._触发了反击=False
        self.暴伤系数=2
        self.青龙灵脉=0
        self.每次暴击后暴伤系数递增=(7+5*self.青龙灵脉)/100 if self.青龙灵脉 else 0
        self.连击率渐减系数=1
    
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
        self.面板_主灵兽伤百分比=0
        self.面板_主灵兽治疗百分比=0
        
        # --- 状 态 ---
        self.需要失去几次行动=0
        
        # --- 灵 兽 ---
        self.主灵兽名称=""
        self.主灵兽伤倍率_乘在攻=0
        self.主灵兽出手频率=0
        
        self.buff=dict.fromkeys(("攻","连","减伤"))
        for key in self.buff:
            self.buff[key]=Buff(key,self,0,0) 
        
        self.主灵兽治疗倍率_乘在攻=0

        
        # --- 增 减 伤 ---
        self.增伤=self.减伤=0


        # --- 对是否支持buff功能的开关 ---
        self.buff_ON=True               
        
        
        # --- 强 弱 灵 ---
        self.强灵=self.弱灵=0

        	
        # --- 精 怪 ---
        self.携带精怪=[]
        
        self.精怪图鉴_魔礼青_层数=0
        self.精怪图鉴_魔礼青_满层=5
        
    
    def 载入精怪(self):
        if "梼杌" in self.携带精怪:
            self.连+=20
            self.反+=20
        if "黑麒麟" in self.携带精怪:
            self.对手.连-=28
            self.对手.暴-=28
         
        
   
    def 设置基础属性(self,*underlying_attributes):
        self.血,self.攻,self.防,self.敏=underlying_attributes
    
    def 获取基本属性(self):
        return (self.血, self.攻, self.防, self.敏)
                
    def 为了专用于新号而开始(self):
        if self.现阶段 in ("筑基", "金丹"):
            self.神通功能开启=False
        else:self.神通功能开启=True

    @property
    def 现阶段(self):
        return self._现阶段
        
    @现阶段.setter    
    def 现阶段(self,value):
         self._现阶段=value
         self.为了专用于新号而开始()
    
    @property
    def 触发了暴击(self):
        return self._触发了暴击
        
    @触发了暴击.setter    
    def 触发了暴击(self,value):
         if self.战场.关闭连暴反:
             value=False
         self._触发了暴击=value
         if self._触发了暴击:
             self.记者.本场触发暴击+=1
             self.记者.累计触发暴击+=1
             
    @property
    def 触发了连击(self):
        return self._触发了连击
        
    @触发了连击.setter    
    def 触发了连击(self,value):        
         if self.战场.关闭连暴反:
             value=False
         self._触发了连击=value        
         if self._触发了连击:
             self.记者.本场触发连击+=1
             self.记者.累计触发连击+=1

    @property
    def 触发了反击(self):
        return self._触发了反击
        
    @触发了反击.setter    
    def 触发了反击(self,value):
         if self.战场.关闭连暴反:
             value=False
         self._触发了反击=value
         if self._触发了反击:
             self.记者.本场触发反击+=1
             self.记者.累计触发反击+=1                  
    
    @property
    def 剩余血量(self):
        return self._剩余血量
    
    @剩余血量.setter
    def 剩余血量(self,value):
        if value>self.血:value=self.血
        self._剩余血量=value
        self.已掉血量=self.血-self.剩余血量
        self.剩余血量百分比=self.剩余血量/self.血*100
        self.已掉血量百分比=self.已掉血量/self.血*100
        if self.已掉血量百分比> self.对手.记者.本场将敌人压到最低血线:
            self.对手.记者.本场将敌人压到最低血线=self.已掉血量百分比         
            
        self.已死亡=self.剩余血量<=0
        if self.已死亡:self.检查复活()
        
    @property
    def 时刻(self):return self._时刻
    
    @时刻.setter
    def 时刻(self,value):
        self._时刻=value
        if self._时刻 in ("掉血之未回妖气","普攻后之未回妖气","受到蚀魂咒","释放道法后"):
            if self.神通功能开启:self.妖气变化()
        elif self._时刻=="普攻后之未发动神通":
            if self.神通功能开启:self.神通跟随()
        elif self._时刻=="回合结束时":
            if self.buff_ON:self.buff变化()
        elif self._时刻=="受击时":
            if "魔礼青" in self.携带精怪 and self.精怪图鉴_魔礼青_层数<self.精怪图鉴_魔礼青_满层:
                self.反+=10
                self.精怪图鉴_魔礼青_层数+=1
                if not self.战场.关闭战报:print(f"⚡️{self.名称}精怪魔礼青触发,现反击率{self.反-self.对手.抗反:g}%",end="")
                if self.精怪图鉴_魔礼青_层数==self.精怪图鉴_魔礼青_满层:
                    if not self.战场.关闭战报:print("(已满层)")
                elif not self.战场.关闭战报:print()
        elif self._时刻=="本场开始":
            self.载入精怪()
            
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
            self.本次伤害出发=(self.攻-self.对手.防)*(1+self.增伤-self.对手.减伤)
            if self.触发了暴击:
                self.本次伤害出发=(self.攻-self.对手.防)*self.暴伤系数*(1+self.增伤-self.对手.减伤)
                self.暴伤系数+=self.每次暴击后暴伤系数递增                
                self.触发了暴击=False
            return
        if 伤害种类=="主灵兽伤":
            self.本次伤害出发=self.攻*self.主灵兽伤倍率_乘在攻*(1+self.强灵-self.对手.弱灵)*(1+self.增伤-self.对手.减伤)
            return
                
    def 计算本次伤害受到(self):
        self.本次伤害受到=self.对手.本次伤害出发
        if not self.战场.关闭战报:
            print("\033[34m" if self.名称=="敌" else "\x1b[31m",end=str())
            print(f"{self.名称}受到伤害:{int(self.本次伤害受到)} 掉血百分比:{self.本次伤害受到/self.血*100:.2f}%")
            print("\033[0m",end="")
            
    def 检查复活(self):
        self.已死亡=self.剩余血量<=0
        左=self.战场.左
        
        if self.已死亡:
            if not self.战场.关闭战报:self.战场.显示该回合战斗结果()            
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
        if self.战场.关闭连暴反:return
        
        有效连击率 = (self.连-self.对手.抗连)*self.连击率渐减系数
        
        
        if 1 <= random.randint(1,100) <= 有效连击率:
            self.触发了连击=True
            self.连击率渐减系数*=0.5
            if not self.战场.关闭战报:
                print(f"❗️{self.名称}触发了连击(此前连击率:{有效连击率:g}%)")
        else:
            self.触发了连击=False
            self.连击率渐减系数=1
              
        
        有效暴击率 = self.暴-self.对手.抗暴
        if 1 <= random.randint(1,100) <= 有效暴击率:
            self.触发了暴击=True
            if not self.战场.关闭战报:
                print(f"❗️{self.名称}触发了暴击(此前暴击率:{有效暴击率:g}%)")
        else:self.触发了暴击=False
   
    def 释放道法(self):
        print("❗️释放道法")
        self.时刻="释放道法后"
    
    def 反击判定(self):
        if self.战场.关闭连暴反:return
        
        有效反击率 = self.反-self.对手.抗反
        #input(有效反击率)             
        if 1 <= random.randint(1,100) <= 有效反击率:
            self.触发了反击=True
            if not self.战场.关闭战报:                
                print(f"❗️{self.名称}触发了反击(此前反击率:{有效反击率:g}%)")
                
        else:self.触发了反击=False
   
        
    def 进行普攻(self):
        if not self.触发了反击:self.时刻="普攻后之未回妖气"
        while True:
            self.连击暴击判定()
            self.计算本次伤害出发("有视防御伤")
            self.对手.计算本次伤害受到()          
            self.进行吸血()            
            self.对手.时刻=="掉血之未回妖气"
            self.对手.时刻="受击时"
            self.时刻="普攻后之未发动神通"
            self.对手.掉血之血条变化()
            self.对手.反击判定()
            if self.触发了连击:          
                self.触发了连击=False
                if not self.对手.触发了反击:continue                       
            if self.对手.触发了反击:
                self.对手.进行普攻()
                self.对手.触发了反击=False
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
        self.面板_有视防御伤=(self.攻-self.对手.防)*(1+self.增伤-self.对手.减伤)
        self.面板_打对方回合数=self.对手.血/self.面板_有视防御伤
        self.面板_打对方实际回合数=math.ceil(self.面板_打对方回合数)
        self.面板_有视防御伤百分比=1/self.面板_打对方回合数
        self.面板_吸血回血量=0 if self.吸-self.对手.抗吸<=0 else int(self.面板_有视防御伤*(self.吸-self.对手.抗吸)/100)
        self.面板_主灵兽伤百分比=self.攻*self.主灵兽伤倍率_乘在攻/self.对手.血*(1+self.增伤-self.对手.减伤)
        self.面板_主灵兽治疗百分比=self.攻*self.主灵兽治疗倍率_乘在攻/self.血
             
    def 进行吸血(self):
        self.吸血回血量=int(self.对手.本次伤害受到*(self.吸-self.对手.抗吸)/100) if self.吸>self.对手.抗吸 else 0
        if not self.战场.关闭战报:print(f"{self.名称}吸血回血量:{self.吸血回血量} 治疗百分比:{self.吸血回血量/self.血*100:.2f}%")
        self.剩余血量+=self.吸血回血量
        
    def 设置战斗属性(self, 均属, 高属名="", 高属=-1):
        self.吸=self.连=self.暴=self.反=均属
        if 高属名:exec(f"self.{高属名}={高属}")
    
    def 设置战斗抗性(self, 均抗, 高抗名="", 高抗=-1):
        self.抗吸=self.抗连=self.抗暴=self.抗反=均抗
        if 高抗名:exec(f"self.{高抗名}={高抗}")
    
    def 使双方战斗属性与抗性完全相等(self):
        pass
            
    def 记者的变化(self):
        if self.战场.谁胜==self.记者.选手:
            self.记者.获胜次数+=1
        elif self.战场.谁胜==None:
            self.记者.平局次数+=1
        self.记者.参赛次数+=1
    
    def buff强制失效(self):
        for _ in self.buff:
            self.buff[_].duration=0
        
        self.buff从激活到失效()
        
    def buff从激活到失效(self):
        # 检查剩余回合数是否足够，若不足则从激活到失效
        # 回退将增益的数值
        if self.buff["攻"].is_about_to_deactivate():
            if not self.战场.关闭战报:print(f"(灵兽效果已结束:此前攻击力{self.攻:g},",end="")
            self.buff["攻"].deactivate()  
            if not self.战场.关闭战报:print(f"现攻击力{self.攻:g})\n")
        
        if self.buff["连"].is_about_to_deactivate():
            if not self.战场.关闭战报:print(f"(灵兽效果已结束:此前连击率{self.连-self.对手.抗连:g}%,",end="")
            self.buff["连"].deactivate()
            if not self.战场.关闭战报:print(f"现连击率{self.连-self.对手.抗连:g}%)\n")
        
        if self.buff["减伤"].is_about_to_deactivate():
            if not self.战场.关闭战报:print(f"(灵兽效果已结束:此前减伤{self.减伤*100:g}%,",end="")
            self.buff["减伤"].deactivate()
            if not self.战场.关闭战报:print(f"现减伤{self.减伤*100:g}%)\n")
            

    def buff变化(self):
        # 回合结束时，对buff剩余回合数进行减量
        if self.时刻=="回合结束时":
            self.buff["攻"].decrement()
            self.buff["连"].decrement()
            self.buff["减伤"].decrement()
                            
        self.buff从激活到失效()
    
    def 灵兽效果(self):
        if not self.buff_ON:return
        
        if self.主灵兽名称=="灵狐":
            if not self.战场.关闭战报:print(f"(灵兽效果:此前攻击力{self.攻:g},",end="")
            # 如果在效果未结束时再次给效果，不叠加。直到上次效果结束才重新相同效果。
            # 再怎么样也只是效果不断，而从来不会是更强的效果。
            # 否则加强效果，连乘多次，太变态了。            
            if self.buff["攻"].active==False:
                # 从失效到激活
                self.buff["攻"].activate("攻",1.2,1)
            if not self.战场.关闭战报:print(f"现攻击力{self.攻:g})")
        
        elif self.主灵兽名称 in ("天马", "鹿蜀"):
            if not self.战场.关闭战报:print(f"(灵兽效果:此前连击率{self.连-self.对手.抗连:g}%,",end="")
            if self.buff["连"].active==False:
                self.buff["连"].activate("连",20,1)
            
            if not self.战场.关闭战报:print(f"现连击率{self.连-self.对手.抗连:g}%)")   	
        
        elif self.主灵兽名称=="鸾鸟":
            if not self.战场.关闭战报:print(f"(灵兽效果:此前减伤{self.减伤*100:g}%,",end="")
            
            if self.buff["减伤"].active==False:
                self.buff["减伤"].activate("减伤",0.15,1)
            
            if not self.战场.关闭战报:print(f"现减伤{self.减伤*100:g}%)")   	
            
 
        
    def 轮序到灵兽(self):
        if not self.主灵兽名称:return
        
        if not self.战场.第几回合%self.主灵兽出手频率==0:return
                
        if self.主灵兽伤倍率_乘在攻:
            if not self.战场.关闭战报:print(f"【{self.名称}{self.哪一方}主灵兽{self.主灵兽名称}行动】")            
            # 先参战技能伤害，再效果
            self.计算本次伤害出发("主灵兽伤")
            self.对手.计算本次伤害受到()        
            self.对手.掉血之血条变化()
            self.灵兽效果()
        
        if self.主灵兽治疗倍率_乘在攻:
            if not self.战场.关闭战报:print(f"【{self.名称}{self.哪一方}主灵兽{self.主灵兽名称}行动】")            
            # 先参战技能治疗，再效果
            self.计算本次治疗("主灵兽治疗")
            self.受到治疗()        
            self.灵兽效果()
   
    def 受到治疗(self):
       self.剩余血量+=self.本次治疗
       if not self.战场.关闭战报:print("\033[32m"+f"{self.名称}受到治疗:{int(self.本次治疗)} 治疗百分比:{self.本次治疗/self.血*100:.2f}%"+"\033[0m")
             
    def 计算本次治疗(self,治疗种类):
        if 治疗种类=="主灵兽治疗":
            self.本次治疗=self.攻*self.主灵兽治疗倍率_乘在攻*(1+self.强灵-self.对手.弱灵)
            return
            
        
