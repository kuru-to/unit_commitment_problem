from .optimizer_constants import BusinessRuleParameters
from .optimizer_input import OptimizerInput


class OptimizerInputSpecification:
    """最適化の入力が制約を満たしているか確認するクラス
    エラー文の作成もこのクラスの責務
    """

    def is_satisfied(self, input_: OptimizerInput, constants: BusinessRuleParameters):
        pass
