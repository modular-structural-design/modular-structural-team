import subprocess

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
