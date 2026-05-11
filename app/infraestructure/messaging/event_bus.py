from collections import defaultdict
from typing import Callable

from app.core.logger import logger


class EventBus:

    def __init__(self):

        self._subscribers = defaultdict(list)

    def subscribe(
        self,
        event_name: str,
        handler: Callable
    ) -> None:

        logger.info(
            f"Subscribing handler to '{event_name}'"
        )

        self._subscribers[event_name].append(
            handler
        )

    def publish(
        self,
        event_name: str,
        payload: dict
    ) -> None:

        logger.info(
            f"Publishing event '{event_name}'"
        )

        handlers = self._subscribers.get(
            event_name,
            []
        )

        for handler in handlers:

            try:

                handler(payload)

            except Exception as error:

                logger.error(
                    f"Event handler failure "
                    f"for '{event_name}': "
                    f"{error}"
                )


event_bus = EventBus()