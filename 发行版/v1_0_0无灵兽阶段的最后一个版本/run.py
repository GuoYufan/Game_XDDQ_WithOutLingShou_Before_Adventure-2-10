from Role import Role
from Fight import Fight


def main():
    # 胜率8%
    我=Role([12695,1877,308,500],"我")
    敌=Role([14445,2080,416,631],"敌")
    战场=Fight(我,敌)
    
    我.现阶段=敌.现阶段="筑基"
    
    
    def 双方信息设置(对手类型="冒险怪"):
        nonlocal 我
        if 对手类型=="冒险怪":
            我.对手.设置战斗抗性(2.6,"抗暴",7.8)
            我.对手.设置战斗属性(1)
            
        我.设置战斗抗性(12)
        我.吸=5.3
        我.连=16
        我.暴=13.4
        
    
    双方信息设置()
    战场.展示双方战前面板信息()
    战场.模糊战况报告()
    战场.记者重新入场()
    战场.第一场()
    # 战场.关闭战报=True    
    while True:
        if 战场.再来多少场()=="quit":break

    

 
if __name__=="__main__":main()

# 2025.1.18
# 《重写》v0.1.0

# 2025.1.23
# 《寻道大千：从为了专用于新号无灵兽阶段开始写的战况报告》v0.1.1

# updated:2025.1.23 13:58
# 基本测试通过，达到第一个可用版本，结束了初步开发的阶段
# 《寻道大千：从为了专用于新号无灵兽阶段开始写的战况报告》v1.0.0

