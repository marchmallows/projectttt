from typing import Optional, List
from pydantic import BaseModel, Field


class createMusicModel(BaseModel):
    id: str = Field(min_length=5, max_length=5)
    picture_urlmusic: str
    picture_urlowner: str
    music_time: float
    link_music: str
    name_music: str
    name_music_owner: str
    country: str
    Type: str


class updateMusicModel(BaseModel):
    music_time: Optional[float]
    name_music_owner: Optional[str]
    name_music: Optional[str]
    country: Optional[str]
    link_music: Optional[str]
    Type: Optional[str]
