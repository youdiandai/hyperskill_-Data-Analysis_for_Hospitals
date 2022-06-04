import pandas as pd


# pd.set_option('display.max_columns', 8)


def check_gender(x):
    if x == "man" or x == "male":
        return "m"
    elif x == "female" or x == "woman":
        return "f"
    elif x in ("f", "m"):
        return x


if __name__ == '__main__':
    # read data from csv file
    general = pd.read_csv('test/general.csv')
    prenatal = pd.read_csv('test/prenatal.csv')
    sports = pd.read_csv("test/sports.csv")
    prenatal.rename(columns={'HOSPITAL': 'hospital', 'Sex': 'gender', }, inplace=True)
    sports.rename(columns={'Hospital': 'hospital', 'Male/female': 'gender', }, inplace=True)
    hospital = pd.concat([general, prenatal, sports], ignore_index=True)
    hospital.drop(columns='Unnamed: 0', inplace=True)
    hospital.dropna(axis=0, how="all", inplace=True)
    hospital.loc[hospital.hospital == "prenatal", "gender"] = "f"
    hospital["gender"] = hospital["gender"].apply(check_gender)

    for x in ("bmi", "diagnosis", "blood_test", "ecg", "ultrasound", "mri", "xray", "children", "months"):
        hospital[x].fillna(0, inplace=True)
    general_df = hospital.loc[hospital.hospital == "general"]
    sports_df = hospital.loc[hospital.hospital == "sports"]
    general_sports_age_df = hospital.pivot_table(index="hospital", aggfunc="median").loc[["general", "sports"],]['age']
    max_blood_test = hospital[hospital.blood_test == "t"].pivot_table(index="hospital", values="blood_test",
                                                                      aggfunc="count")
    print(f"The answer to the 1st question is {hospital.groupby('hospital').apply(lambda x: x.shape[0]).idxmax()}")
    print(
        f"The answer to the 2nd question is {round((general_df.loc[general_df.diagnosis == 'stomach'].shape[0] / general_df.shape[0]), 3)}")
    print(
        f"The answer to the 3rd question is {round((sports_df.loc[sports_df.diagnosis == 'dislocation'].shape[0] / sports_df.shape[0]), 3)}")
    print(f"The answer to the 4th question is {int(general_sports_age_df.max()-general_sports_age_df.min())}")
    print(f"The answer to the 5th question is {max_blood_test.idxmax()[0]}, {max_blood_test.max()[0]} blood tests")
