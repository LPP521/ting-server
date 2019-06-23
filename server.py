from aiohttp import web
from ting89 import Ting89
from woai import Woai

GTing89 = Ting89()
Wa = Woai()

async def handle(request):
    return web.Response(text='only post support')

async def searchHandler(request):
    inData = await request.json()
    inName = inData['name']

    # print('searching',inName)
    data1 = GTing89.search(inName)
    data2 = Wa.search(inName)
    outData = [{'mod':'ting89','data':data1},
                {'mod':'woai','data':data2}]
    return web.json_response(outData)

async def getModListHandler(request):
    outData = [{'name':'ting89'}]
    return web.json_response(outData)

async def getAlbumDataHandler(request):
    inData = await request.json()
    inMod = inData['mod']
    inUrl = inData['url']
    print('getAlbumDataHandler',inUrl)
    if inMod=='ting89':
        outData = GTing89.getAlbumData(inUrl)
        return web.json_response(outData)
    if inMod=='woai':
        outData = Wa.getAlbumData(inUrl)
        return web.json_response(outData)

async def getMP3URLHandler(request):
    inData = await request.json()
    inMod = inData['mod']
    inUrl = inData['url']
    inIndex = inData['index']
    print('getMP3URLHandler',inUrl)
    if inMod=='ting89':
        outData = GTing89.getUrl(inUrl,inIndex)
        return web.json_response(outData)
    if inMod=='woai':
        outData = Wa.getUrl(inUrl,inIndex)
        return web.json_response(outData)

def app(args=()):
    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.post('/search',searchHandler),
                    web.post('/getmodlist',getModListHandler),
                    web.post('/getalbumData',getAlbumDataHandler),
                    web.post('/getmp3url',getMP3URLHandler)])
    return app


# web.run_app(app)