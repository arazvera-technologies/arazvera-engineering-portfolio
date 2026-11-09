"""Synthetic public Level 2 FastAPI contract, in-process only.

No server starts at import. Customer access requires separate trusted IdP
integration, secret management, TLS ingress, RLS review and deployment approval.
"""
from __future__ import annotations
import json
from typing import Any

import psycopg
from fastapi import FastAPI,Header,HTTPException,Path,Query,Request
from pydantic import BaseModel,Field

from storage import Conflict,Denied,PgStore
from token_verify import TokenError,TokenVerifier

class RecordWrite(BaseModel):
    payload:dict[str,Any]
    expected_version:int=Field(ge=0,le=2_147_483_000)

def build_app(store:PgStore,jwks:dict,issuer:str,audience:str)->FastAPI:
    if not isinstance(store,PgStore):raise ValueError("Explicit PostgreSQL store required")
    verifier=TokenVerifier(jwks,issuer,audience)
    app=FastAPI(title="ARAZVERA Public Level 2 Authorized Postgres Lab",
        description="Synthetic integration case, NOT approved for production",
        version="0.1.0",docs_url=None,redoc_url=None,openapi_url=None)

    @app.middleware("http")
    async def secure_headers(request:Request,call_next):
        response=await call_next(request)
        response.headers["Cache-Control"]="no-store"
        response.headers["X-Content-Type-Options"]="nosniff"
        return response

    @app.get("/health")
    def health():
        return {"status":"ok","synthetic":True,"production_approved":False}

    def principal(authorization:str|None):
        if not authorization or not authorization.startswith("Bearer ") or authorization.count(" ")!=1:
            raise HTTPException(401,"Authentication required",headers={"WWW-Authenticate":"Bearer"})
        try:return verifier.verify(authorization[7:])
        except TokenError as exc:
            raise HTTPException(401,"Invalid access token",headers={"WWW-Authenticate":"Bearer"}) from exc

    def run_db(job):
        try:return job()
        except Denied as exc:raise HTTPException(403,"Tenant permission denied") from exc
        except Conflict as exc:raise HTTPException(409,"Conflict with current state") from exc
        except (ValueError,TypeError,OverflowError) as exc:
            raise HTTPException(422,"Invalid submitted data") from exc
        except psycopg.Error as exc:
            raise HTTPException(503,"Service temporarily unavailable") from exc

    TENANT=Path(pattern=r"^[a-z][a-z0-9-]{1,39}$")
    RECORD=Path(pattern=r"^[A-Za-z0-9._:-]{2,100}$")

    @app.get("/v1/tenants/{tenant}/records")
    def list_records(tenant:str=TENANT,limit:int=Query(20,ge=1,le=100),
                     offset:int=Query(0,ge=0,le=10000),
                     authorization:str|None=Header(None)):
        actor=principal(authorization)
        return run_db(lambda:store.list_records(actor,tenant,limit,offset))

    @app.get("/v1/tenants/{tenant}/records/{record}")
    def get_record(tenant:str=TENANT,record:str=RECORD,
                   authorization:str|None=Header(None)):
        actor=principal(authorization)
        row=run_db(lambda:store.get_record(actor,tenant,record))
        if row is None:raise HTTPException(404,"Record not found")
        return row

    @app.put("/v1/tenants/{tenant}/records/{record}")
    def put_record(body:RecordWrite,tenant:str=TENANT,record:str=RECORD,
                   idempotency_key:str|None=Header(None,alias="Idempotency-Key"),
                   authorization:str|None=Header(None)):
        actor=principal(authorization)
        if not idempotency_key or len(idempotency_key)>100:
            raise HTTPException(422,"Valid Idempotency-Key required")
        result=run_db(lambda:store.put_record(actor,tenant,record,body.payload,
                                             body.expected_version,idempotency_key))
        from fastapi.responses import JSONResponse
        return JSONResponse(result["receipt"],
                    status_code=200 if result["replayed"] or body.expected_version>0 else 201)
    return app
