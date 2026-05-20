from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import numpy as np


@dataclass
class Frame:
    camera_id: str
    image: np.ndarray

    timestamp: datetime = field(default_factory=datetime.utcnow)

    fps: Optional[float] = None

    width: Optional[int] = None
    height: Optional[int] = None

    source: Optional[str] = None