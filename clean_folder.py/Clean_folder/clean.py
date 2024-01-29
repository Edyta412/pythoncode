
import os
import shutil
import mimetypes

def normalize(name):
    
    name = name.replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ż', 'z').replace('ź', 'z')
    
    
    name = ''.join(c if c.isalnum() or c in {'_', '.'} else '_' for c in name)
    
    return name

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = file.split('.')[-1].upper()
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type.split('/')[1].upper() if mime_type else None
            
            if mime_type in {'JPEG', 'PNG', 'JPG', 'SVG'}:
                target_folder = 'images'
            elif mime_type in {'AVI', 'MP4', 'MOV', 'MKV'}:
                target_folder = 'video'
            elif mime_type in {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'}:
                target_folder = 'documents'
            elif mime_type in {'MP3', 'OGG', 'WAV', 'AMR'}:
                target_folder = 'audio'
            elif mime_type in {'ZIP', 'GZ', 'TAR'}:
                target_folder = 'archives'
                
                archive_folder = os.path.splitext(file)[0]
                archive_folder_path = os.path.join(root, archive_folder)
                os.makedirs(archive_folder_path, exist_ok=True)
                shutil.unpack_archive(file_path, archive_folder_path)
            else:
                target_folder = 'unknown'
            
            
            if target_folder != 'unknown':
                target_folder_path = os.path.join(root, target_folder)
                os.makedirs(target_folder_path, exist_ok=True)
                target_file_name = normalize(file)
                target_file_path = os.path.join(target_folder_path, target_file_name)
                shutil.move(file_path, target_file_path)

def clean_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: clean-folder <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_folder(folder_path)
    clean_empty_folders(folder_path)

if __name__ == "__main__":
    main()