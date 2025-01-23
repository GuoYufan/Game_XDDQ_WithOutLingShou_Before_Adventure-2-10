import math
class Role():
    def __init__(self,基础属性):
        self.基础属性=dict(zip(("hp","atk","def","spd"),基础属性))
fight=lambda me,opn:opn.基础属性["hp"]/(me.基础属性["atk"]-opn.基础属性["def"])
def 我是先手方吗(me,opn):
    return me.基础属性["spd"]>opn.基础属性["spd"]
def 我胜吗(me_fight_opn,opn_fight_me,先手方):
    if 先手方=="我":
        if me_fight_opn<=opn_fight_me:return True
    else:
        if me_fight_opn-opn_fight_me<0:return True
    return False
敌=Role([2247,789,105,249])
我基=[3312,489,77,260]
我=Role(我基)
我打敌回合数=fight(我,敌)
敌打我回合数=fight(敌,我)
我打敌实际回合数=int(我打敌回合数)+1
敌打我实际回合数=int(敌打我回合数)+1
先手方="我" if  我是先手方吗(我,敌) else "敌"
谁胜="我" if 我胜吗(我打敌实际回合数,敌打我实际回合数,先手方) else "敌"
print(f"我打敌：{我打敌回合数}——{我打敌实际回合数}")
print(f"敌打我：{敌打我回合数}——{敌打我实际回合数}")
print(f"先手方：{先手方}")
print(f"谁胜：{谁胜}")
for i in range(1,10):
    print()
    multi=1+i*0.1
    我基=[int(i*multi) for i in 我基[:-1]]+[我基[-1]]
    我=Role(我基)
    我打敌回合数=fight(我,敌)
    敌打我回合数=fight(敌,我)
    我打敌实际回合数=math.ceil(我打敌回合数)
    敌打我实际回合数=math.ceil(敌打我回合数)
    谁胜="我" if 我胜吗(我打敌实际回合数,敌打我实际回合数,先手方) else "敌"
    print(f"把我变至几倍：{multi}倍 {我基}")
    print(f"我打敌：{我打敌回合数}——{我打敌实际回合数}")
    print(f"敌打我：{敌打我回合数}——{敌打我实际回合数}")
    print(f"谁胜：{谁胜}")
    if 谁胜=="我":break
