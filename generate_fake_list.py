"""Create test dataset for DSA membership list"""

import argparse
import datetime
import logging
import random
from pathlib import Path
from zipfile import ZipFile

from attrs import asdict
import pandas as pd
from tqdm import tqdm
from utils.fake_addresses import (
    get_fake_address,
    get_random_realistic_address,
)
from utils.fake_members import Member


CHAPTER_ZIPS_PATH = Path("./dsa_chapter_zip_codes/chapter_zips.csv")
MAPBOX_TOKEN_PATH = Path(".mapbox_token")


def parse_arguments() -> argparse.Namespace:
    """Get the arguments from the command line"""
    parser = argparse.ArgumentParser(description="Fake DSA Membership List Generator")

    # IF YOU CHANGE THESE, BE SURE TO UPDATE README.MD!!
    parser.add_argument(
        "--dsa-chapter",
        help="DSA Chapter Name.\nAlso used to generate real addresses within the bounds of the specified chapter.\nSee dsa_chapter_zip_codes/chapter_zips.csv",
        type=str,
        default="Maine",
    )
    parser.add_argument("--ydsa-chapter", help="yDSA Chapter Name", type=str, default="")
    parser.add_argument(
        "--zips",
        help="Zip Codes.\nGenerate real addresses based on specific zip codes instead of using chapter name (Ex. --zip 04101 04102 04103).",
        action="extend",
        nargs="+",
        type=str,
    )
    parser.add_argument(
        "-size",
        help="List Size.\nThe number of fake members to be generated.",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--output",
        help="Output File Names.\nThe name to use for the generated files.",
        type=str,
        default="fake_membership_list",
    )

    return parser.parse_args()


def read_chapter_zip_codes(dsa_chapter: str) -> list[str]:
    """Get the appropriate list of zip codes for the specified DSA Chapter"""
    if not dsa_chapter or not CHAPTER_ZIPS_PATH.is_file():
        logging.warning("No chapter zip codes loaded, cannot auto-select zip codes based on chapter.")
        return []

    logging.info("Loading chapter zip codes from %s", CHAPTER_ZIPS_PATH)
    df = pd.read_csv(CHAPTER_ZIPS_PATH)
    chapter_zip_codes = list(df.loc[df["chapter"] == dsa_chapter]["zip"])
    return [str(zip_code).zfill(5) for zip_code in chapter_zip_codes]


def generate_fake_list(args: argparse.Namespace):
    """Create a fake membership list based on the specified arguments"""
    chapter_zip_codes = read_chapter_zip_codes(args.dsa_chapter)

    missing_zips = []
    people = [asdict(Member()) for _ in range(args.size)]
    for person in tqdm(people, unit="comrades"):
        if not MAPBOX_TOKEN_PATH.is_file():
        elif args.zips or chapter_zip_codes:
            zip_code = random.choice(args.zips or chapter_zip_codes)
            address = get_random_realistic_address(zip_code)
            if not address:
                missing_zips.append(zip_code)
                address = get_fake_address(zip_code)
            person.update(asdict(address))

        person["dsa_chapter"] = args.dsa_chapter
        person["ydsa_chapter"] = args.ydsa_chapter

    if missing_zips:
        logging.warning("No realistic address found for %s zip codes:\n%s...", len(missing_zips), missing_zips)

    df = pd.DataFrame(data=people)
    todays_date = datetime.datetime.now().date().strftime("%Y%m%d")
    filename_and_date = f"{args.output}_{todays_date}"

    logging.info("Writing csv file")
    df.to_csv(f"./{filename_and_date}.csv", sep=",", index=False)

    output_zip_file = f"./{filename_and_date}.zip"
    if Path(output_zip_file).is_file():
        logging.info("Deleting file: %s", output_zip_file)
        Path(output_zip_file).unlink()
    with ZipFile(output_zip_file, "x") as list_zip:
        logging.info("Writing zip file")
        list_zip.write(f"./{filename_and_date}.csv", arcname=f"{args.output}.csv")


def main():
    """Create test dataset for DSA membership list"""
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s : %(levelname)s : %(message)s")
    args = parse_arguments()
    generate_fake_list(args)


if __name__ == "__main__":
    main()
