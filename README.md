# NCU_Oauth_with_Flask

先到 Portal 右上角的 Apps 申請一個新的應用程式，取得 client id 與 client secret

在 App 的編輯頁面 Return To Address (也就是 Redirect_uri ) 設定為自己的 domain 網址。 

EX: http://127.0.0.1:5000/auth

```python
#-*- encoding: UTF-8 -*-

from flask import Flask, session, request, redirect, jsonify

# Our oauth
from ncu_oauth import oauth

NCU_APP_REDIRECT_URI = 'http://127.0.0.1:5000/auth' 
NCU_APP_CLIENT_ID = 'your client id' 
NCU_APP_CLIENT_SECRET = 'your client secret'

app = Flask(__name__)
app.secret_key = 'your secrey key'
app.config['JSON_AS_ASCII'] = False

# make a oauth init
ncu = oauth.Oauth(
    redirect_uri=NCU_APP_REDIRECT_URI, 
    client_id=NCU_APP_CLIENT_ID, 
    client_secret=NCU_APP_CLIENT_SECRET
)


@app.route("/")
def home():
    # check if login
    if session.get('logged_in'):
        # get user profile
        return jsonify(ncu.get_profile())
            
    return redirect('/login')

@app.route('/login')
def login():
    # redirect to ncu auth dialog
    return ncu.authorize()

@app.route('/auth')
def auth():
    # user code for getting token
    code=request.args.get('code')
    if code:
        if ncu.get_token(code):
            print("got token")
            return redirect('/')
    
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
```

到 https://portal.ncu.edu.tw/about/howto 查看自己想要取得的 scope 

在 oauth.py 中 ``` get_cdoe_url ``` 的 scope=加上自己想要的項目 (項目要兩個以上，只有一個會出錯，我也不知道為什麼= =)

p.s.記得在 Portal Apps 的介面勾選自己想開通什麼 scopes 
```python  
get_code_url = OAUTH_URL + '/oauth2/authorization?response_type=code&scope=identifier+chinese-name&client_id='+self.client_id+'&redirect_uri='+self.redirect_uri
```
成功取得資訊後應該會得到類似下面的 json 資料

```json
{
    "accountType": "STUDENT",
    "chineseName": "周校長",
    "englishName": "Jay Chou",
    "gender": "1",
    "id": 156848316516847,
    "identifier": "10804055555",
    "studentId": "10804055555"
}

```




