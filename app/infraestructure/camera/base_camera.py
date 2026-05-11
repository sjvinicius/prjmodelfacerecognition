from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class BaseCamera(ABC):

    @abstractmethod
    def start(self) -> None:
        """
        Starts the camera stream.
        """
        pass

    @abstractmethod
    def read(self) -> Optional[np.ndarray]:
        """
        Reads the current frame from the stream.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stops the camera stream.
        """
        pass

    @abstractmethod
    def is_opened(self) -> bool:
        """
        Returns whether the camera is active.
        """
        pass