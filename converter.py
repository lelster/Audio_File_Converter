import os
import time
from tinytag import TinyTag
from pydub import AudioSegment

def list_files(path, ending, export_path, recursive):
    export_path = os.path.normpath(export_path)
    path = os.path.normpath(path)
    if not os.path.exists(export_path):
        os.makedirs(export_path)
    files_processed = 0

    try:
        for x in os.scandir(path):
            if x.is_file() and x.name.endswith(ending):
                tag = TinyTag.get(x.path)
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
                audio_file = AudioSegment.from_file(x.path)
                export_filename = os.path.join(export_path, f"{os.path.splitext(x.name)[0]}.mp3")
                audio_file.export(export_filename, format="mp3", tags=metadata)
                files_processed += 1

            elif x.is_dir() and recursive == True:
                list_files(x.path, ending, export_path, recursive)

    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    except OSError as e:
        pass
    except Exception as e:
        print(f"Failed to convert {x.path}: {str(e)}")
        
    if files_processed == 0:
        error_message = f"No files with the .{ending} extension found in the directory {path}."
        raise FileNotFoundError(error_message)


def main():
    
    origin = input("Which directory do you want to export from? (e.g. C:\music\mp3)\n")
    recursive = input("Do you want it to recursively go through all subdirectories in your directory? (y/n)\n").lower().strip() == 'y'
    ending = input("Which datatype should be exported to mp3? (e.g. flac, wav)\n").strip()
    export = input("To which directory should the files be exported to?\n")

    print("Files are being converted...")
    tic = time.perf_counter()
    list_files(origin, (".", ending), export, recursive)
    toc = time.perf_counter()
    print(f"It took {toc - tic:0.4f} seconds")

if __name__ == '__main__':
    main()