#!/usr/bin/env python
#coding=utf8

import commands
import os,sys
from optparse import OptionParser
import sqlite3

QQMUSIC_FILE_PATH_SYMBOL = 'QQMusicMac'
QQMUSIC_SQLITE3_FILE_NAME = 'qqmusic.sqlite'
QQMUSIC_SQLITE3_TABLE_NAME = 'SONGS'
QQMUSIC_SQLITE3_SONG_NAME_INDEX = 2
QQMUSIC_SQLITE3_SONG_FILE_PATH_INDEX = 11

FILE_NAME_NOT_ALLOW_CHARACTERS = [u'(',u')',u' ']
FILE_TRANS = {'tm0':'mp3','tm3':'mp3'}

class qqMusic:
    def __init__(self):
        self.file_path_symbol = 'find / -name %s 2>/dev/null' % (QQMUSIC_FILE_PATH_SYMBOL,)
        self.qq_music_file_path = self.getMusicFilePath()
        os.chdir(self.qq_music_file_path)

    def getMusicFilePath(self):
        status,output = commands.getstatusoutput(self.file_path_symbol)
        if status > 0 and output:
            return output.strip()
        raise 'get qqmusic file path failed,please check qqmusic is installed!'

    def getMyDownloadFiles(self):
        
        songs_download = []
        conn = sqlite3.connect(QQMUSIC_SQLITE3_FILE_NAME)
        cursor = conn.cursor()
        cursor.execute('select * from %s' % (QQMUSIC_SQLITE3_TABLE_NAME,))
        song = cursor.fetchone()
        while song:
            song_name,song_file_path = song[QQMUSIC_SQLITE3_SONG_NAME_INDEX],song[QQMUSIC_SQLITE3_SONG_FILE_PATH_INDEX]
            song = cursor.fetchone()
            if song_file_path:
                if song_file_path[0] != '.':
                    song_file_path = '.'+song_file_path
                songs_download.append((song_name,song_file_path))
        return songs_download

    def copyFile2MyDir(self,my_dir):
        
        sys_com = 'rm %s/* -rf' % (my_dir,)
        sys_com = sys_com.encode('utf8')
        os.system(sys_com)
        qqmusic_files = self.getMyDownloadFiles()
        for name,file_path in qqmusic_files:
            os.system('cp %s %s' % (file_path,my_dir))
            file_name = file_path.split('/')[-1]
            file_type = file_name.split('.')[-1]
            now_file_path = os.path.join(my_dir,file_name)
            new_name = name+'.'+FILE_TRANS.get(file_type,'mp3')
            for s in FILE_NAME_NOT_ALLOW_CHARACTERS:
                new_name = new_name.replace(s,'')
            new_file_path = os.path.join(my_dir,new_name)
            sys_com = 'mv %s %s' % (now_file_path,new_file_path)
            sys_com = sys_com.encode('utf8')
            os.system(sys_com)
            print new_name

if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option("-o","--out_file",default="~",dest="out_file_path",help="out qqmusic files to where?")
    (options, args) = parser.parse_args()
    print options.out_file_path

    qqmusic = qqMusic()
    qqmusic.copyFile2MyDir(options.out_file_path)
