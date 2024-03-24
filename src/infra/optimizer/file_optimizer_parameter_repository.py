from pathlib import Path

from src.models.optimizer.optimizer_parameter_repository import IOptimizerParametersRepository
from src.models.optimizer.optimizer_parameters import OptimizationParameters
from src.utils.config_util import read_config


class FileOptimizerParametersRepository(IOptimizerParametersRepository):
    def __init__(self, file_path: Path, config_section: str):
        self._file_path = file_path
        self._config_section = config_section

    def read(self) -> OptimizationParameters:
        """config ファイルから読み取る.
        読み取り対象のファイルも config から読み取り

        Args:
            config_section (str): 読み取り対象の section
        """
        config_opt = read_config(str(self._file_path), section=self._config_section)
        return OptimizationParameters(**config_opt)
