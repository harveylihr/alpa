"""Benchmark suite for auto wide-ResNet"""
from benchmark.alpa.suite_paper_wresnet import get_auto_test_case

def copy_cases_with_search_space(cases, search_space):
    new_cases = []
    for case in cases:
        case = list(case)
        overwrite_global_config = case[-1] = dict(case[-1])
        if search_space == "ppdp":
            overwrite_global_config["logical_mesh_search_space"] = "dp_only"
        elif search_space == "intra-only":
            overwrite_global_config["strategy"] = "shard_parallel"
        elif search_space == "inter-only":
            overwrite_global_config["submesh_choices_mode"] = "inter_only"
        new_cases.append(case)
    return new_cases

artifact_search_e2e_wresnet_suite = {  # key = the number of gpus, value = a list of cases
1: get_auto_test_case("250M", [24], 1536),
2: get_auto_test_case("500M", [24], 1536),
4 : get_auto_test_case("1B", [24], 1536),
8: get_auto_test_case("2B", [24], 1536),
16: get_auto_test_case("4B", [32], 1536),
32: get_auto_test_case("6.8B", [38], 1520),
}


artifact_search_e2e_wresnet_ppdp_suite = {
num_gpus: copy_cases_with_search_space(artifact_result_e2e_wresnet_suite[num_gpus], "ppdp") 
for num_gpus in artifact_search_e2e_wresnet_suite
}


artifact_search_e2e_wresnet_intra_only_suite = {
num_gpus: copy_cases_with_search_space(artifact_result_e2e_wresnet_suite[num_gpus], "intra-only") 
for num_gpus in artifact_search_e2e_wresnet_suite
}


artifact_search_e2e_wresnet_inter_only_suite = {
num_gpus: copy_cases_with_search_space(artifact_result_e2e_wresnet_suite[num_gpus], "inter-only") 
for num_gpus in artifact_search_e2e_wresnet_suite
}


artifact_result_e2e_wresnet_suite = {
1: get_auto_test_case("250M", [24], 1536, overwrite_global_config_dict={
    "strategy": "shard_parallel"
}),
2: get_auto_test_case("500M", [24], 1536, overwrite_global_config_dict={
    "strategy": "shard_parallel"
}),
4 : get_auto_test_case("1B", [24], 1536, overwrite_global_config_dict={
    "strategy": "shard_parallel"
}),
8: get_auto_test_case("2B", 24, 1536, overwrite_global_config_dict={
    "pipeline_stage_mode": "manual_gpipe",
    "forward_stage_layer_ids": [[0, 1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14, 15]],
    "sub_physical_mesh_shapes": [(1, 4), (1, 4)],
    "sub_logical_mesh_shapes": [(4, 1), (1, 4)],
    "submesh_autosharding_option_dicts": [{}, {'force_batch_dim_to_mesh_dim': 0}]
}),
16: get_auto_test_case("4B", 32, 1536, overwrite_global_config_dict={
    "pipeline_stage_mode": "manual_gpipe",
    "forward_stage_layer_ids": [[0, 1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15]],
    "sub_physical_mesh_shapes": [(1, 4), (1, 4), (1, 8)],
    "sub_logical_mesh_shapes": [(4, 1), (4, 1), (8, 1)],
    "submesh_autosharding_option_dicts": [{'force_batch_dim_to_mesh_dim': 0}, {'force_batch_dim_to_mesh_dim': 0}, {}]
}),
32: get_auto_test_case("6.8B", 32, 1536, overwrite_global_config_dict={
    "pipeline_stage_mode": "manual_gpipe",
    "forward_stage_layer_ids": [[0, 1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15]],
    "sub_physical_mesh_shapes": [(1, 8), (1, 8), (1, 8), (1, 8)],
    "sub_logical_mesh_shapes": [(8, 1), (8, 1), (8, 1), (8, 1)],
    "submesh_autosharding_option_dicts": [{'force_batch_dim_to_mesh_dim': 0}, {}, {}, {}],
}),
}
