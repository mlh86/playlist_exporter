"""
Takes a UTF-8 M3U8 Playlist file and copies the playlist items to the specified
export folder, which can be a relative or absolute directory path that need not
already exist. The files are prepended with a numeric sequence so that they
follow the order of the playlist.

    Copyright (C) 2022 Mohammad L. Hussain

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import shutil
import argparse

argparser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
argparser.add_argument('playlist_file', help="The path to the playlist file")
argparser.add_argument('export_dir', help="The path to the export folder")

args = argparser.parse_args()

if not os.path.exists(args.playlist_file):
    print("Playlist path seems to be invalid. Please try again.")
    exit()
if os.path.splitext(args.playlist_file)[1].lower() != '.m3u8':
    print("Please a specify an M3U8-format playlist")
    exit()

if os.path.exists(args.export_dir) and not os.path.isdir(args.export_dir):
    print("Please specify a new or existing DIRECTORY as the export target")
    exit()

if not os.path.exists(args.export_dir):
    os.makedirs(args.export_dir)

os.chdir(args.export_dir)
file_num = 1
with open(args.playlist_file,'rt',encoding="utf-8") as playlist_file:
    for line in playlist_file:
        if line.startswith("#EXT"):
            continue
        srcpath = line.strip()
        orig_filename = os.path.basename(srcpath)
        new_filename = f"{file_num:03} - {orig_filename}"
        print(f"Copying {orig_filename}...")
        shutil.copy(srcpath, new_filename)
        file_num += 1
