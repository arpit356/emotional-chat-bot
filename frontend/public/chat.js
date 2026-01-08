const userId = 'u1';
const chatEl = document.getElementById('chat');
const micBtn = document.getElementById('mic');
const audioPlayer = document.getElementById('tts_player');
const botStatusEl = document.getElementById('bot_status');
const inputEl = document.getElementById('input');
const sendBtn = document.getElementById('send');

// Determine backend origin. If frontend served on a different port than 8000, use port 8000 as backend
const BACKEND_ORIGIN = (location.port && location.port !== '8000') ? `${location.protocol}//${location.hostname}:8000` : `${location.protocol}//${location.host}`;
const API = `${BACKEND_ORIGIN}/api/v1/message`;

function appendMessage(who, text){
  const div = document.createElement('div');
  div.className = who === 'user' ? 'message-user' : 'message-bot';
  div.innerHTML = `<b>${who === 'user' ? 'You' : 'Bot'}:</b> ${text}`;
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function setBotStatus(text, showSpinner=false){
  if(!botStatusEl) return;
  botStatusEl.innerText = text || '';
  botStatusEl.classList.toggle('hidden', !text);
  const sp = document.getElementById('stt_spinner');
  if(sp) sp.classList.toggle('hidden', !showSpinner);
}

async function sendTextMessage(text){
  appendMessage('user', text);
  // show typing indicator
  setBotStatus('Assistant is typing...', true);
  inputEl.disabled = true;
  sendBtn.disabled = true;
  try{
    const res = await fetch(API, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({user_id: userId, text})
    });
    if(!res.ok){
      // try to extract a useful message from JSON
      let detail = '';
      try{ const d = await res.json(); detail = d.detail || JSON.stringify(d); }catch(e){ detail = res.statusText }
      appendMessage('bot', `Server error: ${detail}`);
      return;
    }
    const data = await res.json();
    appendMessage('bot', data.text + ` <small>(${data.emotion.label})</small>`);
    if(data.tts_audio){
      playBase64Audio(data.tts_audio);
    }
  }catch(e){
    appendMessage('bot', `Network error: ${e.message || e}`);
    console.error(e);
  }finally{
    // clear typing indicator and re-enable
    setBotStatus('');
    inputEl.disabled = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

function playBase64Audio(b64){
  audioPlayer.src = `data:audio/mp3;base64,${b64}`;
  audioPlayer.hidden = false;
  audioPlayer.play();
}

sendBtn.onclick = () => {
  const text = inputEl.value.trim();
  if(!text) return;
  inputEl.value = '';
  sendTextMessage(text);
}

// allow Enter to send
inputEl.addEventListener('keydown', (e) => {
  if(e.key === 'Enter' && !e.shiftKey){
    e.preventDefault();
    sendBtn.click();
  }
});

// Microphone streaming recording using WebSocket
let mediaRecorder = null;
let ws = null;
let sttStatusEl = document.getElementById('stt_status');

function setSttStatus(text){
  sttStatusEl.innerText = text || '';
}

micBtn.onmousedown = async () => {
  if(!navigator.mediaDevices) return alert('No media devices available');
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  // open websocket for streaming STT to backend origin
  const wsProto = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const backendHost = new URL(BACKEND_ORIGIN).host;
  const wsUrl = `${wsProto}//${backendHost}/api/v1/ws/stt/${userId}`;
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    setSttStatus('Recording...');
  }
  ws.onerror = (ev) => {
    setSttStatus('STT connection error');
    console.error('STT websocket error', ev);
  }
  ws.onclose = (ev) => {
    if(ev && ev.code !== 1000){
      setSttStatus('STT disconnected');
    }
  }
  let _partialTimer = null;
  function showSpinner(show){
    const sp = document.getElementById('stt_spinner');
    if(!sp) return;
    sp.classList.toggle('hidden', !show);
  }

  ws.onmessage = (evt) => {
    try{
      const d = JSON.parse(evt.data);
      if(d.type === 'ready'){
        // ready to receive chunks
      } else if(d.type === 'partial'){
        // Show spinner immediately and debounce the displayed partial text to reduce flicker
        showSpinner(true);
        setSttStatus('Transcribing...');
        if(_partialTimer) clearTimeout(_partialTimer);
        _partialTimer = setTimeout(()=>{
          setSttStatus('Transcribing: ' + (d.text || ''));
          showSpinner(false);
          _partialTimer = null;
        }, 400);
      } else if(d.type === 'final'){
        // clear any pending partial timer and spinner
        if(_partialTimer){ clearTimeout(_partialTimer); _partialTimer = null; }
        showSpinner(false);
        setSttStatus('Final: ' + (d.text || ''));
        // send final text to the normal message flow to get bot response
        sendTextMessage(d.text || '');
      } else if(d.type === 'error'){
        if(_partialTimer){ clearTimeout(_partialTimer); _partialTimer = null; }
        showSpinner(false);
        setSttStatus('STT error: ' + (d.detail || ''));
      }
    }catch(e){
      console.error('WS msg parse error', e);
    }
  }
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.ondataavailable = async (e) => {
    if(e.data && e.data.size > 0 && ws && ws.readyState === WebSocket.OPEN){
      const reader = new FileReader();
      reader.onloadend = () => {
        const dataUrl = reader.result;
        const b64 = dataUrl.split(',')[1];
        ws.send(JSON.stringify({type: 'chunk', audio_b64: b64}));
      }
      reader.readAsDataURL(e.data);
    }
  }
  // request chunks every 700ms
  mediaRecorder.start(700);
  micBtn.innerText = '🔴';
}

micBtn.onmouseup = async () => {
  if(!mediaRecorder) return;
  // stop recorder and ask server for final transcript
  mediaRecorder.stop();
  micBtn.innerText = '🎙️';
  if(ws && ws.readyState === WebSocket.OPEN){
    ws.send(JSON.stringify({type: 'final'}));
    // close after a short delay to receive final
    setTimeout(()=>{ try{ ws.send(JSON.stringify({type:'close'})); ws.close(); }catch(e){} }, 1000);
  }
}

micBtn.onmouseleave = () => {
  if(mediaRecorder && mediaRecorder.state === 'recording'){
    mediaRecorder.stop();
    micBtn.innerText = '🎙️';
    if(ws && ws.readyState === WebSocket.OPEN){
      ws.send(JSON.stringify({type: 'final'}));
      setTimeout(()=>{ try{ ws.send(JSON.stringify({type:'close'})); ws.close(); }catch(e){} }, 1000);
    }
  }
}

// focus input on load
window.addEventListener('load', () => { if(inputEl) inputEl.focus(); });
