from pathlib import Path

from src.infra.optimizer.file_optimizer_parameter_repository import FileOptimizerParametersRepository
from src.utils.config_util import read_config, test_section


def test_read_from_ini_file():
    config = read_config(section=test_section)
    filename_config_opt = Path(config.get("PATH_CONFIG") + config.get("CONFIG_OPTIMIZER"))

    test_repository = FileOptimizerParametersRepository(filename_config_opt, test_section)
    test_parameter = test_repository.read()

    assert test_parameter.NUM_THREADS == 1
