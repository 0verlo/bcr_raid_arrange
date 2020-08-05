#!/usr/bin/env python3
# coding=utf-8
import func.team_info as team_info
import re
print("hello")

team_info = team_info.Team_Info()
#team_info.test_traverse_sheet()

ar_set1=team_info.new_arrange()
#ar_set1.test_traverse_sheet()
ar_set1.show_team()
ar_set1.add_team_set()
ar_set1.check_team_set()

while(1):
    comb_numb = ar_set1.comb_numbs()
    str_input = input("输入"+str(comb_numb)+"个数并用空格各开以表示各个set人数:")

    reExpStr = ("(\d+)"+"[ |,](\d+)"*(comb_numb-1))
    reExp = re.compile(reExpStr)

    str_result = re.match(reExp,str_input)
    if None != str_result:
        inputlist=[]
        for i in range(comb_numb):
            inputlist.append(int(str_result.group(i+1)))
        print(inputlist)
        ar_set1.arrange_stat(inputlist)
    else:
        print("输入有误:",end="")
        print(str_input)

    
