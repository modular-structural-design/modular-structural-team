import subprocess
import sys
sys.path.append("pkgs")
from pkgs import FEM_mulit as FM



# 进行p1: 布局优化设计
# subprocess.run(["python", "main_p1.py"])


# region MiC automated FEM modeling and evaluation
# 进行p2-1: 模块结构分析信息建立
import main_p2

story_height = {"0": 3000, "1": 3000, "2": 3000}
MiC_class = main_p2.MicFeaInfo(
    layout_case="layout_test.json",  # 选择p1优化结果
    modular_type_config="case1",  # 选择mic_type_configuration的一种，与p1设置一致
    fea_case="1",  # 随意命名
    story_height=story_height,
    contraction=200,
)  # 产生一个在FEM_model\"t1"文件夹下，包含结构分析信息的"mic_fem_data.json"，此外，类属性mic_fea_info存放相同的信息 (MiC_class.mic_fea_info)

# 设置多个任务的截面尺寸，导出相应的分析模型信息到文件夹FEM_model\
# 补充结构分析信息"mic_fem_data.json"截面，此外，类属性mic_fea_info存放相同的信息
task_sections = {
    1: {1: [1, 5, 3], 2: [1, 7, 5]},
    2: {1: [1, 5, 3], 2: [1, 7, 5]},
    3: {1: [1, 5, 3], 2: [1, 7, 5]},
    4: {1: [1, 5, 3], 2: [1, 7, 5]},
}

MiC_class.set_multi_tasks(task_sections)

# endregion


###### 请在下面进行开发 ######
# !!! 开发任务 !!!
# 对上述生成的结构分析信息模型，进行单线程/多线程兼容的结构计算、分析，导出相应的计算指标到FEM_model/total_results文件夹中
# 如果更新已存在的文件请入这里所示，使用########分割线进行标注，再其下进行开发。
# 尽量不改动已存在函数

num_thread = 2
#读取所有的mic_fem_data并存入列表
all_mic_fem_data=FM.get_all_MiC_fem_data(len(task_sections))
#创建多线程接口及对应文件夹sap2000
SapModel_name, mySapObject_name, ModelPath_name, File_Path = FM.mulit_sap(num_thread)
#运行多线程计算
all_task_data = FM.thread_sap(File_Path, ModelPath_name, mySapObject_name, SapModel_name, num_thread, all_mic_fem_data, task_sections)
#关闭多线程
FM.close_mulit_sap(mySapObject_name,SapModel_name)
