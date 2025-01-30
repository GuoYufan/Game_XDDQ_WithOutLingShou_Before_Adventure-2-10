import math

class Convert():
    def __init__(self,level,name):
        self.品种列表=["传说","卓越","常见"]
        self.名称列表=["鸾鸟","天马","灵狐"]
        self.找灵兽是哪个品种库=dict(zip(self.名称列表, self.品种列表))

        self.初始属性提升列表=[ i/100 for i in [12,9,5]]
        self.初始属性提升库=dict(zip(self.品种列表, self.初始属性提升列表))
        
        self.每两级属性提升增幅列表=[ i/100 for i in [0.2+0.3,0.2*2,0.1*2]]
        self.每两级属性提升增幅库=dict(zip(self.品种列表, self.每两级属性提升增幅列表))
        
        self.每升一级消耗灵果增幅列表=[100,50,10]
        self.每升一级消耗灵果增幅库=dict(zip(self.品种列表, self.每升一级消耗灵果增幅列表))
        
        self.初始参战技能倍率列表=[0.85,0.9,0.6]
        self.初始参战技能倍率库=dict(zip(self.名称列表, self.初始参战技能倍率列表))
        
        self.每二十级参战技能倍率增幅列表=[0.13,0.135,0.08]
        self.每二十级参战技能倍率增幅库=dict(zip(self.名称列表, self.每二十级参战技能倍率增幅列表))

        
        #'''
        del (
        	 self.品种列表, self.名称列表, 
         self.初始属性提升列表, 
         self.每两级属性提升增幅列表, 
         self.每升一级消耗灵果增幅列表,
         self.初始参战技能倍率列表,
         self.每二十级参战技能倍率增幅列表
         )
         #'''
         
        
               
        self.src_level=level
        self._src_name=name
        self.result={f"{self.src_name}等级":self.src_level}
        self.update_src()
        self._target_name=""
        
    
    def copy(self, pending):
        pending["属性提升"][self.src_name]=eval(f"{self.获取属性提升(self.src_name):g}")
        if self.src_name in pending["伤倍率_乘在攻"]:
            pending["伤倍率_乘在攻"][self.src_name]=eval(f"{self.获取参战技能倍率(self.src_name):g}")
        if self.src_name in pending["治疗倍率_乘在攻"]:
            pending["治疗倍率_乘在攻"][self.src_name]=eval(f"{self.获取参战技能倍率(self.src_name):g}")
        
        
        return pending
        
    
    def update_src(self):
        self.src_breed=self.找灵兽是哪个品种库[self.src_name]
        self.src_epl=self.每升一级消耗灵果增幅库[self.src_breed]
        self.从源等级计算源属性提升()
        self.result[f"{self.src_name}属性提升"]=self.src_improve
        self.从源等级计算源灵果消耗()
        self.result[f"{self.src_name}灵果消耗"]=self.src_expend
        self.从源等级计算源参战技能倍率()
        self.result[f"{self.src_name}参战技能倍率"]=self.src_ability
    
    def 设置要转换到的灵兽叫什么名称(self, target_name):
        self.target_name=target_name
        
    @property
    def target_name(self):return self._target_name
    
    @target_name.setter
    def target_name(self,value):        
        self._target_name=value
        self.target_breed=self.找灵兽是哪个品种库[self._target_name]   
        self.target_epl=self.每升一级消耗灵果增幅库[self.target_breed]
        self.从源灵果消耗计算目标等级()
        self.result[f"{self.target_name}等级"]=self.target_level
        	
    @property
    def src_name(self):return self._src_name
    
    @src_name.setter
    def src_name(self,value):
        self._src_name=value
        self.update_src()
    
    def 从源等级计算源参战技能倍率(self):
        ability_level=self.src_level//20
        self.src_ability=self.初始参战技能倍率库[self.src_name]+self.每二十级参战技能倍率增幅库[self.src_name]*ability_level
        
    def 从源等级计算源属性提升(self):
        # 从等级计算属性提升
        calc=lambda attr_begin,lv,improve_per_two_level:attr_begin+improve_per_two_level*((lv-1)//2)+(lv-1)%2*0.002
             
        arg0=self.初始属性提升库[self.src_breed]
        arg1=int(self.src_level)
        arg2=self.每两级属性提升增幅库[self.src_breed]
        self.src_improve=calc(arg0, arg1, arg2)
        
        
        
    def 从源等级计算源灵果消耗(self):
        src_level=int(self.src_level)
        self.src_expend=sum(range(1,src_level))*self.src_epl
    
    def 从源灵果消耗计算目标等级(self):
        root=lambda a,b,c:(-b+math.sqrt(b*b-4*a*c))/(2*a)
        self.target_level=root(1,1,-self.src_expend/self.target_epl*2)+1
    
    def show(self):
        for k,v in self.result.items():
            
            print(k,f"{v:g}",sep=":")
        

    获取等级=lambda self, name:self.result[name+"等级"]
    获取属性提升=lambda self, name:self.result[name+"属性提升"]
    获取参战技能倍率=lambda self, name:self.result[name+"参战技能倍率"]

def run():
    convert=Convert(24,"天马")
    print("◾️",end="")
    convert.show()
    input()
    
    
    convert.设置要转换到的灵兽叫什么名称("天马")
    convert.show()
    天马等级=convert.获取等级("天马")
    input()
    
    convert.设置要转换到的灵兽叫什么名称("灵狐")
    convert.show()
    灵狐等级=convert.获取等级("灵狐")
    print()
    
    
    convert=Convert(天马等级, "天马")
    print("◾️",end="")
    convert.show()
    print()
    
    convert=Convert(灵狐等级, "灵狐")
    print("◾️",end="")
    convert.show()
    
    

if __name__=="__main__":run()




# updated:2025.1.26
# 《转换器about灵兽信息》第一个可用版本v1.0.0
# 已完成对等级、灵果消耗、属性提升、参战技能倍率的全面支持。
