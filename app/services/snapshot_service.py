from datetime import datetime
from pathlib import Path
from uuid import uuid4

import cv2

from app.core.logger import logger
from app.core.storage import storage


class SnapshotService:

    def save_snapshot(
        self,
        image,
        prefix: str = "snapshot"
    ) -> str:

        now = datetime.utcnow()

        year = now.strftime("%Y")

        month = now.strftime("%m")

        day = now.strftime("%d")

        hour = now.strftime("%H")
        
        minute = now.strftime("%M")

        snapshot_directory = (
            storage.snapshots_path
            / year
            / month
            / day
            / hour
            / minute
        )

        snapshot_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        filename = (
            f"{prefix}_"
            f"{uuid4().hex}.jpg"
        )

        snapshot_path = (
            snapshot_directory / filename
        )

        success = cv2.imwrite(
            str(snapshot_path),
            image
        )

        if not success:

            raise RuntimeError(
                "Failed to save snapshot"
            )

        logger.info(
            f"Snapshot saved at "
            f"'{snapshot_path}'"
        )

        return str(snapshot_path)

    def exists(
        self,
        snapshot_path: str
    ) -> bool:

        return Path(snapshot_path).exists()

    def delete_snapshot(
        self,
        snapshot_path: str
    ) -> None:

        path = Path(snapshot_path)

        if not path.exists():
            return

        path.unlink()

        logger.info(
            f"Snapshot deleted: "
            f"'{snapshot_path}'"
        )


snapshot_service = SnapshotService()