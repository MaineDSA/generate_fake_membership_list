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
    parser.add_argument(
        "-n", help="Number of addresses to generate", default=10, type=int
    )
    parser.add_argument(
        "--output", help="Output file name", default="fake_membership_list"
    )
    parser.add_argument(
        "--real-address-zips",
        help="Generate real addresses for these zip codes (comma-separated)",
    )

    args = parser.parse_args()

    # Access options using args.option1, args.option2, etc.
    print(args)

    people = []
    for _n in tqdm(range(args.n), unit="comrades", leave=False):
        person = generate_member()
        if Path(".mapbox_token") and args.real_address_zips:
            zip_code = random.choice(args.real_address_zips.split(","))
            realistic_address = get_random_realistic_address(zip_code)
            if realistic_address:
                person.update(realistic_address)
            else:
                print("No realistic address found for zip code: ", zip_code, "...")
                break
        else:
            person.update(get_fake_address())
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
