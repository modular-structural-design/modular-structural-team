import copy
import json
import os

import numpy as np

np.bool = np.bool_


def output_structured_data(building_data, modular_plan_x, modular_type, story_height, model_dir, case_name,
                           connection_distance=0.1):
    building_data1 = copy.deepcopy(building_data)
    out_space_num = len(building_data1['outer_space_config'])
    out_space_info = building_data1["outer_space_per_building"]
    out_space_cfg = building_data1["outer_space_config"]
    inner_space_info = building_data1["outer_space_has_inner_space"]
    inner_space_cfg = building_data1["inner_space_config"]
    out_space_relationship = building_data1["outer_space_relationship"]

    # endregion

    def get_key(dic, value):
        if value not in dic.values():
            return None
        result = []
        for key_ in dic:
            if dic[key_] == value:
                result.append(key_)
        return result

    # region nodes
    # 提取全部nodes
    inner_space_nodes_list = []
    for values in out_space_info.values():
        inner_idx = inner_space_info[f"{values['index']}"]
        story = int(values['story'])
        start_height = 0
        end_height = 0
        for i in range(story + 1):
            if i - 1 >= 0:
                start_height += story_height[f"{i - 1}"]
            end_height += story_height[f"{i}"]
        for index in inner_idx:
            node1 = copy.deepcopy(inner_space_cfg[f"{index}"][0])
            node2 = copy.deepcopy(inner_space_cfg[f"{index}"][1])
            node3 = copy.deepcopy(inner_space_cfg[f"{index}"][2])
            node4 = copy.deepcopy(inner_space_cfg[f"{index}"][3])
            node1.append(start_height)
            node2.append(start_height)
            node3.append(start_height)
            node4.append(start_height)
            inner_space_nodes_list.append(node1)
            inner_space_nodes_list.append(node2)
            inner_space_nodes_list.append(node3)
            inner_space_nodes_list.append(node4)
            node5 = copy.deepcopy(inner_space_cfg[f"{index}"][0])
            node6 = copy.deepcopy(inner_space_cfg[f"{index}"][1])
            node7 = copy.deepcopy(inner_space_cfg[f"{index}"][2])
            node8 = copy.deepcopy(inner_space_cfg[f"{index}"][3])
            node5.append(end_height)
            node6.append(end_height)
            node7.append(end_height)
            node8.append(end_height)
            inner_space_nodes_list.append(node5)
            inner_space_nodes_list.append(node6)
            inner_space_nodes_list.append(node7)
            inner_space_nodes_list.append(node8)

    # 去重并写入字典
    unique_inner_nodes_dict = {}
    temp_count = 0
    for term in inner_space_nodes_list:
        # for term1 in term:
        if term not in unique_inner_nodes_dict.values():
            unique_inner_nodes_dict[temp_count] = term
            temp_count += 1
    # endregion

    # region edges
    # 提取全部edges
    total_edges_list = []
    unique_edges_dict = {}
    temp_count = 0
    for values in out_space_info.values():
        inner_idx = inner_space_info[f"{values['index']}"]
        story = int(values['story'])
        start_height = 0
        end_height = 0
        for i in range(story + 1):
            if i - 1 >= 0:
                start_height += story_height[f"{i - 1}"]
            end_height += story_height[f"{i}"]
        for index in inner_idx:
            temp_inner_node = inner_space_cfg[f"{index}"]
            node1 = copy.deepcopy(inner_space_cfg[f"{index}"][0])
            node2 = copy.deepcopy(inner_space_cfg[f"{index}"][1])
            node3 = copy.deepcopy(inner_space_cfg[f"{index}"][2])
            node4 = copy.deepcopy(inner_space_cfg[f"{index}"][3])
            node1.append(start_height)
            node2.append(start_height)
            node3.append(start_height)
            node4.append(start_height)
            node5 = copy.deepcopy(inner_space_cfg[f"{index}"][0])
            node6 = copy.deepcopy(inner_space_cfg[f"{index}"][1])
            node7 = copy.deepcopy(inner_space_cfg[f"{index}"][2])
            node8 = copy.deepcopy(inner_space_cfg[f"{index}"][3])
            node5.append(end_height)
            node6.append(end_height)
            node7.append(end_height)
            node8.append(end_height)

            node1_idx = get_key(unique_inner_nodes_dict, node1)[0]
            node2_idx = get_key(unique_inner_nodes_dict, node2)[0]
            node3_idx = get_key(unique_inner_nodes_dict, node3)[0]
            node4_idx = get_key(unique_inner_nodes_dict, node4)[0]
            node5_idx = get_key(unique_inner_nodes_dict, node5)[0]
            node6_idx = get_key(unique_inner_nodes_dict, node6)[0]
            node7_idx = get_key(unique_inner_nodes_dict, node7)[0]
            node8_idx = get_key(unique_inner_nodes_dict, node8)[0]
            total_edges_list.append([node1_idx, node2_idx])
            total_edges_list.append([node2_idx, node3_idx])
            total_edges_list.append([node3_idx, node4_idx])
            total_edges_list.append([node4_idx, node1_idx])
            total_edges_list.append([node5_idx, node6_idx])
            total_edges_list.append([node6_idx, node7_idx])
            total_edges_list.append([node7_idx, node8_idx])
            total_edges_list.append([node8_idx, node5_idx])
            total_edges_list.append([node1_idx, node5_idx])
            total_edges_list.append([node2_idx, node6_idx])
            total_edges_list.append([node3_idx, node7_idx])
            total_edges_list.append([node4_idx, node8_idx])

    # 去重并写入字典
    unique_edges_dict = {}
    temp_count = 0
    for term in total_edges_list:
        if term not in unique_edges_dict.values():
            unique_edges_dict[temp_count] = term
            temp_count += 1
    # endregion

    # region spaces
    # find nodes_index
    spaces_dict = {}
    for key, values in out_space_info.items():
        temp_key_dict = {}
        temp_key_dict["story"] = values["story"]
        inner_idx = inner_space_info[f"{values['index']}"]
        story = int(values['story'])
        start_height = 0
        end_height = 0
        for i in range(story + 1):
            if i - 1 >= 0:
                start_height += story_height[f"{i - 1}"]
            end_height += story_height[f"{i}"]
        for index in inner_idx:
            temp_inner_node = inner_space_cfg[f"{index}"]
            node1 = copy.deepcopy(inner_space_cfg[f"{index}"][0])
            node2 = copy.deepcopy(inner_space_cfg[f"{index}"][1])
            node3 = copy.deepcopy(inner_space_cfg[f"{index}"][2])
            node4 = copy.deepcopy(inner_space_cfg[f"{index}"][3])
            node1.append(start_height)
            node2.append(start_height)
            node3.append(start_height)
            node4.append(start_height)
            node5 = copy.deepcopy(inner_space_cfg[f"{index}"][0])
            node6 = copy.deepcopy(inner_space_cfg[f"{index}"][1])
            node7 = copy.deepcopy(inner_space_cfg[f"{index}"][2])
            node8 = copy.deepcopy(inner_space_cfg[f"{index}"][3])
            node5.append(end_height)
            node6.append(end_height)
            node7.append(end_height)
            node8.append(end_height)

            node1_idx = get_key(unique_inner_nodes_dict, node1)[0]
            node2_idx = get_key(unique_inner_nodes_dict, node2)[0]
            node3_idx = get_key(unique_inner_nodes_dict, node3)[0]
            node4_idx = get_key(unique_inner_nodes_dict, node4)[0]
            node5_idx = get_key(unique_inner_nodes_dict, node5)[0]
            node6_idx = get_key(unique_inner_nodes_dict, node6)[0]
            node7_idx = get_key(unique_inner_nodes_dict, node7)[0]
            node8_idx = get_key(unique_inner_nodes_dict, node8)[0]
            temp_key_dict["nodes"] = [node1_idx, node2_idx, node3_idx, node4_idx]
            temp_key_dict["edges"] = [get_key(unique_edges_dict, [node1_idx, node2_idx])[0],
                                      get_key(unique_edges_dict, [node2_idx, node3_idx])[0],
                                      get_key(unique_edges_dict, [node3_idx, node4_idx])[0],
                                      get_key(unique_edges_dict, [node4_idx, node1_idx])[0]]
        spaces_dict[key] = temp_key_dict
    # endregion

    # region modulars
    inner_connection = {}
    inner_connection_count = 0
    # region nodes
    # 提取全部nodes
    modular_nodes_dict = {}
    temp_modular_count = 0
    for key, values in out_space_info.items():
        modular_location = copy.deepcopy(out_space_cfg[f"{values['index']}"][0])
        match values["direction"]:
            case "h":
                modular_length = out_space_cfg[f"{values['index']}"][2][1] - out_space_cfg[f"{values['index']}"][0][1]
            case "v":
                modular_length = out_space_cfg[f"{values['index']}"][2][0] - out_space_cfg[f"{values['index']}"][0][0]
        story = int(values['story'])
        start_height = 0
        end_height = 0
        for i in range(story + 1):
            if i - 1 >= 0:
                start_height += story_height[f"{i - 1}"]
            end_height += story_height[f"{i}"]
        modular_location.append(start_height)
        for term in modular_plan_x[int(key)]:
            temp_modular_width = modular_type[term]
            match values["direction"]:
                case "h":
                    loc_x, loc_y, loc_z = modular_location
                    node1 = [loc_x, loc_y, loc_z]
                    node2 = [loc_x + temp_modular_width, loc_y, loc_z]
                    node3 = [loc_x + temp_modular_width, loc_y + modular_length, loc_z]
                    node4 = [loc_x, loc_y + modular_length, loc_z]
                    node5 = [loc_x, loc_y, end_height]
                    node6 = [loc_x + temp_modular_width, loc_y, end_height]
                    node7 = [loc_x + temp_modular_width, loc_y + modular_length, end_height]
                    node8 = [loc_x, loc_y + modular_length, end_height]
                    inner_space_nodes_list.append(node1)
                    inner_space_nodes_list.append(node2)
                    inner_space_nodes_list.append(node3)
                    inner_space_nodes_list.append(node4)
                    inner_space_nodes_list.append(node5)
                    inner_space_nodes_list.append(node6)
                    inner_space_nodes_list.append(node7)
                    inner_space_nodes_list.append(node8)

                    modular_nodes_dict[temp_modular_count] = node1
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node2
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node3
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node4
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node5
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node6
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node7
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node8
                    temp_modular_count += 1

                    modular_location[0] += temp_modular_width
                case "v":
                    loc_x, loc_y, loc_z = modular_location
                    node1 = [loc_x, loc_y, loc_z]
                    node2 = [loc_x + modular_length, loc_y, loc_z]
                    node3 = [loc_x + modular_length, loc_y + temp_modular_width, loc_z]
                    node4 = [loc_x, loc_y + temp_modular_width, loc_z]
                    node5 = [loc_x, loc_y, end_height]
                    node6 = [loc_x + modular_length, loc_y, end_height]
                    node7 = [loc_x + modular_length, loc_y + temp_modular_width, end_height]
                    node8 = [loc_x, loc_y + temp_modular_width, end_height]
                    inner_space_nodes_list.append(node1)
                    inner_space_nodes_list.append(node2)
                    inner_space_nodes_list.append(node3)
                    inner_space_nodes_list.append(node4)
                    inner_space_nodes_list.append(node5)
                    inner_space_nodes_list.append(node6)
                    inner_space_nodes_list.append(node7)
                    inner_space_nodes_list.append(node8)

                    modular_nodes_dict[temp_modular_count] = node1
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node2
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node3
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node4
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node5
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node6
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node7
                    temp_modular_count += 1
                    modular_nodes_dict[temp_modular_count] = node8
                    temp_modular_count += 1

                    modular_location[1] += temp_modular_width

    # 去重并写入字典
    temp_count = len(unique_inner_nodes_dict)
    temp_count1 = 0
    for term in inner_space_nodes_list:
        if term not in unique_inner_nodes_dict.values():
            unique_inner_nodes_dict[temp_count] = term
            temp_count += 1
    # endregion

    # 去重并写入字典
    unique_modular_nodes_dict = {}
    unique_modular_nodes_dict1 = {}
    modular_connect_dict = {}
    temp_count = len(modular_connect_dict)
    for term in modular_nodes_dict.values():
        temp_key = get_key(modular_nodes_dict, term)
        modular_connect_dict[temp_count] = temp_key
        temp_count += 1

    temp_count = len(unique_modular_nodes_dict1)
    for term in modular_connect_dict.values():
        if term not in unique_modular_nodes_dict1.values():
            temp_dict_a = {}
            temp_dict_a["connected_nodes"] = copy.deepcopy(term)
            temp_dict_a["node_value"] = modular_nodes_dict[term[0]]
            unique_modular_nodes_dict[temp_count] = temp_dict_a
            unique_modular_nodes_dict1[temp_count] = copy.deepcopy(term)
            temp_count += 1
    # 给索引赋值
    extra_connected_list = []
    for i in range(len(unique_modular_nodes_dict)):
        for j in range(len(unique_modular_nodes_dict)):
            if i != j:
                if np.linalg.norm(np.array(unique_modular_nodes_dict[i]['node_value']) - np.array(
                        unique_modular_nodes_dict[j]['node_value'])) < connection_distance:
                    if i < j:
                        extra_connected_list.append([i, j])
                    elif i > j:
                        extra_connected_list.append([j, i])
                    # for k in range(len(unique_modular_nodes_dict1[j])):
                    #     unique_modular_nodes_dict[i]['connected_nodes'].append(unique_modular_nodes_dict1[j][k])
    # 去重
    unique_connected_list = []
    for term in extra_connected_list:
        if term not in unique_connected_list:
            unique_connected_list.append(term)

    # region edges and planes
    # 提取全部edges和planes
    total_planes_dict = {}
    temp_key_plane = 0
    for key, values in out_space_info.items():
        modular_location = copy.deepcopy(out_space_cfg[f"{values['index']}"][0])
        match values["direction"]:
            case "h":
                modular_length = out_space_cfg[f"{values['index']}"][2][1] - out_space_cfg[f"{values['index']}"][0][1]
            case "v":
                modular_length = out_space_cfg[f"{values['index']}"][2][0] - out_space_cfg[f"{values['index']}"][0][0]
        story = int(values['story'])
        start_height = 0
        end_height = 0
        for i in range(story + 1):
            if i - 1 >= 0:
                start_height += story_height[f"{i - 1}"]
            end_height += story_height[f"{i}"]
        modular_location.append(start_height)

        for term in modular_plan_x[int(key)]:
            temp_modular_width = modular_type[term]
            match values["direction"]:
                case "h":
                    loc_x, loc_y, loc_z = modular_location
                    node1 = [loc_x, loc_y, loc_z]
                    node2 = [loc_x + temp_modular_width, loc_y, loc_z]
                    node3 = [loc_x + temp_modular_width, loc_y + modular_length, loc_z]
                    node4 = [loc_x, loc_y + modular_length, loc_z]
                    node5 = [loc_x, loc_y, end_height]
                    node6 = [loc_x + temp_modular_width, loc_y, end_height]
                    node7 = [loc_x + temp_modular_width, loc_y + modular_length, end_height]
                    node8 = [loc_x, loc_y + modular_length, end_height]
                    node1_idx = get_key(unique_inner_nodes_dict, node1)[0]
                    node2_idx = get_key(unique_inner_nodes_dict, node2)[0]
                    node3_idx = get_key(unique_inner_nodes_dict, node3)[0]
                    node4_idx = get_key(unique_inner_nodes_dict, node4)[0]
                    node5_idx = get_key(unique_inner_nodes_dict, node5)[0]
                    node6_idx = get_key(unique_inner_nodes_dict, node6)[0]
                    node7_idx = get_key(unique_inner_nodes_dict, node7)[0]
                    node8_idx = get_key(unique_inner_nodes_dict, node8)[0]
                    total_edges_list.append([node1_idx, node2_idx])
                    total_edges_list.append([node2_idx, node3_idx])
                    total_edges_list.append([node3_idx, node4_idx])
                    total_edges_list.append([node4_idx, node1_idx])
                    total_edges_list.append([node5_idx, node6_idx])
                    total_edges_list.append([node6_idx, node7_idx])
                    total_edges_list.append([node7_idx, node8_idx])
                    total_edges_list.append([node8_idx, node5_idx])
                    total_edges_list.append([node1_idx, node5_idx])
                    total_edges_list.append([node2_idx, node6_idx])
                    total_edges_list.append([node3_idx, node7_idx])
                    total_edges_list.append([node4_idx, node8_idx])
                    total_planes_dict[temp_key_plane] = [node1_idx, node2_idx, node3_idx, node4_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node5_idx, node6_idx, node7_idx, node8_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node1_idx, node2_idx, node6_idx, node5_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node4_idx, node3_idx, node7_idx, node8_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node4_idx, node1_idx, node5_idx, node8_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node3_idx, node2_idx, node6_idx, node7_idx]
                    temp_key_plane += 1

                    modular_location[0] += temp_modular_width
                case "v":
                    loc_x, loc_y, loc_z = modular_location
                    node1 = [loc_x, loc_y, loc_z]
                    node2 = [loc_x + modular_length, loc_y, loc_z]
                    node3 = [loc_x + modular_length, loc_y + temp_modular_width, loc_z]
                    node4 = [loc_x, loc_y + temp_modular_width, loc_z]
                    node5 = [loc_x, loc_y, end_height]
                    node6 = [loc_x + modular_length, loc_y, end_height]
                    node7 = [loc_x + modular_length, loc_y + temp_modular_width, end_height]
                    node8 = [loc_x, loc_y + temp_modular_width, end_height]
                    inner_space_nodes_list.append(node1)
                    inner_space_nodes_list.append(node2)
                    inner_space_nodes_list.append(node3)
                    inner_space_nodes_list.append(node4)
                    inner_space_nodes_list.append(node5)
                    inner_space_nodes_list.append(node6)
                    inner_space_nodes_list.append(node7)
                    inner_space_nodes_list.append(node8)
                    node1_idx = get_key(unique_inner_nodes_dict, node1)[0]
                    node2_idx = get_key(unique_inner_nodes_dict, node2)[0]
                    node3_idx = get_key(unique_inner_nodes_dict, node3)[0]
                    node4_idx = get_key(unique_inner_nodes_dict, node4)[0]
                    node5_idx = get_key(unique_inner_nodes_dict, node5)[0]
                    node6_idx = get_key(unique_inner_nodes_dict, node6)[0]
                    node7_idx = get_key(unique_inner_nodes_dict, node7)[0]
                    node8_idx = get_key(unique_inner_nodes_dict, node8)[0]
                    total_edges_list.append([node1_idx, node2_idx])
                    total_edges_list.append([node2_idx, node3_idx])
                    total_edges_list.append([node3_idx, node4_idx])
                    total_edges_list.append([node4_idx, node1_idx])
                    total_edges_list.append([node5_idx, node6_idx])
                    total_edges_list.append([node6_idx, node7_idx])
                    total_edges_list.append([node7_idx, node8_idx])
                    total_edges_list.append([node8_idx, node5_idx])
                    total_edges_list.append([node1_idx, node5_idx])
                    total_edges_list.append([node2_idx, node6_idx])
                    total_edges_list.append([node3_idx, node7_idx])
                    total_edges_list.append([node4_idx, node8_idx])
                    total_planes_dict[temp_key_plane] = [node1_idx, node2_idx, node3_idx, node4_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node5_idx, node6_idx, node7_idx, node8_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node1_idx, node2_idx, node6_idx, node5_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node4_idx, node3_idx, node7_idx, node8_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node4_idx, node1_idx, node5_idx, node8_idx]
                    temp_key_plane += 1
                    total_planes_dict[temp_key_plane] = [node3_idx, node2_idx, node6_idx, node7_idx]
                    temp_key_plane += 1

                    modular_location[1] += temp_modular_width

    # 去重并写入字典
    temp_count = len(unique_edges_dict)
    for term in total_edges_list:
        if term not in unique_edges_dict.values():
            unique_edges_dict[temp_count] = term
            temp_count += 1

    # 去重并写入字典
    unique_planes_dict = {}
    temp_count = len(unique_planes_dict)
    for term in total_planes_dict.values():
        if term not in unique_planes_dict.values():
            unique_planes_dict[temp_count] = term
            temp_count += 1

    # endregion

    # region modulars info

    modular_info_dict = {}
    modular_count = 0
    for key, values in out_space_info.items():
        inner_idx = inner_space_info[f"{values['index']}"]
        inner_space_zone = []
        for index in inner_idx:
            match values["direction"]:
                case "h":
                    inner_space_zone.append([inner_space_cfg[f"{index}"][0][0], inner_space_cfg[f"{index}"][2][0]])
                case "v":
                    inner_space_zone.append([inner_space_cfg[f"{index}"][0][1], inner_space_cfg[f"{index}"][2][1]])
        inner_space_width = []
        for term in inner_space_zone:
            for term1 in term:
                if term1 not in inner_space_width:
                    inner_space_width.append(term1)
        modular_location = copy.deepcopy(out_space_cfg[f"{values['index']}"][0])
        story = int(values['story'])
        start_height = 0
        end_height = 0
        for i in range(story + 1):
            if i - 1 >= 0:
                start_height += story_height[f"{i - 1}"]
            end_height += story_height[f"{i}"]
        modular_location.append(start_height)
        modular_in_inner_space = None
        for term in modular_plan_x[int(key)]:
            detailed_info_dict = {}
            temp_modular_width = modular_type[term]
            match values["direction"]:
                case "h":
                    # nodes
                    loc_x, loc_y, loc_z = modular_location
                    node1 = [loc_x, loc_y, loc_z]
                    node2 = [loc_x + temp_modular_width, loc_y, loc_z]
                    node3 = [loc_x + temp_modular_width, loc_y + modular_length, loc_z]
                    node4 = [loc_x, loc_y + modular_length, loc_z]
                    node5 = [loc_x, loc_y, end_height]
                    node6 = [loc_x + temp_modular_width, loc_y, end_height]
                    node7 = [loc_x + temp_modular_width, loc_y + modular_length, end_height]
                    node8 = [loc_x, loc_y + modular_length, end_height]

                    node1_idx = get_key(unique_inner_nodes_dict, node1)[0]
                    node2_idx = get_key(unique_inner_nodes_dict, node2)[0]
                    node3_idx = get_key(unique_inner_nodes_dict, node3)[0]
                    node4_idx = get_key(unique_inner_nodes_dict, node4)[0]
                    node5_idx = get_key(unique_inner_nodes_dict, node5)[0]
                    node6_idx = get_key(unique_inner_nodes_dict, node6)[0]
                    node7_idx = get_key(unique_inner_nodes_dict, node7)[0]
                    node8_idx = get_key(unique_inner_nodes_dict, node8)[0]
                    detailed_info_dict["nodes"] = [node1_idx, node2_idx, node3_idx, node4_idx, node5_idx, node6_idx,
                                                   node7_idx, node8_idx]

                    # edges
                    edge1_idx = get_key(unique_edges_dict, [node1_idx, node2_idx])[0]
                    edge2_idx = get_key(unique_edges_dict, [node2_idx, node3_idx])[0]
                    edge3_idx = get_key(unique_edges_dict, [node3_idx, node4_idx])[0]
                    edge4_idx = get_key(unique_edges_dict, [node4_idx, node1_idx])[0]
                    edge5_idx = get_key(unique_edges_dict, [node5_idx, node6_idx])[0]
                    edge6_idx = get_key(unique_edges_dict, [node6_idx, node7_idx])[0]
                    edge7_idx = get_key(unique_edges_dict, [node7_idx, node8_idx])[0]
                    edge8_idx = get_key(unique_edges_dict, [node8_idx, node5_idx])[0]
                    edge9_idx = get_key(unique_edges_dict, [node1_idx, node5_idx])[0]
                    edge10_idx = get_key(unique_edges_dict, [node2_idx, node6_idx])[0]
                    edge11_idx = get_key(unique_edges_dict, [node3_idx, node7_idx])[0]
                    edge12_idx = get_key(unique_edges_dict, [node4_idx, node8_idx])[0]
                    detailed_info_dict["edges"] = [edge1_idx, edge2_idx, edge3_idx, edge4_idx, edge5_idx, edge6_idx,
                                                   edge7_idx, edge8_idx, edge9_idx, edge10_idx, edge11_idx, edge12_idx]

                    # planes
                    plane1_idx = get_key(unique_planes_dict, [node1_idx, node2_idx, node3_idx, node4_idx])[0]
                    plane2_idx = get_key(unique_planes_dict, [node5_idx, node6_idx, node7_idx, node8_idx])[0]
                    plane3_idx = get_key(unique_planes_dict, [node1_idx, node2_idx, node6_idx, node5_idx])[0]
                    plane4_idx = get_key(unique_planes_dict, [node4_idx, node3_idx, node7_idx, node8_idx])[0]
                    plane5_idx = get_key(unique_planes_dict, [node4_idx, node1_idx, node5_idx, node8_idx])[0]
                    plane6_idx = get_key(unique_planes_dict, [node3_idx, node2_idx, node6_idx, node7_idx])[0]
                    detailed_info_dict["planes"] = [plane1_idx, plane2_idx, plane3_idx, plane4_idx, plane5_idx,
                                                    plane6_idx]

                    # space
                    loc_x, loc_y, loc_z = modular_location
                    modular_loc_l = loc_x
                    modular_loc_r = loc_x + temp_modular_width
                    for ii in range(len(inner_space_width) - 1):
                        if modular_loc_l >= inner_space_width[ii] and modular_loc_r <= inner_space_width[ii + 1]:
                            modular_space = [inner_idx[ii]]
                            break
                        else:
                            modular_in_inner_space = False
                    if not modular_in_inner_space:
                        for ii in range(len(inner_space_width) - 1):
                            if modular_loc_l <= inner_space_width[ii + 1] and modular_loc_r >= inner_space_width[
                                ii + 1]:
                                modular_space = [inner_idx[ii - 1], inner_idx[ii]]
                                break
                    detailed_info_dict["space"] = modular_space
                    detailed_info_dict["modular_type"] = int(term)

                    modular_info_dict[modular_count] = detailed_info_dict
                    modular_location[0] += temp_modular_width
                    modular_count += 1

                case "v":
                    # nodes
                    loc_x, loc_y, loc_z = modular_location
                    node1 = [loc_x, loc_y, loc_z]
                    node2 = [loc_x + modular_length, loc_y, loc_z]
                    node3 = [loc_x + modular_length, loc_y + temp_modular_width, loc_z]
                    node4 = [loc_x, loc_y + temp_modular_width, loc_z]
                    node5 = [loc_x, loc_y, end_height]
                    node6 = [loc_x + modular_length, loc_y, end_height]
                    node7 = [loc_x + modular_length, loc_y + temp_modular_width, end_height]
                    node8 = [loc_x, loc_y + temp_modular_width, end_height]

                    node1_idx = get_key(unique_inner_nodes_dict, node1)[0]
                    node2_idx = get_key(unique_inner_nodes_dict, node2)[0]
                    node3_idx = get_key(unique_inner_nodes_dict, node3)[0]
                    node4_idx = get_key(unique_inner_nodes_dict, node4)[0]
                    node5_idx = get_key(unique_inner_nodes_dict, node5)[0]
                    node6_idx = get_key(unique_inner_nodes_dict, node6)[0]
                    node7_idx = get_key(unique_inner_nodes_dict, node7)[0]
                    node8_idx = get_key(unique_inner_nodes_dict, node8)[0]
                    detailed_info_dict["nodes"] = [node1_idx, node2_idx, node3_idx, node4_idx, node5_idx, node6_idx,
                                                   node7_idx, node8_idx]
                    # edges
                    edge1_idx = get_key(unique_edges_dict, [node1_idx, node2_idx])[0]
                    edge2_idx = get_key(unique_edges_dict, [node2_idx, node3_idx])[0]
                    edge3_idx = get_key(unique_edges_dict, [node3_idx, node4_idx])[0]
                    edge4_idx = get_key(unique_edges_dict, [node4_idx, node1_idx])[0]
                    edge5_idx = get_key(unique_edges_dict, [node5_idx, node6_idx])[0]
                    edge6_idx = get_key(unique_edges_dict, [node6_idx, node7_idx])[0]
                    edge7_idx = get_key(unique_edges_dict, [node7_idx, node8_idx])[0]
                    edge8_idx = get_key(unique_edges_dict, [node8_idx, node5_idx])[0]
                    edge9_idx = get_key(unique_edges_dict, [node1_idx, node5_idx])[0]
                    edge10_idx = get_key(unique_edges_dict, [node2_idx, node6_idx])[0]
                    edge11_idx = get_key(unique_edges_dict, [node3_idx, node7_idx])[0]
                    edge12_idx = get_key(unique_edges_dict, [node4_idx, node8_idx])[0]
                    detailed_info_dict["edges"] = [edge1_idx, edge2_idx, edge3_idx, edge4_idx, edge5_idx, edge6_idx,
                                                   edge7_idx, edge8_idx, edge9_idx, edge10_idx, edge11_idx, edge12_idx]

                    # planes
                    plane1_idx = get_key(unique_planes_dict, [node1_idx, node2_idx, node3_idx, node4_idx])[0]
                    plane2_idx = get_key(unique_planes_dict, [node5_idx, node6_idx, node7_idx, node8_idx])[0]
                    plane3_idx = get_key(unique_planes_dict, [node1_idx, node2_idx, node6_idx, node5_idx])[0]
                    plane4_idx = get_key(unique_planes_dict, [node4_idx, node3_idx, node7_idx, node8_idx])[0]
                    plane5_idx = get_key(unique_planes_dict, [node4_idx, node1_idx, node5_idx, node8_idx])[0]
                    plane6_idx = get_key(unique_planes_dict, [node3_idx, node2_idx, node6_idx, node7_idx])[0]
                    detailed_info_dict["planes"] = [plane1_idx, plane2_idx, plane3_idx, plane4_idx, plane5_idx,
                                                    plane6_idx]

                    # space
                    loc_x, loc_y, loc_z = modular_location
                    modular_loc_l = loc_y
                    modular_loc_r = loc_y + temp_modular_width
                    for ii in range(len(inner_space_width) - 1):
                        if modular_loc_l >= inner_space_width[ii] and modular_loc_r <= inner_space_width[ii + 1]:
                            modular_space = [inner_idx[ii]]
                            break
                        else:
                            modular_in_inner_space = False
                    if not modular_in_inner_space:
                        for ii in range(len(inner_space_width) - 1):
                            if modular_loc_l <= inner_space_width[ii + 1] and modular_loc_r >= inner_space_width[
                                ii + 1]:
                                modular_space = [inner_idx[ii - 1], inner_idx[ii]]
                                break
                    detailed_info_dict["space"] = modular_space
                    detailed_info_dict["modular_type"] = int(term)

                    modular_location[1] += temp_modular_width
                    modular_info_dict[modular_count] = detailed_info_dict
                    modular_count += 1

    # 去重并写入字典
    temp_count = len(unique_edges_dict)
    for term in total_edges_list:
        if term not in unique_edges_dict.values():
            unique_edges_dict[temp_count] = term
            temp_count += 1
    # endregion

    # endregion

    project_info = {}
    project_info["nodes"] = unique_inner_nodes_dict
    project_info["edges"] = unique_edges_dict
    project_info["planes"] = unique_planes_dict
    project_info["spaces"] = spaces_dict
    project_info["modulars"] = modular_info_dict

    # print(project_info)

    file_path = os.path.join(model_dir, case_name)
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_data = os.path.join(file_path, 'data1.json')
    with open(file_data, 'w') as f:
        json.dump(project_info, f, indent=4)

    return project_info


def implement_modular_structure_data(model_dir, case_name, connection_distance=1):
    # file1 = os.path.join(file_path, 'basic_structure_data.json')
    file_path = os.path.join(model_dir, case_name)
    file_data = os.path.join(file_path, 'data1.json')
    with open(file_data, 'r') as f:
        project_info = json.load(f)
    modulars = project_info["modulars"]
    nodes = project_info["nodes"]
    edges = project_info["edges"]
    planes = project_info["planes"]
    spaces = project_info["spaces"]

    new_spaces = {}
    new_spaces['nodes'] = nodes
    new_spaces['edges'] = edges
    new_spaces['entities'] = {}
    for i in range(len(spaces)):
        new_spaces['entities'][i] = spaces[str(i)]

    new_modulars = {}
    count = -1
    for i in range(len(modulars)):
        new_nodes = {}
        new_edges = {}
        new_planes = {}
        node_index = {}
        edge_index = {}
        plane_index = {}
        new_edge_types = []
        new_plane_types = []

        modular = modulars[str(i)]

        for j in range(len(modular['nodes'])):
            count += 1
            node_index[modular['nodes'][j]] = count
            new_nodes[count] = nodes[str(modular['nodes'][j])]
        for j in range(len(modular['edges'])):
            tp = edges[str(modular['edges'][j])]
            new_edges[j] = [node_index[tp[0]], node_index[tp[1]]]
            if j < 4:
                new_edge_types.append(0)
            elif j < 8:
                new_edge_types.append(1)
            else:
                new_edge_types.append(2)
        for j in range(len(modular['planes'])):
            tp = planes[str(modular['planes'][j])]
            tp2 = [node_index[tp[k]] for k in range(len(tp))]
            new_planes[j] = tp2
            if j == 0:
                new_plane_types.append(0)
            elif j == 1:
                new_plane_types.append(1)
            else:
                new_plane_types.append(2)

        new_modulars[i] = {}
        new_modulars[i]['nodes'] = new_nodes
        new_modulars[i]['edges'] = new_edges
        new_modulars[i]['planes'] = new_planes
        new_modulars[i]['edge_types'] = new_edge_types
        new_modulars[i]['plane_types'] = new_plane_types
        new_modulars[i]['space'] = modular['space']
        new_modulars[i]['modular_type'] = modular['modular_type']

    new_inter_connections = {}
    count = -1
    for i in range(len(new_modulars) - 1):
        modular1 = new_modulars[i]
        nodes1 = modular1['nodes']
        for j in range(i + 1, len(new_modulars)):
            modular2 = new_modulars[j]
            nodes2 = modular2['nodes']
            for k, value1 in nodes1.items():
                for t, value2 in nodes2.items():
                    tp1 = np.array(value1)
                    tp2 = np.array(value2)
                    if np.linalg.norm(tp1 - tp2) < connection_distance:
                        count += 1
                        new_inter_connections[count] = [k, t]

    # information summary
    mic_info = {}
    mic_info["spaces"] = new_spaces
    mic_info["modulars"] = new_modulars
    mic_info["inter_connections"] = new_inter_connections

    # file2 = os.path.join(file_path, 'mic_structure_data.json')
    file_data = os.path.join(file_path, 'data2.json')
    with open(file_data, 'w') as f:
        json.dump(mic_info, f, indent=4)

    return mic_info


def transform_mic_data(mic_info):
    spaces = mic_info['spaces']
    modulars = mic_info['modulars']

    nodes_dict = {}
    for i in range(len(modulars)):
        tp_nodes = modulars[i]['nodes']
        for key, value in tp_nodes.items():
            nodes_dict[key] = value
    nodes = []
    for i in range(len(nodes_dict)):
        nodes.append(nodes_dict[i])

    edges = []
    for i in range(len(modulars)):
        tp_edges = modulars[i]['edges']
        for key, value in tp_edges.items():
            edges.append(value)

    planes = []
    for i in range(len(modulars)):
        tp_planes = modulars[i]['planes']
        for key, value in tp_planes.items():
            planes.append(value)

    return (nodes, edges, planes)


def transform_mic_data2(mic_info):
    spaces = mic_info['spaces']
    modulars = mic_info['modulars']
    inter_connections = mic_info['inter_connections']

    nodes_dict = {}
    for i in range(len(modulars)):
        tp_nodes = modulars[str(i)]['nodes']
        for key, value in tp_nodes.items():
            nodes_dict[key] = value
    nodes = []
    for i in range(len(nodes_dict)):
        nodes.append(nodes_dict[str(i)])

    edges = []
    for i in range(len(modulars)):
        tp_edges = modulars[str(i)]['edges']
        for key, value in tp_edges.items():
            edges.append(value)

    for i in range(len(inter_connections)):
        edges.append(inter_connections[i])

    planes = []
    for i in range(len(modulars)):
        tp_planes = modulars[str(i)]['planes']
        for key, value in tp_planes.items():
            planes.append(value)

    return (nodes, edges, planes)


def find_adjust_direction(point, center_point):
    direction = []
    for i in range(len(point)):
        if center_point[i] > point[i]:
            direction.append(1)
        else:
            direction.append(-1)

    return direction


def modify_mic_geo(model_dir, case_name, contraction=100):
    # file1 = os.path.join(file_path, 'mic_structure_data.json')
    file_path = os.path.join(model_dir, case_name)
    file_data = os.path.join(file_path, 'data2.json')
    with open(file_data, 'r') as f:
        mic_info = json.load(f)
    modulars = mic_info['modulars']

    new_modulars = {}
    for i in range(len(modulars)):
        nodes = modulars[str(i)]['nodes']
        tp_node = []
        for j, value in nodes.items():
            tp_node.append(nodes[j])
        tp_node = np.array(tp_node)
        center_point = np.sum(tp_node, axis=0) / tp_node.shape[0]

        for j, value in nodes.items():
            tp_node = np.array(nodes[j])
            direction = find_adjust_direction(tp_node, center_point)
            tp_node = tp_node + contraction * np.array(direction)
            nodes[j] = tp_node.tolist()
        modulars[str(i)]['nodes'] = nodes

    new_modulars = modulars

    new_inter_connections = {}
    count = -1
    for i in range(len(new_modulars) - 1):
        modular1 = new_modulars[str(i)]
        nodes1 = modular1['nodes']
        for j in range(i + 1, len(new_modulars)):
            modular2 = new_modulars[str(j)]
            nodes2 = modular2['nodes']
            for k, value1 in nodes1.items():
                for t, value2 in nodes2.items():
                    tp1 = np.array(value1)
                    tp2 = np.array(value2)
                    if np.linalg.norm(tp1 - tp2) < contraction * 2.001:
                        count += 1
                        new_inter_connections[count] = [int(k), int(t)]

    # information summary
    mic_info_new = {}
    mic_info_new["spaces"] = mic_info["spaces"]
    mic_info_new["modulars"] = new_modulars
    mic_info_new["inter_connections"] = new_inter_connections

    # file2 = os.path.join(file_path, 'mic_structure_data2.json')
    file_data = os.path.join(file_path, 'data3.json')
    with open(file_data, 'w') as f:
        json.dump(mic_info_new, f, indent=4)

    return mic_info_new


def implement_FEA_info_enrichment(model_dir, case_name, loading_path, bottom=200.):
    # file1 = os.path.join(file_path, 'mic_structure_data2.json')
    # file2 = os.path.join(file_path, 'FEA_loading.json')

    file_path = os.path.join(model_dir, case_name)
    file_data = os.path.join(file_path, 'data3.json')
    with open(file_data, 'r') as f:
        mic_info = json.load(f)
    with open(loading_path, 'r') as f:
        loading_info = json.load(f)
    # with open(os.path.join(file_path, 'FEA_semantic_lists.json'), 'r') as f:
    #     semantics = json.load(f)

    nodes_geo = {}
    frames_index = {}
    frames_sections = {}
    plane_index = {}
    inter_connections_index = {}
    inter_connections_type = {}
    boundary_nodes = []
    frame_loads = {}
    plane_loads = {}

    spaces = mic_info['spaces']
    modulars = mic_info['modulars']
    inter_connections = mic_info['inter_connections']

    nodes_dict = {}
    for i in range(len(modulars)):
        tp_nodes = modulars[str(i)]['nodes']
        for key, value in tp_nodes.items():
            nodes_dict[key] = value
    for i in range(len(nodes_dict)):
        nodes_geo["nodes" + str(i)] = nodes_dict[str(i)]

    count = -1
    for i in range(len(modulars)):
        type = modulars[str(i)]['modular_type']
        tp_edges = modulars[str(i)]['edges']
        tp_edge_types = modulars[str(i)]['edge_types']
        edge_count = -1
        for key, value in tp_edges.items():
            count += 1
            edge_count += 1
            frames_index["frame" + str(count)] = value
            frames_sections["frame" + str(count)] = {"modular_type": type, "edge_type": tp_edge_types[edge_count]}

    count = -1
    for i in range(len(modulars)):
        tp_planes = modulars[str(i)]['planes']
        for key, value in tp_planes.items():
            count += 1
            plane_index["plane" + str(count)] = value

    count = -1
    for i in range(len(inter_connections)):
        count += 1
        inter_connections_index["inter_connection" + str(count)] = inter_connections[str(i)]
        node1 = nodes_geo['nodes' + str(inter_connections[str(i)][0])]
        node2 = nodes_geo['nodes' + str(inter_connections[str(i)][1])]
        tp = np.array(node1) - np.array(node2)

        if abs(tp[2]) < 1e-2:
            inter_connections_type["inter_connection" + str(count)] = 1
        else:
            inter_connections_type["inter_connection" + str(count)] = 2

    # boundary nodes
    for key, value in nodes_geo.items():
        if abs(value[2] - bottom) < 1e-1:
            boundary_nodes.append(key)

    # load patterns
    load_patterns = loading_info['load_patterns']

    # loadings: frame
    count = -1
    for i in range(len(modulars)):
        type = modulars[str(i)]['modular_type']
        tp_edges = modulars[str(i)]['edges']
        for key, value in tp_edges.items():
            count += 1
            if key == '0' or key == '1' or key == '2' or key == '3':
                frame_name = "frame" + str(count)
                LoadPat = loading_info['frame_load']['0']['type']
                MyType = 1
                Dir = loading_info['frame_load']['0']['direction']
                Dist1 = 0
                Dist2 = 1
                Val1 = loading_info['frame_load']['0']['value']
                Val2 = loading_info['frame_load']['0']['value']
                frame_loads[frame_name] = {"LoadPat": LoadPat, "MyType": MyType, "Dir": Dir, "Val1": Val1, "Val2": Val2,
                                           "Dist1": Dist1, "Dist2": Dist2}
            # frames_index[] = value
            # frames_sections["frame" + str(count)] = {"modular_type": type, "edge_type": tp_edge_types[edge_count]}

    # loadings: planes
    count = -1
    for i in range(len(modulars)):
        tp_planes = modulars[str(i)]['planes']
        for key, value in tp_planes.items():
            count += 1
            plane_name = "plane" + str(count)
            if key == '0':
                plane_loads[plane_name] = {
                    "0": {
                        "LoadPat": loading_info['plane_load']['0']['type'],
                        "Value": loading_info['plane_load']['0']['value'],
                        "Dir": loading_info['plane_load']['0']['direction'],
                        "DistType": 2,
                        "Replace": True,
                        "CSys": "Global"
                    },
                    "1": {
                        "LoadPat": loading_info['plane_load']['1']['type'],
                        "Value": loading_info['plane_load']['1']['value'],
                        "Dir": loading_info['plane_load']['1']['direction'],
                        "DistType": 2,
                        "Replace": True,
                        "CSys": "Global"
                    },
                }
            if key == '1':
                plane_loads[plane_name] = {
                    "0": {
                        "LoadPat": loading_info['plane_load']['2']['type'],
                        "Value": loading_info['plane_load']['2']['value'],
                        "Dir": loading_info['plane_load']['2']['direction'],
                        "DistType": 2,
                        "Replace": True,
                        "CSys": "Global"
                    },
                }

    # loadings: seismic and combination
    seismic_info = loading_info['earthquake_load']
    load_combinations = loading_info['load_combinations']

    # summarize information
    total_info = {}
    total_info["frames_index"] = frames_index
    total_info["frames_sections"] = frames_sections
    total_info["nodes_geo"] = nodes_geo
    total_info["plane_index"] = plane_index
    total_info["inter_connections_index"] = inter_connections_index
    total_info["inter_connections_type"] = inter_connections_type
    total_info["boundary_nodes"] = boundary_nodes
    total_info["load_patterns"] = load_patterns
    total_info["frame_loads"] = frame_loads
    total_info["plane_loads"] = plane_loads
    total_info["seismic_info"] = seismic_info
    total_info["load_combinations"] = load_combinations

    # with open(os.path.join(file_path, 'mic_FEM_data.json'), 'w') as f:
    #     json.dump(total_info, f, indent=4)
    file_data = os.path.join(file_path, 'mic_fem_data.json')
    with open(file_data, 'w') as f:
        json.dump(total_info, f, indent=4)

    return total_info

