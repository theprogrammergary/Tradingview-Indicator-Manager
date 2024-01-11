"""
Python build script for creating a pyinstaller GUI app.
"""

import os
import platform
import shutil
import subprocess


class BuildApp:
    """
    Buils pyinstaller GUI application
    """

    def __init__(self) -> None:
        self.cwd: str = os.path.join(
            os.path.dirname(p=os.path.abspath(path=__file__)), ".."
        )

        self.output_dir: str = os.path.join(self.cwd, "..", "app")
        self.entry_path: str = os.path.join(self.cwd, "main.py")

        self.png_path: str = os.path.join(self.cwd, ".setup", "logo.png")
        self.ico_path: str = os.path.join(self.cwd, ".setup", "logo.ico")
        self.icns_path: str = os.path.join(self.cwd, ".setup", "logo.icns")

        self.build_dir = "build"

        self.system: str = platform.system()
        self.icon_path: str = (
            self.ico_path if self.system == "Windows" else self.png_path
        )

        if self.system in ["Darwin", "Linux", "Windows"]:
            self.build()
        else:
            print(f"BUILD FAILED: System={self.system} not recognized")

    def build(self) -> None:
        """
        Build PyInstaller GUI
        """

        pyinstaller_command: list[str] = [
            "pyinstaller",
            f"--add-data={self.png_path}:./.setup/",
            f"--add-data={self.ico_path}:./.setup/",
            f"--icon={self.icon_path}",
            "-nTradingview Indicator Access Management",
            "--onefile",
            "--windowed",
            "--distpath",
            self.output_dir,
            self.entry_path,
        ]

        try:
            subprocess.run(args=pyinstaller_command, check=True)
            print("PyInstaller build completed successfully.")

            try:
                shutil.rmtree(self.build_dir, ignore_errors=True)
                os.remove(
                    path=os.path.join(
                        os.getcwd(), "Tradingview Indicator Access Management.spec"
                    )
                )
                print("\nBuild files cleaned up successfully.")

            except Exception as e:  # pylint:disable = W0718
                print(f"Error: {e}")

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    build = BuildApp()
