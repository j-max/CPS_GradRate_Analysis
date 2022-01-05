
STUDENT_POP_FEATURE_LIST = [
    "Student_Count_Total",
    "Student_Count_Low_Income",
    "Student_Count_Special_Ed",
    "Student_Count_English_Learners",
    "Student_Count_Black",
    "Student_Count_Hispanic",
    "Student_Count_White",
    "Student_Count_Asian",
    "Student_Count_Native_American",
    "Student_Count_Other_Ethnicity",
    "Student_Count_Asian_Pacific_Islander",
    "Student_Count_Multi",
    "Student_Count_Hawaiian_Pacific_Islander",
    "Student_Count_Ethnicity_Not_Available"]

STUDENT_POP_PERC_LIST = ["perc_" + feature for feature in
                         STUDENT_POP_FEATURE_LIST if feature !=
                         "Student_Count_Total"]
