[![Check Python Code](https://github.com/MaineDSA/generate_fake_membership_list/actions/workflows/ruff.yml/badge.svg)](https://github.com/MaineDSA/generate_fake_membership_list/actions/workflows/ruff.yml) [![CodeQL](https://github.com/MaineDSA/generate_fake_membership_list/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/MaineDSA/generate_fake_membership_list/actions/workflows/github-code-scanning/codeql)
# Fake DSA Membership List Generator
A python module to randomly generate a membership list in the style of DSA National for use in testing DSA tech tools.

## Getting Started
To run this code, you'll need to have Python 3.9, 3.10, 3.11, or 3.12 installed on your machine. [Windows installation instructions](https://learn.microsoft.com/en-us/windows/python/beginners).
You'll also need to clone this repository into a folder on your computer.
Once you have done this, you need to install the required packages by running the following commands from inside the project folder:

1. Create a virtual environment named `.venv`:
```shell
python -m venv .venv
```

2. Activate the new virtual envronment `.venv`:
```shell
source .venv/bin/activate
```

3. Install the required Python modules
```shell
python -m pip install -r requirements.txt
```

## Features
* Creates a fake membership list containing sharable data for use in testing DSA tech tools.
* Can create lists with "real" / mappable addresses within the geographic boundary of the specified chapter.

## Usage
1. Open the repository folder you downloaded earlier in a terminal and run the command:
```shell
python -m generate_fake_list [--args]
```
2. The output files will be located in the repository directory and has the default name `fake_membership_list.csv` and `fake_membership_list.zip`.

## Options
```
  -h, --help                Show this help message and exit.
  --dsa-chapter DSA_CHAPTER
                            DSA Chapter Name. Also used to generate real addresses within the bounds of the specified chapter.
                            See dsa_chapter_zip_codes/chapter_zips.csv.
  --ydsa-chapter YDSA_CHAPTER
                            yDSA Chapter Name.
  --zips ZIPS [ZIPS ...]
                            Zip Codes. Generate real addresses based on specific zip codes (Ex. --zip 04101 04102 04103).
  -size SIZE                List Size. The number of fake members to be generated.
  --output OUTPUT           Output File Names. The name to use for the generated files.
```

Feel free to explore the code and modify it according to your needs!
