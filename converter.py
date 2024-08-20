import os
import time
from tinytag import TinyTag
from pydub import AudioSegment

def scan_files(path, ending_one, recursive):
    path = os.path.normpath(path)
    files_to_process = []

    try:
        for x in os.scandir(path):
            if x.is_file() and x.name.endswith(ending_one):
                files_to_process.append(x.path)
            elif x.is_dir() and recursive:
                files_to_process.extend(scan_files(x.path, ending_one, recursive))
    except Exception as e:
        print(f"Error while scanning directory {path}: {str(e)}")

    return files_to_process

def list_files(path, ending_one, ending_two, export_path, recursive):
    files_to_process = scan_files(path, ending_one, recursive)

    if not files_to_process:
        error_message = f"No files with the {ending_one} extension found in the directory {path}."
        raise FileNotFoundError(error_message)
    
    export_path = os.path.normpath(export_path)
    if not os.path.exists(export_path):
        os.makedirs(export_path)
    
    files_processed = 0
    for x in files_to_process:
        try:
            tag = TinyTag.get(x)
            metadata = {
                'artist': tag.artist,
                'title': tag.title,
                'album': tag.album,
                'composer': tag.composer,
                'genre': tag.genre,
                'track': tag.track,        
                'track_total': tag.track_total,
                'disc': tag.disc,
                'disc_total': tag.disc_total,
                'year': tag.year,
                'albumartist': tag.albumartist
            }
            metadata = {k: v for k, v in metadata.items() if v is not None}
            audio_file = AudioSegment.from_file(x)
            export_filename = os.path.join(export_path, f"{os.path.splitext(os.path.basename(x))[0]}.{ending_two}")
            audio_file.export(export_filename, format=ending_two, tags=metadata)
            files_processed += 1
        except Exception as e:
            print(f"Failed to convert {x}: {str(e)}")
    
    return files_processed

def main():
    origin = input("Which directory do you want to export from? (e.g. C:\\music\\mp3)\n")
    recursive = input("Do you want it to recursively go through all subdirectories in your directory? (y/n)\n").lower().strip() == 'y'
    ending_one = input("Which Datatype should be converted? (e.g. flac, wav, mp3)\n").strip()
    ending_two = input("To which Datatype should it be converted? (e.g. flac, wav, mp3)\n").strip()
    export = input("To which directory should the files be exported to?\n")
    print("Files are being converted...")
    tic = time.perf_counter()
    try:
        files_processed = list_files(origin, f".{ending_one}", ending_two, export, recursive)
        toc = time.perf_counter()
        if files_processed > 0:
            print(f"Successfully processed {files_processed} files.")
        print(f"It took {toc - tic:0.4f} seconds")
    except FileNotFoundError as e:
        print(e)

if __name__ == '__main__':
    main()
