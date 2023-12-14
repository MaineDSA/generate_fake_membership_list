"""Create test dataset for DSA membership list"""

import argparse
import random
import datetime
from pathlib import Path
from zipfile import ZipFile
import pandas as pd
from tqdm import tqdm

from utils.fake_members import generate_member
from utils.fake_addresses import get_random_realistic_address, get_random_business_address, get_fake_address


def main():
    """Write a test dataset to file, both as CSV and zipped CSV"""
    parser = argparse.ArgumentParser(description="Member list generator")
    parser.add_argument(
        "--dsa-chapter",
        help="DSA Chapter Name\nGenerate real addresses for the specified chapter.\nSee ./dsa_chapter_zip_codes/chapter_zips.csv",
        type=str,
        default="Maine",
    )
    parser.add_argument("--ydsa-chapter", help="yDSA Chapter Name\n", type=str, default="")
    parser.add_argument(
        "--zips",
        help="Generate real addresses based on zip codes (comma-separated)",
        action="extend",
        nargs="+",
        type=str,
    )
    parser.add_argument("-size", help="List Size\nThe number of fake members to be generated.", type=int, default=10)
    parser.add_argument("--output", help="Output File Names\nThe name to use for the generated files.", type=str, default="fake_membership_list")

    args = parser.parse_args()

    # print(args)

    chapter_zip_codes = []
    if args.dsa_chapter and Path("./dsa_chapter_zip_codes/chapter_zips.csv"):
        df = pd.read_csv("./dsa_chapter_zip_codes/chapter_zips.csv")
        chapter_zip_codes = list(df.loc[df["chapter"] == args.dsa_chapter]["zip"])
        chapter_zip_codes = [str(zip_code).zfill(5) for zip_code in chapter_zip_codes]

    people = []
    for _n in tqdm(range(args.size), unit="comrades"):
        person = generate_member()
        if not Path(".mapbox_token"):
            person.update(get_fake_address())
        elif args.zips or chapter_zip_codes:
            zip_code = random.choice(args.zips or chapter_zip_codes)
            realistic_address = get_random_realistic_address(zip_code)
            if realistic_address:
                person.update(realistic_address)
            else:
                print("No realistic address found for zip code: ", zip_code, "...")
                business_address = get_random_business_address(zip_code)
                if business_address:
                    person.update(business_address)
                else:
                    print("No business addresses found for zip code: ", zip_code, "...")
                    person.update(get_fake_address())

        person["dsa_chapter"] = args.dsa_chapter
        person["ydsa_chapter"] = args.ydsa_chapter
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
