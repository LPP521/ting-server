from aiohttp import web
from ting89 import Ting89

GTing89 = Ting89()

async def handle(request):
    return web.Response(text='only post support')

async def post_handler(request):
    data = await request.json()
    print(data)
    print(data['title'])
    return web.Response(text='abc')

async def getModListHandler(request):
    outData = [{'name':'ting89'}]
    return web.json_response(outData)

async def getMP3ListHandler(request):
    inData = await request.json()
    inMod = inData['mod']
    inUrl = inData['url']
    if inMod=='ting89':
        outData = GTing89.getList(inUrl)
        return web.json_response(outData)   

async def getMP3URLHandler(request):
    inData = await request.json()
    inMod = inData['mod']
    inUrl = inData['url']
    inIndex = inData['index']
    if inMod=='ting89':
        outData = GTing89.getUrl(inUrl,inIndex)
        return web.json_response(outData)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.post('/getmodlist',getModListHandler),
                web.post('/getmp3list',getMP3ListHandler),
                web.post('/getmp3url',getMP3URLHandler)])

web.run_app(app)