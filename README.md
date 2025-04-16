# -Discord Ticket Bot  
Advance Ticket Bot For Discord  

# 🤖 Discord Ticket Bot

Advance Ticket Bot For Discord  

---

## ⚙️ Step 1: Discord Developer Portal par Bot Banao

1. Apne browser me ye link khol lo:  
   🔗 [https://discord.com/developers/applications](https://discord.com/developers/applications)

2. **"New Application"** button pe click karo.

3. Apne bot ka naam daalo (jaise: `DestroyerBot`)  
   ➤ Fir **"Create"** pe click karo.

---

### 🔐 Step 2: Bot ka Token lo (IMPORTANT!)

"Bot" section me neeche aake **Token** dikh raha hoga.

- **"Reset Token"** dabao (agar pehle kabhi use hua ho)  
- Fir **"Copy"** dabao — _ye hi bot ka token hai._

> ⚠️ **Token kisi ko mat dena** — ye password jaise hota hai!

---

## 🔗 Step 3: Bot ko Discord Server me Add karo

1. Left sidebar me jao aur **OAuth2** > **URL Generator** section open karo.

2. **Scopes** me ye tick karo:
   - ✅ `bot`
   - ✅ `applications.commands` (agar slash commands chahiye ho)

3. Neeche scroll karo aur **Bot Permissions** select karo (jo chahiye), jaise:
   - ✅ `Administrator`  
     _ya specific permissions like `Manage Messages`, `Kick Members`, etc._

4. Niche ek **Generated URL** milega.

5. Us URL ko copy karo aur browser me open karo.

6. Ab tu **apna server select** karega jaha bot add karna hai.

7. URL ko server me paste karo aur open karo.

8. ✅ **"Authorize"** dabao aur captcha complete karo.

> 🎉 Tumhara bot ab server me add ho gaya!  
> Lekin abhi bot kuch nahi karega kyunki abhi tak usme code nahi dala gaya hai. Follow the next steps! 👇

---

## 💻 Step 4: Code Editor Setup & Bot Configuration

### 🧠 1. Code Editor Install Karo
- **VS Code** ya **PyCharm** install karo.

### 📝 2. Python File Banao
- File ka naam kuch bhi ho sakta hai jaise: `destroyerbot.py`

### 📋 3. Code Paste Karo
- Apna bot code is file me paste kar do.

---

## 🔑 Step 5: Token Dalna (Line 184)

- Line 184 me jaake apna token yaha daalo:
- line 148 to 158 you can customize rule for the ticket or add any message
- in line 163 you can add any gif
- in line 89 you can add after ticket created message `\n` used for new line
- in line 28 to 38 you can change dropdown channel name and its description.

Run the Bot and enjoy 
-use /setup_ticket cmd for ticket setup

```python
bot.run("discord bot token")"
