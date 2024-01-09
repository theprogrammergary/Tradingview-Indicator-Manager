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
        self.system: str = platform.system()

        if self.system == "Darwin":
            self.mac_os()

        elif self.system == "Windows":
            self.windows()

        elif self.system == "Linux":
            self.mac_os()

        else:
            print(f"BUILD FAILED: System={self.system} not recognized")

    def mac_os(self) -> None:
        """
        Build MAC OS GUI
        """

        cwd: str = os.path.join(os.path.dirname(p=os.path.abspath(path=__file__)), "..")

        output_dir: str = os.path.join(cwd, "..", "app")

        entry_path: str = os.path.join(cwd, "main.py")

        png_path: str = os.path.join(cwd, ".setup", "logo.png")
        ico_path: str = os.path.join(cwd, ".setup", "logo.ico")

        build_dir = "build"
        # DIST_DIR = "dist"

        pyinstaller_command: list[str] = [
            "pyinstaller",
            f"--add-data={png_path}:./.setup/",
            f"--add-data={ico_path}:./.setup/",
            f"--icon={png_path}",
            "-nTradingvview Indicator Access Management",
            "--onefile",
            "--windowed",
            "--uac-admin",
            "--distpath",
            output_dir,
            entry_path,
        ]

        try:
            subprocess.run(args=pyinstaller_command, check=True)
            print("PyInstaller build completed successfully.")

            try:
                shutil.rmtree(build_dir, ignore_errors=True)
                os.remove(
                    path=os.path.join(
                        os.getcwd(), "Tradingvview Indicator Access Management.spec"
                    )
                )
                print("\nBuild files cleaned up successfully.")

            except Exception as e:  # pylint:disable = W0718
                print(f"Error: {e}")

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def windows(self) -> None:
        """
        Build WIN GUI
        """

        cwd: str = os.path.join(os.path.dirname(p=os.path.abspath(path=__file__)), "..")

        output_dir: str = os.path.join(cwd, "..", "app")

        entry_path: str = os.path.join(cwd, "main.py")

        png_path: str = os.path.join(cwd, ".setup", "logo.png")
        ico_path: str = os.path.join(cwd, ".setup", "logo.ico")

        build_dir = "build"
        # DIST_DIR = "dist"

        pyinstaller_command: list[str] = [
            "pyinstaller",
            f"--add-data={png_path}:./.setup/",
            f"--add-data={ico_path}:./.setup/",
            f"--icon={ico_path}",
            "-nTradingvview Indicator Access Management",
            "--onefile",
            "--windowed",
            "--distpath",
            output_dir,
            entry_path,
        ]

        try:
            subprocess.run(args=pyinstaller_command, check=True)
            print("PyInstaller build completed successfully.")

            try:
                shutil.rmtree(build_dir, ignore_errors=True)
                os.remove(
                    path=os.path.join(
                        os.getcwd(), "Tradingvview Indicator Access Management.spec"
                    )
                )
                print("\nBuild files cleaned up successfully.")

            except Exception as e:  # pylint:disable = W0718
                print(f"Error: {e}")

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    build = BuildApp()
