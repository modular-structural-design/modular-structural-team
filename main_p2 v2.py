import json
from importlib import reload
import os
from pkgs import utils_p2 as ut2

# region Reading data
data_paths = ut2.load_paths_p2()

with open(data_paths['building_data'], 'r') as f:
    building_data = json.load(f)

out_space_num = len(building_data['outer_space_config'])
out_space_info = building_data["outer_space_per_building"]
out_space_cfg = building_data["outer_space_config"]
inner_space_info = building_data["outer_space_has_inner_space"]
inner_space_cfg = building_data["inner_space_config"]
out_space_relationship = building_data["outer_space_relationship"]

FEM_loading = data_paths['FEM_loading']
FEM_sematics = data_paths['FEM_semantics']
SAP_path = data_paths["sap_dir"]
# endregion


# region read modular information
story_height = {"0": 3000, "1": 3000, "2": 3000}

case_number = 1
case_name = 'layout' + str(case_number) + '.json'
with open(os.path.join(data_paths["Layout_dir"], case_name), 'r') as f:
    modular_plan = json.load(f)
modular_plan = {int(key): value for key, value in modular_plan.items()}

with open(data_paths['modular_type_data'], 'r') as f:
    tp = json.load(f)
modular_type = tp['case1']
modular_type = {int(key): value for key, value in modular_type.items()}
# endregion

# region process analysis information - mic basic geometry and FEM
from pkgs import FEM_preprocess as FEA_pre

reload(FEA_pre)
case_name = 'case1'
project_info = FEA_pre.output_structured_data(building_data, modular_plan, modular_type, story_height,
                                              data_paths['FEM_model_dir'], case_name)
MiC_info = FEA_pre.implement_modular_structure_data(data_paths['FEM_model_dir'], case_name)
nodes, edges, planes = FEA_pre.transform_mic_data(MiC_info)
MiC_info2 = FEA_pre.modify_mic_geo(data_paths['FEM_model_dir'], case_name, contraction=200)
nodes, edges, planes = FEA_pre.transform_mic_data2(MiC_info2)
FEA_info2 = FEA_pre.implement_FEA_info_enrichment(data_paths['FEM_model_dir'], case_name, FEM_loading)
# endregion

#### 下面就需要进行更新 #########

# region  process analysis information - update mic FEM sections
modular_FEM = {
    1: {"sections": [6, 8, 12]},
    2: {"sections": [2, 7, 17]}
}

# endregion


# region FEM information enrichment and generation
reload(ut)
# FEA_info = ut.implement_FEA_info('FEMData_prescribed/')


FEA_info2 = ut.implement_FEA_info_enrichment(FEM_mic_data_ref, FEM_loading, mic_FEM_data)

from pkgs import FEM_parser as FEA, FEM_Index_calculation as FC, FEM_run as MF

reload(FEA)
# FEA.parsing_to_sap2000(FEA_info2, FEM_sematics, modular_FEM, os.path.dirname(mic_FEM_data))
# endregion -------------------


# region Evaluationt

# reload(FC)
# FC.output_index(modular_FEM, mic_FEM_data, os.path.dirname(mic_FEM_data))

# endregion

# region single FEM analysis


# endregion

# region multi-process FEM analysis
modular_num = 3  # 模块种类数
num_thread = 2  # 线程数
pop_size = 4  # 种群数量

section_info = FC.extract_section_info()
# 生成初始种群
pop2 = MF.generate_chromosome(modular_num, section_info, pop_size)
# 所有生成运行及保存路径
SapModel_name, mySapObject_name, ModelPath_name, File_Path = MF.mulit_sap(num_thread)
# 多线程运算
MF.thread_sap(File_Path, ModelPath_name, mySapObject_name, SapModel_name, num_thread, pop2, mic_FEM_data, FEM_sematics,
              modular_num, FEA_info2)
# 关闭所有线程模型
for i in range(len(mySapObject_name)):
    ret = mySapObject_name[i].ApplicationExit(False)
    SapModel_name[i] = None
    mySapObject_name[i] = None

# endregion
