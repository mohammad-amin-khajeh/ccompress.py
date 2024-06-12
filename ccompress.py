#!/usr/bin/env python

import argparse
from glob import glob
from os import chdir, getenv, makedirs, path
from shutil import move, rmtree
from subprocess import call
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

try:
    import notify2
except ModuleNotFoundError:
    pass
else:
    notify_me = True

HOME = getenv("HOME")

parser = argparse.ArgumentParser(
    description="compresses manga/comic to read on smartphones with low storage."
)


parser.add_argument(
    "-o",
    "--output",
    metavar="",
    help="specify the output directory",
    type=str,
    nargs=1,
    default=f"{HOME}/Documents/manga/compressed",
)


parser.add_argument(
    "-q",
    "--quality",
    metavar="",
    help="specify the value for the -quality flag of imagemagick, defaults to 50",
    type=str,
    default="50",
)


parser.add_argument(
    "-r",
    "--resize",
    metavar="",
    help="specify the value for the -resize flag of imagemagick, defaults to 70",
    type=str,
    default="60%",
)


parser.add_argument(
    "-e",
    "--extension",
    metavar="",
    help="specify the format to use for conversion, defaults to webp",
    type=str,
    default="webp",
)


parser.add_argument(
    "-f",
    "--filter",
    metavar="",
    help="specify the filter for imagemagick to use, defaults to catrom",
    type=str,
    default="catrom",
)


parser.add_argument(
    "input",
    metavar="",
    help="comics to compress",
    type=str,
    nargs="+",
)

group = parser.add_mutually_exclusive_group()


group.add_argument(
    "-v",
    "--verbose",
    help="be verbose",
    action="store_true",
)


group.add_argument(
    "--quiet",
    help="be quiet",
    action="store_true",
)


args = parser.parse_args()


def ok(comic: str) -> bool:
    correct_formats = (".cbz", ".cbr", ".zip")
    if not comic.endswith(correct_formats):
        print("not a valid comic")
        return False
    else:
        return True


def requirements(temp_dir: str, raw_dir: str, compressed_dir: str) -> None:
    if not path.exists(args.output):
        makedirs(args.output, exist_ok=True)

    if not path.exists(temp_dir):
        makedirs(temp_dir, exist_ok=True)

    if not path.exists(raw_dir):
        makedirs(raw_dir, exist_ok=True)

    if not path.exists(compressed_dir):
        makedirs(compressed_dir, exist_ok=True)


def unzip(comic: str, raw_dir: str) -> bool:
    try:
        with ZipFile(comic, "r") as original_comic:
            original_comic.extractall(raw_dir)
            return True
    except BadZipFile:
        try:
            call(f"unzip '{comic}' -d '{raw_dir}' ")
            return True
        except:
            print("could not convert the comic.")
            return False


def compress(raw_dir: str) -> None:
    chdir(raw_dir)
    images = glob("*.png") + glob("*.webp") + glob("*.jpeg") + glob("*.jpg")
    for image in images:
        image_extension = image.split(".")[-1]
        output_image = image.removesuffix(image_extension)
        call(
            f"convert '{image}' -filter '{args.filter}' -resize '{args.resize}' -quality '{args.quality}' '../compressed/{output_image}{args.extension}'",
            shell=True,
        )
        if args.verbose:
            print(image, "has been converted.")
        elif args.quiet:
            pass
        else:
            print("converting...\r", end="")


def package(output_name: str, compressed_dir: str) -> None:
    chdir(compressed_dir)
    images = glob(f"*.{args.extension}")
    with ZipFile(output_name, "w", ZIP_DEFLATED) as zip_file:
        for image in images:
            zip_file.write(image)
    move(output_name, args.output)


def cleanup(comic_temp_dir: str) -> None:
    rmtree(comic_temp_dir)


def notify(comic_name: str) -> None:
    if notify_me:
        notify2.init("ccompress")
        notification = notify2.Notification(
            "completed!", f"{comic_name} has been converted successfully."
        )
        notification.show()


def main():
    for comic in args.input:
        comic_file = str(comic).split("/")[-1]
        temp_dir = f"/tmp/comic/{comic_file}"
        raw_dir = temp_dir + "/raw"
        compressed_dir = temp_dir + "/compressed"
        if not ok(comic):
            continue
        if path.isfile(args.output + "/" + comic_file):
            print("file already exists! aborting.")
            continue
        requirements(temp_dir, raw_dir, compressed_dir)
        unzipped = unzip(comic, raw_dir)
        if not unzipped:
            continue
        compress(raw_dir)
        package(comic_file, compressed_dir)
        cleanup(temp_dir)
        notify(comic_file)


if __name__ == "__main__":
    main()
