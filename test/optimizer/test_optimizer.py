import itertools
import time
from dataclasses import dataclass
from pathlib import Path

import pulp

from src.infra.optimizer.file_optimizer_parameter_repository import FileOptimizerParametersRepository
from src.models.optimizer.optimizer import IOptimizer
from src.models.optimizer.optimizer_constants import BusinessRuleParameters
from src.models.optimizer.optimizer_input import OptimizerInput
from src.models.optimizer.optimizer_output import InfeasibleResult, OptimizedResult
from src.models.optimizer.optimizer_parameters import OptimizationParameters
from src.utils.config_util import read_config, test_section


@dataclass(frozen=True)
class Worker:
    name: str


@dataclass(frozen=True)
class Task:
    name: str


class PulpTestInput(OptimizerInput):
    def __init__(self):
        self.workers = [Worker(i) for i in ["Aさん", "Bさん", "Cさん"]]
        self.tasks = [Task(j) for j in ["仕事イ", "仕事ロ", "仕事ハ"]]

        # 作業員 i を タスク j に割り当てたときのコストの集合（一時的なリスト）
        cc = [
            [1, 2, 3],
            [4, 6, 8],
            [10, 13, 16],
        ]

        self.costs = {}
        for i, worker in enumerate(self.workers):
            for j, task in enumerate(self.tasks):
                self.costs[worker, task] = cc[i][j]


class PulpTestConstants(BusinessRuleParameters):
    upper_assignment: int = 1


@dataclass(frozen=True)
class Assignment:
    worker: Worker
    task: Task


@dataclass
class PulpTestOutput(OptimizedResult):
    data: list[Assignment]
    elapsed_time: float
    sol_objective: float

    def display_result_detail(self, input_: PulpTestInput):
        for assignment in self.data:
            print(f"{assignment.worker.name}, {assignment.task} is assigned")


class PulpTestSolver(IOptimizer):
    _parameters: OptimizationParameters
    _problem: pulp.LpProblem

    def validate(self, input_: PulpTestInput, constants: PulpTestConstants):
        pass

    def solve(self, _input: PulpTestInput, constants: PulpTestConstants) -> PulpTestOutput:
        start_time = time.time()

        # 数理最適化問題（最小化）を宣言
        self._problem = pulp.LpProblem("Problem-2", pulp.LpMinimize)

        # 変数集合を表す辞書
        x = {}

        # 0-1変数を宣言
        for i in _input.workers:
            for j in _input.tasks:
                x[i, j] = pulp.LpVariable(f"x({i},{j})", 0, 1, pulp.LpInteger)

        # 目的関数を宣言
        self._problem += (
            pulp.lpSum(_input.costs[i, j] * x[i, j] for i in _input.workers for j in _input.tasks),
            "TotalCost",
        )

        # 制約条件を宣言
        # 各作業員 i について、割り当ててよいタスク数は1つ以下
        for i in _input.workers:
            self._problem += sum(x[i, j] for j in _input.tasks) <= constants.upper_assignment, f"Constraint_leq_{i}"
            # 制約条件ラベルに '[' や ']' や '-' を入れても、なぜか '_' に変わる…？

        # 各タスク j について、割り当てられる作業員数はちょうど1人
        for j in _input.tasks:
            self._problem += sum(x[i, j] for i in _input.workers) == 1, f"Constraint_eq_{j}"

        result_status = self._problem.solve(pulp.PULP_CBC_CMD())

        if result_status < 0:
            return InfeasibleResult()

        lst_assignment = []
        for i, j in itertools.product(_input.workers, _input.tasks):
            if round(x[i, j].value()) == 1:
                lst_assignment.append(Assignment(i, j))
        return PulpTestOutput(lst_assignment, time.time() - start_time, pulp.value(self._problem.objective))


def test_pulp_optimize():
    config = read_config(section=test_section)
    filename_config_opt = Path(config.get("PATH_CONFIG") + config.get("CONFIG_OPTIMIZER"))

    test_repository = FileOptimizerParametersRepository(filename_config_opt, test_section)
    PulpTestSolver(test_repository.read()).run(PulpTestInput(), PulpTestConstants())
