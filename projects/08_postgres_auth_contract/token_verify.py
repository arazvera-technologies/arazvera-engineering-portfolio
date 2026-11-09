"""Offline RS256 token verifier for a synthetic authorized-integration example.

Not an identity provider, OAuth login, or live key discovery. Trusts only
the startup-supplied JWKS; never trusts token-supplied URLs or algorithms.
"""
import base64,json,re,time
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding,rsa

_IDENT=re.compile(r"^[a-z][a-z0-9-]{1,39}$")
_SUB=re.compile(r"^[A-Za-z0-9._:-]{1,100}$")
_KID=re.compile(r"^[A-Za-z0-9._:-]{1,100}$")
_B64=re.compile(r"^[A-Za-z0-9_-]+$")

class TokenError(PermissionError):pass

def decode(value):
    if not isinstance(value,str) or not 1<=len(value)<=8192 or not _B64.fullmatch(value):
        raise TokenError("Unauthorized")
    try:
        blob=base64.urlsafe_b64decode(value+"="*((-len(value))%4))
        if base64.urlsafe_b64encode(blob).rstrip(b"=").decode()!=value:
            raise ValueError("Non-canonical token")
        return blob
    except (ValueError,base64.binascii.Error) as exc:
        raise TokenError("Unauthorized") from exc

def unique_json(raw):
    def pairs(seq):
        result={}
        for k,v in seq:
            if k in result:raise ValueError("Duplicate key")
            result[k]=v
        return result
    try:
        val=json.loads(raw,object_pairs_hook=pairs)
        if not isinstance(val,dict):raise ValueError("JWT JSON object required")
        return val
    except (ValueError,UnicodeDecodeError) as exc:raise TokenError("Unauthorized") from exc

class TokenVerifier:
    def __init__(self,jwks,issuer,audience):
        if not isinstance(issuer,str) or not issuer.startswith("https://") or not isinstance(audience,str) or not audience:
            raise ValueError("Trusted HTTPS issuer and audience required")
        if not isinstance(jwks,dict) or not isinstance(jwks.get("keys"),list):
            raise ValueError("Preapproved JWKS required")
        self.issuer=issuer;self.audience=audience;self.keys={}
        for item in jwks["keys"]:
            if not isinstance(item,dict) or item.get("kty")!="RSA" or item.get("alg")!="RS256" or item.get("use")!="sig":
                raise ValueError("Unexpected key metadata")
            kid=item.get("kid")
            if not isinstance(kid,str) or not _KID.fullmatch(kid) or kid in self.keys:
                raise ValueError("Key ID missing or duplicate")
            numbers=rsa.RSAPublicNumbers(int.from_bytes(decode(item["e"]),"big"),int.from_bytes(decode(item["n"]),"big"))
            k=numbers.public_key()
            if k.key_size<2048:raise ValueError("RSA key too small")
            self.keys[kid]=k
        if not self.keys:raise ValueError("At least one public key required")

    def verify(self,token,now=None):
        if not isinstance(token,str) or not 10<=len(token)<=12000 or token.count(".")!=2:
            raise TokenError("Unauthorized")
        raw_header,raw_payload,raw_sig=token.split(".")
        h=unique_json(decode(raw_header));claims=unique_json(decode(raw_payload))
        if h.get("typ")!="at+jwt" or h.get("alg")!="RS256":
            raise TokenError("Unauthorized")
        if any(k in h for k in ("jku","x5u","crit","jwk")):
            raise TokenError("Unauthorized")
        key=self.keys.get(h.get("kid"))
        if key is None:raise TokenError("Unauthorized")
        try:key.verify(decode(raw_sig),(raw_header+"."+raw_payload).encode(),padding.PKCS1v15(),hashes.SHA256())
        except (InvalidSignature,ValueError) as exc:raise TokenError("Unauthorized") from exc
        clock=int(time.time()) if now is None else int(now)
        if claims.get("iss")!=self.issuer or claims.get("aud")!=self.audience:
            raise TokenError("Unauthorized")
        if any(type(claims.get(k)) is not int for k in ("iat","nbf","exp")):
            raise TokenError("Unauthorized")
        if not claims["iat"]<=clock or claims["nbf"]>clock or claims["exp"]<=clock or claims["exp"]-claims["iat"]>3600:
            raise TokenError("Unauthorized")
        subject=claims.get("sub");tenant=claims.get("tenant");scope=claims.get("scope")
        if not isinstance(subject,str) or not _SUB.fullmatch(subject):
            raise TokenError("Unauthorized")
        if not isinstance(tenant,str) or not _IDENT.fullmatch(tenant):
            raise TokenError("Unauthorized")
        if not isinstance(scope,str) or len(scope)>240:
            raise TokenError("Unauthorized")
        grants=frozenset(scope.split())
        if not grants.issubset({"records:read","records:write"}):
            raise TokenError("Unauthorized")
        return {"sub":subject,"tenant":tenant,"scope":grants}
