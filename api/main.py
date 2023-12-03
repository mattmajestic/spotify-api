from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Get Spotify API credentials from environment variables
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Initialize the Spotify API client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Initialize the Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/get_artist", response_class=JSONResponse)
async def get_artist_stats(request: Request,artist_id: str = None):
    try:
        # Fetch artist data, including monthly listeners and images
        artist_data = sp.artist(artist_id)
        monthly_listeners = artist_data["followers"]["total"]
        artist_name = artist_data["name"]
        images = artist_data["images"]

        artist_info = {
            "artist_name": artist_name,
            "monthly_listeners": monthly_listeners,
            "images": images
        }

        return templates.TemplateResponse("artist.html", {"request": request, "data": artist_info})
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching artist statistics: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)