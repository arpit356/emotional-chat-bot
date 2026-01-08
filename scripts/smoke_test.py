import asyncio
import sys, os
# allow running script from project root without installing package
root = os.path.dirname(os.path.dirname(__file__))
# add backend path so 'app' package can be imported
sys.path.append(os.path.join(root, 'backend'))
from app.db import database
from app.api.v1.messaging import handle_message

async def main():
    database.init_db()
    database.ensure_user_exists('u1')
    class Msg:
        def __init__(self, text):
            self.user_id = 'u1'
            self.text = text
            self.audio_b64 = None
            self.session_id = 's1'
    res = await handle_message(Msg('I am feeling sad today'))
    print('Sad message response:', res)
    # test reminder
    res2 = await handle_message(Msg('Remind me to call mom tomorrow'))
    print('Reminder response:', res2)
    print('Memories:', database.get_memories('u1'))

if __name__ == '__main__':
    asyncio.run(main())
