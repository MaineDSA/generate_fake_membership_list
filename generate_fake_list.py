"""Create test dataset for DSA membership list"""

import argparse
import datetime
import logging
import random
from pathlib import Path
from zipfile import ZipFile
from tqdm import tqdm
import pandas as pd

from utils.fake_members import generate_member
from utils.fake_addresses import (
    get_random_realistic_address,
    get_random_business_address,
    get_fake_address,
)


logging.basicConfig(level=logging.WARNING, format="%(asctime)s : %(levelname)s : %(message)s")


# Constants
CHAPTER_ZIPS_FILE = "./dsa_chapter_zip_codes/chapter_zips.csv"
MAPBOX_TOKEN_FILE = ".mapbox_token"


def parse_arguments():
    """Get the arguments from the command line"""
    parser = argparse.ArgumentParser(description="Fake Membership List Generator")
    parser.add_argument(
        "--dsa-chapter",
        help="DSA Chapter Name\nGenerate real addresses for the specified chapter.\nSee dsa_chapter_zip_codes/chapter_zips.csv",
        type=str,
        default="Maine",
    )
    parser.add_argument(
        "--ydsa-chapter", help="yDSA Chapter Name\n", type=str, default=""
    )
    parser.add_argument(
        "--zips",
        help="Generate real addresses based on zip codes (comma-separated)",
        action="extend",
        nargs="+",
        type=str,
    )
    parser.add_argument(
        "-size",
        help="List Size\nThe number of fake members to be generated.",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--output",
        help="Output File Names\nThe name to use for the generated files.",
        type=str,
        default="fake_membership_list",
    )
    return parser.parse_args()


def read_chapter_zip_codes(dsa_chapter):
    """Get the appropriate list of zip codes for the specified DSA Chapter"""
    if not dsa_chapter or not Path(CHAPTER_ZIPS_FILE).is_file():
        return []

    logging.info("Loading chapter zip codes from %s", CHAPTER_ZIPS_FILE)
    df = pd.read_csv(CHAPTER_ZIPS_FILE)
    chapter_zip_codes = list(df.loc[df["chapter"] == dsa_chapter]["zip"])
    chapter_zip_codes = [str(zip_code).zfill(5) for zip_code in chapter_zip_codes]
    return chapter_zip_codes


def generate_fake_list(args):
    """Create a fake membership list based on the specified arguments"""
    chapter_zip_codes = read_chapter_zip_codes(args.dsa_chapter)

    people = []
    for _ in tqdm(range(args.size), unit="comrades"):
        person = generate_member()

        if not Path(MAPBOX_TOKEN_FILE).is_file():
            person.update(get_fake_address())
        elif args.zips or chapter_zip_codes:
            zip_code = random.choice(args.zips or chapter_zip_codes)
            realistic_address = get_random_realistic_address(zip_code)
            if realistic_address:
                person.update(realistic_address)
            else:
                logging.warning("No realistic address found for zip code: %s...", zip_code)
                business_address = get_random_business_address(zip_code)
                if business_address:
                    person.update(business_address)
                else:
                    logging.warning("No business addresses found for zip code: %s...", zip_code)
                    person.update(get_fake_address())

        person["dsa_chapter"] = args.dsa_chapter
        person["ydsa_chapter"] = args.ydsa_chapter
        people.append(person)

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
    args = parse_arguments()
    generate_fake_list(args)


if __name__ == "__main__":
    main()
