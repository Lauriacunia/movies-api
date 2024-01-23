import email
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jwt import encode, decode
from config import settings

#ENCODED =  PAYLOAD + SECRET + ALGORITMO HS256
def create_access_token(data: dict) -> str:
    return encode(data, settings.SECRET_KEY, algorithm="HS256")

#PAYLOAD  =  ENCODED + SECRET + ALGORITMO HS256
def decode_access_token(token: str) -> dict:
    return decode(token, settings.SECRET_KEY, algorithms=["HS256"])

class JWTBearer(HTTPBearer):
    
    async def __call__(self, request: Request): 
        auth= await super(JWTBearer, self).__call__(request)
        token = auth.credentials # str 
        #convertir el token str en un diccionario
        token_dict = eval(token)
        token = token_dict['access_token']
        data = decode_access_token(token)
        if not data:
           raise HTTPException(status_code=403, detail="Invalid authorization code.")
        if data['email'] != "admin@admin":
            raise HTTPException(status_code=403, detail="Invalid user.")
        return data
    