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
    key = f"rate_limit_{client_ip}"

    pipe = redis_client.pipeline()
    pipe.incr(key)
    # Only set expire if it's a new key to create a fixed 60-second window , the pipeline executes all at once, so we can't easily conditionally expire in a simple pipe
    # Setting expire every time creates a sliding inactivity window, which is okay for basic rate limiting.
    pipe.expire(key, 60)
    results = pipe.execute()
    
    current_count = results[0]

    if current_count > 10:
        raise HTTPException(status_code=429,detail="Too many request")
    
