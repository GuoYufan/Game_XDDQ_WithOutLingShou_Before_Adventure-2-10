import os,sys

here=__file__
for _ in range(1):
    here=os.path.dirname(here)
sys.path.append(
os.sep.join((here,"modules"))
)
del os,sys

import math
from Role import Role
from Fight import Fight
from 对手模板 import *
from 转换器about灵兽信息 import Convert
from 穿换任意两件来计算基值 import Beast, Equip


def 找到面板基值(attr):
    temp=dict(zip("血攻防",range(3)))
    #面板_鸾鸟=(19469,3004,479)
    #面板_天马=(18176,2809,446)
    
    面板_鸾鸟=(20962,3205,514)
    面板_天马=(19570,2996,479)
    
    先=Beast("鸾鸟",0.17)    
    后=Beast("天马",0.09)
    equip=Equip((先, 后))


    先.be_worn(面板_鸾鸟[temp[attr]])
    后.be_worn(面板_天马[temp[attr]])
    equip.to_be_taken_off()
    
    return equip.基值, equip.剩余全部属性提升_先
    
    
	
# 我.灵兽.下阵()
# 我.灵兽.上阵()
def 下阵灵兽(我, 可选主灵兽, 改属性提升吗):    
    if 改属性提升吗:
        收集 = []
        for attr in "血攻防":
            收集.append(找到面板基值(attr))
        input(f"{收集}\n😋\n")
        
        面板 = 我.获取基本属性()[:-1]
        新面板 = []        
        improve = 可选主灵兽["属性提升"][我.主灵兽名称]
        for i in range(3):
            该项基础属性的基值 = 收集[i][0]
            削弱值 = 该项基础属性的基值 * improve
            新面板.append( 面板[i] - 削弱值 )
       
        我.血, 我.攻, 我.防 = 新面板
        #input(新面板)
    我.主灵兽名称=""

    
def 上阵灵兽(我, 可选主灵兽, 改属性提升吗):
    if 改属性提升吗:
        收集 = []
        for attr in "血攻防":
            收集.append(找到面板基值(attr))
        
        面板 = 我.获取基本属性()[:-1]
        新面板 = []
        improve = 可选主灵兽["属性提升"][我.主灵兽名称]
        for i in range(3):
            该项基础属性的基值 = 收集[i][0]
            加强值 = 该项基础属性的基值 * improve
            新面板.append( 面板[i] + 加强值 )
   
        我.血, 我.攻, 我.防 = 新面板
        #input(新面板)

    我.主灵兽出手频率=可选主灵兽["出手频率"][我.主灵兽名称]
    try:
        我.主灵兽伤倍率_乘在攻=可选主灵兽["伤倍率_乘在攻"][我.主灵兽名称]
    except KeyError:pass
    try: 
        我.主灵兽治疗倍率_乘在攻=可选主灵兽["治疗倍率_乘在攻"][我.主灵兽名称]
    except KeyError:pass
    


def 使所有灵兽升级到消耗相同灵果(level, name,可选主灵兽, only_first_one=False):    
    convert=Convert(level, name)
    可选主灵兽=convert.copy(可选主灵兽)
    
    #convert.show()
    
    if only_first_one:return 可选主灵兽
    
    其他所有灵兽=[pending_name for pending_name in 可选主灵兽["属性提升"] if not pending_name==name]
    其他所有灵兽对应等级库=dict()
    
    for targer_name in 其他所有灵兽:
        convert.设置要转换到的灵兽叫什么名称(targer_name)
        其他所有灵兽对应等级库[targer_name]=int(convert.获取等级(targer_name))
       
    for pending_name,pending_level in 其他所有灵兽对应等级库.items():
        convert.__init__(pending_level, pending_name)
        #convert.show()
        #input()
        可选主灵兽=convert.copy(可选主灵兽)
    
    #input(可选主灵兽)
    return 可选主灵兽





def run():
    我=Role([20962,3205,514,718],"我")
    我.主灵兽名称=("鸾鸟","天马")[0]
    敌=Role([63298,2745,913,946],"敌")
    战场=Fight(我,敌)
        
    我.现阶段=敌.现阶段="金丹"
    
    def 双方信息设置(对手类型="冒险怪"):
        nonlocal 我
        if 对手类型=="冒险怪":
            我.对手.设置战斗抗性(7.1,"抗连",19.3)
            我.对手.设置战斗属性(3.4,"连",10.2)
        elif 对手类型=="斗法":
            '''
            伤11.14%对14.69%。鸟治疗14.98%。
            9回合对7回合。
            还要考虑灵兽伤害。帝江伤害17.74%。
            算出来在第6回合他先手灵兽帝江打死我。
            我人物只能行动5回合。
            所以9回合对5回合。
            
            
            鸟把5回合拖到9回合。
            第9回合他先手人物打死我。
            我人物只能行动8回合。
            14.69%*8+17.74%*2-14.98%*4=93.08%
            
            93.08%+14.69%=107.77%
            
            这还没考虑鸾鸟减伤。
            他先手灵兽不被减。
            在第2、4、6、8回合（共4个回合，与鸾鸟出手次数一致）人物被减。
            每次减2.2035%。
            14.69%×9+17.74%×2−14.98%×4−2.2035%×4=98.956%。
            
            
            第9回合我还没死。我能行动。
            算了就当8回合。
            
            
            8*11.14%=89.12%
            	
            	
            无连暴的情况下，我打不死他，我必输。
            我第9回合输，只行动8回合。
                        
            
            他17%击晕率晕1.53次每8回合。
            他在第3、6回合37%击晕率。
            晕2.96次每8回合。
            
            2*0.37+1.53=0.74+1.53=2.27
            
            他能把我伤害减少2~3次。
            
            算作2次
            
            
            8*11.14%-2*11.14%=66.84%。
            我6次行动机会。
            
            我需要连暴反3~4次才有机会必胜。
            
            我的连暴反概率(26+6+8)%=40%
            	
            6次机会40%得2.4次。
            
            2.4次距离3~4次为80%~60%。
            
            所以我的胜率66%~50%。
            
            
            自动战斗模拟（没考虑击晕）：
            鸾鸟胜率：96%
            天马胜率：36.2%
（无连暴68.24%血线5回合行动。
第一次打掉一管血在第4场，5回合连暴反4次=需要概率80%。
理想胜率=1/4=25%。）
            灵狐胜率：20.75%
（无连暴66.83%血线5回合行动。
第一次打掉一管血在第4场，5回合连暴反4次=需要概率80%。
理想胜率=1/4=25%。）
            
            
            用增加血量的方式来考虑他的击晕：          
            因为击晕实际上是不仅减少伤害且减少行动机会。
            而减少伤害对应的是增加血量。
            减少行动机会对应的是战斗属性的概率触发。
            因为击晕不会增加伤害。
            '''
            我.对手.设置战斗抗性(3,"抗吸",3)
            我.对手.连=12.7
            我.对手.吸=0
            我.对手.暴=0
            我.对手.血=23562
            我.对手.攻=3593
            我.对手.防=590
            我.对手.敏=913
            我.对手.主灵兽名称="帝江"
            我.对手.主灵兽伤倍率_乘在攻=1.035
            我.对手.主灵兽出手频率=3
            
    def 帮助是否换装备之决策(n):
        nonlocal 我
        我.吸+=(-3.8,0)[n]
        我.暴+=(-2.5,0)[n]
        我.连+=(-1.3,0)[n-1]
        我.血+=(300)+3000
        我.攻+=(2,0)[n]+500
        我.防+=(1,0)[n]+70
        
                    
    我.设置战斗抗性(12)
    我.吸=0
    我.连=29+(0,0)[0]
    我.暴=8.6
    我.增伤=0.004
    双方信息设置("斗法")
    
    #帮助是否换装备之决策(1)
    
    
    可选主灵兽={"属性提升":{"灵狐":0.05, "天马":0.09,"鸾鸟":0.12},
        "出手频率":{"灵狐":3, "天马":3, "鸾鸟":2},
        "伤倍率_乘在攻":{"灵狐":0.6, "天马":eval(f"{0.9:g}")},
        "治疗倍率_乘在攻":{"鸾鸟":0.85},
        }    
    
    
    # 会根据主灵兽的情况去转换到其他灵兽相同灵果消耗的情况
    # 之前未支持转换到的：参战技能倍率 现已支持
    # 已支持转换到相同灵果的：等级、属性提升、参战技能倍率
    可选主灵兽=使所有灵兽升级到消耗相同灵果(21,"鸾鸟",可选主灵兽)
    input(f"{可选主灵兽}\n😋\n")
    
    是否改属性提升 = True
    
    # 下阵灵兽
    下阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    # 上阵灵兽
    我.主灵兽名称=("灵狐","天马","鸾鸟")[-1]
    #可选主灵兽["属性提升"][我.主灵兽名称]=0.162    
    上阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    # --- O N / O F F
    # 主灵兽的参战技能和效果的开关
    #我.主灵兽名称=""
    
    # --- O N / O F F
    # 对是否支持buff功能的开关(默认开。用去注释关）
    #我.buff_ON=False
           
    # 是否使用对手模板？
    #战场=冒险怪3_5()
    
    # --- 开 始 进 入 战 斗 ---
    战场.展示双方战前面板信息()
    战场.模糊战况报告()
    战场.记者重新入场()
    战场.第一场()
    战场.记者重新入场()
    while True:
        # 设置是否关闭连暴
        # 如果关闭连暴，可以看到每一场都是一模一样的。
        # 如果第一场输，再打499场也是0%胜率。
        if 战场.再来多少场()=="quit":break

    

 
if __name__=="__main__":run()

# 2025.1.18
# 《重写》v0.1.0

# 2025.1.23
# 《寻道大千：从为了专用于新号无灵兽阶段开始写的战况报告》v0.1.1

# updated:2025.1.23 13:58
# 基本测试通过，达到第一个可用版本，结束了初步开发的阶段
# 《寻道大千：从为了专用于新号无灵兽阶段开始写的战况报告》v1.0.0

# updated:2025.1.23 17:33
# v1.1.0-alpha
# 开始加入灵兽

# updated:2025.1.23 18:30
# 初步测试通过了
# 升级到v1.1.0-beta
# note:2025.1.23 18:45
# 精准测试度过冒险怪3-5至3-6两个关卡


# updated:2025.1.25
# v1.2.0-beta.1
# 用10回合连暴3相较于8回合连暴5、5回合连暴5的优势精准度过冒险怪3-7-1
