from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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

@app.get("/get_artist_stats")
async def get_artist_stats():
    try:
        # Fetch artist data, including monthly listeners
        artist_data = sp.artist("3AUIYVmhwrsw8UOPHEv91Z")
        monthly_listeners = artist_data
        return JSONResponse(content=monthly_listeners)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching artist statistics: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
