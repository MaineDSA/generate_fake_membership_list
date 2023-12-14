"""Create test dataset for DSA membership list"""

import argparse
import random
import datetime
from pathlib import Path
from zipfile import ZipFile
import pandas as pd
from tqdm import tqdm

from utils.fake_members import generate_member
from utils.fake_addresses import get_random_realistic_address, get_fake_address


def main():
    """Write a test dataset to file, both as CSV and zipped CSV"""
    parser = argparse.ArgumentParser(description="Member list generator")
    parser.add_argument("--chapter-name", help="Chapter name", default="Maine")
    parser.add_argument("--y-chapter-name", help="Youth chapter name", default="")
    parser.add_argument("-n", help="Number of addresses to generate", default=10, type=int)
    parser.add_argument("--output", help="Output file name", default="fake_membership_list")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--chapter-addresses",
        help="Generate real addresses for the specified chapter (see ./dsa_chapter_zip_codes/chapter_zips.csv)",
    )
    group.add_argument(
        "--zip-addresses",
        help="Generate real addresses based on zip codes (comma-separated)",
    )

    args = parser.parse_args()

    # Access options using args.option1, args.option2, etc.
    print(args)

    manual_zip_codes = []
    if args.zip_addresses:
        manual_zip_codes = list(args.zip_addresses.split(","))

    chapter_zip_codes = []
    if args.chapter_addresses and Path("./dsa_chapter_zip_codes/chapter_zips.csv"):
        df = pd.read_csv("./dsa_chapter_zip_codes/chapter_zips.csv")
        chapter_zip_codes = list(df.loc[df["chapter"] == args.chapter_addresses]["zip"])
        chapter_zip_codes = [str(zip_code).zfill(5) for zip_code in chapter_zip_codes]

    people = []
    for _n in tqdm(range(args.n), unit="comrades"):
        person = generate_member()
        if not Path(".mapbox_token"):
            person.update(get_fake_address())
        elif manual_zip_codes or chapter_zip_codes:
            zip_code = random.choice(manual_zip_codes or chapter_zip_codes)
            realistic_address = get_random_realistic_address(zip_code)
            if realistic_address:
                person.update(realistic_address)
            else:
                print("No realistic address found for zip code: ", zip_code, "...")
                break
        people.append(person)

    df = pd.DataFrame(data=people)
    todays_date = datetime.datetime.now().date().strftime("%Y%m%d")
    filename_and_date = f"{args.output}_{todays_date}"
    df.to_csv(f"./{filename_and_date}.csv", sep=",", index=False)

    if Path(f"./{filename_and_date}.zip").is_file():
        Path(f"./{filename_and_date}.zip").unlink()
    with ZipFile(f"./{filename_and_date}.zip", "x") as list_zip:
        list_zip.write(f"./{filename_and_date}.csv", arcname=f"{args.output}.csv")


if __name__ == "__main__":
    main()
