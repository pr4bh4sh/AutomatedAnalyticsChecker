import sys
import yaml
import hashlib
import re

from urllib import parse
from mitmproxy.script import concurrent


#
# def start():
#     return OmnitureLogger()
#

class AnalyticsLogger:
    """
    :Key_keys_to_remove store the keys, which are dynamic(may change with every call).
    """
    keys_to_remove = ['.a', '.app', '.build', '.c', '.device', '.skymiles', 'a.', 'aamb', 'aamlh', 'app.', 'build.',
                      'c.', 'ce', 'device.', 'manufacturermodel', 'mid', 'screendensity', 'screendimensions', 't',
                      'vid']

    @staticmethod
    def to_dict(input_list):
        """
        Converts provided list to dictionary object
        :param input_list:
        :return:
        """
        new_dict = dict()
        for list_item in input_list:
            key = list_item[0]
            val = list_item[1] if len(list_item) > 1 else ""
            new_dict.update({key: val})
        return new_dict

    @staticmethod
    def generate_hash(keys):
        """
        Uses the list of keys to create a Unique hash for the provided key combination so, we can store/retrieve the
        dump files based on unique name
        :param keys:
        :return:
        """
        concatenated_key_string = "".join(keys)
        key_hash = hashlib.md5()
        key_hash.update(concatenated_key_string.encode('utf-8'))
        return key_hash.hexdigest()

    def sanitize_dictionary(self, dict_to_sanitize):
        """
        Deletes the keys which are not critical for the comparision and returns sanitized dictionary
        :param dict_to_sanitize:
        :return:
        """
        for key in self.keys_to_remove:
            if key in dict_to_sanitize.keys():
                del dict_to_sanitize[key]
        return dict_to_sanitize

    def create_dict_of_params(self, request_text):
        """
        Unquotes the JSON/query param data to human format encoding and converts the data into dictionary
        :param request_text:
        :return:
        """
        # decoded_request = parse.unquote(request_text.fields)
        decoded_request = request_text.fields # tuple of tuple
        param_map = dict(decoded_request).items()
        print(param_map)
        dict_of_params = self.to_dict(param_map)
        return dict_of_params

    @staticmethod
    def create_filename_with_hash(page_name_value, md5_hashsum):
        """
        Returns file name as string
        :param page_name_value:
        :param md5_hashsum:
        :return:
        """
        page_name = page_name_value.replace(':', '').replace(' ', '_')
        filename_with_hash = page_name + '_' + md5_hashsum + '.yml'
        print(filename_with_hash)
        return filename_with_hash

    @staticmethod
    def save_to_yaml(filename_with_hash, required_dict):
        """
        Creates YAML dump file
        :param filename_with_hash:
        :param required_dict:
        :param mode:
        :return:
        """
        with open("base_line/" + filename_with_hash, 'w+') as file_to_write:
            yaml.dump(required_dict, file_to_write, default_flow_style=False, explicit_start=True)


@concurrent
def request(flow):
    """
    MITM's interface method, MITM passes every network call as flow object
    :param flow:
    :return:
    """
    # if len(sys.argv) != 2:
    #     raise ValueError("Usage: mitmdump -s 'analytics_logger.py collect/compare'")
    #
    # mode = sys.argv[1]

    if 'deltaairlines.tt.omtrdc.net/m2/deltaairlines/mbox' in flow.request.url:
        print("Host: " + flow.request.url + "\n\n")
        omniture_collect = AnalyticsLogger()
        dict_of_params = omniture_collect.create_dict_of_params(flow.request.query)
        required_dict = omniture_collect.sanitize_dictionary(dict_of_params)
        md5_hashsum = omniture_collect.generate_hash(required_dict.keys())
        file_name = required_dict['profile.airportcode']
        filename_with_hash = omniture_collect.create_filename_with_hash(file_name, md5_hashsum)
        omniture_collect.save_to_yaml(filename_with_hash, required_dict)
#
#
