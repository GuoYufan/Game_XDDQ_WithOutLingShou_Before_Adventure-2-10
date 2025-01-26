class Buff():
    def __init__(self, name, role, gain, duration):
        # 累计触发了几次
        self.time=0
        # 名称：攻 或 连
        self.name = name
        # 角色：从属于哪个角色
        self.role = role
        # 增益效果
        self.gain = gain
        # 持续回合数
        self.duration = duration
        # 是否激活
        self.active = False
        
    # 生效 / 应用效果
    def apply(self):
        if not self.active:
            if self.name=="攻":
                self.role.攻 += self.gain *self.role.攻
                self.role.攻 = int(self.role.攻)
            elif self.name=="连":
                self.role.连 += self.gain
            elif self.name=="减伤":
            	self.role.减伤 += self.gain
            self.active = True

    # 刷新持续回合数
    def refresh(self,d):
        self.duration = d
        
    # 剩余回合数减少
    def decrement(self):
        if self.active:
            self.duration -= 1
            if self.duration <= 0: pass
    
    # 触发效果          
    def activate(self, n, m, d):
        self.time+=1
        self.name = n
        self.gain = m        
        self.apply()
        self.refresh(d)
        self.active = True
    
    # 是否从激活到失效         
    def is_deactivated(self):
        return self.time>0 and self.active==True and self.duration==0
    
    
    # 当从激活到失效时
    def deactivate(self):
        if self.name=="攻":
            self.role.攻-=self.gain*self.role.攻
            self.role.攻=int(self.role.攻)
        elif self.name=="连":
            self.role.连-=self.gain
        elif self.name=="减伤":
        	self.role.减伤-=self.gain
        self.active=False
            