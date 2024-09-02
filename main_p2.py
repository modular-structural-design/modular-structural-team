import json
from importlib import reload
import os
from pkgs import utils_p2 as ut2
from pkgs import FEM_preprocess as FEA_pre

# region Reading data
data_paths = ut2.load_paths_p2()

with open(data_paths["building_data"], "r") as f:
    building_data = json.load(f)

out_space_num = len(building_data["outer_space_config"])
out_space_info = building_data["outer_space_per_building"]
out_space_cfg = building_data["outer_space_config"]
inner_space_info = building_data["outer_space_has_inner_space"]
inner_space_cfg = building_data["inner_space_config"]
out_space_relationship = building_data["outer_space_relationship"]
FEM_loading = data_paths["FEM_loading"]
FEM_sematics = data_paths["FEM_semantics"]
# SAP_path = data_paths["sap_dir"]
# endregion


# # region read modular information
# story_height = {"0": 3000, "1": 3000, "2": 3000}
#
# case_number = 1
# case_name = "layout" + str(case_number) + ".json"
# with open(os.path.join(data_paths["Layout_dir"], case_name), "r") as f:
#     modular_plan = json.load(f)
# modular_plan = {int(key): value for key, value in modular_plan.items()}
#
# with open(data_paths["modular_type_data"], "r") as f:
#     tp = json.load(f)
# modular_type = tp["case1"]
# modular_type = {int(key): value for key, value in modular_type.items()}
# # endregion
#
# # region process analysis information - mic basic geometry and FEM
# case_name = "case1"
# project_info = FEA_pre.output_structured_data(
#     building_data, modular_plan, modular_type, story_height, data_paths["FEM_model_dir"], case_name
# )
# MiC_info = FEA_pre.implement_modular_structure_data(data_paths["FEM_model_dir"], case_name)
# nodes, edges, planes = FEA_pre.transform_mic_data(MiC_info)
# MiC_info2 = FEA_pre.modify_mic_geo(data_paths["FEM_model_dir"], case_name, contraction=200)
# nodes, edges, planes = FEA_pre.transform_mic_data2(MiC_info2)
# FEA_info2 = FEA_pre.implement_FEA_info_enrichment(data_paths["FEM_model_dir"], case_name, FEM_loading)
# # endregion


# region  process analysis information - update mic FEM sections
modular_FEM = {1: {"sections": [6, 8, 12]}, 2: {"sections": [2, 7, 17]}}


# endregion


# region INTEGRATION into class
class MicFeaInfo(object):
    def __init__(self, layout_case, modular_type_config, fea_case, story_height, contraction):
        self.layout_case = layout_case
        self.modular_type_config = modular_type_config
        self.fea_case = fea_case
        self.story_height = story_height
        self.contraction = contraction
        self.mic_fea_info = self.generate_basic_info()
        pass

    def generate_basic_info(self):
        case_name = self.layout_case
        modular_type = self.modular_type_config
        with open(os.path.join(data_paths["Layout_dir"], case_name), "r") as f:
            modular_plan = json.load(f)
        modular_plan = {int(key): value for key, value in modular_plan.items()}

        with open(data_paths["modular_type_data"], "r") as f:
            tp = json.load(f)
        modular_type = tp[modular_type]
        modular_type = {int(key): value for key, value in modular_type.items()}

        fea_case_name = self.fea_case
        project_info = FEA_pre.output_structured_data(
            building_data, modular_plan, modular_type, self.story_height, data_paths["FEM_model_dir"], fea_case_name
        )
        MiC_info = FEA_pre.implement_modular_structure_data(data_paths["FEM_model_dir"], fea_case_name)
        nodes, edges, planes = FEA_pre.transform_mic_data(MiC_info)
        MiC_info2 = FEA_pre.modify_mic_geo(data_paths["FEM_model_dir"], fea_case_name, contraction=self.contraction)
        nodes, edges, planes = FEA_pre.transform_mic_data2(MiC_info2)
        FEA_info2 = FEA_pre.implement_FEA_info_enrichment(data_paths["FEM_model_dir"], fea_case_name, FEM_loading)

        # self.mic_fea_info = FEA_info2
        return FEA_info2

    def implement_sections(self, section_num, fea_case_name):
        mic_info = FEA_pre.modify_mic_info_section(
            self.mic_fea_info, data_paths["FEM_model_dir"], fea_case_name, section_num
        )
        self.mic_fea_info = mic_info
        pass

    def set_multi_tasks(self, section_lists):
        case_name_dir = {}
        for key, value in section_lists.items():
            case_name = "fea_case" + str(key)
            file_path = os.path.join(data_paths["FEM_model_dir"], case_name)
            case_name_dir[case_name] = file_path
            mic_info = FEA_pre.modify_mic_info_section(self.mic_fea_info, data_paths["FEM_model_dir"], case_name, value)
        return None


# endregion
