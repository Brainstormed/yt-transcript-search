from flask import Flask, url_for, render_template, request
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi


app = Flask(__name__)


def id_of_url(url: str):
    if (url.lower().count("youtube.com/v/") != 0):
        start_index = url.index("v/") + 2
        end_index = start_index + 13
        return url[start_index:end_index]
    elif (url.lower().count("youtu.be/") != 0):
        start_index = url.index("youtu.be") + 9
        end_index = start_index + 12
        return url[start_index:end_index]

    start_index = url.index("=") + 1
    end_index = start_index + 11
    return url[start_index:end_index]


@app.route("/", methods=["GET", "POST"])
def index(name=None):
    if request.method == "POST":
        data = request.form
        yt = YouTube(data["id"])
        transcript = YouTubeTranscriptApi.get_transcript(
            id_of_url(data["id"])
        )

        count = 0
        cc_arr = []
        cc_final = ""

        for i in transcript:
            cc_arr.append(i["text"])
            cc_final = " ".join(cc_arr).lower().split(" ")

        for i in cc_final:
            count += i.count(data["word"].lower())

        response = {
            "id": data["id"],
            "word": data["word"],
            "count": count,
            "title": yt.title,
            "thumbnail": yt.thumbnail_url,
            "cc": cc_final,
        }
        return render_template("index.html", response=response)

    return render_template("index.html", name=name)

@app.errorhandler(500)
def internal_server_error(error=None):
    return render_template("index.html", error="The url you have provided is invalid!")
