from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os

app = Flask(__name__)

# Home route with a form for YouTube URL
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        if not youtube_url:
            return render_template("index.html", error="Please enter a valid YouTube URL!")

        try:
            # Download video using pytube
            yt = YouTube(youtube_url)
            stream = yt.streams.get_highest_resolution()
            video_path = stream.download(output_path="downloads")

            # Generate download link
            return render_template(
                "index.html",
                title=yt.title,
                download_link=f"/download?path={video_path}",
            )
        except Exception as e:
            return render_template("index.html", error=f"Error: {str(e)}")
    
    return render_template("index.html")


# Route to handle file download
@app.route("/download", methods=["GET"])
def download():
    video_path = request.args.get("path")
    if video_path and os.path.exists(video_path):
        return send_file(video_path, as_attachment=True)
    return "File not found!", 404


# Clean up downloaded videos (optional)
@app.teardown_appcontext
def cleanup(exception=None):
    download_dir = "downloads"
    if os.path.exists(download_dir):
        for file in os.listdir(download_dir):
            os.remove(os.path.join(download_dir, file))


if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)  # Ensure the downloads folder exists
    app.run(debug=True)
