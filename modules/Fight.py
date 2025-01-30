import traceback, sys, math, copy


class FightEnd(Exception):
    def __str__(self):
        return "本场结束!"
        
class Fight():
    def __init__(self,左,右):
        self.设置双方(左,右)
        self.先手方=None
        self.关闭战报=False
        self.谁胜=None
        self.第几回合=0
        self.第几场=0
        self.关闭连暴反=False        
        self._本场结束=False
        self.最大回合数=15
    
    @property
    def 本场结束(self):return self._本场结束
    
    @本场结束.setter
    def 本场结束(self,value):
        self._本场结束=value
        if value:
            [_.记者的变化() for _ in (self.左, self.左.对手)]
            [_.buff强制失效() for _ in (self.左, self.左.对手)]
            
            
    def 设置双方(self,左,右):
        self.左=左
        self.左.对手=右
        self.左.对手.对手=左
        for _ in (self.左, self.左.对手):
            _.战场=self
            _.记者.选手=_
            for key in _.buff:
                _.buff[key].role=_
       
 
                
    def 分出先后手方(self):
        if self.左.敏>self.左.对手.敏:
            self.左.哪一方="先手"
            self.左.对手.哪一方="后手"
            self.先手方=self.左
        else:
            self.左.对手.哪一方="先手"
            self.左.哪一方="后手"            
            self.先手方=self.左.对手                        
            
    def 展示双方战前面板信息(self):
        [_.计算单方面板() for _ in (self.左,self.左.对手)]
        
        for _ in (self.左, self.左.对手):
            print("血:%g 攻:%g 防:%g 敏:%g"%(_.血, _.攻, _.防, _.敏))
        print()
        
        words=[]
        word="%s主灵兽%s伤%g%%(%g%%),治疗%g%%(%g%%)"
        for _ in (self.左, self.左.对手):
            words.append( word%(
            _.名称, _.主灵兽名称,
            _.面板_主灵兽伤百分比*100,
            _.面板_主灵兽伤百分比*100*(1+_.强灵-_.对手.弱灵)*(1+_.增伤-_.对手.减伤),
            	_.面板_主灵兽治疗百分比*100,
            		_.面板_主灵兽治疗百分比*100*(1+ _.强灵 - _.对手.弱灵)*(1+_.增伤-_.对手.减伤),
            	))

        print(("|".join(words)).join("[]"))
                       
        
        print("[%s精怪%s|%s精怪%s]"%(
            	self.左.名称,
            	",".join(self.左.携带精怪),
            	self.左.对手.名称,
        	    ",".join(self.左.对手.携带精怪)
            	)
          	)        
        
        print("[%s神通%s|%s神通%s]"%(
            	self.左.名称,
            	",".join(self.左.携带神通),
            	self.左.对手.名称,
        	    ",".join(self.左.对手.携带神通)
            	)
          	)
                
        
        print("[%s吸血率%g%%,连击率%g%%,暴击率%g%%,反击率%g%%%s"%(
            	self.左.名称,
             self.左.吸-self.左.对手.抗吸,
             self.左.连-self.左.对手.抗连,
             self.左.暴-self.左.对手.抗暴,
             self.左.反-self.左.对手.抗反,
             "(已关闭连暴反)" if self.关闭连暴反 else "",
             )
        	)
        	
        print("|%s吸血率%g%%,连击率%g%%,暴击率%g%%,反击率%g%%%s]"%(
            	self.左.对手.名称,
             self.左.对手.吸-self.左.抗吸,
             self.左.对手.连-self.左.抗连,
             self.左.对手.暴-self.左.抗暴,
             self.左.对手.反-self.左.抗反,
             "(已关闭连暴反)" if self.关闭连暴反 else "",
             )
        	)

    
    def 左胜吗(self):
        self.分出先后手方()
        if self.左.哪一方=="先手":
            if self.左.面板_打对方实际回合数<=self.左.对手.面板_打对方实际回合数:return True
        else:
            if self.左.面板_打对方实际回合数<self.左.对手.面板_打对方实际回合数:return True
        return False
    
    def 计算双方面板(self):
        [_.计算单方面板() for _ in (self.左,self.左.对手)]
        self.分出先后手方()
        self.面板_谁胜=self.左 if self.左胜吗() else self.左.对手

    
    def 模糊战况报告(self):
        print("\x1b[7m",end="")
        print("\n\t《战场：模糊战况报告》\t",end="")
        print("\033[0m")
        self.计算双方面板()
        print(f"我打敌多少回合：{self.左.面板_打对方回合数}——{self.左.面板_打对方实际回合数}回合")
        print(f"敌打我多少回合：{self.左.对手.面板_打对方回合数}——{self.左.对手.面板_打对方实际回合数}回合")
        print(f"我打敌一下掉血百分比：{self.左.面板_有视防御伤百分比*100:.2f}%——{math.ceil(1/self.左.面板_有视防御伤百分比)}回合")
        print(f"敌打我一下掉血百分比：{self.左.对手.面板_有视防御伤百分比*100:.2f}%——{math.ceil(1/self.左.对手.面板_有视防御伤百分比)}回合")
        print(f"我打敌一下有视防御伤：{int(self.左.面板_有视防御伤)}")
        print(f"敌打我一下有视防御伤：{int(self.左.对手.面板_有视防御伤)}")
        print(f"我打敌一下吸血回血量：{self.左.面板_吸血回血量}")
        print(f"敌打我一下吸血回血量：{self.左.对手.面板_吸血回血量}")
        print(f"先手方：{self.先手方.名称}")
        print(f"谁胜：{self.面板_谁胜.名称}")
        
        def 是否需要对策():
            nonlocal self
            return self.面板_谁胜.名称=="敌"
            
        def 提供对策():
            nonlocal self
            
            几个回合结束=min(self.左.面板_打对方实际回合数,self.左.对手.面板_打对方实际回合数)
            我已行动了几个回合=几个回合结束-(1 if self.先手方==self.左.对手 else 0)
            我已造成掉血百分比=self.左.面板_有视防御伤百分比*我已行动了几个回合
            对策_需要进行多少次连击=(1-我已造成掉血百分比)/self.左.面板_有视防御伤百分比
          
            print(f"对策：需要进行{对策_需要进行多少次连击}次连击")
            print(f"对策：平均每回合进行{对策_需要进行多少次连击/几个回合结束}次连击)")
        
        if 是否需要对策():提供对策()

    
    # --- 同 一 对 手 连 续 打 多 场 存 档 ---
    	
    def 记者重新入场(self):
        self.第几场=0
        
        for _ in (self.左, self.左.对手):
            _.记者.__init__()
            _.记者.选手=_ 

 
        
    def 进行选手存档(self):        
        self.存档_左=copy.copy(self.左)        
        self.存档_左.对手=copy.copy(self.左.对手)
        


    # --- 媒 体 活 动 与 赛 程 安 排 ---
    
    def 记者召开发布会(self,这几场):
        print("\033[32;40m",end="")
        print(f"\n---《针对{这几场}记者召开发布会》---")
        print("\033[0m",end="")
        
        print("\033[1;34m")
        self.左.记者.发布会()
        print("\x1b[31m")
        self.左.对手.记者.发布会()
        print("\033[0m")

    def 第一场(self):
        self.战况报告()
        self.记者召开发布会("第一场")

        
    def 再来多少场(self):
        while True:
            answer=input("❓再来多少场？\n(Q/q:退出 |R/r:切换开关战报 |F/f:切换开关连暴反):\n\t")
            if answer.lower()=="q":
                return "quit"
            elif answer.lower()=="r":
                self.关闭战报=not self.关闭战报
                print("⚡️战报已关闭\n" if self.关闭战报 else "⚡️战报已开启\n")  
                continue
            elif answer.lower()=="f":
                self.关闭连暴反=not self.关闭连暴反
                print("⚡️连暴反已关闭\n" if self.关闭连暴反 else "⚡️连暴反已开启\n")
                continue
                
            try:场次=int(answer)
            except:
                print("❌场数必须是整数\n")
                continue
            if 场次<1:
                print("❌场数不能小于1\n")
                continue
            break
            
        print("\033[32;40m",end="")
        print(f"\n---《再来{场次}场（火力全开）》---")
        print("\033[0m")
        
        if 场次>3:
            prompt=["❓场次过多(每次最多支持连续3场战况显示(已",
            	"\x1b[7m", 
            	f"第{self.第几场}场",
            	"\033[0m",
            	"))强制关闭战报，是否允许？",
            	"(如果不允许，则强制关闭场次)\n(Enter(推荐):强制关闭战报 |否:强制关闭场次)\n"]
            prompt="".join(prompt)
            answer=input(prompt)
            if not answer:self.关闭战报=True
            else:场次=0
        for i in range(场次):
            self.战况报告()
        
        self.记者召开发布会(f"这{场次}场")

    # --- 每到下一场刷新删档 ---
    def 整场数据重置(self):
        self.本场结束=False
        self.谁胜=None
        self.第几回合=0
        左=copy.copy(self.存档_左)
        右=copy.copy(self.存档_左.对手)
        self.设置双方(左, 右)
        for _ in (self.左, self.左.对手):
            _.记者.本场将敌人压到最低血线=0
            _.记者.本场触发暴击=_.记者.本场触发连击=_.记者.本场触发反击=0
        
        '''
        self.本场结束=False      
        此方.已触发暴击=此方.已触发连击=此方.已触发反击=False
        此方.记者.本场将敌人压到最低血线=0
        self.谁胜=None
        self.第几回合=0
        此方.剩余血量=此方.血
        此方.暴伤系数=2
        此方.记者.最近一场有效吸血率历史记录.clear()
        此方.记者.最近一场有效连击率历史记录.clear()
        此方.记者.最近一场有效暴击率历史记录.clear()
        此方.需要失去几次行动=0
        此方.记者.本场触发暴击=此方.记者.本场触发连击=此方.记者.本场触发反击=0
        '''
            
    def 回合开始(self):
        self.第几回合+=1
        if not self.关闭战报:print(f"第{self.第几回合}回合\n~~~~~~")
    
    def 显示该回合战斗结果(self):
        words=[]
        word="%s%g(%.2f%%)"
        for _ in (self.左, self.左.对手):
            words.append(word%(_.名称, _.剩余血量, _.已掉血量百分比))
            
        print("（目前剩余血量："," VS ".join(words), "）", sep="")
        
        
        if not any([_.神通功能开启 for _ in (self.左, self.左.对手)]):
            return
        words=[]
        word="%s%g(%.2f%%)"
        
        for _ in (self.左, self.左.对手):
            words.append(word%(_.名称, _.妖气))
                     
        print("（目前妖气："," VS ".join(words),"）", sep="")
        
                
    def 战况报告(self):
        self.第几场+=1
        if not self.关闭战报:
            print("\x1b[7m",end="")
            print(f"\n\t《战场：准确战况报告》之第{self.第几场}场\t",end="")
            print("\033[0m")
        self.整场数据重置()
        
        if not self.关闭战报:print("\n📝\n---《进入战斗》---\n")
        for i in range(self.最大回合数):
            self.回合开始()
            self.分出先后手方()
            try:
                self.先手方.轮序到灵兽()
                self.先手方.对手.轮序到灵兽()
                self.先手方.轮序到人物()
                self.先手方.对手.轮序到人物()
            except Exception as e:
                if not isinstance(e,FightEnd):
                    traceback.print_exc()
                    sys.exit(1)
                else:
                    if not self.关闭战报:
                        print(type(e).__name__,e.__str__(),sep=":")     
                    self.本场结束=True
                    break
            if not self.关闭战报:self.显示该回合战斗结果()
            
            # 本场结束：回合数完了还打不完
            if i+1==self.最大回合数 and not self.谁胜:
                self.本场结束=True
                if not self.关闭战报:print("\n(回合数打完仍未决出胜负)")
            if not self.关闭战报:print()
            self.先手方.时刻="回合结束时"
            self.先手方.对手.时刻="回合结束时"
            
            
                     
            
