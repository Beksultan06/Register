from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/api/welcome/")
async def welcome(request: Request):
    data = await request.json()
    print(f"🎉 Приветствуем {data['full_name']} на экране фандомата!")
    return {"message": f"Привет, {data['full_name']}"}