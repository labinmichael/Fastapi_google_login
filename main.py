from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi import Request
import json




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



@app.get('/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


        