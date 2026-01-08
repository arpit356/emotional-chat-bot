from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import base64
from app.services import stt as stt_svc

router = APIRouter()

@router.websocket("/ws/stt/{user_id}")
async def websocket_stt(websocket: WebSocket, user_id: str):
    await websocket.accept()
    # buffer of base64 chunks
    buffer = []
    try:
        await websocket.send_json({"type": "ready", "message": "send chunks with type=chunk and a final message with type=final"})
        while True:
            data = await websocket.receive_json()
            msg_type = data.get('type')
            if msg_type == 'chunk':
                audio_b64 = data.get('audio_b64')
                # try quick partial transcription of this chunk
                try:
                    partial = stt_svc.transcribe_audio_base64(audio_b64).get('text', '')
                    # send partial back to client
                    await websocket.send_json({"type": "partial", "text": partial})
                except Exception as e:
                    await websocket.send_json({"type": "error", "detail": str(e)})
                buffer.append(audio_b64)
            elif msg_type == 'final':
                # combine chunks and perform a final transcription
                try:
                    combined = b''.join([base64.b64decode(b) for b in buffer])
                    final = stt_svc.transcribe_audio_bytes(combined).get('text', '')
                    await websocket.send_json({"type": "final", "text": final})
                except Exception as e:
                    await websocket.send_json({"type": "error", "detail": str(e)})
                buffer = []
            elif msg_type == 'close':
                await websocket.send_json({"type": "closed"})
                await websocket.close()
                break
            else:
                await websocket.send_json({"type": "error", "detail": "unknown message type"})
    except WebSocketDisconnect:
        # client disconnected
        return
    except Exception:
        try:
            await websocket.send_json({"type": "error", "detail": "server error"})
        except Exception:
            pass
        return
