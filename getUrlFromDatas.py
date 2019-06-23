def getUrlFromDatas(text):
    datas = text.split('datas=')[1].split(';')[0].split("('")[1].split("')")[0].split('*')
    a=""
    for d in datas:
        if d!='':
            a = a+chr(int(d))
    return a.split('&')[0]