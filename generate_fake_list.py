"""Create test dataset for DSA membership list"""

import argparse
import datetime
from zipfile import ZipFile
import pandas as pd
import random

from utils.fake_members import generate_member
from utils.fake_addresses import get_random_realistic_address, get_fake_address

def main():
    """Write a test dataset to file, both as CSV and zipped CSV"""
    parser = argparse.ArgumentParser(description='Member list generator')
    parser.add_argument('--chapter-name', help='Chapter name', default="Heaven")
    parser.add_argument('--y-chapter-name', help='Young chapter name', default="")
    parser.add_argument('-n', help='Number of addresses to generate', default=10, type=int)
    parser.add_argument('--output', help='Output file name', default='fake-members.csv')
    parser.add_argument('--real-address-zips', help='Generate real addresses for these zip codes (comma-separated)')
    parser.add_argument('--mapbox-token', help='Mapbox API key (required for real addresses)')


    args = parser.parse_args()

    # Access options using args.option1, args.option2, etc.
    print(args)
  

    people = []
    for _n in range(args.n):
        person = generate_member()
        if args.mapbox_token and args.real_address_zips:
            zip_code = random.choice(args.real_address_zips.split(","))
            realistic_address = get_random_realistic_address(zip_code, args.mapbox_token)
            if realistic_address:
                person.update(realistic_address)
            else:
                print("No realistic address found for zip code: ", zip_code, "...")
                break
        else:
            person.update(get_fake_address())
        people.append(person)

  
    df = pd.DataFrame(data=people)
    todays_date = datetime.datetime.now().date().strftime('%Y%m%d')
    df.to_csv(f"./{args.output}-{todays_date}", sep=",", index=False)
    
    # with ZipFile(f"./test_membership_list_{todays_date}.zip", "x") as list_zip:
    #     list_zip.write("test_membership_list.csv")

if __name__ == "__main__":
    main()
