import os
import shutil
import unicodedata
    
def normalize(text):
    normalized_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    normalized_text = ''.join(char if char.isalnum() or char in (' ', '_') else '_' for char in normalized_text)
    return normalized_text

def process_folder(folder_path):
    for root, dirs, files in os.walk("C:\Users\ASUS\Edyta\Do przejrzenia"):
        for dir_name in dirs:
            normalized_dir_name = normalize(dir_name)
            if dir_name != normalized_dir_name:
                os.rename(os.path.join(root, dir_name), os.path.join(root, normalized_dir_name))

        for file_name in files:
            normalized_file_name = normalize(file_name)
            if file_name != normalized_file_name:
                os.rename(os.path.join(root, file_name), os.path.join(root, normalized_file_name))

            process_file(os.path.join(root, normalized_file_name))

def process_file(file_path):
    _, extension = os.path.splitext(file_path)
    extension = extension[1:].upper()

    if extension in ('JPEG', 'PNG', 'JPG', 'SVG'):
        move_file(file_path, 'images')
    elif extension in ('AVI', 'MP4', 'MOV', 'MKV'):
        move_file(file_path, 'video')
    elif extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
        move_file(file_path, 'documents')
    elif extension in ('MP3', 'OGG', 'WAV', 'AMR'):
        move_file(file_path, 'audio')
    elif extension in ('ZIP', 'GZ', 'TAR'):
        extract_archive(file_path)
    else:
        move_file(file_path, 'unknown_extensions')

def move_file(file_path, category):
    category_folder = os.path.join(os.path.dirname(file_path), category)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)
    
    shutil.move(file_path, os.path.join(category_folder, os.path.basename(file_path)))

def extract_archive(archive_path):
    archive_folder = os.path.join(os.path.dirname(archive_path), 'archives', os.path.basename(archive_path)[:-4])
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    shutil.unpack_archive(archive_path, archive_folder)
    shutil.rmtree(archive_path)

def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/folder")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(f"C:\Users\ASUS\Edyta\Do przejrzenia"):
        print("Specified folder does not exist.")
        sys.exit(1)

    process_folder("C:\Users\ASUS\Edyta\Do przejrzenia")

if __name__ == "__main__":
    main() 
