EXCEL_NAME = "test.xlsx"
BOXSHEET_NAME = "Sheet1"
TEAMSHEET_NAME = "Sheet2"

PLAYER_NAME = ["吴彦祖","达令","胖子队长","闪耀OxO","你们的爸爸","水无月空","gkd","兰佩路基","竹林落叶","秋衣~小小撸爷","VikedalS","兮年","Tero","CRLyle","电气白兰","Min","百冠 折樱","进击的小笼包","yyy","静琉","傲娇啵酱","傻飞飞","里面不可以","大叔已成精","周小杰","妖妖妖精","极乐丸","UNLuv422","好人一生平安","SK"]

#CHARACTER_NAME =  ["黑骑","黄骑","狼","狗","忍","女仆","千歌","妈","猫拳","tp","暴击弓","亚里沙","病娇","xcw","伊利亚","兔子","熊锤","布丁","充电宝","深月","黑猫","妹法","空花","望","猫剑","圣母","姐姐","羊驼"]
CHARACTER_NAME = ["布丁","黑骑","抖M","望","玲奈(暴击)","栞(tp)","亚里沙","香织(狗)","日和莉(猫拳)","珠希(猫剑)","惠理子(病娇)","姬塔","真琴(狼)","深月","忍","可可罗(妈)","咲恋(充电宝)","美美(兔子)","姐姐(静流)","镜华(小仓唯)","伊利亚","妹法","凯露(臭鼬)","美里","黄骑"]

BOSS_NAME = ["A1","A2","A3","A4","A5"]
BOSS_HP = [6000000,8000000,10000000,12000000,20000000]

####-表格长啥样-####
BOXSHEET_PLAYER_COL = 0
BOXSHEET_CHARACTER_ROW = 1

BOXSHEET_PLAYER_NUM = PLAYER_NAME.__len__()
BOXSHEET_CHARACTER_NUM = CHARACTER_NAME.__len__()
#数据列从玩家列右边开始,到+角色数结束
BOXSHEET_DATA_START_COL = BOXSHEET_PLAYER_COL+1
BOXSHEET_DATA_END_COL = BOXSHEET_PLAYER_COL + BOXSHEET_CHARACTER_NUM
#数据行从角色行下方开始,到+玩家数结束
BOXSHEET_DATA_START_ROW = BOXSHEET_CHARACTER_ROW+1
BOXSHEET_DATA_END_ROW = BOXSHEET_CHARACTER_ROW + BOXSHEET_PLAYER_NUM

TEAMSHEET_BOSS_COL = 0
#作业行从开始需要标明,尾部要用程序检测
TEAMSHEET_DATA_START_ROW = 1
#作业列从王列右边开始,到+4个角色后结束
TEAMSHEET_DATA_START_COL = TEAMSHEET_BOSS_COL+1
TEAMSHEET_DATA_END_COL = TEAMSHEET_BOSS_COL+5
#作业表伤害记录位置
TEAMSHEET_DAMAGE_COL = TEAMSHEET_DATA_END_COL+1
