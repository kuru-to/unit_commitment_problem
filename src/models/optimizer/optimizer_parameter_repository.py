"""最適化のソルバーに関する設定を読み込むためのレポジトリクラスのインターフェース
"""

import abc

from .optimizer_parameters import OptimizationParameters


class IOptimizerParametersRepository(abc.ABC):
    @abc.abstractmethod
    def read(self) -> OptimizationParameters:
        pass
