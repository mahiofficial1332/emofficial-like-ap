from flask import Flask, request, jsonify
import asyncio, json, binascii, requests, aiohttp, urllib3, threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf.json_format import MessageToJson
from google.protobuf.message import DecodeError
import like_pb2, like_count_pb2, uid_generator_pb2
from config import URLS_INFO ,URLS_LIKE,FILES

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

# --- Global Lock for token assignment ---
token_lock = threading.Lock()
token_index = 0

def load_tokens(server):
    files = FILES
    return json.load(open(f"tokens/{files.get(server,'token_bd.json')}"))

def get_headers(token):
    return {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB50",
    }

def encrypt_message(data):
    cipher = AES.new(b'Yg&tc%DEuh6%Zc^8', AES.MODE_CBC, b'6oyZDr22E3ychjM%')
    return binascii.hexlify(cipher.encrypt(pad(data, AES.block_size))).decode()

def create_like(uid, region):
    m = like_pb2.like()
    m.uid, m.region = int(uid), region
    return m.SerializeToString()

def create_uid(uid):
    m = uid_generator_pb2.uid_generator()
    m.saturn_, m.garena = int(uid), 1
    return m.SerializeToString()

async def send(token, url, data):
    headers = get_headers(token)
    async with aiohttp.ClientSession() as s:
        async with s.post(url, data=bytes.fromhex(data), headers=headers) as r:
            return await r.text() if r.status == 200 else None

async def multi(uid, server, url):
    global token_index
    enc = encrypt_message(create_like(uid, server))
    tokens = load_tokens(server)

    # প্রতি রিকোয়েস্টে নতুন 100 টোকেন সিলেক্ট করা হবে
    with token_lock:
        start = token_index
        end = token_index + 100
        token_index = end if end < len(tokens) else 0

    selected = tokens[start:end] if end <= len(tokens) else tokens[start:] + tokens[:end - len(tokens)]

    # এখন 100 টোকেন দিয়ে 100 লাইক পাঠানো হবে
    tasks = [send(t["token"], url, enc) for t in selected]
    results = await asyncio.gather(*tasks)
    return len([r for r in results if r is not None])

def get_info(enc, server, token):
    urls = URLS_INFO
    r = requests.post(
        urls.get(server, "https://clientbp.ggblueshark.com/GetPlayerPersonalShow"),
        data=bytes.fromhex(enc),
        headers=get_headers(token),
        verify=False
    )
    try:
        p = like_count_pb2.Info()
        p.ParseFromString(r.content)
        return p
    except DecodeError:
        return None

@app.route("/like")
def like():
    uid = request.args.get("uid")
    server = request.args.get("server", "").upper()
    if not uid or not server:
        return jsonify(error="UID and server required"), 400

    tokens = load_tokens(server)
    enc = encrypt_message(create_uid(uid))
    before, tok = None, None

    for t in tokens[:10]:
        before = get_info(enc, server, t["token"])
        if before:
            tok = t["token"]
            break

    if not before:
        return jsonify(error="Player not found"), 500

    before_like = int(json.loads(MessageToJson(before)).get('AccountInfo', {}).get('Likes', 0))
    urls = URLS_LIKE

    added = asyncio.run(multi(uid, server, urls.get(server, "https://clientbp.ggblueshark.com/LikeProfile")))

    after = json.loads(MessageToJson(get_info(enc, server, tok)))
    after_like = int(after.get('AccountInfo', {}).get('Likes', 0))

    return jsonify({
        "credits": "emofficial.team.com",
        "likes_added": added,
        "likes_before": before_like,
        "likes_after": after_like,
        "player": after.get('AccountInfo', {}).get('PlayerNickname', ''),
        "uid": after.get('AccountInfo', {}).get('UID', 0),
        "status": 1 if added else 2,
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)









    
#URL_ENPOINTS ="http://127.0.0.1:5000/like?uid=13002831333&server=me"
#credits : "emofficial.team.com/"
