import os
import platform
import shutil
import subprocess


class BuildApp:
    def __init__(self) -> None:
        self.system: str = platform.system()

        if self.system == "Darwin":
            self.mac_os()

        else:
            print("BUILD FAILED: System not recognized")

    def mac_os(self) -> None:
        CWD: str = os.path.join(os.path.dirname(p=os.path.abspath(path=__file__)), "..")

        OUTPUT_DIR: str = os.path.join(CWD, "..", "app")

        ENTRY_PATH: str = os.path.join(CWD, "main.py")

        ICON_PATH: str = os.path.join(CWD, ".setup", "logo.png")

        BUILD_DIR = "build"
        # DIST_DIR = "dist"

        pyinstaller_command: list[str] = [
            "pyinstaller",
            f"--add-data={ICON_PATH}:./.setup/",
            f"--icon={ICON_PATH}",
            "-nTradingvview Indicator Access Management",
            "--onefile",
            "--windowed",
            "--uac-admin",
            "--distpath",
            OUTPUT_DIR,
            ENTRY_PATH,
        ]

        try:
            subprocess.run(args=pyinstaller_command, check=True)
            print("PyInstaller build completed successfully.")

            try:
                shutil.rmtree(BUILD_DIR, ignore_errors=True)
                os.remove(
                    path=os.path.join(
                        os.getcwd(), "Tradingvview Indicator Access Management.spec"
                    )
                )
                print("\nBuild files cleaned up successfully.")

            except Exception as e:
                print(f"Error: {e}")

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    build = BuildApp()