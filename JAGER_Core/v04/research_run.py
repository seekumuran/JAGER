from .hunter import JagerHunter
from .research import ResearchAnalyzer


def main():
    hunter = JagerHunter(
        seed=42,
        budget=1000,
    )

    hunter.run()

    analyzer = ResearchAnalyzer(
        hunter
    )

    summary = analyzer.summary()

    print("=" * 60)
    print("JÄGER RESEARCH RUN")
    print("=" * 60)

    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
