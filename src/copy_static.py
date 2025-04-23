import os
import shutil

def copy_static_to_public(source_dir, dest_dir):
    """
    Copy all contents from source directory to destination directory recursively.
    First deletes all contents of the destination directory to ensure a clean copy.
    
    Args:
        source_dir (str): Path to source directory (e.g., 'static')
        dest_dir (str): Path to destination directory (e.g., 'public')
    """
    print(f"Starting copy from {source_dir} to {dest_dir}")
    
    # Check if destination directory exists, create it if not
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
        print(f"Created destination directory: {dest_dir}")
    
    # Delete all contents from destination directory
    print(f"Cleaning destination directory: {dest_dir}")
    for item in os.listdir(dest_dir):
        item_path = os.path.join(dest_dir, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Deleted file: {item_path}")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Deleted directory: {item_path}")
    
    # Start the recursive copy
    _recursive_copy(source_dir, dest_dir)
    
    print("Copy completed successfully!")

def _recursive_copy(source, dest):
    """
    Internal helper function to recursively copy files and directories.
    
    Args:
        source (str): Source path
        dest (str): Destination path
    """
    # List all items in the source directory
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)
        
        # If it's a file, copy it
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")
        
        # If it's a directory, create it and copy contents recursively
        elif os.path.isdir(source_path):
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
                print(f"Created directory: {dest_path}")
            
            # Recursively copy contents of this subdirectory
            _recursive_copy(source_path, dest_path)

if __name__ == "__main__":
    # Example usage
    copy_static_to_public("static", "public")