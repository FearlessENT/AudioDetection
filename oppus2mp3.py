import os
import subprocess

def convert_mp3_to_aac(input_path, output_path):
    try:
        subprocess.run(['ffmpeg', '-i', input_path, '-c:a', 'aac', '-strict', 'experimental', output_path], check=True)
        print(f"Conversion successful: {input_path} -> {output_path}")
    except subprocess.CalledProcessError:
        print(f"Conversion failed: {input_path}")

def batch_convert_mp3_to_aac(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".mp3"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".m4a")
                convert_mp3_to_aac(input_path, output_path)


                

if __name__ == "__main__":
    input_folder = "E:\AA Temp\music"
    output_folder = "E:\AA Temp\music\output"

    batch_convert_mp3_to_aac(input_folder, output_folder)
