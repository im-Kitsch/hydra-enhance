from typing import Any 
from dataclasses import dataclass 
from typing import overload 
from hydra.utils import instantiate 
import torch


@dataclass 
class root_bConfig: 
    c: Any 
    d: Any 


@dataclass 
class root_tConfig: 
    _target_: Any 


@dataclass 
class rootConfig: 
    a: Any 
    b: root_bConfig 
    t: root_tConfig 


@overload 
def instantiate_new(config: root_tConfig, *args: Any, **kwargs: Any) -> "torch.nn.Linear": 
    ... 


def instantiate_new(config: Any, *args: Any, **kwargs: Any) -> Any: 
    return instantiate(config, *args, **kwargs) 


