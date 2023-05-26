import os


async def temp_del()-> None:
    voice_dir = './voice_files'
    files = os.listdir(voice_dir)
    if len(files) > 15:
        files.sort(key=lambda x: os.path.getctime(os.path.join(voice_dir, x)))
        first_file = os.path.join(voice_dir, files[1])
        os.remove(first_file)
