import pandas as pd

### =================================================================================

def intersect(*lists):
    return list(set.intersection(*map(set, lists)))

def logCollection(col,log='log.txt'):
    log = open(log,'a')
    for entry in col:
        log.write(str(entry)+"\n")
    log.close()
    return

### =================================================================================

df_04 = pd.read_csv("data/data/top_pan_2500_04_w1.csv")
df_05 = pd.read_csv("data/data/top_pan_2500_05_w1.csv")
df_06 = pd.read_csv("data/data/top_pan_2500_06_w1.csv")
df_07 = pd.read_csv("data/data/top_pan_2500_07_w1.csv")
df_08 = pd.read_csv("data/data/top_pan_2500_08_w1.csv")
df_09 = pd.read_csv("data/data/top_pan_2500_09_w1.csv")

list_04 = df_04['pan'].tolist()
list_05 = df_05['pan'].tolist()
list_06 = df_06['pan'].tolist()
list_07 = df_07['pan'].tolist()
list_08 = df_08['pan'].tolist()
list_09 = df_09['pan'].tolist()

list_all = intersect(list_04,list_05,list_06,list_07,list_08,list_09)

logCollection(list_all,'top_pan_semester.txt')

# print len(list_all)
