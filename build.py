import os
import sys
import shutil

PROGRAM_FILES_ROOTS = [
    os.environ.get("ProgramFiles", "C:\\Program Files"),
    os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
]
VISUAL_STUDIO_INSTALLED_VERSION = 2022
VISUAL_STUDIO_INSTALLED_VARIANT = [
    "Community", "Professional", "Enterprise", "BuildTools"
]

MS_BUILD_PATH_TEMPLATE = '{}\\Microsoft Visual Studio\\{}\\{}\\MSBuild\\Current\\Bin\\MSBuild.exe'
MS_BUILD_PATH = None

for program_files in PROGRAM_FILES_ROOTS:
    for variant in VISUAL_STUDIO_INSTALLED_VARIANT:
        candidate = MS_BUILD_PATH_TEMPLATE.format(
            program_files, VISUAL_STUDIO_INSTALLED_VERSION, variant
        )
        if os.path.exists(candidate):
            MS_BUILD_PATH = candidate
            break
    if MS_BUILD_PATH:
        break

# Fall back to msbuild on PATH (e.g. set by microsoft/setup-msbuild in CI).
if not MS_BUILD_PATH:
    MS_BUILD_PATH = shutil.which("msbuild") or shutil.which("MSBuild.exe") or "msbuild"

PROJECT_SOLUTION_PATH = os.path.join(os.path.curdir, 'FedoraWSL.sln')
MS_BUILD_TARGET = "Build"
MS_BUILD_CONFIG = "Debug"
MS_BUILD_PLATFORM = "x64"

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        if sys.argv[i].startswith("--target="):
            MS_BUILD_TARGET = sys.argv[i].split("=")[1].capitalize()
            if MS_BUILD_TARGET == "Clean":
                break
        elif sys.argv[i].startswith("--config="):
            MS_BUILD_CONFIG = sys.argv[i].split("=")[1].capitalize()
        elif sys.argv[i].startswith("--platform="):
            MS_BUILD_PLATFORM = sys.argv[i].split("=")[1]
            # Normalize ARM64: the .vcxproj/.sln configurations declare
            # Platform=ARM64 (uppercase) and recent MSBuild versions match
            # the platform string case-sensitively.
            if MS_BUILD_PLATFORM.lower() == "arm64":
                MS_BUILD_PLATFORM = "ARM64"

BUILD_COMMAND = "\"{}\" {} /t:{} /m /nr:true /p:Configuration={};Platform={}"

BUILD_COMMAND = BUILD_COMMAND.format(
    MS_BUILD_PATH,
    PROJECT_SOLUTION_PATH,
    MS_BUILD_TARGET,
    MS_BUILD_CONFIG,
    MS_BUILD_PLATFORM
)

exitCode = os.system(BUILD_COMMAND)

if (MS_BUILD_TARGET == "Clean"):
    cleanDirs = [
        "FedoraWSL\\x64",
        "FedoraWSL\\ARM64",
        "FedoraWSL-Appx\\x64",
        "FedoraWSL-Appx\\ARM64",
        "FedoraWSL-Appx\\BundleArtifacts",
        "x64\\Debug",
        "x64\\Release",
        "AppPackages"
    ]

    cleanFiles = [
        "FedoraWSL-Appx\\FedoraWSL-Appx.vcxproj.user",
        "FedoraWSL\\FedoraWSL.vcxproj.user",
        "FedoraWSL\\MSG00409.bin",
    ]

    for cleanDir in cleanDirs:
        if os.path.exists(cleanDir):
            shutil.rmtree(cleanDir)

    for cleanFile in cleanFiles:
        if os.path.exists(cleanFile):
            os.remove(cleanFile)

sys.exit(exitCode)
