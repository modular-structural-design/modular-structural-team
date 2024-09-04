import os
import queue
import threading
from pkgs import FEM_parser as FEA
import json
from pkgs import FEM_Index_calculation as FC

def mulit_sap(num_thread):
    File_Path = []
    all_SapModel = []
    all_mySapObject = []
    all_model_path = []
    for i in range(num_thread):
        File_Path.append(os.path.join(os.getcwd(), f"FEM_model\\cases{i}"))
        sap_model_file = os.path.join(File_Path[i], 'FEM_sap2000\\MiC1.sdb')
        SapModel, mySapObject = FEA.sap2000_initialization(File_Path[i])
        all_SapModel.append(SapModel)
        all_mySapObject.append(mySapObject)
        all_model_path.append(sap_model_file)
    return all_SapModel, all_mySapObject, all_model_path, File_Path


def get_all_MiC_fem_data(popsize):
    all_data = []
    for i in range(popsize):
        # File_Path=os.path.join(os.getcwd(), f"FEM_model\\fea_case{i+1}\\mic_fem_data.json")
        with open(f'FEM_model\\fea_case{i+1}\\mic_fem_data.json', 'r') as file:
            data = json.load(file)
            all_data.append(data)
    return all_data
def thread_sap(File_Path, ModelPath, mySapObject_name, SapModel_name, num_thread, all_mic_fem_data, task_sections):

    task_data = {}
    for i in range(len(task_sections)):
        task_data[f'task{i}'] = {
            'section': task_sections[i+1]
        }

    q = queue.Queue()
    threads = []
    for i in range(len(all_mic_fem_data)):
        q.put(i)
    for i in range(num_thread):
        t = threading.Thread(target=mulitrun_GA_1, args=(
        File_Path[i], ModelPath[i], mySapObject_name[i], SapModel_name[i], all_mic_fem_data, q, task_data,task_sections))
        t.start()
        threads.append(t)
    for i in threads:
        i.join()
    # return result,weight_1,col_up,beam_up,gx_te
    return task_data


def mulitrun_GA_1(File_Path, ModelPath, mySapObject, SapModel, all_mic_fem_data, q,all_chro_data,task_sections):
    while True:
        if q.empty():
            break
        time = q.get()
        mic_FEM_data = all_mic_fem_data[time]
        modular_FEM = task_sections[time+1]


        FEA.parsing_to_sap2000_mulit(mic_FEM_data, modular_FEM, File_Path, SapModel, mySapObject, ModelPath)

        FC.output_index(modular_FEM, File_Path, File_Path, mic_FEM_data)
        calaulate_fitness(File_Path, all_chro_data, 10000, time)


def close_mulit_sap(mySapObject_name,SapModel_name):
    for i in range(len(mySapObject_name)):
        ret = mySapObject_name[i].ApplicationExit(False)
        SapModel_name[i] = None
        mySapObject_name[i] = None


def calaulate_fitness(file_path, all_chrom_data, u, run_time):
    with open(os.path.join(file_path, 'max_values.json'), 'r') as file:
        index_data = json.load(file)
    value_dict = {key: item["value"] for key, item in index_data.items()}
    values_list = list(value_dict.values())
    value_id = []
    for j in range(len(values_list) - 1):
        if values_list[j] < 0:
            value_id.append(0)
        else:
            value_id.append(values_list[j])
    weight = values_list[-1]
    fit = weight + u * (sum(value_id))
    all_chrom_data[f'task{run_time}']['fitness'] = fit
    all_chrom_data[f'task{run_time}']['weight'] = weight

