"""Creates a dict of information for a single fake DSA member keyed to the column names found in nationally-provided membership lists, with the exception of an address"""

import datetime
import numpy as np
from dateutil.relativedelta import relativedelta
from faker import Faker
from faker_education import SchoolProvider

fake = Faker()
fake.add_provider(SchoolProvider)


def generate_member():
    """Creates a dict of information for a single fake DSA member keyed to the column names found in nationally-provided membership lists, with the exception of an address"""
    person = {}

    person["first_name"] = fake.first_name()
    person["middle_name"] = np.random.choice(
        [fake.first_name()[0] + ".", fake.first_name(), ""], 1, p=[0.08, 0.06, 0.86]
    )[0]
    person["last_name"] = fake.last_name()

    person["email"] = fake.email()

    person["do_not_call"] = np.random.choice(["True", ""], 1, p=[0.08, 0.92])[0]
    person["p2ptext_optout"] = np.random.choice(["TRUE", ""], 1, p=[0.16, 0.84])[0]

    person["mobile_phone"] = np.random.choice(
        [fake.basic_phone_number(), ""], 1, p=[0.7, 0.3]
    )[0]
    person["home_phone"] = np.random.choice(
        [fake.basic_phone_number(), ""], 1, p=[0.5, 0.5]
    )[0]
    person["work_phone"] = ""
    person["best_phone"] = next(
        (
            s
            for s in [
                person["mobile_phone"],
                person["home_phone"],
                person["work_phone"],
            ]
            if s
        ),
        "",
    )

    person["join_date"] = fake.past_date(start_date="-15y").isoformat()
    person[
        "join_date"
    ] = fake.date_between_dates(  # date must be between 1982-06-01 and today.
        date_start=(datetime.datetime.strptime("1982-06-01", "%Y-%m-%d").date()),
        date_end=(datetime.datetime.now().date()),
    ).isoformat()
    expiration_date = fake.date_between_dates(
        date_start=(
            datetime.datetime.strptime(person["join_date"], "%Y-%m-%d").date()
            + relativedelta(
                years=1
            )  # date must be at least 1 yr after join date but no more than one year in the future.
        ),
        date_end=(datetime.datetime.now().date() + relativedelta(years=1)),
    ).isoformat()
    person["xdate"] = np.random.choice(
        [expiration_date, "2099-11-01"],
        1,
        p=[0.99, 0.01],  # Lifetime members have join date of 2099-11-01
    )[0]

    person["membership_status"] = "Lapsed"
    person["memb_status_letter"] = "L"
    if (
        datetime.datetime.strptime(person["xdate"], "%Y-%m-%d").date()
        >= datetime.datetime.now().date()
    ):
        person["membership_status"] = "Member in Good Standing"
        person["memb_status_letter"] = "M"
    elif datetime.datetime.strptime(person["xdate"], "%Y-%m-%d").date() > (
        datetime.datetime.now().date() - relativedelta(years=1)
    ):
        person["membership_status"] = "Member"
        person["memb_status_letter"] = "M"

    person["membership_type"] = np.random.choice(
        ["", "one-time", "yearly", "annual", "monthly", "income-based"],
        1,
        p=[0.01, *([0.2] * 4), 0.19],
    )[0]

    monthly_dues_types = [
        "lapsed",
        "past_due",
        "canceled_by_processor",
        "canceled_by_admin",
        "canceled_by_failure",
    ]
    if person["membership_status"] == "Member in Good Standing":
        monthly_dues_types.append("active")

    person["monthly_dues_status"] = np.random.choice(
        monthly_dues_types,
        1,
    )[0]

    yearly_dues_types = [
        "",
        "never",
        "canceled_by_user",
        "canceled_by_processor",
        "canceled_by_admin",
        "canceled_by_failure",
    ]
    if (person["membership_status"] == "Member in Good Standing") and (
        person["monthly_dues_status"] != "active"
    ):
        yearly_dues_types.append("active")

    person["yearly_dues_status"] = np.random.choice(
        yearly_dues_types,
        1,
    )[0]

    person["union_member"] = np.random.choice(
        [
            "",
            "Yes, current union member",
            "Yes, retired union member",
            "No, but former union member",
            "No, not a union member",
            "Currently organizing my workplace",
        ],
        1,
        p=[0.05, *([0.19] * 5)],
    )[0]
    person["union_name"] = ""
    person["union_local"] = ""
    if person["union_member"].find("Yes") == 0:
        person["union_name"] = np.random.choice(
            [
                "",
                "NEA",
                "SEIU",
                "AFSCME",
                "Teamsters",
                "UFCW",
                "UAW",
                "USW",
                "AFT",
                "IBEW",
                "LIUNA",
            ],
            1,
            p=[0.1, *([0.09] * 10)],
        )[0]
        person["union_local"] = fake.random_int(min=5, max=5999)

    person["accomodations"] = ""

    person["race"] = np.random.choice(
        [
            "Asian",
            "Black / of African Descent",
            "Hispanic / Latinx",
            "Jewish",
            "Native American / Indigenous",
            "Other",
            "Pacific Islander",
            "Prefer Not to Say",
            "West Asian / Middle Eastern",
            "White / of European Descent",
        ],
        1,
    )[0]

    person["student_yes_no"] = np.random.choice(
        [
            "",
            "No",
            "Yes, college student",
            "Yes, high school student",
            "Yes, graduate student",
        ],
        1,
    )[0]
    person["student_school_name"] = ""
    if person["student_yes_no"].find("Yes") == 0:
        person["student_school_name"] = fake.school_name()

    person["mailing_pref"] = np.random.choice(
        [
            "Yes",
            "No",
            "Membership card only",
        ],
        1,
    )[0]

    person["actionkit_id"] = fake.unique.random_int(min=1000, max=999999)

    person["dsa_chapter"] = ""
    person["ydsa_chapter"] = ""

    person["congressional_district"] = np.random.choice(
        [
            "ME_01",
            "ME_02",
        ],
        1,
    )[0]

    return person
