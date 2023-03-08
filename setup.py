import sys
import cx_Freeze

base = None

if (sys.platform == 'win32'):
    base = "Win32GUI"


executables = [cx_Freeze.Executable("main.py",
                                    shortcut_name="AI6WINArcTool",
                                    shortcut_dir="AI6WINArcTool",
                                    #base="Win32GUI"
                                    )]

cx_Freeze.setup(
        name="AI6WINArcTool",
        version="1.1",
        description="Dual languaged (rus+eng) tool for packing and unpacking archives of Silky Engine.\n"
                    "Двуязычное средство (рус+англ) для распаковки и запаковки архивов Silky Engine.",
        options={"build_exe": {"packages": []}},
        executables=executables
)