"""
Creates a dict of information for a single fake DSA member keyed to the column names
found in nationally-provided membership lists, with the exception of an address
"""

import datetime
from attrs import define, Factory
from dateutil.relativedelta import relativedelta
from faker import Faker
from faker_education import SchoolProvider
import numpy as np

fake = Faker()
fake.add_provider(SchoolProvider)


def generate_middle_name() -> str:
    return np.random.choice([fake.first_name() + ".", fake.first_name(), ""], p=[0.08, 0.06, 0.86])


def generate_do_not_call() -> str:
    return np.random.choice(["True", ""], p=[0.08, 0.92])


def generate_p2ptext_optout() -> str:
    return np.random.choice(["TRUE", ""], p=[0.16, 0.84])


def generate_mobile_phone() -> str:
    return np.random.choice([fake.basic_phone_number(), ""], p=[0.7, 0.3])


def generate_home_phone() -> str:
    return np.random.choice([fake.basic_phone_number(), ""], p=[0.5, 0.5])


def generate_work_phone() -> str:
    return ""


def generate_best_phone(self) -> str:
    return max(
        [
            self.mobile_phone,
            self.home_phone,
            self.work_phone,
        ],
        key=bool,
        default="",
    )


def generate_join_date() -> str:
    return fake.date_between_dates(  # date must be between 1982-06-01 and today.
        date_start=(datetime.datetime.strptime("1982-06-01", "%Y-%m-%d").date()),
        date_end=(datetime.datetime.now().date()),
    ).isoformat()


def generate_xdate(self) -> str:
    expiration_date = fake.date_between_dates(
        date_start=(
            datetime.datetime.strptime(self.join_date, "%Y-%m-%d").date() + relativedelta(years=1)
        ),  # date must be at least 1 yr after join date but no more than one year in the future.
        date_end=(datetime.datetime.now().date() + relativedelta(years=1)),
    ).isoformat()
    # Lifetime members have join date of 2099-11-01
    return np.random.choice([expiration_date, "2099-11-01"], p=[0.99, 0.01])


def generate_membership_status(self) -> str:
    if datetime.datetime.strptime(self.xdate, "%Y-%m-%d").date() >= datetime.datetime.now().date():
        return "Member in Good Standing"
    elif datetime.datetime.strptime(self.xdate, "%Y-%m-%d").date() > (datetime.datetime.now().date() - relativedelta(years=1)):
        return "Member"
    return "Lapsed"


def generate_memb_status_letter(self) -> str:
    if self.membership_status.find("Member") == 0:
        return "M"
    return "L"


def generate_membership_type() -> str:
    return np.random.choice(
        ["", "one-time", "yearly", "annual", "monthly", "income-based"],
        p=[0.01, *([0.2] * 4), 0.19],
    )


def generate_monthly_dues_status(self) -> str:
    monthly_dues_types = [
        "lapsed",
        "past_due",
        "canceled_by_processor",
        "canceled_by_admin",
        "canceled_by_failure",
    ]
    if self.membership_status == "Member in Good Standing":
        monthly_dues_types.append("active")
    return np.random.choice(monthly_dues_types)


def generate_yearly_dues_status(self) -> str:
    yearly_dues_types = [
        "",
        "never",
        "canceled_by_user",
        "canceled_by_processor",
        "canceled_by_admin",
        "canceled_by_failure",
    ]
    if (self.membership_status == "Member in Good Standing") and (self.monthly_dues_status != "active"):
        yearly_dues_types.append("active")
    return np.random.choice(yearly_dues_types)


def generate_union_member() -> str:
    return np.random.choice(
        [
            "",
            "Yes, current union member",
            "Yes, retired union member",
            "No, but former union member",
            "No, not a union member",
            "Currently organizing my workplace",
        ],
        p=[0.05, *([0.19] * 5)],
    )


def generate_union_name(self) -> str:
    if self.union_member.find("Yes") != 0:
        return ""
    return np.random.choice(
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
        p=[0.1, *([0.09] * 10)],
    )


def generate_union_local(self) -> str:
    if self.union_member.find("Yes") != 0:
        return ""
    return fake.random_int(min=5, max=5999)


def generate_accomodations() -> str:
    return ""


def generate_race() -> str:
    return np.random.choice(
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
    )


def generate_student_yes_no() -> str:
    return np.random.choice(
        [
            "",
            "No",
            "Yes, college student",
            "Yes, high school student",
            "Yes, graduate student",
        ],
    )


def generate_student_school_name(self) -> str:
    if self.student_yes_no.find("Yes") != 0:
        return ""
    return fake.school_name()


def generate_mailing_pref() -> str:
    return np.random.choice(
        [
            "Yes",
            "No",
            "Membership card only",
        ],
    )


def generate_actionkit_id() -> int:
    return fake.unique.random_int(min=1000, max=999999)


def generate_chapter() -> str:
    return ""


def generate_congressional_district() -> str:
    return np.random.choice(
        [
            "ME_01",
            "ME_02",
        ],
    )


@define
class Member:
    """Represents the data of a single fake member"""

    first_name: str = Factory(fake.first_name)
    middle_name: str = Factory(generate_middle_name)
    last_name: str = Factory(fake.last_name)
    email: str = Factory(fake.email)
    do_not_call: str = Factory(generate_do_not_call)
    p2ptext_optout: str = Factory(generate_p2ptext_optout)
    mobile_phone: str = Factory(generate_mobile_phone)
    home_phone: str = Factory(generate_home_phone)
    work_phone: str = Factory(generate_work_phone)
    best_phone: str = Factory(generate_best_phone, takes_self=True)
    join_date: str = Factory(generate_join_date)
    xdate: str = Factory(generate_xdate, takes_self=True)
    membership_status: str = Factory(generate_membership_status, takes_self=True)
    memb_status_letter: str = Factory(generate_memb_status_letter, takes_self=True)
    membership_type: str = Factory(generate_membership_type)
    monthly_dues_status: str = Factory(generate_monthly_dues_status, takes_self=True)
    yearly_dues_status: str = Factory(generate_yearly_dues_status, takes_self=True)
    union_member: str = Factory(generate_union_member)
    union_name: str = Factory(generate_union_name, takes_self=True)
    union_local: str = Factory(generate_union_local, takes_self=True)
    accomodations: str = Factory(generate_accomodations)
    race: str = Factory(generate_race)
    student_yes_no: str = Factory(generate_student_yes_no)
    student_school_name: str = Factory(generate_student_school_name, takes_self=True)
    mailing_pref: str = Factory(generate_mailing_pref)
    actionkit_id: int = Factory(generate_actionkit_id)
    dsa_chapter: int = Factory(generate_chapter)
    ydsa_chapter: int = Factory(generate_chapter)
    congressional_district: int = Factory(generate_congressional_district)
