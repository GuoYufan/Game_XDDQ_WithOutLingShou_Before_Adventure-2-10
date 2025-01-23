import math,random

# --- 战斗类 ---
class Fight():
    def __init__(self,我方,对方):
        self.我方=我方
        self.对方=对方
        self.先手方=self.后手方=None
        self.谁胜=str()
        self.第几回合=0
        self.最近一场结束时进行到第几回合=list()
        self.易得=False
        self.去除连击=self.去除暴击=False
        self.被选中的那个回合=0
        self.击晕行动=self.连击行动=False
        self.被晕方=None
        self.彩排=False
        
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
        [self.计算单方(i) for i in (self.先手方,self.后手方)]
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
    
    # --- 模 糊 战 况 ---
    	
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
        
        def 是否需要对策():
            nonlocal self
            return self.谁胜=="敌"
            
        def 提供对策():
            nonlocal self
            
            几个回合结束=min(self.我方.打对方实际回合数_白板,self.对方.打对方实际回合数_白板)
            我已行动了几个回合=几个回合结束-(1 if self.先手方==self.对方 else 0)
            我已造成掉血百分比=self.我方.有视防御伤百分比*我已行动了几个回合
            对策_需要进行多少次连击=(1-我已造成掉血百分比)/self.我方.有视防御伤百分比
          
            print(f"对策：需要进行{对策_需要进行多少次连击}次连击")
            print(f"对策：平均每回合进行{对策_需要进行多少次连击/几个回合结束}次连击)")
        
        if 是否需要对策():提供对策()
        
    # --- 准 确 战 况 ---
    
    def 获取彼方(self,此方):
        return self.后手方 if 此方==self.先手方 else self.先手方   
        
    def 受伤(self,此方,本次掉血多少):
        此方.剩余血量-=本次掉血多少
        
        
    def 每次轮序数据重置(self,此方,彼方):
        此方.本次回血=彼方.本次回血=此方.本次伤害=彼方.本次伤害=0
    
    # --- 同一对手连续打多场存档 ---
    def 记者重新入场(self):
        self.我方.记者.__init__()
        self.我方.记者.名称="我"
        self.对方.记者.__init__()
        self.对方.记者.名称="敌"
        self.最近一场结束时进行到第几回合.clear()

    
    # --- 每到下一场刷新删档 ---
    def 整场数据重置(self,此方):
        self.第几回合=0
        此方.剩余血量=此方.血
        此方.暴伤系数=2
        此方.记者.最近一场有效吸血率历史记录.clear()
        此方.记者.最近一场有效连击率历史记录.clear()
        此方.记者.最近一场有效暴击率历史记录.clear()
        此方.需要失去几次行动=0
        
        
    def 造成本次治疗之吸血(self,此方):
        此方.吸血回血量=0 if 此方.战斗属性之有效吸血率<=0 else int(此方.本次伤害*此方.战斗属性之有效吸血率)
        此方.本次回血=此方.吸血回血量 if 此方.已掉血量>=此方.吸血回血量 else 此方.已掉血量
        此方.剩余血量+=此方.本次回血
  
    def 每次轮序必要的计算(self,此方,彼方):
        此方.战斗属性之有效吸血率=(此方.战斗属性之吸血-彼方.战斗抗性之抗吸)/100
        if not 此方.强制连击率吗:此方.战斗属性之有效连击率=(此方.战斗属性之连击-彼方.战斗抗性之抗连)*1.5/100
        此方.战斗属性之有效暴击率=(此方.战斗属性之暴击-彼方.战斗抗性之抗暴)*2/100
        
        此方.记者.最近一场有效吸血率历史记录.append(f"{round(此方.战斗属性之有效吸血率*100,2)}%")
        此方.记者.最近一场有效连击率历史记录.append(f"{round(此方.战斗属性之有效连击率*100,2)}%")
        此方.记者.最近一场有效暴击率历史记录.append(f"{round(此方.战斗属性之有效暴击率*100,2)}%")
        
        
    def 进行普攻(self,此方,彼方):
        此方.本次伤害=此方.有视防御伤=此方.攻-彼方.防
        
        
    # --- 轮序到人物 ---    
    def 轮序到人物(self,此方):
        彼方=self.获取彼方(此方)
        self.每次轮序数据重置(此方,彼方)
        self.每次轮序必要的计算(此方,彼方)
        #self.每次轮序相应面板报告()
        #input(此方.__dict__)
        #input(彼方.__dict__)
        
        if self.击晕行动:
            # 下次轮序到，检查被晕状态的恢复
            if self.第几回合>=self.被选中的那个回合:
                if not 此方.可行动:
                    self.被晕方=此方
                    此方.需要失去几次行动-=1
                    return
                elif 此方==self.被晕方:
                    print(f"✅被晕方即{self.被晕方.名称}方，已解除晕眩，宣告击晕行动完成。")
                    self.击晕行动=False
                    
            # 使在随机一回合被击晕一次，失去一次行动后下次恢复行动       
            if self.第几回合==self.被选中的那个回合 and 此方==self.我方:
                if 彼方.需要失去几次行动>0:
                    print(f"❌当前轮序到的<{此方.名称}方>的对手<{彼方.名称}方>不可被击晕")
                else:
                    彼方.需要失去几次行动+=1
                    print(f"❗️当前轮序到的<{此方.名称}方>把对手<{彼方.名称}方>击晕在第{self.第几回合}回合")

        self.进行普攻(此方,彼方)
        
        if self.去除连击:此方.战斗属性之有效连击率=0
        if self.去除暴击:此方.战斗属性之有效暴击率=0
        
        if self.连击行动 and self.第几回合==self.被选中的那个回合 and 此方==self.我方:
            此方.本次伤害+=此方.有视防御伤
            print(f"❗️连击行动于第{self.第几回合}回合完成")
            self.连击行动=False
            self.受伤(彼方,此方.本次伤害)
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
                if random.randint(0,100)<=此方.战斗属性之有效暴击率*100:
                    if not self.易得:print(f"❗️触发暴击,暴伤系数{此方.暴伤系数}")
                    此方.本次伤害+=此方.有视防御伤*此方.暴伤系数
                    此方.触发了暴击()
                else:此方.本次伤害+=此方.有视防御伤
                
        self.受伤(彼方,此方.本次伤害)

    def 分出胜负(self):
        if self.先手方.剩余血量<=0:
            self.谁胜=self.后手方.名称
            return True
        elif self.后手方.剩余血量<=0:
            self.谁胜=self.先手方.名称
            return True
        return False
        
    def 记者的变化(self,此方):         
        if self.谁胜==此方.名称:
            此方.记者.获胜次数+=1
        此方.记者.参赛次数+=1
     
        
    # --- 战 况 报 告 ---
    	
    def 准确战况报告(self):
        # --- 重置上一场双方需要重置的数据 ---
        [self.整场数据重置(i) for i in (self.我方,self.对方)]
        
        # --- 提示这是第几场 ---
        #print(f"第{self.我方.记者.参赛次数+1}场")
        
        # --- 提示本场双方初始信息 ---
        if not self.易得:print("双方初始基础属性:\n{0} PK {1}".format(self.我方.基础属性列表,self.对方.基础属性列表))
        
        # --- 本场的第一回合开始 ---
        for i in range(15):
            self.第几回合=i+1
            # ---关于强制连击率的设置的生效 ---
            if self.我方.强制连击率吗:
                if self.第几回合<=self.我方.整场有多少回合强制连击率:
                    if self.第几回合==1:
                        if self.我方.强制连击率之第一回合是否可连击:
                            self.我方.战斗属性之有效连击率=100/100
                        else:self.我方.战斗属性之有效连击率=0
                    else:self.我方.战斗属性之有效连击率=100/100
                else:self.我方.战斗属性之有效连击率=0
            
            # --- 提示本场当前进行到第几回合 ---
            if not self.易得:print(f"\n第{self.第几回合}回合:")
            
            # --- 先手方和后手方轮流行动 ---
            for 此方 in (self.先手方,self.后手方):
                彼方=self.获取彼方(此方)
                if not self.易得:print(f"【{此方.名称}行动】",end="\t")
                self.轮序到人物(此方)
                
                # --- 提示双方掉血和治疗情况 ---
                if not self.易得:print("{0}(+{3:.2%}|{2:.2%})  {1}(+{5:.2%}|{4:.2%})".\
format(self.我方.剩余血量,self.对方.剩余血量,self.我方.已掉血量/self.我方.血,\
 	self.我方.本次回血/self.我方.血,self.对方.已掉血量/self.对方.血,	self.对方.本次回血/self.对方.血))
                此方.记者.更新历史将敌人压到最低血线(彼方.已掉血量/彼方.血)
                
                # --- 该回合能否分出胜负 ---
                if self.分出胜负():
                    if not self.易得:print(f"谁胜:{self.谁胜}")
                    self.最近一场结束时进行到第几回合.append(self.第几回合)
                    
                    [self.记者的变化(i) for i in (self.我方,self.对方)]
                    break
            else:continue
            break


    # --- 媒 体 活 动 与 赛 程 安 排 ---
    	
    def 记者召开发布会(self,第几场):
        print("\033[32;40m",end="")
        print(f"\n---《针对{第几场}记者召开发布会》---")
        print("\033[0m",end="")
        
        print("\033[1;34m")
        self.我方.记者.发布会()
        print("\x1b[31m")
        self.对方.记者.发布会()
        print("\033[0m")
        
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

        for i in range(场次):self.准确战况报告()
        input()
        self.记者召开发布会(f"这{场次}场")
        input()
    
    def 重新进行一百场(self):
        print("\033[32;40m",end="")
        print("\n---《重新进行一百场（火力全开）（清空原记者）》---")
        print("\033[0m")
        
        self.易得=True
        self.去除连击=self.去除暴击=False
        for i in range(100):self.准确战况报告()
        input()
        self.记者召开发布会("这一百场")
        input()
        
    def 第四场(self):
        print("\033[32;40m",end="")
        print("\n---《继续进行第四场（火力全开但强制必连或必不连）》---")
        print("\033[0m")
        
        self.易得=False
        self.去除暴击=True
        self.去除连击=False
        self.我方.强制连击率吗=True
        self.我方.整场有多少回合强制连击率=5
        self.我方.强制连击率之第一回合是否可连击=True
        self.准确战况报告()
        self.我方.强制连击率吗=False
        input()
        self.记者召开发布会("第四场")
        input()
        
    def 第三场(self):
        print("\033[32;40m",end="")
        print("\n---《继续进行第三场（连击一次）》---")
        print("\033[0m")
        
        self.易得=False
        self.连击行动=True
        self.被选中的那个回合=random.randint(1,min(self.最近一场结束时进行到第几回合))
        self.准确战况报告()
        input()
        self.记者召开发布会("第三场")
        input()
        
    def 第二场(self):
        print("\033[32;40m",end="")
        print("\n---《继续进行第二场（去除连击暴击+晕一次）》---")
        print("\033[0m")
        
        self.易得=False
        self.去除连击=self.去除暴击=True
        self.击晕行动=True
        self.被选中的那个回合=random.randint(1,min(self.最近一场结束时进行到第几回合))
        self.准确战况报告()
        self.击晕行动=False
        input()
        self.记者召开发布会("第二场")
        input()
        
        
    def 第一场(self):
        print("\033[32;40m",end="")
        print("\n---《进行第一场（去除连击暴击）》---")
        print("\033[0m")
        
        self.易得=False
        self.去除连击=self.去除暴击=True
        self.准确战况报告()
        input()
        self.记者召开发布会("第一场")
        input()


