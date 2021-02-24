import json

from config import input_file_path, table_config
from utils.log_utils import function_logger


@function_logger
def get_bmi_info():
    """
    This method is used to get the basic info from input json file and calculate the bmi, category and health risk
    based on the given height and weight.
    :return:
    """
    with open(input_file_path, 'r') as json_file:  # Read sample json file
        sample_json_data = json.load(json_file)

    overweight_count = 0
    for i, sample in enumerate(sample_json_data):  # loop over the sample json data given
        height_cm = sample.get('HeightCm')
        weight_kg = sample.get('WeightKg')
        person_bmi = get_bmi(height_cm, weight_kg)  # get bmi according to height and weight
        category_data = get_category(person_bmi)  # get category according to bmi
        sample_json_data[i]['bmi'] = person_bmi
        sample_json_data[i]['Category'] = category_data['Category']
        sample_json_data[i]['HealthRisk'] = category_data['HealthRisk']
        if category_data["Category"] == "Overweight":
            overweight_count += 1

    return dict(Message="Success", data=sample_json_data, overweight_count=overweight_count)


@function_logger
def get_bmi(height, weight):
    """
    This method is used to calculate the bmi based on height(cm) and weight(kg)
    :param height:
    :param weight:
    :return:
    """
    height = height / 100  # Converting to meter
    bmi = round(float(weight / (height ** 2)), 2)  # Find BMI using formula and round of 2 decimal points
    return bmi


def get_category(bmi):
    """
    This method is used to find the category based on the bmi
    :param bmi:
    :return:
    """
    for data in table_config:
        if bmi <= data.get('bmi'):  # if the bmi is lower then category high limit then its in that category
            return data
    return table_config[-1]
