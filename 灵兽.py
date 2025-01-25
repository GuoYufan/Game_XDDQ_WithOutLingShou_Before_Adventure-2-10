class Spirit_Fruit():
    def __init__(self,begin,step):
        self.初始升一级消耗=begin
        self.之后每升一级增加消耗=step
        self.升下一级需要消耗=0
        self.已消耗=0

class Game():
    def __init__(self):
        pass
        
    def add_beast(self,灵兽):
        self.灵兽=灵兽
        
    def click_beast_fruit(self):
        print(f"{self.灵兽.名称}已消耗灵果{self.灵兽.灵果.已消耗}")
    
    def click_beast_level(self):
        print(f"{self.灵兽.名称}等级为{self.灵兽.等级}级")
        
class Spirit_Beast():
    def __init__(self,name):
        self.名称=name
        self.灵果=Spirit_Fruit(100,100)
        self.等级=1
    
    def 升级(self):
        self.灵果.升下一级需要消耗+=self.灵果.之后每升一级增加消耗
        self.灵果.已消耗+=self.灵果.升下一级需要消耗            
        self.等级+=1
        
鸾鸟=Spirit_Beast("鸾鸟")
游戏=Game()
游戏.add_beast(鸾鸟)

for i in range(15):
    鸾鸟.升级()

    游戏.click_beast_fruit()
    游戏.click_beast_level()
    

        
        