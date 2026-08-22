import platform
import socket


def collect_system_identity():

    return {
        "platform": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "python_version": platform.python_version(),
    }


def print_identity():

    identity = (
        collect_system_identity()
    )

    print(
        "Platform:",
        identity["platform"],
    )

    print(
        "Release:",
        identity["release"],
    )

    print(
        "Architecture:",
        identity["architecture"],
    )

    print(
        "Hostname:",
        identity["hostname"],
    )

    print(
        "Python:",
        identity["python_version"],
    )


if __name__ == "__main__":
    print_identity()
