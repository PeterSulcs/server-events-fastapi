import asyncio
import json
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

async def generate_json_objects(a):
    data = []
    for i in range(10):
        obj = {"token": {'text': i, 'name': f'Object {i} {a}'}}
        data.append(i)
        yield json.dumps(obj)
    i = -1
    data.append(i)
    yield json.dumps({"token": {'text': i, "name": f'Object {i} {a}'}, 'generated_text': "".join([f"{d}" for d in data])})

@app.post("/generate_stream")
async def generate_stream(request: Request):
    data = await request.json()
    stream = data.get("stream")
    async def event_stream():
        async for json_data in generate_json_objects(stream):
            yield f"data: {json_data}\n"
            await asyncio.sleep(0.05)  # Delay between sending events

    return StreamingResponse(event_stream(), media_type="json/event-stream")


#    uvicorn example:app --reload
# curl -X POST -H "Content-Type: application/json" -d '{"stream": true}' http://localhost:8000/generate_stream
