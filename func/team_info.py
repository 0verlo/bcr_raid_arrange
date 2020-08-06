import copy
import xlrd
import re

#import setting as INFO
import func.setting as INFO

#多层嵌套字典
#XXX:可能要改回json
class Vividict(dict):
    def __missing__(self,key):
        value = self[key] = type(self)()
        return value

class Team_Info(object):
    def __init__(self):
        #玩家队伍结构体,可通过info[玩家][角色][star/rank/equment]获取对应信息
        self.__box_info=Vividict()
        #作业结构体，通过set[王][组成/伤害]获取对应信息
        self.__team_set=dict()
        #读取EXCEL
        self.__wb=xlrd.open_workbook(filename=INFO.EXCEL_NAME)
        self.__box_sh=self.__wb.sheet_by_name(INFO.BOXSHEET_NAME)
        self.__teamset_sh=self.__wb.sheet_by_name(INFO.TEAMSHEET_NAME)
        #EXCEL内容写入结构体
        self.__traverse_box_sheet()

    #### 初始化用遍历EXCEL ####
    def __traverse_box_sheet(self):
        ##遍历Box数据部分获取玩家名字
        for rx in range(INFO.BOXSHEET_DATA_START_ROW,INFO.BOXSHEET_DATA_END_ROW+1):
            playerName = self.__box_sh.cell_value(rx,INFO.BOXSHEET_PLAYER_COL)
            if '' == playerName:
                print("Info gose wrong in (%d,%d)")
                continue
            #遍历数据区域获取角色名并取值存储在对应结构体中
            for cx in range(INFO.BOXSHEET_DATA_START_COL,INFO.BOXSHEET_DATA_END_COL+1):
                characterName = self.__box_sh.cell_value(INFO.BOXSHEET_CHARACTER_ROW,cx)
                characterAttr = self.__box_sh.cell_value(rx,cx)
                #取得内容转为Dirct后再存储
                attrDirct = self.__reg_conv(characterAttr)
                if 0 != attrDirct["star"]:
                    self.__box_info[playerName][characterName] = attrDirct

        ##遍历Team数据部分获取作业
        teamsh_info={"name":[],"index":[],"end":0}
        #获取boss名字及其作业对应行数
        for rx in range(INFO.TEAMSHEET_DATA_START_ROW,self.__teamset_sh.nrows):
            boss_name = self.__teamset_sh.cell_value(rx,INFO.TEAMSHEET_BOSS_COL)
            data = self.__teamset_sh.cell_value(rx,INFO.TEAMSHEET_DATA_START_COL)
            if "" != boss_name:
                teamsh_info["name"].append(boss_name)
                teamsh_info["index"].append(rx)
            if ("" != data)&(teamsh_info["end"] < rx):
                teamsh_info["end"]=rx+1
        teamsh_info["index"].append(teamsh_info["end"])

        for boss_num in range(0,teamsh_info["name"].__len__()):
            boss_name = teamsh_info["name"][boss_num]
            if boss_name in self.__team_set:
                pass
            else:
                self.__team_set[boss_name]=[]

            datastart_row = teamsh_info["index"][boss_num]
            dataend_row = teamsh_info["index"][boss_num+1]
            #获取作业队伍属性字典
            team_dict = {"team":[],"damage":0} 
            for rx in range(datastart_row,dataend_row)[::2]:
                for cx in range(INFO.TEAMSHEET_DATA_START_COL,INFO.TEAMSHEET_DATA_END_COL+1):
                    #print(str(rx)+str(cx)+":",end="")
                    characterName = self.__teamset_sh.cell_value(rx,cx)
                    characterAttr = self.__teamset_sh.cell_value(rx+1,cx)
                    character_dict = self.__reg_conv(characterAttr)
                    character_dict["name"]=characterName
                    #print(character_dict,end="")
                    team_dict["team"].append(character_dict)
                #print(self.__teamset_sh.cell_value(rx,INFO.TEAMSHEET_DAMAGE_COL))
                team_dict["damage"] = int(self.__teamset_sh.cell_value(rx,INFO.TEAMSHEET_DAMAGE_COL))
                self.__team_set[boss_name].append(team_dict)
                team_dict = {"team":[],"damage":0} 
                #print("")
        #print(self.__team_set)

        #XXX:增加队伍的函数抽出来
        #append字典到list上面

    #### 测试用遍历打印box结构体 ####
    def test_traverse_sheet(self):
        #for playerName in self.__box_info:
        playerName = INFO.PLAYER_NAME[10]
        print(playerName+":{",end="")
        for characterName in self.__box_info[playerName]:
            #print(characterName+":"+str(self.__box_info[playerName][characterName]["rank"]),end="")
            #print(characterName+":"+str(self.__box_info[playerName][characterName]["star"]),end="")
            print(characterName+":"+str(self.__box_info[playerName][characterName]["equment"]),end="")
        print("}")

    def new_arrange(self):
        box_info = copy.deepcopy(self.__box_info)
        team_set = copy.deepcopy(self.__team_set)
        arrange_set=Arrange_Set(box_info,team_set)
        return arrange_set

    #### 文字转数据接口 ####
    #该版本为"5-9-5"->{"star":5,"rank":9,"equment":5}
    def __reg_conv(self,strTmp):
        if (('' == strTmp)|('无' == strTmp)):
            return {"rank":0,"star":0,"equment":0}
        #print(strTmp+":",end="")
        str_re = re.match(r'\s*([0-6])[-|+](\d+)[-|+]([0-6]).*',strTmp)
        if (None != str_re):
            star = int(str_re.group(1))
            rank = int(str_re.group(2))
            equment = int(str_re.group(3))
            attrDirct = {"star":star,"rank":rank,"equment":equment}
            #print(attrDirct)
            #print("0"+str_re.group(1)+"1"+str_re.group(2)+"2"+str_re.group(3)+"end")
            return attrDirct
        print("Str input conv faild: "+strTmp)
        return {"rank":0,"star":0,"equment":0}

class Arrange_Set(object):
    def __init__(self,box_info,team_set):
        #玩家队伍结构体,可通过info[玩家][角色][star/rank/equment]获取对应信息
        self.__box_info=box_info
        #作业结构体，通过set[王][序号(随机)][team/damage]获取对应信息
        self.__team_set=team_set
        self.__team_set["comb"]=[]

    #打印作业
    def show_team(self):
        _boss_index = 0
        for boss_name in INFO.BOSS_NAME:
            charName_offset = max([len(x) for x in INFO.CHARACTER_NAME])+2
            bossName_offset = max([len(x) for x in INFO.BOSS_NAME])+2
            _team_index = 0
            team_sets = self.__team_set[boss_name]
            if 0 != _boss_index:
                print("="*((bossName_offset*2+4+(charName_offset*2+5)*5)+10))
            _boss_index = _boss_index+1
            for team in team_sets: 
                print(self.aligns(boss_name,bossName_offset),end="")
                boss_name = ""
                print((str(_team_index)+":").ljust(4),end="")
                _team_index = _team_index+1
                for character in team["team"]:
                    rankInfo="0-0-0"
                    if 0 != character["star"]:
                        rankInfo=(str(character["star"])+"-"+\
                            str(character["rank"])+"-"+\
                            str(character["equment"]))
                    print(rankInfo,end="")
                    print(self.aligns((character["name"]),charName_offset),end="")
                print(str(team["damage"]).rjust(9))

    #打印显示对齐
    def aligns(self,string,length=10):
        len_diff = length - len(string)
        if 0 == len_diff:
            return string
        elif 0 > len_diff:
            print ("Input str length gose wrong!")
            string = ""
        new_string = ""
        space = '　'
        for char in string:
            codes = ord(char) #字符串转为ASCII或UNICODE
            if codes <= 126: #若是半角字符
                new_string = new_string + chr(codes+65248) #转为全角字符
            else:
                new_string = new_string + char
        return new_string + space*(len_diff)

    #### 增排刀 ####
    def add_team_set(self):
        #生成排刀时用？暂时写死
        #XXX:3刀的组合需要有优先级
        self.__team_set["comb"]=[]
        self.__team_set["comb"].append({"team":[["A4",0],["A3",0],["A5",0]],"player":[]})
        self.__team_set["comb"].append({"team":[["A3",0],["A5",3],["A5",0]],"player":[]})
        self.__team_set["comb"].append({"team":[["A4",1],["A3",0],["A5",1]],"player":[]})
        self.__team_set["comb"].append({"team":[["A2",0],["A1",1],["A5",0]],"player":[]})

    def comb_numbs(self):
        return len(self.__team_set["comb"])
        
    #### 增加作业队伍接口 ####
    def team_add(self,team_list,boss_name,damage):
        pass

    #### 检查排刀 ####
    def check_team_set(self):
        for combin in self.__team_set["comb"]:
            char_need = []
            for teamInfo in combin["team"]:
                char_need = char_need + self.__team_set[teamInfo[0]][teamInfo[1]]["team"]
                #print(char_need)
            for player in INFO.PLAYER_NAME:
            #for numb in range(10,15):
                #player = INFO.PLAYER_NAME[numb]
                box_info_for_check = copy.deepcopy(self.__box_info)
                charact_del ={} 
                charact_miss = []
                charact_miss_count = 0
                for charact in char_need:
                    if(box_info_for_check[player].get(charact["name"], False)):
                        charact_check = box_info_for_check[player][charact["name"]]
                    else:
                        charact_miss_count = charact_miss_count + 1
                        charact_miss.append(charact)
                        continue
                    if((charact["star"]<=charact_check["star"])&\
                        (charact["rank"]<=charact_check["rank"])&\
                        (charact["equment"]<=charact_check["equment"])): 
                        charact_del[charact["name"]] = box_info_for_check[player].pop(charact["name"])
                    else:
                        charact_miss_count = charact_miss_count + 1
                        charact_miss.append(charact)
                if charact_miss_count <= 3:
                    #print(player)
                    #print(charact_del)
                    #print(charact_miss)
                    combin["player"].append(player)
                else:
                    #print(player+" box not enough.Fail to use this set.")
                    #print(charact_miss)
                    self.__box_info[player].update(charact_del)
            #print(combin["player"])
        player_with_set = []
        for index in range(0,len(self.__team_set["comb"])):
            player_with_set = list(set(player_with_set).union(set(self.__team_set["comb"][index]["player"])))
            #print(len(player_with_set),end="")
            #print(player_with_set)
        player_left = list(set(INFO.PLAYER_NAME).difference(set(player_with_set))) 
        #print(player_left)
        if [] != player_left: 
            print("Set not enough! ",end="")
            print(player_left,end="")
            print(" don't got usable set!")
        else:
            print("All player got at least one set!")
                        
    #### 删除排刀 ####
    def del_team_set(self):
        #退回时用？
        pass
    
    #### 查询排的状态 ####
    def arrange_stat(self,input_set_numb=[]):
        #显示所有组合的刀数 以及对boss造成的伤害 以及剩余无安排的人
        damage=[0,0,0,0,0]
        all_combins = copy.deepcopy(self.__team_set["comb"])
        set_numb=[0,0,0,0]
        #取参数
        for i in range(len(input_set_numb)):
            if((4 > i)&(0 < input_set_numb[i])):
                set_numb[i]=input_set_numb[i]
        #print(set_numb)

        #去除已经安排的 
        i=0
        player_used=[]
        for combin in all_combins:
            if set_numb[i] > len(combin["player"]):
                set_numb[i] = len(combin["player"])
            for j in range(0,set_numb[i]):
                player_used.append(combin["player"].pop())
                #print(combin["player"])
            i=i+1
            #清除已经定好set的人
            #print(list(set(combin["player"]).difference(set(player_used))))
            for combin_clean in all_combins:
                combin_clean["player"]=list(set(combin_clean["player"]).difference(set(player_used)))
                #print(len(combin_clean["player"]),end="")
                #print(",",end="")
            #print("")

        print("="*80)
        #打印队伍结果
        index_=0
        for combin in all_combins:
            print(("set"+str(index_)+":").ljust(8),end="")
            for i in range(0,3):
                boss_name = combin["team"][i][0]
                boss_index = combin["team"][i][1]
                damage[INFO.BOSS_NAME.index(boss_name)] += (self.__team_set[boss_name][boss_index]["damage"])*set_numb[index_]
                print((boss_name+":").ljust(3),end="")
                print((str(self.__team_set[boss_name][boss_index]["damage"])).rjust(8),end="")
                print("    ",end="")
            print(("used:"+str(set_numb[index_])).ljust(8),end="")
            print(("left:"+str(len(combin["player"]))).ljust(8))
            index_=index_+1
        #print(damage)

        print("="*80)
        #打印剩余血量
        rount_1 = copy.deepcopy(INFO.BOSS_HP)
        print("boss_HP".ljust(10),end="")
        for i in range(len(rount_1)):
            print(str(rount_1[i]).rjust(12),end="")
        print("")
        print("left".ljust(10),end="")
        for i in range(len(rount_1)):
            print(str(rount_1[i] - damage[i]).rjust(12),end="")
        print("")

    #### 测试用测试修改 ####
    def test_change_test(self):
        #for playerName in self.__box_info:
        playerName = INFO.PLAYER_NAME[10]
        for characterName in self.__box_info[playerName]:
            self.__box_info[playerName][characterName]["equment"]=0
            #self.__box_info[playerName][characterName]["rank"]=0
            #self.__box_info[playerName][characterName]["star"]=0
            
    #### 测试用测试内容变化 ####
    def test_traverse_sheet(self):
        #for playerName in self.__box_info:
        playerName = INFO.PLAYER_NAME[13]
        print(playerName+":{",end="")
        for characterName in self.__box_info[playerName]:
            print(characterName+":",end="")
            print(str(self.__box_info[playerName][characterName]["star"]),end="")
            print("-"+str(self.__box_info[playerName][characterName]["rank"]),end="")
            print("-"+str(self.__box_info[playerName][characterName]["equment"]),end="")
        print("}")

