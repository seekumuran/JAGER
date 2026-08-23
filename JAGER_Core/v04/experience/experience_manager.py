from .experience_index import (
    ExperienceIndex,
)

from .experience_store import (
    ExperienceStore,
)

from .experience_record import (
    ExperienceRecord,
)

from .retrieval import (
    ExperienceRetriever,
)


class ExperienceManager:

    def __init__(
        self,
        maximum_size: int = 10000,
    ):

        self.store = ExperienceStore(
            maximum_size
        )

        self.index = ExperienceIndex()

        self.retriever = (
            ExperienceRetriever()
        )

    def add(
        self,
        experience: ExperienceRecord,
    ):

        existing = self.store.get(
            experience.experience_id
        )

        if existing is not None:
            self.index.remove(
                existing
            )

        self.store.add(
            experience
        )

        self.index.add(
            experience
        )

        return experience

    def get(
        self,
        experience_id: str,
    ):

        return self.store.get(
            experience_id
        )

    def retrieve(
        self,
        target: str,
        tags=None,
        limit: int = 5,
    ):

        candidates = []

        target_ids = (
            self.index.target_ids(
                target
            )
        )

        if tags:

            for tag in tags:

                target_ids |= (
                    self.index.tag_ids(
                        tag
                    )
                )

        for experience_id in target_ids:

            experience = self.store.get(
                experience_id
            )

            if experience is not None:
                candidates.append(
                    experience
                )

        return self.retriever.retrieve(
            candidates,
            target,
            tags,
            limit,
        )

    def discoveries(self):

        return self.store.discoveries()

    def size(self):

        return self.store.size()

    def snapshot(self):

        return [
            record.to_dict()
            for record
            in self.store.all()
        ]
