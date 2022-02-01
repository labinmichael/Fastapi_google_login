from fastapi import FastAPI,status
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth,OAuthError
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi import Request
import json
from fastapi import HTTPException
from starlette.responses import JSONResponse



app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config('.env')
oauth = OAuth(config)



CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

'''
@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        '''
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )'''
        return RedirectResponse()
    #return HTMLResponse("/login")
    return RedirectResponse(url='/login')

'''
    
    
    
 @app.get('/')
def test():
    return "server start"

@app.get('/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)




@app.get('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        ) 


    user_data = await oauth.google.parse_id_token(request, access_token)
    # TODO: validate email in our database and generate JWT token
    jwt = f'sample jwt {user_data["email"]}'
    # TODO: return the JWT token to the user so it can make requests to our /api endpoint
    return JSONResponse({'data':user_data,'result': True, 'access_token': jwt})
   
       

@app.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')

