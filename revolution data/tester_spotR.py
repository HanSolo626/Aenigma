
h = [
    [(23,7),0,70,0]
    # (x, y),type,size,V_H
    ]


a = [(23,7),0,70,0]
b = [(23,7),0,70,1]
print(a == b)


# prop data
p = [
    [(5, 6), 4],
    [(5, 5), 6],
    [(40, 5), 5],
# [img num, (x, y)]
]

def get_prop_num(e):
    return e[0][1]
p.sort(key=get_prop_num)
print(p)