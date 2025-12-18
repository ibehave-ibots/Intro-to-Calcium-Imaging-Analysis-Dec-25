# Intro to Calcium Imaging Analysis December 2025

**Dates**:
- 18.12.2025 @ 1:30pm - 6:00pm
- 19.12.2025 @ 1:30pm - 6:00pm

**Instructor**: Dr. Ole Bialas

**Agenda**:
- Fundamentals of Spike Train Analysis
- Single-Pixel Fluoresence in Calcium Imaging
- Spike Inference for Calcium Traces

## Installation

**Requirements**
- VSCode: https://code.visualstudio.com/download
- Pixi: https://pixi.sh/latest/#installation
- Git: https://git-scm.com/downloads

Clone this repository and install the pixi environment:

```
git clone https://github.com/ibehave-ibots/Intro-to-Calcium-Imaging-Analysis-Dec-25.git
cd Intro-to-Calcium-Imaging-Analysis-Dec-25
pixi install
```

If you get an error when downloading the package, try deactiving TLS certificate validation:

```
pixi config set tls-no-verify true
```

If VSCode can't find the pixi environment try installing the kernel

```
pixi run install-kernel
```

and then clicking Select Kernel > Jupyter Kernels > intro2caim
If you can't find the intro2caim kernel, try clicking the reload button in the top right
