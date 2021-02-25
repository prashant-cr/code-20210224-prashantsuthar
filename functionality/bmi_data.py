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

    result_data_list, overweight_count = get_result_according_data(sample_json_data)

    return dict(Message="Success", data=result_data_list, overweight_count=overweight_count)


def get_result_according_data(data_list):
    """
    This is a common function used for the result data according to the sample.
    :param data_list:
    :return:
    """
    overweight_count = 0
    for i, sample in enumerate(data_list):  # loop over the sample json data given
        height_cm = sample.get('HeightCm')
        weight_kg = sample.get('WeightKg')
        person_bmi = get_bmi(height_cm, weight_kg)  # get bmi according to height and weight
        category_data = get_category(person_bmi)  # get category according to bmi
        data_list[i]['bmi'] = person_bmi
        data_list[i]['Category'] = category_data['Category']
        data_list[i]['HealthRisk'] = category_data['HealthRisk']
        if category_data["Category"] == "Overweight":
            overweight_count += 1

    return data_list, overweight_count


def get_bmi(height, weight):
    """
    This method is used to calculate the bmi based on height(cm) and weight(kg)
    :param height:
    :param weight:
    :return:
    """
    try:
        height = height / 100  # Converting to meter
        bmi = round(float(weight / (height ** 2)), 2)  # Find BMI using formula and round of 2 decimal points
    except ZeroDivisionError:  # Zero Division Exception handled
        bmi = 0
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


@function_logger
def post_bmi_info(**kwargs):
    """
    This is post method used to calculate the bmi and category based on post input payload.
    :param kwargs:
    :return:
    """
    data = kwargs.get('data')
    result_data_list, overweight_count = get_result_according_data(data)
    return dict(Message="Success", data=result_data_list, overweight_count=overweight_count)
