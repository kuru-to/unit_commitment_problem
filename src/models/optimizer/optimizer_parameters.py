import pydantic


@pydantic.dataclasses.dataclass
class OptimizationParameters:
    """開発者が設定するパラメータ群(スレッド数, 目的関数の傾斜など)"""

    MODEL_NAME: str

    NUM_THREADS: int
    MAX_SECONDS: int

    CPLEX_LOG_FILE: str
