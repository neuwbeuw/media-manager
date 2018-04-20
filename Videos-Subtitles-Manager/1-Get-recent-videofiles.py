import io
import os
import time
import configparser

def fatal(errMsg):
    print('[FATAL] ' + errMsg)
    print('[FATAL] Program is now exiting.')
    time.sleep(2)
    exit()

def main():
    if not os.path.isfile('config.ini'): fatal('Cannot find \'config.ini\'')
    # open config.ini for reading
    config = configparser.ConfigParser()
    config.read('config.ini')

    # get values from config file
    TVSHOWS_PATH = config['Paths']['TVShowsPath']
    MOVIES_PATH = config['Paths']['MoviesPath']
    RECENT_VIDEOFILES_TXT = config['Paths']['RecentVideosPath']
    MAX_AGE = float(config['DEFAULT']['MaxAgeForVideos'])

    if not os.path.isdir(TVSHOWS_PATH): fatal(TVSHOWS_PATH + ' not found. Make sure to set the config.ini')
    if not os.path.isdir(MOVIES_PATH): fatal(MOVIES_PATH + ' not found. Make sure to set the config.ini')

    # open file for writing
    print('Getting recent video files\n')
    wfile = io.open(RECENT_VIDEOFILES_TXT, 'w', encoding='utf_8_sig')

    # recursively walk through tv shows path and common video files
    currTime = time.time()
    for root, dirs, files in os.walk(TVSHOWS_PATH):
        for filename in files:
            if filename.endswith('.mp4') or filename.endswith('.mkv') or filename.endswith('.avi') or filename.endswith('.m4v') or filename.endswith('.ts'):
                filefound = os.path.join(root,filename)
                crTime = os.path.getctime(filefound)
                if ((currTime-crTime)/(60*60*24)) <= MAX_AGE:
                    print('Added ' + os.path.basename(filefound))
                    wfile.write(filefound + '\n')

    # recursively walk through movies path and find common video files
    for root, dirs, files in os.walk(MOVIES_PATH):
        for filename in files:
            if filename.endswith('.mp4') or filename.endswith('.mkv') or filename.endswith('.avi') or filename.endswith('.m4v') or filename.endswith('.ts'):
                filefound = os.path.join(root,filename)
                crTime = os.path.getctime(filefound)
                if ((currTime-crTime)/(60*60*24)) <= MAX_AGE:
                    print('Added ' + os.path.basename(filefound))
                    wfile.write(filefound + '\n')

    print('\nDone')
    time.sleep(2)

if __name__ == '__main__':
    main()