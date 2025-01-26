class Beast():
    def __init__(self,name,improve):
        self.名称=name
        self.属性提升=improve
    def be_worn(self, 面板):
        self.面板=面板
        
def format_g(value):
    formatted_string=f"{value:g}"
    return float(formatted_string)
    
class Equip():
    def __init__(self,wear):    
        self.先穿, self.后穿=wear
        self.基值=0
        
    def show(self):
        self.to_be_taken_off()
        两者名=self.先穿.名称, self.后穿.名称
        两者属性提升=self.先穿.属性提升, self.后穿.属性提升
        两者面板=self.先穿.面板, self.后穿.面板

        '''
        print(f"%s的属性提升为%g,穿上%s后的面板值为%g"%(
        两者名[0],两者属性提升[0],两者名[0],两者面板[0]))
        	
        print(f"%s的属性提升为%g,穿上%s后的面板值为%g"%(
        两者名[1],两者属性提升[1],两者名[1],两者面板[1]))
        '''
        prompt="◾️%s的属性提升为%g,穿上%s后的面板值为%g"
        [print(prompt%(两者名[i],两者属性提升[i],两者名[i],两者面板[i])) for i in range(2)]
        	
        print("⚡️由两者得出基值为:",self.基值)
        	
        prompt="◾️x*(1+%g+n)=%g"
        [print(prompt%(两者属性提升[i],两者面板[i])) for i in range(2)]
        	
        print(f"⚡️其中x为基值,x为{self.基值}")
        print(f"⚡️n为{self.剩余全部属性提升_先}或{self.剩余全部属性提升_后}")
        print("⚡️x*(1+n)=%g"%(self.基值*(1+self.剩余全部属性提升_先)))
        
    def ask(self):
        while True:
            answer=input("\n❓请输入要换上的属性提升:\n")
            try:change_into=float(answer)
            except:
                print("❌必须为数字\n")
                continue
            break
        print("换上后面板为:%g"%(self.基值*(1+self.剩余全部属性提升_先+change_into)))
        
        	
    def to_be_taken_off(self):
        self.基值=(self.先穿.面板-self.后穿.面板)/(self.先穿.属性提升-self.后穿.属性提升)
        self.基值=eval(f"{self.基值:g}")
        
        self.剩余全部属性提升_先=self.先穿.面板/self.基值-self.先穿.属性提升-1
        self.剩余全部属性提升_后=self.后穿.面板/self.基值-self.后穿.属性提升-1
        
        self.剩余全部属性提升_先=format_g(self.剩余全部属性提升_先)
        self.剩余全部属性提升_后=format_g(self.剩余全部属性提升_后)



def test():
    # 依次为：血/攻/防
    面板_鸾鸟=(19469,3004,479)
    面板_天马=(18176,2809,446)
    
    先=Beast("鸾鸟",0.17)    
    后=Beast("天马",0.09)
    equip=Equip((先, 后))
    
    for i in range(3):
        print("\n📝")
        先.be_worn(面板_鸾鸟[i])
        后.be_worn(面板_天马[i])
        equip.show()
        input()
    
    [print(":".join(i)) for i in zip("012","血攻防")] 
    while True:
        answer=input("\n❓请对哪一组进行换?(Q/q:退出)(可选:0~2)\n\t")        
        if answer.lower()=="q":break
        try:selected=int(answer)
        except:
            print("❌序号必须是数字\n")
            continue
        if not 0<= selected <3:
            print("❌不在可选序号(0~2)内\n")
            continue
        
        先.be_worn(面板_鸾鸟[selected])
        后.be_worn(面板_天马[selected])
        equip.to_be_taken_off()
    
        while True:
            equip.ask()
            if input("\n#Q/q to quit:").lower()=="q":break
        
    


if __name__=="__main__":
    test()

# updated:2025.1.26 21:43
# 《穿换任意两件来计算基值》
# 测试通过，作为第一个可用版本。
