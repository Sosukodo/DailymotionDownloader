import requests
import json
import sys
import subprocess
import os

from pathlib import Path 

if len(sys.argv) > 2:
    video_url = sys.argv[1]
    base_path = Path(sys.argv[2])
elif len(sys.argv) > 1:
    video_url = sys.argv[1]
    base_path = Path(os.getcwd())
else:
    # this is most likely never used
    #video_url = input("Enter the Dailymotion video URL: ")
    print("usage: cli.py url [download directory]")
    exit(0)

if not base_path.is_dir():
    print(f"{base_path} is not a directory")
    exit(1)

if not base_path.exists():
    printf(f"{base_path} does not exist")
    exit(1)


metadata_url = (
    f"https://www.dailymotion.com/player/metadata/video/{video_url.split('/')[-1]}"
)
print(f"Metadata URL: {metadata_url}")

response = requests.get(metadata_url)
# print(f"Response Status Code: {response.status_code}")
# print(f"Response Content: {response.text}")

try:
    metadata = json.loads(response.text)
    # print(f"Metadata: {json.dumps(metadata, indent=2)}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    print("Response content was not valid JSON.")
    # quit program
    exit(1)

file_name = metadata["title"] + ".mp4"
file_path = str(base_path / file_name)

m3u8_url = metadata["qualities"]["auto"][0]["url"]
print(f"M3U8 URL: {m3u8_url}")

# read m3u8 file
response = requests.get(m3u8_url)
if response.status_code == 200:
    print("M3U8 file content:")
    print(response.text)
else:
    print(f"Failed to fetch M3U8 file. Status code: {response.status_code}")

# m3u8_url = response.text.splitlines()[-1]  # Get the first URL from the M3U8 file
print(f"Extracted M3U8 URL: {m3u8_url}")

# Unnecessary computing that we can leave ffmpeg to do
# response = requests.get(m3u8_url)
# if response.status_code == 200:
#    print("M3U8 file content:")
#     print(response.text)
# else:
#    print(f"Failed to fetch M3U8 file. Status code: {response.status_code}")

# Disregard this. its a stupid way of doing it and requires me to mess with timestamps but i love my life. just pass m3u8_url directly to ffmpeg
# Download the segments
"""
def download_segments(m3u8_url, output_dir="video_segments"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    count = 0
    response = requests.get(m3u8_url)
    if response.status_code == 200:
        lines = response.text.splitlines()
        for line in lines:
            if line.startswith("#EXTINF:"):
                continue
            if line.startswith("#EXT-X-PLAYLIST-TYPE") or line.startswith(
                "#EXT-X-TARGETDURATION"
            ):
                continue
            if line.startswith("#EXT-X-VERSION") or line.startswith("#EXTM3U"):
                continue
            if line.startswith("#EXT-X-STREAM-INF"):
                continue
            if line.startswith("#EXT-X-ENDLIST"):
                break
            segment_url = line.strip()
            print(f"Found segment URL: {segment_url}")
            if segment_url:
                # append the base URL
                segment_url = m3u8_url.rsplit("/", 1)[0] + "/" + segment_url
                print(f"Full segment URL: {segment_url}")
                # segment_name = os.path.join(output_dir, os.path.basename(segment_url))
                segment_name = os.path.join(output_dir, f"segment_{count}.ts")
                print(f"Downloading segment: {segment_name}")
                segment_response = requests.get(segment_url)
                if segment_response.status_code == 200:
                    with open(segment_name, "wb") as f:
                        f.write(segment_response.content)
                    count += 1
                    print(f"Downloaded: {segment_name}")
                else:
                    print(
                        f"Failed to download segment: {segment_url}, Status code: {segment_response.status_code}"
                    )
    else:
        print(f"Failed to fetch M3U8 file. Status code: {response.status_code}")


download_segments(m3u8_url)


def join_segments(output_dir="video_segments", output_file="output_video.mp4"):
    segment_files = [
        os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".ts")
    ]
    # segment_files.sort()
    # sort in a way that they are in the correct order
    segment_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
    if not segment_files:
        print("No segments found to join.")
        return

    print(f"Joining {len(segment_files)} segments into {output_file}")
    with open("segments.txt", "w") as f:
        for segment in segment_files:
            f.write(f"file '{segment}'\n")

    # Use ffmpeg to join the segments
    command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        "segments.txt",
        "-c",
        "copy",
        output_file,
    ]
    subprocess.run(command)


join_segments()
print("Video segments joined into output_video.mp4")
"""


def download_video_direct(m3u8_url, output_file="output_video.mp4"):
    """Download video directly from m3u8 URL using ffmpeg"""
    # check if mp4 file already exists
    if output_file.endswith(".mp4") and os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping download.")
        return
    command = [
        "ffmpeg",
        "-i",
        m3u8_url,
        "-c",
        "copy",
        "-avoid_negative_ts",
        "make_zero",
        "-y",
        output_file,
    ]
    print("Downloading...")
    cmd_string = ' '.join(command)
    print(f"FFMPEG command: \n{cmd_string})

    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Video saved to: {output_file}")
    else:
        print(f"Error downloading video: {result.stderr}")
        print("Trying with re-encoding...")
        # Fallback to re-encoding
        command_reencode = [
            "ffmpeg",
            "-i",
            m3u8_url,
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-y",
            output_file,
        ]
        result = subprocess.run(command_reencode, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Video saved (re-encoded) to: {output_file}")
        else:
            print(f"Failed to download video: {result.stderr}")


# Use this instead of downloading segments manually
download_video_direct(m3u8_url, file_path)
