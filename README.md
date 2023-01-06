# Fedora WSL

## Installation

- You can install Fedora WSL from [Microsoft Store](https://apps.microsoft.com/store/detail/fedora-wsl/9NPCP8DRCHSN)

- Or if you don't want to use Microsoft Store then download the latest msix package from [Release Page](https://github.com/VsTechDev/Fedora-WSL/releases/latest)

***Note*** - to install manually from the msix package you need to install the .cer file first to the "Trusted Root Certificate Store" of the "local machine"

## Build

### Prerequisites

- Visual Studio 2022
- Python

### Getting Started

- Fork and clone your fork of the Project

- Generate a test certificate:

  - In Visual Studio, open FedoraWSL-Appx/MyDistro.appxmanifest
  - Select the Packaging tab
  - Select "Choose Certificate"
  - Click the Configure Certificate drop-down and select Create test certificate.

- Copy tar.gz containing your distro into the x64 folder at the root of the project and rename it to rootfs.tar.gz

***Note*** - You can get the rootfs.tar.gz file from the releases page 

- Then open a terminal window in the root of the project and type in the command

```sh
python build.py --target=build --config=debug --platform=x64
```

### Root FS

- The main Root FS file this app is based on is at - https://github.com/VsTechDev/Fedora-WSL-RootFS

- It is based on Fedora Docker Image with few tweaks and pre-installed dependencies
