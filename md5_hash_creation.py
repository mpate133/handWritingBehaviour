import hashlib
import os


print('Creating MD5 Hash list for all images')
os.chdir('data_original')
with open('../md5_hash_list', 'w') as hash_file:
    for image in os.listdir('.'):
        if os.path.isfile(image):
            with open(image, "rb") as f:
                img_hash = hashlib.md5()
                while chunk := f.read(8192):
                    img_hash.update(chunk)
                hash_file.write(img_hash.hexdigest())
            print('', file=hash_file)

os.chdir('..')
print("All image hash are created and saved in md5_hash_list")
