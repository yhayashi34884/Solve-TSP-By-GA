# coding:utf-8
# GAで巡回セールスマン問題を解く
# とりあえず九州版 (各県の一番大きい駅を巡回する)
# コストは公共交通機関を利用した場合の最安移動費
# 各県の移動は、乗り継ぎなしとする（ただし、沖縄は空港-駅間の乗り継ぎも考慮,航空機の運賃は0917現在のもの)
# 求める解は最安巡回コストとそのルート
# 求めたコストと世代数はグラフ化、求めたルートはOpenStreetMapにプロットする

import numpy as np
import random
import copy
import matplotlib.pyplot as pl
import folium
import pandas as pd
import csv
import codecs

routelist = []
next_routelist = []
totalcostlist = []
compatible = []
start = 46        #スタート地点
generation = 101  #世代数

# CSVに移動コスト・駅隣接関係を入れたらCSVから読み込む
list = [40,41,42,43,44,45,46,47]

route = {40:[41,42,43,44,45,46,47],    # 40:博多駅
         41:[40,42],                   # 41:佐賀駅
         42:[40,41,43,44,45,46,47],    # 42:長崎駅
         43:[40,42,44,45,46,47],       # 43:熊本駅
         44:[40,42,43,45,46],          # 44:大分駅
         45:[40,42,43,44,46,47],       # 45:宮崎駅
         46:[40,42,43,44,45,47],       # 46:鹿児島中央駅
         47:[40,42,43,45,46]           # 47:那覇空港駅
        }

costs = {40:[-1,1110,2570,2160,3190,4630,5450,4250],    # 40:博多駅
         41:[1110,-1,2130,-1,-1,-1,-1,-1],              # 41:佐賀駅
         42:[2570,2130,-1,3700,4630,6690,6690,18000],   # 42:長崎駅
         43:[2160,-1,3700,-1,2780,4630,3700,17900],     # 43:熊本駅
         44:[3190,-1,4630,2780,-1,2800,5660,-1],        # 44:大分駅
         45:[4630,-1,6690,4630,2800,-1,2480,13340],     # 45:宮崎駅
         46:[5450,-1,6690,3700,5660,2480,-1,14650],     # 46:鹿児島中央駅
         47:[4250,-1,18000,17900,-1,13340,14650,-1]     # 47:那覇空港駅
         }


# CSVから駅情報を読み込み、リストに格納して返却する関数
def ReadCsv():
    # CSV読み込み
    with codecs.open('station20170403free.csv','r','utf-8','ignore') as file:
        stations = pd.read_table(file,delimiter=',')

    lines = pd.read_csv('line20170403free.csv')
    # 特定の行のみ抽出
    station_name = stations.loc[:,['station_name']]
    station_lat = stations.loc[:,['lat']]
    station_lon = stations.loc[:,['lon']]
    station_pref = stations.loc[:,['pref_cd']]
    # リストに変換
    station_name = station_name.values.tolist()
    station_lat = station_lat.values.tolist()
    station_lon = station_lon.values.tolist()
    station_pref = station_pref.values.tolist()
    
    return station_name,station_lat,station_lon,station_pref


# 個体数を取得する関数
def numget():
    if len(next_routelist) == 0:
        return 10
    else:
        return len(next_routelist)


# 巡回判定関数
def Patrolflag(plist,n):
    f_flag = 0
    if plist[0] != start: # スタート県が要素0番目でなかったら
        f_flag = 1
    for i in range(n-1):
        if (plist[i+1] in route[plist[i]]) == False:   # [i]県と[i+1]県が接続していなかったら
            f_flag = 1
    if (plist[0] in route[plist[n-1]]) == False: # リスト末尾の県とスタート県が接続していなかったら
        f_flag = 1
    return f_flag


# 初期化
def Init(n):    # n:個体数
    while len(routelist) < n:
        base = copy.copy(list)
        # listの中からスタート県を削除
        base.remove(start)
        random.shuffle(base)
        base.insert(0,start)   # 先頭にstartを追加
        if Patrolflag(base,len(base)) == 0:  # 各県が接続していて巡回できる個体のみ追加
            routelist.append(base)


# ある個体の巡回トータルコストを求める
def Getcost(rlist):
    totalcost = 0
    for i in range(len(rlist)):
        if i == len(rlist)-1 :
            totalcost += costs[rlist[i]][rlist[0]-40]    # 全国版の場合は-40しなくてok
            if costs[rlist[i]][rlist[0]-40] == -1:
                return -1
        else:
            totalcost += costs[rlist[i]][rlist[i+1]-40]  # 全国版の場合は-40しなくてok
            if costs[rlist[i]][rlist[i+1]-40] == -1:
                return -1

    return totalcost


# 各個体のトータルコストをもとに適合率を求める
def comparison():
    tcl = []
    sum = 0
    for i in range(len(totalcostlist)):
        tcl.append(totalcostlist[i]**2)
        sum += tcl[i]
        
    for i in range(len(tcl)):
        compatible.append(round(100*(float(max(tcl)-tcl[i])/sum),5))
    
    del tcl[:]


# エリート保存戦略
def elitecopy():
    per = copy.copy(compatible)
    per.sort()
    per.reverse()
    flag1 = 0
    flag2 = 0
    flag3 = 0
    flag4 = 0
    flag5 = 0
    for i, com in enumerate(compatible):
        if com == per[0] and flag1 == 0:
            next_routelist.append(routelist[i])
            flag1 = 1
        if com == per[1] and flag2 == 0:
            next_routelist.append(routelist[i])
            flag2 = 1
        if com == per[2] and flag3 == 0:
            next_routelist.append(routelist[i])
            flag3 = 1
        if com == per[3] and flag4 == 0:
            next_routelist.append(routelist[i])
            flag4 = 1
        if com == per[4] and flag5 == 0:
            next_routelist.append(routelist[i])
            flag5 = 1


# 順序表現による交叉法
def crossover():
    child_pass = []
    
    while len(child_pass) < 2:
        parents = []
        parent_order = []
        cross = []
        # 交叉点をランダムに選択
        for i in range(len(list)):
            cross.append(i)
        point = random.choice(cross)
            
        # 親を選択
        for i in range(2):
            parents.append(random.choice(routelist))

        # 各親をパス表現から順序表現に変換
        for i in range(2):
            par = []
            baselist = copy.copy(list)
            for j in range(len(list)):
                par.append(baselist.index(parents[i][j]))
                baselist.remove(parents[i][j])
            parent_order.append(par)

        # 交叉点以降の順序表現を交叉する
        parent_order[0][point:] = parent_order[1][point:]

        #順序表現からパス表現に逆変換
        for i in range(2):
            c = []
            baselist = copy.copy(list)
            for j in range(len(list)):
                c.append(baselist[parent_order[i][j]])
                baselist.pop(parent_order[i][j])
            child_pass.append(c)
        # 巡回判定関数にひっかかったらやり直し
        for i in range(2):
            if Patrolflag(child_pass[i],len(child_pass[i])) == 1:
                child_pass = []
                break

    for i in range(2):
        next_routelist.append(child_pass[i])


# 突然変異
def mutation():
    dna = []
    while len(dna) < 2:
        dn = []
        # 親を選択
        for i in range(2):
            dn.append(random.choice(routelist))
        
        for i in range(2):
            test = []
            # 突然変異（シャッフル）
            test = copy.copy(dn[i])
            test.remove(start)
            random.shuffle(test)
            test.insert(0,start)
            dna.append(test)
                
        # 巡回判定関数にひっかかったらやり直し
        for i in range(2):
            if Patrolflag(dna[i],len(dna[i])) == 1:
                dna = []
                break

    for i in range(2):
        next_routelist.append(dna[i])


# OpenStreetMap上にTPSの結果を描画し、HTMLファイルで保存する関数
def map_show(ansroute):
    # OpenStreetMapの表示位置
    map = folium.Map(location=[35.690163, 139.699187], zoom_start=5)
    WEIGHT = 5
    points = []

    # 駅情報をCSVファイルで読み込む
    name,lat,lon,pref = ReadCsv()

    # map上の駅座標にマーカーを配置する
    for i in range(len(lat)):
        folium.CircleMarker(
                            [lat[i][0], lon[i][0]],
                            radius=WEIGHT,
                            popup=name[i][0],
                            color='#3186cc',
                            fill_color='#3186cc',
                            ).add_to(map)
    
    for i in range(len(ansroute)):
        # ポリライン描画用タプルリストに駅座標を追加
        points.append(tuple([lat[ansroute[i]-1][0],lon[ansroute[i]-1][0]]))
    points.append(tuple([lat[ansroute[0]-1][0],lon[ansroute[0]-1][0]]))

    # 駅座標をポリラインで結ぶ
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(map)

    # HTMLファイルとして保存
    map.save('map.html')
    
    
    
num = numget()
Init(num)
cnt = 1
while cnt < generation:
    num = numget()
    mincost = 0
    ans = 0
    del compatible[:]
    del totalcostlist[:]
    if len(next_routelist) != 0:
        del routelist[:]
        routelist = copy.copy(next_routelist)
        del next_routelist[:]
    for i in range(num):
        totalcostlist.append(Getcost(routelist[i]))
    mincost = min(totalcostlist)
    ans = routelist[totalcostlist.index(mincost)]
    print ('************************ Number of generations : {} *************************'.format(cnt))
    pl.plot(cnt,mincost,"r.")
    comparison()
    print ('Fitness = {}'.format(compatible))
    print ('Minimum Cost = {}'.format(mincost))
    print ('Route = {}'.format(ans))
    elitecopy()
    crossover()
    mutation()
    cnt += 1

map_show(ans)
pl.title(u"minimum cost")
pl.ylabel(u"yen")
pl.xlabel(u"ganerations")
pl.show()

