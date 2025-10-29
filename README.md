# FreeFire Like System - Full Version 🚀

## ✨ Features

✅ **Uses ALL available tokens** - No limit! All tokens in your JSON file will be utilized  
✅ **100 likes per ID** - Each user ID receives exactly 100 likes  
✅ **Efficient token rotation** - Every 100 tokens handles 30 different IDs  
✅ **Multi-server support** - IND, BR, US, SAC, NA servers  
✅ **Vercel deployment ready** - Deploy to Vercel with one click  
✅ **Real-time capacity tracking** - Know exactly how many IDs you can handle  

---

## 📊 System Logic

### How It Works:
- **Every 100 tokens** → can handle **30 IDs**
- **Each ID** receives **100 likes**
- Tokens are **rotated/recycled** efficiently using modulo operation
- Same token can be used for multiple IDs

### Capacity Calculation:
```
Formula: (Total Tokens ÷ 100) × 30 = Total IDs you can handle
```

### Examples:
| Tokens | Calculation | IDs You Can Handle |
|--------|-------------|-------------------|
| 1000 | (1000 ÷ 100) × 30 | 300 IDs |
| 3000 | (3000 ÷ 100) × 30 | 900 IDs |
| 5000 | (5000 ÷ 100) × 30 | 1500 IDs |
| 10000 | (10000 ÷ 100) × 30 | 3000 IDs |

---

## 🚀 Quick Start

### 1. Add Your Tokens
Put your tokens in the appropriate file inside the `tokens/` folder:

**For India Server:**
```json
// tokens/token_ind.json
[
  {"token": "your_actual_token_1"},
  {"token": "your_actual_token_2"},
  {"token": "your_actual_token_3"},
  ...
]
```

**For Brazil/US/SAC/NA Servers:**
```json
// tokens/token_br.json
[
  {"token": "your_actual_token_1"},
  {"token": "your_actual_token_2"},
  ...
]
```

### 2. Run Locally
```bash
python app.py
```

Server will start on: `http://localhost:5000`

### 3. Use the API

**API Endpoint:**
```
GET /like?uid=<USER_ID>&server=<SERVER>
```

**Parameters:**
- `uid` - The FreeFire user ID to send likes to
- `server` - Server region (IND, BR, US, SAC, or NA)

**Example Request:**
```
http://localhost:5000/like?uid=1234567890&server=IND
```

---

## 📤 API Response

```json
{
  "credits": "em.official.team",
  "likes_added": 100,
  "likes_before": 450,
  "likes_after": 550,
  "player": "PlayerName",
  "uid": 1234567890,
  "status": 1,
  "total_tokens_available": 5000,
  "likes_sent_to_this_id": 100,
  "likes_per_id": 100,
  "tokens_per_batch": 100,
  "ids_per_batch": 30,
  "total_batches": 50,
  "max_ids_can_handle": 1500,
  "info": "Every 100 tokens handles 30 IDs. With 5000 tokens, you can send 100 likes to 1500 different IDs"
}
```

### Response Fields:
- `likes_added` - How many likes were successfully added
- `likes_before` - Likes before this request
- `likes_after` - Likes after this request
- `total_tokens_available` - Total tokens in your JSON file
- `likes_sent_to_this_id` - Likes sent in this request (should be 100)
- `max_ids_can_handle` - Maximum IDs you can process with your tokens
- `status` - 1 = Success, 2 = Failed

---

## 🌐 Supported Servers

| Server Code | Region | URL |
|-------------|--------|-----|
| IND | India | client.ind.freefiremobile.com |
| BR | Brazil | client.us.freefiremobile.com |
| US | United States | client.us.freefiremobile.com |
| SAC | South America | client.us.freefiremobile.com |
| NA | North America | client.us.freefiremobile.com |

---

## 🔧 Project Structure

```
.
├── app.py                    # Main Flask application
├── config.py                 # Server URLs and file mappings
├── like_pb2.py              # Protobuf message for likes
├── like_count_pb2.py        # Protobuf message for like counts
├── uid_generator_pb2.py     # Protobuf message for UID generation
├── requirements.txt         # Python dependencies
├── vercel.json              # Vercel deployment config
├── .gitignore               # Git ignore rules
└── tokens/                  # Token storage directory
    ├── token_ind.json       # India server tokens
    └── token_br.json        # Brazil/US/SAC/NA server tokens
```

---

## 🚀 Deploy to Vercel

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Deploy
```bash
vercel deploy
```

### Step 3: Production Deploy
```bash
vercel --prod
```

Your API will be live at: `https://your-project.vercel.app/like?uid=...&server=...`

---

## 📦 Dependencies

- **Flask** - Web framework
- **aiohttp** - Async HTTP requests for better performance
- **pycryptodome** - AES encryption for secure communication
- **protobuf** - Protocol buffer serialization
- **requests** - HTTP library
- **urllib3** - HTTP client

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 🔒 Security Features

- ✅ AES encryption for all API requests
- ✅ Secure token management
- ✅ No tokens exposed in responses
- ✅ SSL verification disabled for specific endpoints
- ✅ Bearer token authentication

**Encryption Details:**
- Algorithm: AES CBC mode
- Key: `Yg&tc%DEuh6%Zc^8`
- IV: `6oyZDr22E3ychjM%`

---

## 💡 Tips

1. **More Tokens = More IDs**: Add as many tokens as you want - the system will use ALL of them!
2. **Check Capacity**: The API response tells you exactly how many IDs you can handle
3. **Token Format**: Make sure your tokens are in the correct JSON format
4. **Server Selection**: Use the correct server code for your region

---

## 🎯 Example Usage

### With 5000 Tokens:

**Request:**
```bash
curl "http://localhost:5000/like?uid=1234567890&server=IND"
```

**What Happens:**
- System loads all 5000 tokens
- Sends 100 likes to UID 1234567890
- Uses token rotation for efficiency
- Tells you that you can handle 1500 more IDs

**Capacity:**
- Total tokens: 5000
- Batches: 50 (5000 ÷ 100)
- IDs per batch: 30
- Total capacity: 1500 IDs (50 × 30)

---

## ❓ FAQ

**Q: Will all my tokens be used?**  
A: YES! The system uses ALL tokens in your JSON file with efficient rotation.

**Q: How many likes does each ID get?**  
A: Exactly 100 likes per ID.

**Q: Can I add more tokens later?**  
A: Yes! Just add them to your JSON file and restart the server.

**Q: What if I have 10,000 tokens?**  
A: You can handle 3000 different IDs (10000 ÷ 100 × 30 = 3000 IDs)!

---

## 📝 Credits

**Original Team:** em.official.team  
**Modified:** October 28, 2025 - Full token utilization system  
**Version:** 2.0 - Complete Edition

---

## 🎉 Ready to Use!

Your system is now ready! Just:
1. ✅ Add your tokens to the JSON files
2. ✅ Run `python app.py`
3. ✅ Start sending likes to unlimited IDs!

**No limits. No restrictions. Use ALL your tokens!** 🚀
