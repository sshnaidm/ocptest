#!/usr/bin/env python3

import argparse
import sys
import os

# add parent directory to sys.path so we can import from plugins
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plugins.module_utils.ocp_image_lib import OCPImage
# while running in a console, I still have a problem     from plugins.modules.ocp_version import OCPVersion
#ModuleNotFoundError: No module named 'plugins'
# fix it
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder


def parse_args():
    argparser = argparse.ArgumentParser()

    argparser.add_argument("-t", "--tag", help="OCP tag (4.12, 4.11, etc)")
    argparser.add_argument(
        "-r",
        "--release",
        choices=["ci", "nightly", "stable", "candidate", "dev-preview"],
        help="OCP release type. Choose from %(choices)s",
    )
    argparser.add_argument(
        "-f", "--full-tag", required=False, help="Full OCP tag (4.12.0-0.nightly-2023-03-09-142909, etc)"
    )
    argparser.add_argument("-j", "--image", help="Full image name to use for install")
    args = argparser.parse_args()
    if args.full_tag and (args.tag or args.release):
        argparser.error("Full tag cannot be used with tag or release")
    elif args.image and (args.tag or args.release):
        argparser.error("Image cannot be used with tag or release")
    elif args.full_tag and args.image:
        argparser.error("Full tag cannot be used with image")
    elif not args.full_tag and not (args.tag and args.release) and not args.image:
        argparser.error(
            "Both tag and release must be specified, or full tag or image must be specified")
    return args


def main():
    args = parse_args()
    print(args)
    full_image = args.image or OCPImage(
        tag=args.tag, release=args.release, full_tag=args.full_tag).resolve_tag()
    print(f"Resolved image: {full_image}")


if __name__ == "__main__":
    main()
