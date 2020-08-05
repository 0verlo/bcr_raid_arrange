#!/usr/bin/env python
# coding=utf-8
import func.setting as SETS
import xlrd
import json

print("hello!")

BoxSheet_player_col = 0 
BoxSheet_player_numb = 30
BoxSheet_character_row = 1 
BoxSheet_data_start = 1

inputFileName = 'test.xlsx'
wb = xlrd.open_workbook(filename=inputFileName)

sheetName = 'Sheet1'
table = wb.sheet_by_name(sheetName)

def traverse_sheet_v1():
    for crange in table.col_label_ranges:
        rlo,rhi,clo,chi = crange
        print(crange)
        for rx in xrange(rlo,rhi):
            for cx in xrange(clo,chi):
                print("(rowx:%d,clox:%d)-%r" %(rx,cx,table.cell_value(rx,cx)))

#多层嵌套字典
class Vividict(dict):
    def __missing__(self,key):
        value = self[key] = type(self)()
        print("value:",end="")
        print(value)
        print(";self[key]:",end="")
        print(self[key])
        print(";type(self):",end="")
        print(type(self))
        return value

data = Vividict()
def traverse_sheet1_try1():
    for rx in range(BoxSheet_character_row+1,BoxSheet_character_row+1+BoxSheet_player_numb):
        playerName = table.cell_value(rx,BoxSheet_player_col)
        if '' != playerName:
            print(playerName)
            for cx in range(BoxSheet_player_col+1,table.ncols):
                data[playerName][table.cell_value(BoxSheet_character_row,cx)]=\
                        table.cell_value(rx,cx)
    return data


with open('data.txt','w') as outfile:
    chatar_data = traverse_sheet1_try1()
    print(chatar_data)
    for player in chatar_data:
        for chatacter in chatar_data[player]:
            print(chatacter+chatar_data[player][chatacter])

    json.dump(chatar_data,outfile)

'''
with open('sheet_ref.txt') as json_file:
    sheet_info = json.load(json_file)
    print(sheet_info)
'''

#def sheet_generator():

