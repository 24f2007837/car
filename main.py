import time
import uuid
from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-eq14wx.example.com"
USER_EMAIL = "24f2007837@ds.study.iitm.ac.in"

# Strict CORS configuration (no wildcards)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response

@app.get("/stats")
def compute_stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        # Parse comma-separated integers
        nums = [int(v.strip()) for v in values.split(",") if v.strip() != ""]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid integer format in values parameter.")
    
    if not nums:
        raise HTTPException(status_code=400, detail="Values list cannot be empty.")
    
    count = len(nums)
    total_sum = sum(nums)
    min_val = min(nums)
    max_val = max(nums)
    mean_val = total_sum / count

    return {
        "email": USER_EMAIL,
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }