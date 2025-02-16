import traceback, sys, math

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
        
    def 设置双方(self,左,右):
        self.左=左
        self.左.对手=右
        self.左.对手.对手=左
        self.左.战场=self.左.对手.战场=self
                
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
            print("血:%s 攻:%s 防:%s 敏:%s"%(_.血, _.攻, _.防, _.敏))
        print()
        
        
        print("[%s神通%s|%s神通%s]"%(
            	self.左.名称,
            	",".join(self.左.携带神通),
            	self.左.对手.名称,
        	    ",".join(self.左.对手.携带神通)
            	)
          	)
        print("[%s吸血率%g%%,连击率%g%%,暴击率%g%%]"%(
            	self.左.名称,
             self.左.吸-self.左.对手.抗吸,
             self.左.连-self.左.对手.抗连,
             self.左.暴-self.左.对手.抗暴,
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
        self.分出先后手方()
        [_.计算单方面板() for _ in (self.先手方,self.先手方.对手)]
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
        print(f"我打敌一下有视防御伤：{self.左.面板_有视防御伤}")
        print(f"敌打我一下有视防御伤：{self.左.对手.面板_有视防御伤}")
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
        self.左.记者.__init__()
        self.左.对手.记者.__init__()
        self.左.记者.选手=self.左
        self.左.对手.记者.选手=self.左.对手


    # --- 媒 体 活 动 与 赛 程 安 排 ---
    
    def 记者召开发布会(self,第几场):
        print("\033[32;40m",end="")
        print(f"\n---《针对{第几场}记者召开发布会》---")
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
            answer=input("再来多少场？(输入Q/q退出):")
            if answer.lower()=="q":
                return "quit"
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
        
        if self.第几场+场次>5:
            answer=input(f"❓场次过多(最多支持最近5场战况显示(已第{self.第几场}场))，强制关闭战报，是否允许？(如果不允许，则强制关闭场次)\n(默认:是(Enter:默认))\n")
            if not answer:self.关闭战报=True
            else:场次=0
        for i in range(场次):
            self.战况报告()
        self.记者召开发布会(f"这{场次}场")
        input()

    # --- 每到下一场刷新删档 ---
    def 整场数据重置(self,此方):
        self.第几回合=0
        此方.剩余血量=此方.血
        此方.暴伤系数=2
        此方.记者.最近一场有效吸血率历史记录.clear()
        此方.记者.最近一场有效连击率历史记录.clear()
        此方.记者.最近一场有效暴击率历史记录.clear()
        此方.需要失去几次行动=0
            
    def 回合开始(self):
        self.第几回合+=1
        if not self.关闭战报:print(f"第{self.第几回合}回合\n~~~~~~")
    
                
    def 战况报告(self):
        if not self.关闭战报:
            print("\x1b[7m",end="")
            print("\n\t《战场：准确战况报告》\t",end="")
            print("\033[0m")
        [self.整场数据重置(i) for i in (self.左, self.左.对手)]
        
        左=self.左
        if not self.关闭战报:print("\n📝\n---《进入战斗》---\n")
        for i in range(15):
            self.回合开始()
            self.分出先后手方()
            for 此方 in (self.先手方, self.先手方.对手):
                try:此方.轮序到人物()
                except Exception as e:
                    if not isinstance(e,FightEnd):
                        traceback.print_exc()
                        sys.exit(1)
                    else:
                        if not self.关闭战报:
                            print(type(e).__name__,e.__str__(),sep=":")                        
                        [_.记者的变化() for _ in (此方,此方.对手)]
                        self.第几场+=1                    
                    return
                if not self.关闭战报:print("（目前剩余血量：%s%g(%.2f%%) VS %s%g(%.2f%%)）"%(\
                         左.名称, 左.剩余血量, 左.已掉血量百分比,
                     
                         左.对手.名称, 左.对手.剩余血量, 左.对手.已掉血量百分比
                         )
                     )
                if self.左.神通功能开启 and not self.关闭战报:
                    print("（目前妖气：%s%g VS %s%g）"%(\
                    	    左.名称,左.妖气,\
                    	    左.对手.名称,左.对手.妖气))
                if not self.关闭战报:print()       
            
