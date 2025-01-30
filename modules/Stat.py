class Stat():
    def __init__(self):
        self.选手=None
        self.本场触发连击=0
        self.本场触发暴击=0
        self.本场触发反击=0
        self.累计触发连击=0
        self.累计触发暴击=0
        self.累计触发反击=0
        self.获胜次数=0
        self.参赛次数=0
        self.最近一场有效吸血率历史记录=[]        
        self.最近一场有效连击率历史记录=[]
        self.最近一场有效暴击率历史记录=[]
        self._本场将敌人压到最低血线=0
        self.历史将敌人压到最低血线=dict(zip(["数值","那一场附带信息"],[0,""]))
        self.第一次使敌人掉一管血=""
        self.平局次数=0
        

    @property
    def 本场将敌人压到最低血线(self):return self._本场将敌人压到最低血线
    
    @本场将敌人压到最低血线.setter
    def 本场将敌人压到最低血线(self,value):
        self._本场将敌人压到最低血线=value
        
        if value > self.历史将敌人压到最低血线["数值"]:
            self.历史将敌人压到最低血线["那一场附带信息"]=\
f"(那一场：连击{self.本场触发连击}次，暴击{self.本场触发暴击}次，"+\
f"反击{self.本场触发反击}次，"+\
f"出现在第{self.选手.战场.第几场}场)"

            if self.历史将敌人压到最低血线["数值"] < 100 <= value:
                self.第一次使敌人掉一管血=("第一次打掉敌人100%以上血是在"+self.历史将敌人压到最低血线["那一场附带信息"][1:-1]).join("()")
         
            self.历史将敌人压到最低血线["数值"]=value


    @property    	
    def 胜率(self):
        if (self.参赛次数==0):
            raise ZeroDivisionError("❌除数不能为0")
        return self.获胜次数/self.参赛次数
    

    
    def 发布会(self):
        if self.选手.战场.谁胜==self.选手:
            print(f"【{self.选手.名称}本场胜】")                    
        print(f"{self.选手.名称}参赛{self.参赛次数}次")
        print(f"{self.选手.名称}本场触发连击{self.本场触发连击}次(反击{self.本场触发反击}次)")
        print(f"{self.选手.名称}本场触发暴击{self.本场触发暴击}次")
        print(f"{self.选手.名称}累计触发连击{self.累计触发连击}次(反击{self.累计触发反击}次)")
        print(f"{self.选手.名称}累计触发暴击{self.累计触发暴击}次")
        
        print(f"{self.选手.名称}最近一场有效吸血率历史记录:{self.最近一场有效吸血率历史记录}")
        print(f"{self.选手.名称}最近一场有效连击率历史记录:{self.最近一场有效连击率历史记录}")
        print(f"{self.选手.名称}最近一场有效暴击率历史记录:{self.最近一场有效暴击率历史记录}")
        print(f"{self.选手.名称}本场将敌人压到最低血线:%.2f%%"%self.本场将敌人压到最低血线)
        print(f"{self.选手.名称}历史将敌人压到最低血线:%.2f%%"%self.历史将敌人压到最低血线['数值'])
        print(self.历史将敌人压到最低血线["那一场附带信息"])
        if self.第一次使敌人掉一管血:print(self.第一次使敌人掉一管血)
        print(f"{self.选手.名称}获胜{self.获胜次数}次")
        if self.平局次数>0:
            print(f"双方平局{self.平局次数}次")        
        print(f"{self.选手.名称}胜率{self.胜率*100:g}%")


        
