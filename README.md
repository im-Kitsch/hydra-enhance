# hydra-enhance

enhance hydra utility

# TODO 1

add IDE integration for autocomplete

simple type support, i.e. int float, str, bool, list(seq), set, dict(map) https://pyyaml.org/wiki/PyYAMLDocumentation

add support of structured config

check unused variable in config and calling un variable in python file?

add type hint "!!" for every list item in config should be re-considered
 
long string is not considered in config, e.g. if string contains "_target_" will cause error

something special is not considered, e.g. "_target_:&xxxxx blablabla"

- Duck typing is annoying for hydra, since use structured config, we assume that the config is dataclass, but actually it's DictConfig

- recursive logic for instantiate and dataclass definition

# TODO 2
add readme

add pypi package release

add license

# yaml rule

- comment: there must be empty character after colon "#", e.g "key#abc: value" is a valid comment
- general structure:   
  "  key: !!type value # comment"  
  "  key: value # comment"   
  "  key: "   
  i.e. space*, key, space* is must,  others are optional  
  Firstly, the pattern must consider "key:" and "# comment" in priority  



