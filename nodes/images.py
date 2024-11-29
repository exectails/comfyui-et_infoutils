import json
import os
import random
import re

from PIL import Image
from PIL.PngImagePlugin import PngInfo
import numpy as np

import folder_paths
from comfy.cli_args import args


class ETPresentImageNode:
    """
    A node that displays the input images and optionally saves them to disk.
    Essentially a merger of the Preview and Save Image nodes, but with more
    control over the paths and names and with a simple toggle to enable or
    disable saving.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to handle."}),
                "save": ("BOOLEAN", {"default": True, "label_off": "no", "label_on": "yes", "tooltip": "Whether to save the images to disk."}),
                "folder_path": ("STRING", {"default": "", "tooltip": "The folder path to save the images to. If empty, the default output directory will be used."}),
                "file_name": ("STRING", {"default": "ComfyUI_%counter%_", "tooltip": "The name of the file to save. Use %counter% to insert a counter."}),
            },
            "hidden": {
                "prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "process"

    OUTPUT_NODE = True

    CATEGORY = "exectails/Info"
    DESCRIPTION = "Displays the input images and optionally saves them to disk."

    def process(self, images, save, folder_path, file_name, prompt=None, extra_pnginfo=None):
        preview_type = "output" if save else "temp"
        compression_level = 6 if save else 1

        if not save:
            folder_path = folder_paths.get_temp_directory()
            file_name_prefix = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(10)) + "_"
            file_name = file_name_prefix + file_name
        elif folder_path == "":
            folder_path = folder_paths.get_output_directory()
        elif not os.path.isabs(folder_path):
            folder_path = os.path.join(folder_paths.get_output_directory(), folder_path)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        counter = self.get_counter(folder_path, file_name)
        results = list()

        for (batch_number, image) in enumerate(images):
            counter += 1

            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            file_name = file_name.replace("%counter%", f"{counter:05}") + ".png"
            file_path = os.path.join(folder_path, file_name)

            img.save(file_path, pnginfo=metadata, compress_level=compression_level)

            results.append({
                "filename": file_name,
                "subfolder": folder_path,
                "type": preview_type,
            })

        return {"ui": {"images": results}}

    def get_counter(self, folder_path, file_name):
        counter = 0

        file_name_pattern = file_name.replace("%counter%", "(?P<counter>[0-9]{5})")

        for file in os.listdir(folder_path):
            match = re.match(file_name_pattern, file)
            if match:
                if match.groupdict().get("counter"):
                    counter = max(counter, int(match.group("counter")))

        return counter
