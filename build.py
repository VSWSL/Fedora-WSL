import os
import sys

PROGRAM_FILES = os.environ["ProgramFiles"]
VISUAL_STUDIO_INSTALLED_VERSION = 2022
VISUAL_STUDIO_INSTALLED_VARIANT = "Community"

MS_BUILD_PATH = '{}\\Microsoft Visual Studio\\{}\\{}\\MSBuild\\Current\\Bin\\MSBuild.exe'

MS_BUILD_PATH = MS_BUILD_PATH.format(
    PROGRAM_FILES,
    VISUAL_STUDIO_INSTALLED_VERSION,
    VISUAL_STUDIO_INSTALLED_VARIANT
)

if not os.path.exists(MS_BUILD_PATH):
    print("MSBuild 2022 not found")
    sys.exit(1)

PROJECT_SOLUTION_PATH = os.path.join(os.path.curdir, 'FedoraWSL.sln')
MS_BUILD_TARGET = "Build"
MS_BUILD_CONFIG = "Debug"
MS_BUILD_PLATFORM = "x64"

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("--config="):
            MS_BUILD_CONFIG = sys.argv[i].split("=")[1].capitalize()
        elif sys.argv[i].startswith("--target="):
            MS_BUILD_TARGET = sys.argv[i].split("=")[1].capitalize()
        elif sys.argv[i].startswith("--platform="):
            MS_BUILD_PLATFORM = sys.argv[i].split("=")[1]

BUILD_COMMAND = "\"{}\" {} /t:{} /m /nr:true /p:Configuration={};Platform={}"

BUILD_COMMAND = BUILD_COMMAND.format(
    MS_BUILD_PATH,
    PROJECT_SOLUTION_PATH,
    MS_BUILD_TARGET,
    MS_BUILD_CONFIG,
    MS_BUILD_PLATFORM
)

print(BUILD_COMMAND)

os.system(BUILD_COMMAND)
