from fasthtml.common import *
import httpx

async def auth_before(req,sess):
    token = req.cookies.get("access_token")
    if not token:
        return RedirectResponse('/login',status_code=303)
    
    async with httpx.AsyncClient() as client:
        res = await client.get('http://127.0.0.1:8000/auth/protected/',headers={"Authorization":f"Bearer {token}"})
    if res.status_code != 200:
        return RedirectResponse('/login',status_code=303)

    return


