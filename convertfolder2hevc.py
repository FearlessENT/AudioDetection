import os
import subprocess
import sys

def convert_videos(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_name = f"libx265_{filename}"
            output_file_path = os.path.join(output_folder, output_file_name)

            # Run the FFmpeg command
            ffmpeg_command = [
                "ffmpeg",
                "-i", input_file_path,
                "-c:v", "libx265",
                "-preset", "fast",
                "-crf", "23",
                "-vf", "scale=-1:720",
                "-r", "24",
                "-c:a", "aac",
                output_file_path
            ]
            subprocess.run(ffmpeg_command)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_folder> <output_folder>")
    else:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        convert_videos(input_folder, output_folder)
