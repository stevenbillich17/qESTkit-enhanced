from abc import ABC, abstractmethod
from typing import List, Dict, Union, Optional, Tuple, Any
import numpy as np


class QuantumSimulator(ABC):
    @abstractmethod
    def run(self, circuit: Any, shots: int = 1024) -> Dict[str, int]:
        pass


    @abstractmethod
    def get_num_qubits(self) -> int:
        pass


    @abstractmethod
    def apply_gate(
            self,
            gate_name: str,
            targets: Union[int, List[int]],
            controls: Optional[Union[int, List[int]]] = None,
            params: Optional[List[float]] = None,
    ):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def apply_custom_gate(
            self,
            gate_matrix: np.ndarray,# todo: maybe it will require other form
            targets: Union[int, List[int]],
            controls: Optional[Union[int, List[int]]] = None,
    ):
        pass

    @abstractmethod
    def calculate_expectation_value(
            self,
            observable: np.ndarray,
            state_vector: np.ndarray
    ) -> float:
        pass