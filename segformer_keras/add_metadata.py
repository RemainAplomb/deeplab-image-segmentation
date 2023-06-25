import os
from tflite_support.metadata_writers import image_segmenter
from tflite_support.metadata_writers import writer_utils

import os

""" Creating a directory """
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Set the path to the directory containing the TFLite models
MODEL_PATH = "tflite/MITb5/"
BASE_PATH = "tflite_metadata/MITb5/"

create_dir(BASE_PATH)

# Task Library expects label files that are in the same format as the one below.
LABEL_FILE = "labelmap_6class.txt"

# Normalization parameters are required when reprocessing the image. It is
# optional if the image pixel values are in the range of [0, 255] and the input
# tensor is quantized to uint8. See the introduction for normalization and
# quantization parameters below for more details.
# https://www.tensorflow.org/lite/models/convert/metadata#normalization_and_quantization_parameters)
INPUT_NORM_MEAN = 127.5
INPUT_NORM_STD = 127.5

# Iterate over all files in the MODEL_PATH directory
for file_name in os.listdir(MODEL_PATH):
    if file_name.endswith(".tflite"):
        # Create the metadata writer.
        model_path = os.path.join(MODEL_PATH, file_name)
        writer = image_segmenter.MetadataWriter.create_for_inference(
            writer_utils.load_file(model_path), [INPUT_NORM_MEAN], [INPUT_NORM_STD],
            [LABEL_FILE])

        # Verify the metadata generated by the metadata writer.
        print(writer.get_metadata_json())

        # Set the path to save the TFLite file with metadata
        save_to_path = os.path.join(BASE_PATH, file_name.replace(".tflite", "_metadata.tflite"))

        # Populate the metadata into the model.
        writer_utils.save_file(writer.populate(), save_to_path)

        # Optional: You can download the TFLite file with metadata if needed.
        # files.download(save_to_path)
