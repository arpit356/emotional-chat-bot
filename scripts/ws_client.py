import asyncio
import json

async def test():
    try:
        import websockets
    except Exception as e:
        print('websockets not installed:', e)
        return
    uri = 'ws://127.0.0.1:8000/api/v1/ws/stt/u1'
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({'type':'chunk','audio_b64':''}))
        print('sent chunk')
        msg = await ws.recv()
        print('recv:', msg)
        await ws.send(json.dumps({'type':'final','audio_b64':''}))
        print('sent final')
        msg = await ws.recv()
        print('recv:', msg)
        await ws.send(json.dumps({'type':'close'}))
        print('sent close')

if __name__ == '__main__':
    asyncio.run(test())
