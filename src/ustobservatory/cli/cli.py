import argparse
import os
import logging
from ustobservatory.image.image import Image

# we assume that these data
# have been background-subtracted, if necessary linearized,
# flat-fielded, and scaled appropriately.


def cli():
    parser = argparse.ArgumentParser(
        description="Process fits images and produce a color image"
    )
    parser.add_argument("-d", "--dir", help="Path to red image", dest="directory_path")
    parser.add_argument("-r", "--red", help="Path to red image", dest="red_image_path")
    parser.add_argument(
        "-g", "--green", help="Path to green image", dest="green_image_path"
    )
    parser.add_argument(
        "-b", "--blue", help="Path to blue image", dest="blue_image_path"
    )
    parser.add_argument(
        "-a", "--alpha", help="Path to alpha image", dest="alpha_image_path"
    )
    parser.add_argument(
        "-s",
        "--stretch",
        nargs=1,
        default=["linear,70,0.3"],
        help="Comma separated list of stretch and its parameter. Example: linear,70,0.3",
        dest="inputStretch",
    )
    parser.add_argument(
        "-o",
        "--output-destination",
        help="Path to a destination directory for saving resulting images",
        dest="destination",
    )

    args = parser.parse_args()
    input_image_data = dict
    log = logging.getLogger(__name__)

    if args.directory_path:
        path = args.directory_path
        if not os.path.isdir(path):
            log.error(f"Incorrect Directory {path}")
            raise Exception(f"Incorrect Directory Path {path}")
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                # check what color is the file
                log.info(f"File: {file_path}")
        exit(0)
    else:
        if args.red_image_path:
            input_image_data["red"] = {
                "path": args.red_image_path,
                "image": [Image(args.red_image_path, path)],
            }
        if args.green_image_path:
            input_image_data["green"] = {"path": args.green_image_path}
        if args.blue_image_path:
            input_image_data["blue"] = {"path": args.blue_image_path}
        if args.alpha_image_path:
            input_image_data["green"] = {"path": args.alpha_image_path}

    for color_name in input_image_data:
        path = color_name["path"]
        if not path:
            log.error(f"Empty file path {path}")
            continue

        if not os.path.isfile(path):
            raise Exception(f"File {path} does not exists")

        log.info(f"Saving {color_name} image path data.")
        input_image_data[color_name] = Image(color_name, path)

    log.info("Finished")


if __name__ == "__main__":
    cli()
