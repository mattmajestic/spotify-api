from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
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

@app.get("/get_artist/{artist_id}", response_class=JSONResponse)
async def get_artist_stats(artist_id: str):
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

        return JSONResponse(content=artist_info)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching artist statistics: {str(e)}")

@app.get("/artist_page/{artist_id}", response_class=HTMLResponse)
async def get_artist_page(artist_id: str):
    try:
        # Fetch artist data, including monthly listeners and images
        artist_data = sp.artist(artist_id)
        monthly_listeners = artist_data["followers"]["total"]
        artist_name = artist_data["name"]
        images = artist_data["images"]

        # Generate the HTML page
        html_content = f"""
        <html>
        <head>
            <title>Artist Page: {artist_name}</title>
        </head>
        <body>
            <h1>Artist: {artist_name}</h1>
            <p>Monthly Listeners: {monthly_listeners}</p>
            <h2>Images</h2>
            <ul>
        """

        for image in images:
            html_content += f'<li><img src="{image["url"]}" alt="Image" width="{image["width"]}" height="{image["height"]}"></li>'

        html_content += """
            </ul>
        </body>
        </html>
        """

        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching artist statistics: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
