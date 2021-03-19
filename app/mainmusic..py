import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException
from starlette.responses import JSONResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from database.mongodb import MongoDB
from config.development import config
from model.music import createMusicModel, updateMusicModel

mongo_config = config["mongo_config"]
mongo_db = MongoDB(
    mongo_config["host"],
    mongo_config["port"],
    mongo_config["user"],
    mongo_config["password"],
    mongo_config["auth_db"],
    mongo_config["db"],
    mongo_config["collection"],
)
mongo_db._connect()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# CRUD
# http method [post,get,[put, patch],delete]


@app.get("/")
def index():

    return JSONResponse(content={"message": "attraction  music Info"}, status_code=200)


@app.get("/music/")
def get_music(
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, min_length=3, max_length=4),
):

    try:
        result = mongo_db.find(sort_by, order)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


@app.get("/music/{music_id}")
def get_music_by_id(music_id: str = Path(None, min_length=5, max_length=5)):
    try:
        result = mongo_db.find_one(music_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if result is None:
        raise HTTPException(status_code=404, detail="music Id not found !!")

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


@app.post("/music")
def create_music(music: createMusicModel):
    try:
        music_id = mongo_db.create(music)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "music_id": music_id,
            },
        },
        status_code=201,
    )


@app.patch("/music/{music_id}")
def update_music(
    music: updateMusicModel,
    music_id: str = Path(None, min_length=5, max_length=5),
):
    print("music", music)
    try:
        updated_music_id, modified_count = mongo_db.update(music_id, music)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"music Id: {updated_music_id} is not update want fields",
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "music_id": updated_music_id,
                "modified_count": modified_count,
            },
        },
        status_code=200,
    )


@app.delete("/music/{music_id}")
def delete_music_by_id(music_id: str = Path(None, min_length=5, max_length=5)):
    try:
        deleted_music_id, deleted_count = mongo_db.delete(music_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"music Id: {deleted_music_id} is not Delete",
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "music_id": deleted_music_id,
                "deleted_count": deleted_count,
            },
        },
        status_code=200,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3001, reload=True)
