from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoRequest(BaseModel):
  url: str
  mode: str = "auto"
  quality: str = "720"


@app.get("/")
def home():
  return {"status": "Working!"}


@app.post("/extract")
def extract_link(req: VideoRequest):
  ydl_opts = {
      "quiet": True,
      "no_warnings": True,
      "format": (
          "bestaudio/best"
          if req.mode == "audio"
          else f"best[height<={req.quality}][ext=mp4]/best[ext=mp4]/best"
      ),
  }
  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(req.url, download=False)
      return {"success": True, "url": info.get("url")}
  except Exception as e:
    return {"success": False, "error": str(e)}
