from dataclasses import dataclass
from importlib import import_module
from typing import List


@dataclass(frozen=True)
class ImportResult:

    module: str
    imported: bool
    error: str = ""


class ImportAudit:

    def __init__(
        self,
        modules: List[str],
    ):

        self.modules = list(modules)

    def run(self):

        results = []

        for module in self.modules:

            try:

                import_module(module)

                results.append(
                    ImportResult(
                        module=module,
                        imported=True,
                    )
                )

            except Exception as exc:

                results.append(
                    ImportResult(
                        module=module,
                        imported=False,
                        error=str(exc),
                    )
                )

        return results

    def passed(self):

        return all(
            result.imported
            for result in self.run()
        )

    def summary(self):

        results = self.run()

        return {
            "total": len(results),
            "passed": sum(
                result.imported
                for result in results
            ),
            "failed": sum(
                not result.imported
                for result in results
            ),
            "healthy": all(
                result.imported
                for result in results
            ),
        }
