from omegaconf import DictConfig, OmegaConf
import subprocess


# FIXME, _target_ actually also point to object, which is not supported here yet, this also relates to padding
# TODO, add command line parameter  like +a=1 +b=2
# TODO, consider add default value for the class
def get_config(file_path: str):
    try:
        result = subprocess.run(
            ['python', f'{file_path}', '-c', 'job'], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out_text = result.stdout
        cfg = OmegaConf.create(out_text)
        return cfg
    except subprocess.CalledProcessError as err:
        print("error occured")
        print(err.stderr)
        raise err


def get_instantiate_string(cfg_name: str, target_name: str):
    overload_str = f"@overload \n"
    overload_str += f"def instantiate_new(config: {cfg_name}, *args: Any, **kwargs: Any) -> \"{target_name}\": \n"
    overload_str += f"    ... \n"
    overload_str += "\n"
    return overload_str


def get_module_from_string(target_str):
    parts = target_str.split(".", maxsplit=1)
    assert len(parts) > 1
    module_name = parts[0]
    return module_name


# TODO, variable name is messy, refactor it
def generate_dataclass(parent_key:str, cls_cfg: DictConfig, global_cfg_list, instantiate_list, module_to_import):
    class_def = ""
    class_def += f"@dataclass \n"
    class_name = f"{parent_key}Config"
    class_def += f"class {class_name}: \n"

    for _k in cls_cfg.keys():
        if not OmegaConf.is_missing(cls_cfg, _k):
            _v = cls_cfg[_k]
            if _k == "_target_":
                # FIXME, add handle for failure(not defined or not right definition)
                instantiate_list.append(get_instantiate_string(class_name, _v))
                module_name = get_module_from_string(_v)
                module_to_import.add(f"import {module_name}\n")
        else:
            _v = "???"
        if isinstance(_v, DictConfig):
            _cls_name = generate_dataclass(
                f"{parent_key}_{_k}", _v, global_cfg_list,
                instantiate_list, module_to_import=module_to_import)
            class_def += f"    {_k}: {_cls_name} \n"
        else:
            class_def += f"    {_k}: Any \n"
    class_def += "\n"
    global_cfg_list.append(class_def)
    return class_name


def generate_structured_default_list(file_path) -> list[str]:
    cfg = get_config(file_path)

    cfg_list = []
    instantiate_list = []
    module_to_import = set()
    generate_dataclass(parent_key='root', cls_cfg=cfg, global_cfg_list=cfg_list,
                       instantiate_list=instantiate_list, module_to_import=module_to_import)

    final_string: list[str] = ["from typing import Any \n", "from dataclasses import dataclass \n",
                               "from typing import overload \n", "from hydra.utils import instantiate \n"]

    for _module_i in module_to_import:
        final_string.append(_module_i)
    final_string.append("\n")
    final_string.append("\n")

    final_string.extend(cfg_list)

    final_string.extend(instantiate_list)

    final_string.append("\n")
    final_string.append("def instantiate_new(config: Any, *args: Any, **kwargs: Any) -> Any: \n")
    final_string.append("    return instantiate(config, *args, **kwargs) \n")
    final_string.append("\n")
    final_string.append("\n")

    # print("".join(final_string))
    return final_string


# generate_structured_default_list('../example/generate_structured_config/run_exp.py')
