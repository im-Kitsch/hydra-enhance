import hydra

# FIXME, first time it will failure, since run_exp_cfg is not generated yet
from run_exp_cfg import rootConfig
from run_exp_cfg import instantiate_new as instantiate


@hydra.main(config_path="./", config_name="config", version_base=None)
def main(config: "rootConfig"):
    aa = instantiate(config.t)

    return


if __name__ == "__main__":
    main()