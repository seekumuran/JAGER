from collections import defaultdict
from typing import Dict, Set


class ExperienceIndex:

    def __init__(self):

        self.by_target: Dict[
            str, Set[str]
        ] = defaultdict(set)

        self.by_tag: Dict[
            str, Set[str]
        ] = defaultdict(set)

    def add(self, experience):

        self.by_target[
            experience.target
        ].add(
            experience.experience_id
        )

        for tag in experience.tags:

            self.by_tag[tag].add(
                experience.experience_id
            )

    def remove(self, experience):

        self.by_target[
            experience.target
        ].discard(
            experience.experience_id
        )

        for tag in experience.tags:

            self.by_tag[tag].discard(
                experience.experience_id
            )

    def target_ids(
        self,
        target: str,
    ):

        return set(
            self.by_target.get(
                target,
                set(),
            )
        )

    def tag_ids(
        self,
        tag: str,
    ):

        return set(
            self.by_tag.get(
                tag,
                set(),
            )
        )

    def clear(self):

        self.by_target.clear()
        self.by_tag.clear()
