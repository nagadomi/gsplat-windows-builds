import sys
import urllib.request
import json
import re
import subprocess
import torch


def install_gsplat_windows(gsplat_version, release_url):
    if sys.platform != "win32":
        raise RuntimeError("install_gsplat_windows() only supports Windows.")

    py_tag = f"cp{sys.version_info.major}{sys.version_info.minor}"
    ver = torch.__version__.split("+")[0].split(".")
    pt_tag = f"pt{ver[0]}{ver[1]}"
    if not torch.version.cuda:
        raise RuntimeError(
            "This PyTorch build does not include CUDA support. "
            "Please install a CUDA-enabled version of PyTorch."
        )
    cu_tag = "cu" + torch.version.cuda.replace(".", "")

    with urllib.request.urlopen(release_url) as res:
        data = json.load(res)
        assets = data["assets"]

    pattern = re.compile(rf"{gsplat_version}\+{pt_tag}{cu_tag}-{py_tag}-{py_tag}")
    for item in assets:
        name = item["name"]
        if name.endswith(".whl") and pattern.search(name):
            whl_url = item["browser_download_url"]
            print("Found:", name)
            print("Downloading:", whl_url)
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", whl_url])
            break
    else:
        raise RuntimeError("No matching wheel found for this environment.")


def sample_code():
    GSPLAT_VERSION = "1.5.3"
    # GSPLAT_WINDOWS_RELEASE_URL = "https://api.github.com/repos/nagadomi/gsplat-windows-builds/releases/latest"
    GSPLAT_WINDOWS_RELEASE_URL = "https://api.github.com/repos/nagadomi/gsplat-windows-builds/releases/tags/v20251230_6"
    install_gsplat_windows(GSPLAT_VERSION, GSPLAT_WINDOWS_RELEASE_URL)


if __name__ == "__main__":
    sample_code()
