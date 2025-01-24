while True:
    try:
        me_hp=float(input("◾️我的血量:"))
        opn_hp=float(input("◾️敌的血量:"))
    except:continue
    break
print()

lostHP_percent=lambda dmg,hp:f"{dmg/hp*100}%"

while True:
    print("⚙️")
    for item in zip("01","我敌"):
        print(":".join(item))
    
    while True:
        try:answer=int(input("❓谁受到伤害(或治疗)？\n答:"))
        except Exception as e:
            print("❌%s:%s\n"%(type(e).__name__,e))
            continue
        if answer not in (0,1):
            print("❌must be 0~1\n")
            continue
        break
    while True:
        try:damage=float(input("◾️受到伤害量(或治疗量):"))
        except Exception as e:
            print("❌%s:%s\n"%(type(e).__name__,e))
            continue
        break
    if answer==0:
        result=lostHP_percent(damage,me_hp)
    else:result=lostHP_percent(damage,opn_hp)
    input(f"⚡️得出掉血/治疗百分比:\n{result}\n")
    
