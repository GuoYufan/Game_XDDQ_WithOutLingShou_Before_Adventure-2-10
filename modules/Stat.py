class Stat():
    def __init__(self):
        self._选手=None
        self.本场触发连击=0
        self.本场触发暴击=0
        self.累计触发连击=0
        self.累计触发暴击=0
        self.获胜次数=0
        self.参赛次数=0
        self.最近一场有效吸血率历史记录=[]        
        self.最近一场有效连击率历史记录=[]
        self.最近一场有效暴击率历史记录=[]
        self.历史将敌人压到最低血线=dict(zip(["数值","那一场附带信息"],[0,""]))
        self.第一次使敌人掉一管血=""
        
    @property    	
    def 胜率(self):
        if (self.参赛次数==0):
            raise ZeroDivisionError("除数不能为0")
        return self.获胜次数/self.参赛次数
    
    def 发布会(self):
        print(f"{self.选手.名称}参赛{self.参赛次数}次")
        print(f"{self.选手.名称}本场触发连击{self.本场触发连击}次")
        print(f"{self.选手.名称}本场触发暴击{self.本场触发暴击}次")
        print(f"{self.选手.名称}累计触发连击{self.累计触发连击}次")
        print(f"{self.选手.名称}累计触发暴击{self.累计触发暴击}次")
        print(f"{self.选手.名称}最近一场有效吸血率历史记录:{self.最近一场有效吸血率历史记录}")
        print(f"{self.选手.名称}最近一场有效连击率历史记录:{self.最近一场有效连击率历史记录}")
        print(f"{self.选手.名称}最近一场有效暴击率历史记录:{self.最近一场有效暴击率历史记录}")
        print(f"{self.选手.名称}历史将敌人压到最低血线:%.2f%%"%(self.历史将敌人压到最低血线['数值']))
        print(self.历史将敌人压到最低血线["那一场附带信息"])
        if self.第一次使敌人掉一管血:print(self.第一次使敌人掉一管血)
        print(f"{self.选手.名称}获胜{self.获胜次数}次")
        print(f"{self.选手.名称}胜率{self.胜率*100:g}%")

        
