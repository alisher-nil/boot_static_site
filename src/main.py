import os
import shutil

from src.constants import PUBLIC_DIR, STATIC_DIR


def main():
    reset_public_directory()


def reset_public_directory():
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR)
    os.mkdir(PUBLIC_DIR)
    copy_files(STATIC_DIR, PUBLIC_DIR)


def copy_files(src, dst):
    for item in os.listdir(src):
        if os.path.isfile(os.path.join(src, item)):
            shutil.copy(os.path.join(src, item), dst)
        else:
            os.mkdir(os.path.join(dst, item))
            copy_files(os.path.join(src, item), os.path.join(dst, item))


if __name__ == "__main__":
    main()
