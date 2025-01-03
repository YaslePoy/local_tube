from pytubefix import YouTube
import json
import multiprocessing

def download_shorts(url):
    try:
        video = YouTube(url)
        stream = video.streams.filter(file_extension='mp4', only_video=False, only_audio=False).first()
        if stream is not None:
            stream.download()
            print("Download complete.")
        else:
            print("No compatible video found.")
    except Exception as e:
        print("An error occurred during download:", str(e))

# # URL of the YouTube Shorts you want to download
# shorts_url = "https://youtube.com/shorts/D4w7bnt0c5A?si=DSPJUuY8gtSoPZ4Z"
#
# # Call the download function
# download_shorts(shorts_url)

def load(i, total, ls):
    link = ls[i]
    print(link)
    print(f'loading {i + 1} of {total}')
    try:
        video = YouTube(link)
        raw_streams = video.streams.filter(file_extension='mp4', only_video=False, only_audio=False)
        streams = list(filter(lambda s: s.includes_audio_track and s.video_codec is not None, raw_streams))
        stream = streams[0]
        for s in streams:
            if s.resolution == '1080p':
                stream = s
                break
            if s.resolution == '720p':
                stream = s
                break
            if s.resolution == '480p':
                stream = s
                break

        if stream is not None:
            print(f'{i+1}: resolution: {stream.resolution}')
            stream.download(output_path="local_library", filename=f'#{i+1} {stream.default_filename}', timeout=7)
            print(f"{i+1}: Download complete.")
        else:
            print("No compatible video found.")
    except Exception as e:
        print("An error occurred during download:", str(e))
        try:
            print('Try again')
            stream.download(output_path="local_library", filename=f'#{i+1} {stream.default_filename}', timeout=7)
            print(f"{i+1}: Download complete.")
        except Exception as ei:
            print("Bad shorts")

if __name__ == '__main__':
    with open('result.json', 'r',  encoding='utf_8_sig') as file:
        lines = file.readlines()
        lines = list(filter(lambda l: 'https://youtube.com/shorts' in l, lines))
        i = int(input())
        lines = list(dict.fromkeys(list(map(lambda s: s.rsplit(sep='"')[3], lines))))
        total = len(lines)

        while True:
            com = input()
            if com == '+':
                i = i + 1
                proc = multiprocessing.Process(target=load, args=(i, total, lines))
                proc.start()


            if com == '*':
                proc.kill()
                proc = multiprocessing.Process(target=load, args=(i, total, lines))
                proc.start()

