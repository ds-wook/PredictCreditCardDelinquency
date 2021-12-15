import warnings
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore")


def category_income(data: pd.DataFrame) -> pd.DataFrame:
    data["income_total"] = data["income_total"] / 10000
    conditions = [
        (data["income_total"].le(18)),
        (data["income_total"].gt(18) & data["income_total"].le(33)),
        (data["income_total"].gt(33) & data["income_total"].le(49)),
        (data["income_total"].gt(49) & data["income_total"].le(64)),
        (data["income_total"].gt(64) & data["income_total"].le(80)),
        (data["income_total"].gt(80) & data["income_total"].le(95)),
        (data["income_total"].gt(95) & data["income_total"].le(111)),
        (data["income_total"].gt(111) & data["income_total"].le(126)),
        (data["income_total"].gt(126) & data["income_total"].le(142)),
        (data["income_total"].gt(142)),
    ]
    choices = [i for i in range(10)]

    data["income_total"] = np.select(conditions, choices)
    return data


def load_dataset(path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(path + "train.csv")
    train = train.drop(["index"], axis=1)
    train.fillna("NAN", inplace=True)

    test = pd.read_csv(path + "test.csv")
    test = test.drop(["index"], axis=1)
    test.fillna("NAN", inplace=True)

    # absolute
    train["DAYS_EMPLOYED"] = train["DAYS_EMPLOYED"].map(lambda x: 0 if x > 0 else x)
    train["DAYS_EMPLOYED"] = np.abs(train["DAYS_EMPLOYED"])
    test["DAYS_EMPLOYED"] = test["DAYS_EMPLOYED"].map(lambda x: 0 if x > 0 else x)
    test["DAYS_EMPLOYED"] = np.abs(test["DAYS_EMPLOYED"])
    train["DAYS_BIRTH"] = np.abs(train["DAYS_BIRTH"])
    test["DAYS_BIRTH"] = np.abs(test["DAYS_BIRTH"])
    train["begin_month"] = np.abs(train["begin_month"]).astype(int)
    test["begin_month"] = np.abs(test["begin_month"]).astype(int)

    # DAYS_BIRTH
    train["DAYS_BIRTH_month"] = np.floor(train["DAYS_BIRTH"] / 30) - (
        (np.floor(train["DAYS_BIRTH"] / 30) / 12).astype(int) * 12
    )
    train["DAYS_BIRTH_month"] = train["DAYS_BIRTH_month"].astype(int)
    train["DAYS_BIRTH_week"] = np.floor(train["DAYS_BIRTH"] / 7) - (
        (np.floor(train["DAYS_BIRTH"] / 7) / 4).astype(int) * 4
    )
    train["DAYS_BIRTH_week"] = train["DAYS_BIRTH_week"].astype(int)
    test["DAYS_BIRTH_month"] = np.floor(test["DAYS_BIRTH"] / 30) - (
        (np.floor(test["DAYS_BIRTH"] / 30) / 12).astype(int) * 12
    )
    test["DAYS_BIRTH_month"] = test["DAYS_BIRTH_month"].astype(int)
    test["DAYS_BIRTH_week"] = np.floor(test["DAYS_BIRTH"] / 7) - (
        (np.floor(test["DAYS_BIRTH"] / 7) / 4).astype(int) * 4
    )
    test["DAYS_BIRTH_week"] = test["DAYS_BIRTH_week"].astype(int)

    # Age
    train["Age"] = np.abs(train["DAYS_BIRTH"]) // 360
    test["Age"] = np.abs(test["DAYS_BIRTH"]) // 360

    # DAYS_EMPLOYED
    train["DAYS_EMPLOYED_month"] = np.floor(train["DAYS_EMPLOYED"] / 30) - (
        (np.floor(train["DAYS_EMPLOYED"] / 30) / 12).astype(int) * 12
    )
    train["DAYS_EMPLOYED_month"] = train["DAYS_EMPLOYED_month"].astype(int)
    train["DAYS_EMPLOYED_week"] = np.floor(train["DAYS_EMPLOYED"] / 7) - (
        (np.floor(train["DAYS_EMPLOYED"] / 7) / 4).astype(int) * 4
    )
    train["DAYS_EMPLOYED_week"] = train["DAYS_EMPLOYED_week"].astype(int)
    test["DAYS_EMPLOYED_month"] = np.floor(test["DAYS_EMPLOYED"] / 30) - (
        (np.floor(test["DAYS_EMPLOYED"] / 30) / 12).astype(int) * 12
    )
    test["DAYS_EMPLOYED_month"] = test["DAYS_EMPLOYED_month"].astype(int)
    test["DAYS_EMPLOYED_week"] = np.floor(test["DAYS_EMPLOYED"] / 7) - (
        (np.floor(test["DAYS_EMPLOYED"] / 7) / 4).astype(int) * 4
    )
    test["DAYS_EMPLOYED_week"] = test["DAYS_EMPLOYED_week"].astype(int)

    # EMPLOYED
    train["EMPLOYED"] = train["DAYS_EMPLOYED"] / 360
    test["EMPLOYED"] = test["DAYS_EMPLOYED"] / 360

    # before_EMPLOYED
    train["before_EMPLOYED"] = train["DAYS_BIRTH"] - train["DAYS_EMPLOYED"]
    train["before_EMPLOYED_month"] = np.floor(train["before_EMPLOYED"] / 30) - (
        (np.floor(train["before_EMPLOYED"] / 30) / 12).astype(int) * 12
    )
    train["before_EMPLOYED_month"] = train["before_EMPLOYED_month"].astype(int)
    train["before_EMPLOYED_week"] = np.floor(train["before_EMPLOYED"] / 7) - (
        (np.floor(train["before_EMPLOYED"] / 7) / 4).astype(int) * 4
    )
    train["before_EMPLOYED_week"] = train["before_EMPLOYED_week"].astype(int)
    test["before_EMPLOYED"] = test["DAYS_BIRTH"] - test["DAYS_EMPLOYED"]
    test["before_EMPLOYED_month"] = np.floor(test["before_EMPLOYED"] / 30) - (
        (np.floor(test["before_EMPLOYED"] / 30) / 12).astype(int) * 12
    )
    test["before_EMPLOYED_month"] = test["before_EMPLOYED_month"].astype(int)
    test["before_EMPLOYED_week"] = np.floor(test["before_EMPLOYED"] / 7) - (
        (np.floor(test["before_EMPLOYED"] / 7) / 4).astype(int) * 4
    )
    test["before_EMPLOYED_week"] = test["before_EMPLOYED_week"].astype(int)

    # gender_car_reality
    train["user_code"] = (
        train["gender"].astype(str)
        + "_"
        + train["car"].astype(str)
        + "_"
        + train["reality"].astype(str)
    )
    test["user_code"] = (
        test["gender"].astype(str)
        + "_"
        + test["car"].astype(str)
        + "_"
        + test["reality"].astype(str)
    )

    del_cols = [
        "gender",
        "car",
        "reality",
        "email",
        "child_num",
        "DAYS_BIRTH",
        "DAYS_EMPLOYED",
    ]
    train.drop(train.loc[train["family_size"] > 7, "family_size"].index, inplace=True)
    train.drop(del_cols, axis=1, inplace=True)
    test.drop(del_cols, axis=1, inplace=True)

    cat_cols = [
        "income_type",
        "edu_type",
        "family_type",
        "house_type",
        "occyp_type",
        "user_code",
    ]

    for col in cat_cols:
        label_encoder = LabelEncoder()
        label_encoder = label_encoder.fit(train[col])
        train[col] = label_encoder.transform(train[col])
        test[col] = label_encoder.transform(test[col])

    return train, test
