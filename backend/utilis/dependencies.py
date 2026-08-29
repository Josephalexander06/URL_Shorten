from fastapi import Request, HTTPException
import redis


redis_client = redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)

def find_ip_address(request):

    x_forward_for = request.headers.get("x-forwarded-for")
    if x_forward_for:
        client_ip = x_forward_for.split(",")[0].strip()
    elif request.client:
        client_ip = request.client.host
    else:
        client_ip = None
    
    return client_ip


def rate_limiter(request:Request):
    client_ip = find_ip_address(request)
    req_mode = redis_client.get(f"rate_limit_{client_ip}")

    if req_mode and int(req_mode) > 10:
        raise HTTPException(status_code=429,detail="Too many requests")
    
    redis_client.incr(f"rate_limit_{client_ip}")
    redis_client.expire(f"rate_limit_{client_ip}",60)