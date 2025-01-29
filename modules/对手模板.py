from Role import Role
from Fight import Fight


'''
    # 《冒险怪：无尽荒原-3-16》
    # 连击率27.9%+暴击率4.4%。
    # 500场97%胜率其他全平局。稳过。
    # 我=Role([17691,2764,438,669],"我")
    # 我.主灵兽名称="鸾鸟"
    # 敌=Role([33718,2920,729,739],"敌")
'''
def 冒险怪_3_16():
    我=Role([17691,2764,438,669],"我")
    我.主灵兽名称="鸾鸟"
    敌=Role([33718,2920,729,739],"敌")
    战场=Fight(我,敌)
    
    我.现阶段=敌.现阶段="金丹"    
    
    def 双方信息设置(对手类型="冒险怪"):
        nonlocal 我
        if 对手类型=="冒险怪":
            我.对手.设置战斗抗性(5.6,"抗连",16.8)
            我.对手.设置战斗属性(2.5,"连",7.7)
        elif 对手类型=="斗法":
            我.对手.设置战斗抗性(12,"抗吸",40)
            我.对手.连=9.4
            我.对手.吸=16.6
            我.对手.暴=13.4+7.5
            我.对手.血=17944
            我.对手.攻=2745
            我.对手.防=458
            我.对手.敏=673
            我.对手.主灵兽名称="天马"
            我.对手.主灵兽伤倍率_乘在攻=0.9
            我.对手.主灵兽出手频率=3
            
    def 帮助是否换装备之决策(n):
        nonlocal 我
        我.吸+=(-3.8,0)[n]
        我.暴+=(-2.5,0)[n]
        我.连+=(-1.3,0)[n-1]
        我.血+=(300)
        我.攻+=(2,0)[n]
        我.防+=(1,0)[n]
        
    
    双方信息设置()                
    我.设置战斗抗性(12)
    我.吸=0
    我.连=24.7+20
    我.暴=10
    
    
    #帮助是否换装备之决策(1)
    
    
    可选主灵兽={"属性提升":{"灵狐":0.05, "天马":0.09,"鸾鸟":0.12+0.005*(14//2)+0.02*(14%2)},
        "出手频率":{"灵狐":3, "天马":3, "鸾鸟":2},
        "伤倍率_乘在攻":{"灵狐":0.76, "天马":eval(f"{0.9:g}")},
        "治疗倍率_乘在攻":{"鸾鸟":0.98},
        }    
    
    
    # 会根据主灵兽的情况去转换到其他灵兽相同灵果消耗的情况
    # 已支持转换到相同灵果的：等级、属性提升、
    # 未支持转换到：释放技能倍率_乘在攻
    可选主灵兽=使所有灵兽升级到消耗相同灵果(21,"鸾鸟",可选主灵兽)
    #input(可选主灵兽)
    
    是否改属性提升=True
    
    # 下阵灵兽
    下阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    # 上阵灵兽
    我.主灵兽名称=("灵狐","天马","鸾鸟")[-1]
    #可选主灵兽["属性提升"][我.主灵兽名称]=0.162
    上阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    # 对是否支持buff功能的开关
    我.buff_ON=True
    
    # 设置是否关闭连暴
    # 如果关闭连暴，可以看到每一场都是一模一样的。
    # 如果第一场输，再打499场也是0%胜率。
    #关闭双方连暴(我)
    
    return 战场


'''
《冒险怪3-14》

    我=Role([15850,2386,400,605],"我")
    我.主灵兽名称="鸾鸟"
    敌=Role([33194,2874,718,801],"敌")
    战场=Fight(我,敌)
    
500场：面板连暴率20%，鸾鸟3.2%胜率。撑到13回合（行动12回合）。
第16场打到掉血100%以上。最理想胜率：1/16=6.25%。
需要12回合连暴8次。回合数=12，但攻击机会>=12。
不是0%胜率，不是完全不能赢，而是赢过。
但需要13回合连暴8次。

    我=Role([16495,2476,412,633],"我")
    我.主灵兽名称="鸾鸟"
    敌=Role([33194,2874,718,801],"敌")
    战场=Fight(我,敌)
    
5%胜率。第一次打掉敌一管血是第12场。
1/12=8.3%理想胜率。

    我=Role([16911,2538,423,650],"我")
    我.主灵兽名称="鸾鸟"
    敌=Role([33194,2874,718,801],"敌")
    战场=Fight(我,敌)

    
他打不死我。15回合打不完，打掉我99%血。
他打我几乎全是平局。
不过不能认为平局是我的胜率，不能认为平局多就容易赢。
因为平局应该算作我输。
而现在刚好平局已经不计算入我的胜率，这是对的。
他是0%胜率。我是51%胜率。
他平的局就是49%。
所以其实我有49%的败率。
但是我不打算记入为他的胜率。
因为虽然对于我而言，平和败没差别；但是对于他，平和胜有差别。
如果算作他的胜率，会造成我觉得没希望。
平了和胜了，他胜率都没变化。但是战斗的难度肯定有变化。所以不相符。
所以看到他胜率低，我就知道有希望。



我15回合连暴4次干掉他了。

好多次回合结束都打不完。98%对99%那种。
导致不是从try..except...退出本场的。
里面的记者的变化()没调用到。参赛次数没+1。于是参赛次数0。
除以0出错。
'''

def 冒险怪3_14():
    我=Role([16911,2538,423,650],"我")
    我.主灵兽名称="鸾鸟"
    敌=Role([33194,2874,718,801],"敌")
    战场=Fight(我,敌)
    
    我.现阶段=敌.现阶段="筑基"    
    
    def 双方信息设置(对手类型="冒险怪"):
        nonlocal 我
        if 对手类型=="冒险怪":
            我.对手.设置战斗抗性(4.8,"抗连",14.6)
            我.对手.设置战斗属性(2.3,"连",6.9)
        elif 对手类型=="斗法":
            '''
            我=Role([16594,2491,415,633],"我")
            
            伤11.33%对14.04%。
            筑基后期打金丹中期赢了。
            他连不了，他带了蘑菇精只有8.9%暴击率，以及4.6%吸血率（回血量+107）。否则也暴不了。
            我暴不了，我16.8%连击率。
            
            面板他8回合胜（我后手人物行动只有7回合），我把他压到75.49%。（我需要9回合且后手。）
            所以我还差24.51%，也就是2.16个伤11.33%。也就是需要在7回合连3次。
            
            他没暴，我最后一回合第7回合后手连了2次。
            '''            
            我.对手.设置战斗抗性(12,"抗吸",40)
            我.对手.连=9.4
            我.对手.吸=16.6
            我.对手.暴=13.4+7.5
            我.对手.血=17944
            我.对手.攻=2745
            我.对手.防=458
            我.对手.敏=673
            我.对手.主灵兽名称="天马"
            我.对手.主灵兽伤倍率_乘在攻=0.9
            我.对手.主灵兽出手频率=3
            
    def 帮助是否换装备之决策(n):
        nonlocal 我
        我.吸+=(-3.8,0)[n]
        我.暴+=(-2.5,0)[n]
        我.连+=(-1.3,0)[n-1]
        我.血+=(300)
        我.攻+=(2,0)[n]
        我.防+=(1,0)[n]
        
    
    双方信息设置()                
    我.设置战斗抗性(12)
    我.吸=0
    我.连=28.8
    我.暴=12.6
    
    
    #帮助是否换装备之决策(1)
    
    
    可选主灵兽={"属性提升":{"灵狐":0.05, "天马":0.09,"鸾鸟":0.12+0.005*(14//2)+0.02*(14%2)},
        "出手频率":{"灵狐":3, "天马":3, "鸾鸟":2},
        "伤倍率_乘在攻":{"灵狐":0.6, "天马":eval(f"{0.9:g}")},
        "治疗倍率_乘在攻":{"鸾鸟":0.98},
        }    
    
    
    
    可选主灵兽=使所有灵兽升级到消耗相同灵果(20,"鸾鸟",可选主灵兽,True)
   
    #input(可选主灵兽)
    是否改属性提升=True
    
    # 下阵灵兽
    下阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    # 上阵灵兽
    我.主灵兽名称=("灵狐","天马","鸾鸟")[-1]
    #可选主灵兽["属性提升"][我.主灵兽名称]=0.162
    上阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    # 减伤buff的开关
    我.buff_ON=True
    
    # 设置是否关闭连暴
    # 如果关闭连暴，可以看到每一场都是一模一样的。
    # 如果第一场输，再打499场也是0%胜率。
    #关闭双方连暴(我)
    
    return 战场
    
    

def 冒险怪3_13():
    '''
    《冒险怪3-13》
    《公平比较之灵兽》
16级鸾鸟=12000灵果=22级天马=35级灵狐

[灵狐 |连暴率31.8% |伤5.21%对15.14% |7回合 |无连暴情况下，7回合，最低压敌血线到43.08%|有连暴情况下，最低压敌血线到95.07%，出现在第352场，需要6回合连暴9次|0%胜率]

[天马 |连暴率31.8% |伤5.31%对14.93% |7回合 |无连暴情况下，7回合，最低压敌血线到47.31%|有连暴情况下，最低压敌血线到95.07%，出现在第42场，需要6回合连暴9次|0%胜率]

[鸾鸟 |连暴率31.8% |伤5.47%对14.55% |治疗12.79% |7回合 |拖至15回合（人物行动14回合） |无连暴情况下，15回合（已死亡），最低压敌血线到76.61% |有连暴情况下，第一次压敌血线到100%出现在第1场 ，需要14回合连暴6次|58%胜率]

    我=Role([15809,2379,399,605],"我")
    我.主灵兽名称="鸾鸟"
    敌=Role([31157,2699,674,747],"敌")
    
两把就过了。
因为实际连暴率会是39%~41%，比面板的31%高。
因为6回合不一定是6次攻击机会。
只要触发一次连击或反击，就是7次攻击机会。
    
装备的好坏不能单纯通过自动战斗来对比。
因为存在对手的因素。
必须记住：一切战斗必须看对手。
'''

    我=Role([15809,2379,399,605],"我")
    我.主灵兽名称="鸾鸟"
    敌=Role([31157,2699,674,747],"敌")
    战场=Fight(我,敌)
    
    我.现阶段=敌.现阶段="筑基"    
    
    def 双方信息设置(对手类型="冒险怪"):
        nonlocal 我
        if 对手类型=="冒险怪":
            我.对手.设置战斗抗性(4.5)
            我.对手.设置战斗属性(2.1,"连",6.5)
        elif 对手类型=="斗法":
            我.对手.抗暴=1.4
            我.对手.抗吸=14.6
            我.对手.连=13.6
            我.对手.吸=11.1
            我.对手.血=15632
            我.对手.攻=2350
            我.对手.防=385
            我.对手.敏=667
            我.对手.主灵兽名称="天马"
            我.对手.主灵兽伤倍率_乘在攻=0.9
            我.对手.主灵兽出手频率=3
            
    def 帮助是否换装备之决策(n):
        nonlocal 我
        我.吸+=(-3.8,0)[n]
        我.暴+=(-2.5,0)[n]
        我.连+=(1.3,0)[n-1]
        我.血+=(-30)
        我.攻+=(2,0)[n]
        我.防+=(1,0)[n]

            
    双方信息设置()                
    我.设置战斗抗性(12)
    我.吸=0
    我.连=24.3
    我.暴=16.5
    
    
    #帮助是否换装备之决策(1)
    
    
    可选主灵兽={"属性提升":{"灵狐":0.05, "天马":0.09,"鸾鸟":0.12+0.005*(14//2)+0.02*(14%2)},
        "出手频率":{"灵狐":3, "天马":3, "鸾鸟":2},
        "伤倍率_乘在攻":{"灵狐":0.6, "天马":eval(f"{0.9:g}")},
        "治疗倍率_乘在攻":{"鸾鸟":0.85},
        }    
    
    
    #可选主灵兽=使所有灵兽升级到消耗相同灵果(16,"鸾鸟",可选主灵兽)
   
    #input(可选主灵兽)
    是否改属性提升=True
    
    # 下阵灵兽
    下阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    # 上阵灵兽
    我.主灵兽名称=("灵狐","天马","鸾鸟")[-1]
    #可选主灵兽["属性提升"][我.主灵兽名称]=0.162
    上阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    # 减伤buff的开关
    我.buff_ON=True
    
    # 设置是否关闭连暴
    # 如果关闭连暴，可以看到每一场都是一模一样的。
    # 如果第一场输，再打499场也是0%胜率。
    #关闭连暴(我)

    return 战场
    
    
#直到《冒险3-13》。
#没记录下来：《冒险3-10》一遍过，7次连暴+1次反。
#没记录下来：《冒险3-8》一遍过，大于5次连暴，丝血绝杀。

def 冒险怪3_7_1():
    # 《冒险怪3-7-1》
    # 上阵假设14级（属性提升+16.2%）鸾鸟带减伤：
    # [8%对16%|47%胜率|6回合变10回合|10回合3次连暴即可必胜]
    # 鸾鸟无减伤：8.2%胜率。
    # 因为减伤每次2.26%，10回合共5次，是减了共11%。
    # 差不多多减了一回合的伤害。这样拖了一回合。
    # 一回合多打一次人物白板普攻。8*9变8*10，
    # 所以可以少打一次连暴。并且是在更长的回合少打一次连暴，
    # 需要在9回合内打4次连暴 变 10回合内打3次连暴
    # 而连暴的难易度最微小的变动都是影响胜率最大的因素
    # 天马（提升至与鸾鸟相同属性）：2.4%胜率
    
    # 鸾鸟减伤模拟是10回合连暴3。
    # 实战是9回合连暴4，一遍过。
    # 我=Role([14141,2133,355,529],"我")
    # 我.主灵兽名称="鸾鸟"
    # 敌=Role([19179,2762,552,656],"敌")
    
    
    我=Role([14141,2133,355,529],"我")
    我.主灵兽名称="鸾鸟"
    敌=Role([19179,2762,552,656],"敌")
    战场=Fight(我,敌)
    
    我.现阶段=敌.现阶段="筑基"
    
    
    def 双方信息设置(对手类型="冒险怪"):
        nonlocal 我
        if 对手类型=="冒险怪":
            我.对手.设置战斗抗性(3,"抗暴",9)
            我.对手.设置战斗属性(1.4)
    
    def 帮助是否换装备之决策(n):
        nonlocal 我
        我.吸-=(3.8,0)[n]
        #我暴-=2.5
        我.连+=(2.6,0)[n]
        我.血+=(609-392)
        我.攻+=(2,0)[n]
        我.防-=(1,0)[n]

    # 我.灵兽.下阵()
    # 我.灵兽.上阵()
    def 下阵灵兽(我, 可选主灵兽, mode):
        if mode:我.血,我.攻,我.防=[i/(1+可选主灵兽["属性提升"][我.主灵兽名称]) for i in (我.血, 我.攻, 我.防)]
        我.主灵兽名称=""
        
    def 上阵灵兽(我, 可选主灵兽, mode):
        if mode:我.血,我.攻,我.防=[i*(1+可选主灵兽["属性提升"][我.主灵兽名称]) for i in (我.血, 我.攻, 我.防)]
        我.主灵兽出手频率=可选主灵兽["出手频率"][我.主灵兽名称]
        try:
            我.主灵兽伤倍率_乘在攻=可选主灵兽["伤倍率_乘在攻"][我.主灵兽名称]
        except KeyError:pass
        try: 
            我.主灵兽治疗倍率_乘在攻=可选主灵兽["治疗倍率_乘在攻"][我.主灵兽名称]
        except KeyError:pass


        
    双方信息设置()                
    我.设置战斗抗性(12)
    我.吸=0
    我.连=20.1
    我.暴=15.6

    #帮助是否换装备之决策(1)

    可选主灵兽={"属性提升":{"灵狐":0.05, "天马":0.13,"鸾鸟":0.12+0.0025*14},
        "出手频率":{"灵狐":3, "天马":3, "鸾鸟":2},
        "伤倍率_乘在攻":{"灵狐":0.6, "天马":0.9+0.135},
        "治疗倍率_乘在攻":{"鸾鸟":0.85},
        }    
    
    是否改属性提升=True
    
    # 下阵灵兽
    下阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    # 上阵灵兽
    我.主灵兽名称=("灵狐","天马","鸾鸟")[2]
    #可选主灵兽["属性提升"][我.主灵兽名称]=0.162
    上阵灵兽(我, 可选主灵兽, 是否改属性提升)
    
    #减伤buff的开关
    我.buff_ON=True
    
    return 战场


def 冒险怪3_7():
    # 《冒险怪3-7》
    # 7%对18%。
    # 面板6回合压到52.19%血线。
    # 平均每回合压8.6%。
    # 需要连击(100-52)/7=6次。
    # 6回合13.3%连击率，理论连击0.798次一场。
    # 一场连击一次的概率是79.8%。
    # 一场连击6次的概率是13.3%。
    # 错。
    # 6次机会一次都不连击的概率是42%。
    # 至少连击一次的概率是58%。
    # 胜率0%。
    # 打500场，压到90%血线，胜率0%。
    # 打1000场，压到103%血线，赢了两场，胜率0.2%。   
    #我=Role([13419,1984,325,496],"我")
    #敌=Role([18035,2598,520,609],"敌")
    #第一场胜在第79场，所以模糊胜率=1.2%
    #跑出来430多场赢7场
    
    #我=Role([13550,2012,335,514],"我")
    #我.主灵兽名称="天马"
    #敌=Role([18035,2598,520,609],"敌")
    #天马下阵是攻1809，因为天马属性提升是11.2%
    #天马下阵换灵狐是攻1900，因为灵狐属性提升是5%
    #打500场：天马胜率7.7%。灵狐胜率0.79%。
    #天马第1次打到100%以上敌血线平均是在第2~6场。
    #灵狐是在第109场。
    
    #我=Role([13565,2033,339,521],"我")
    #我.主灵兽名称="天马"
    #敌=Role([18035,2598,520,609],"敌")
    #500场16.2%胜率
    
    
    #500场|连2暴2或连3|胜率31.8%
    #我=Role([13811,2083,347,529],"我")
    #我.主灵兽名称="天马"
    #敌=Role([18035,2598,520,609],"敌")
    #战场=Fight(我,敌)
    #[伤8.67%+11.95%(3)]对[伤16.3%|7回合]
    #实战4次连暴（连2暴2）赢了于第6回合天马行动
    我=Role([13811,2083,347,529],"我")
    我.主灵兽名称="天马"
    敌=Role([18035,2598,520,609],"敌")
    战场=Fight(我,敌)
    
    我.现阶段=敌.现阶段="筑基"
    
    
    # 我.灵兽.下阵()
    # 我.灵兽.上阵()
    def 下阵灵兽(我, 可选主灵兽):
        我.血,我.攻,我.防=[i/(1+可选主灵兽["属性提升"][我.主灵兽名称]) for i in (我.血, 我.攻, 我.防)]
        我.主灵兽名称=""
        
    def 上阵灵兽(我, 可选主灵兽):
        我.血,我.攻,我.防=[i*(1+可选主灵兽["属性提升"][我.主灵兽名称]) for i in (我.血, 我.攻, 我.防)]
        我.主灵兽出手频率=可选主灵兽["出手频率"][我.主灵兽名称]
        我.主灵兽伤倍率_乘在攻=可选主灵兽["伤倍率_乘在攻"][我.主灵兽名称]

    
    def 双方信息设置(对手类型="冒险怪"):
        nonlocal 我
        if 对手类型=="冒险怪":
            我.对手.设置战斗抗性(2.8,"抗暴",8.6)
            我.对手.设置战斗属性(1.2)
    
    def 帮助是否换装备之决策():
        nonlocal 我
        我.吸-=3.8
        #我暴-=2.5
        我.连+=2.6
        我.血+=(991-901)
        我.攻+=2
        我.防-=1
        
    双方信息设置()                
    我.设置战斗抗性(12)
    我.吸=0
    我.连=20.1
    我.暴=15.6


    #帮助是否换装备之决策()

    可选主灵兽={"属性提升":{"灵狐":0.05,"天马":0.128},
        "出手频率":{"灵狐":3,"天马":3},
        "伤倍率_乘在攻":{"灵狐":0.6,"天马":0.9+0.135},
        }    
    
    
    # 下阵灵兽
    下阵灵兽(我, 可选主灵兽)
    
    # 上阵灵兽
    我.主灵兽名称=("灵狐","天马")[1]
    上阵灵兽(我, 可选主灵兽)


    
    # 是否使用对手模板？
    # 战场=冒险怪3_5()   

    
    return 战场


def 冒险怪3_6():
    # 胜率25%~27%。（需要3次连击胜。）（实战：2暴一连。）

    我=Role([12695,1877,308,500],"我")
    敌=Role([15652,2254,451,690],"敌")
    战场=Fight(我,敌)
    
    我.现阶段=敌.现阶段="筑基"
    
    
    def 双方信息设置(对手类型="冒险怪"):
        nonlocal 我
        if 对手类型=="冒险怪":
            我.对手.设置战斗抗性(2.7,"抗吸",8.2)
            我.对手.设置战斗属性(1.1)
            
        我.设置战斗抗性(12)
        我.吸=5.3
        我.连=16
        我.暴=13.4
        我.主灵兽名称="灵狐"
        我.主灵兽出手频率=3
        我.主灵兽伤倍率_乘在攻=0.6
    
    双方信息设置()
    
    return 战场


'''
《对手模板：冒险怪3-5》
胜率70%~75%(只要有一次连击就是100%胜率。
而8回合13.4%连击率，8*13.4%=1.072。
一场很容易有一次。所以胜率很接近100%。
'''
def 冒险怪3_5():
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
        我.主灵兽名称="灵狐"
        我.主灵兽出手频率=3
        我.主灵兽伤倍率_乘在攻=0.6
        
    双方信息设置()
    
    return 战场