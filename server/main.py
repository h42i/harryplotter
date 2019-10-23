#!/usr/bin/python2
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, url_for, request, send_file
from subprocess import call
import serial
import time
import uuid
from threading import Thread
from PIL import Image, ImageDraw, ImageSequence
import imageio
import sys
import numpy

TEMP_HPGL_PATH = "/tmp/harry-temp.hpgl"
PREVIEW_PATH = "/tmp/harry-preview.gif"

app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config.from_object(__name__)

@app.route("/")
@app.route("/upload", methods=["GET"])
@app.route("/plot", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']

    if file:
        print("Receiving hpgl file")
        data = file.read()

        #try:
        print("Opening hpgl file")
        out = open(TEMP_HPGL_PATH, "wb")
        out.write(data)
        out.close()

        preview_name = uuid.uuid1().hex + ".gif"
        render_hpgl(TEMP_HPGL_PATH, PREVIEW_PATH, (20, 20), 0.01386029411764706)
        #except:
        #    print("There was an error rendering the hpgl data")

    return render_template("index.html", state="upload", preview=("preview/" + preview_name))

@app.route("/preview/<whatsoever>")
def preview_image(whatsoever):
    return send_file(PREVIEW_PATH, mimetype="image/gif")

@app.route("/plot", methods=["POST"])
def plot():
    Thread(target=plot_thread).start()

    return render_template("index.html", state="plot")

def plot_thread():
    try:
        data = open(TEMP_HPGL_PATH, "rb")

        # just do not ask
        for i in range(0, 30):
            try:
                ser = serial.Serial("/dev/ttyUSB" + str(i), 19200, timeout=1)
                ser.write(data.read())
                ser.close()
                break
            except:
                continue
    except:
        pass

def get_coords(coords_str):
    plain_coords = coords_str.split(",")
    coords = [ (int(plain_coords[2 * i]), int(plain_coords[2 * i + 1])) for i in range(len(plain_coords) // 2) ]

    return coords

def scale_coords(coords, pos, size, scale):
    x, y = pos
    w, h = size
    return list(map(lambda c: (int(w - x - (c[1]) * scale), int(h - y - (c[0]) * scale)), coords))

def render_hpgl(hpgl, output, pos, scale):
    x, y = pos
    frames = []

    image = Image.open("static/harryplotter_roll.gif")
    palette = image.palette.getdata()

    print("Rendering hpgl")

    # So let's be honest. I have no idea why exactly this is working and
    # why i need four \x00 instead of just three of them. But hey, it's
    # working!
    #i = 0

    #while not (palette[1][i] == 0xFF and palette[1][i + 1] == 0xFF and palette[1][i + 2] == 0xFF):
    #    i += 4

    tmp_palette = bytearray(image.palette.palette)
    tmp_palette[100 * 3] = 0
    tmp_palette[100 * 3 + 1] = 0
    tmp_palette[100 * 3 + 2] = 0
    image.palette.palette = bytes(tmp_palette)
    black_idx = 100

    w, h = image.size
    draw = ImageDraw.Draw(image)

    hpgl_cmds = open(hpgl).read().split(";")

    last_coord = (0, 0)
    ani_counter = 0

    # Count pen moves
    pen_moves = 0
    frame_count = 30

    for cmd in hpgl_cmds:
        if cmd[:2] == "PD" or cmd[:2] == "PA":
            pen_moves += cmd.count(",")

    frame_skip = pen_moves // (frame_count - 1)

    for cmd in hpgl_cmds:
        if cmd[:2] == "PU":
            coords = scale_coords(get_coords(cmd[2:]), (x, y), (w, h), scale)

            last_coord = coords[-1]
        elif cmd[:2] == "PD" or cmd[:2] == "PA":
            coords = scale_coords(get_coords(cmd[2:]), (x, y), (w, h), scale)

            for coord in coords:
                draw.line(last_coord + coord, fill=black_idx)
                last_coord = coord
                ani_counter += 1

                if frame_skip == 0:
                    image.save("/tmp/frame.gif")
                    frames.append(imageio.imread("/tmp/frame.gif"))
                elif ani_counter % frame_skip == 0:
                    image.save("/tmp/frame.gif")
                    frames.append(imageio.imread("/tmp/frame.gif"))

    image.save("/tmp/frame.gif")
    for i in range(frame_count // 2):
        frames.append(imageio.imread("/tmp/frame.gif"))

    del draw

    print("Writing gif")
    #writeGif(output, frames, duration=0.2)
    imageio.mimsave(output, frames)

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=80, debug=True)
    app.run(host="0.0.0.0", port=8081, debug=True)

