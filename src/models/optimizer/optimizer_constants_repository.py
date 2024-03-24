"""最適化における定数を読み込むためのレポジトリクラスのインターフェース
"""

import abc

from .optimizer_constants import BusinessRuleParameters


class IOptimizerConstantsRepository(abc.ABC):
    @abc.abstractmethod
    def read(self) -> BusinessRuleParameters:
        pass
