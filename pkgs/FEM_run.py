import copy
import FEM_parser as FEA
import utils as ut
import numpy as np
import math as m
import json
import FEM_Index_calculation as FC
import random
from random import randint
import pyvista as pv
import os
import queue
import threading
import configparser
import comtypes.client
import sys

class FEM_run():
    def __init__(self, FEMData_path):
        self.FEMData_path = FEMData_path
        return

    def mulit_sap(self, num_thread):
        File_Path = []
        all_SapModel = []
        all_mySapObject = []
        all_model_path = []
        for i in range(num_thread):
            File_Path.append(os.path.join(self.FEMData_path, f"cases{i}"))
            sap_model_file = os.path.join(File_Path[i], 'FEM_sap2000\\MiC1.sdb')
            SapModel, mySapObject = FEA.sap2000_initialization(File_Path[i])
            all_SapModel.append(SapModel)
            all_mySapObject.append(mySapObject)
            all_model_path.append(sap_model_file)
        return all_SapModel, all_mySapObject, all_model_path, File_Path




def thread_sap(File_Path, ModelPath, mySapObject_name, SapModel_name, num_thread, pop2, mic_FEM_data, FEM_sematics,
               modular_num, FEA_info2):
    q = queue.Queue()
    threads = []
    for i in range(len(pop2)):
        q.put(i)

    for i in range(num_thread):
        t = threading.Thread(target=mulitrun_GA_1, args=(
            File_Path[i], ModelPath[i], mySapObject_name[i], SapModel_name[i], pop2, q, mic_FEM_data, FEM_sematics,
            modular_num, FEA_info2))
        t.start()
        threads.append(t)

    for i in threads:
        i.join()
    # return result,weight_1,col_up,beam_up,gx_te


def mulitrun_GA_1(File_Path, ModelPath, mySapObject, SapModel, pop_all, q, mic_FEM_data, FEM_sematics, modular_num,
                  FEA_info2):
    while True:
        if q.empty():
            break
        time = q.get()
        pop2 = pop_all[time]
        # 染色体解码
        merged_list = [pop2[i:i + 3] for i in range(0, len(pop2), 3)]
        modular_FEM = {}

        # 用 for 循环生成字典
        for i in range(0, modular_num):  # 假设你需要生成键 1 到 2
            modular_FEM[i + 1] = {"sections": merged_list[i]}

        FEA.parsing_to_sap2000_mulit(FEA_info2, FEM_sematics, modular_FEM, File_Path, SapModel, mySapObject, ModelPath)

        FC.output_index(modular_FEM, File_Path, File_Path, mic_FEM_data)


def generate_chromosome(modular_num, section_info, pop_size):
    all_chro = []
    for i in range(pop_size):
        chromo = [random.randint(0, len(section_info) - 1) for _ in range(modular_num * 3)]
        all_chro.append(chromo)
    return all_chro

