from typing import Optional, Dict, Any, List, Callable, Union
from surrealdb.connections.async_ws import AsyncWsSurrealConnection
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from surrealdb import RecordID
import json

from app.models.account import AccountModel, Account, Auth
from app.db import db
from app.repositories.account import AccountRepository

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths: List[str] = []):
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/account/login", "/account/register" ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path

        for exclude_path in self.exclude_paths:
            if path.startswith(exclude_path):           
                return await call_next(request)
        
        if request.method == "GET":
            query_params = dict(request.query_params)
            if "username" not in query_params or "token" not in query_params:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Missing authentication credentials"}
                )
            
            auth = Auth(username=query_params["username"], token=query_params["token"])
            if not await AccountRepository.verify_auth(db, auth.username, auth.token):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid authentication credentials"}
                )
            
            request.state.auth = auth
            
            return await call_next(request)
        else:
            body_bytes = await request.body()
            
            if not body_bytes:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Missing request body"}
                )
            
            try:
                body = json.loads(body_bytes)
            except:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Invalid request body"}
                )

        if "auth" not in body:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing authentication credentials"}
            )
        
        try:
            auth = Auth(**body["auth"])
        except:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication format"}
            )
        
        if not await AccountRepository.verify_auth(db, auth.username, auth.token):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authentication credentials"}
            )
        
        request.state.auth = auth
        
        if request.method == "GET":
            request.state.params = body.get("params", {})
        else:
            request.state.data = body.get("data", {})
            await request.body()
            setattr(request, "_body", json.dumps(body.get("data", {})).encode())
            
        return await call_next(request)
