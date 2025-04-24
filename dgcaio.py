#!/usr/bin/env python3
# DGC-All-In-One by DiamondGotCat
# MIT License
# Copyright (c) 2025 DiamondGotCat

import json
import requests
import argparse

import os
from os.path import expanduser
from datetime import datetime, timezone, timedelta

import pylo2
run_pylo = pylo2.run_text

# ----- Versions -----

dgcaio_version = "1.0"
pylo_version = pylo2.Interpreter.VERSION

# ----- Variables -----

aiofiles = []
aio_list = {}
aiopackages_array = []
aiopackages_dict = {}
installed_packages = []

# ----- DGC Epoch -----
DGC_EPOCH_BASE = datetime(2000, 1, 1, tzinfo=timezone.utc)

def datetime_to_dgc_epoch64(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = dt - DGC_EPOCH_BASE
    milliseconds = int(delta.total_seconds() * 1000)
    binary_str = format(milliseconds, '064b')  # 64ビット固定長
    return binary_str

def dgc_epoch64_to_datetime(dgc_epoch_str: str) -> datetime:
    milliseconds = int(dgc_epoch_str, 2)
    return DGC_EPOCH_BASE + timedelta(milliseconds=milliseconds)

# ----- Functions -----
def main():
    parser = argparse.ArgumentParser(prog='dgcaio', description='Most Customizable Package Installer', epilog='MIT License, Copyright (c) 2025 DiamondGotCat')
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # list サブコマンド
    list_parser = subparsers.add_parser("list", help="List installed packages")
    list_parser.add_argument("content", help="Packages / Repositorys", choices=["packages", "repositorys"])

    # install サブコマンド
    run_parser = subparsers.add_parser("run", help="Run Package Script")
    run_parser.add_argument("id", help="Specify package script")
    run_parser.add_argument("package", help="ID of the package")
    run_parser.add_argument("--version", help="Specify package version", default="none")

    # add_repo サブコマンド
    add_repo_parser = subparsers.add_parser("add_repo", help="Add a new repository")
    add_repo_parser.add_argument("id", help="Repository ID")
    add_repo_parser.add_argument("path", help="Repository Path")
    add_repo_parser.add_argument("--isremote", help="Is Remote Repository", choices=["true", "false"], default="true")

    # remove_repo サブコマンド
    remove_repo_parser = subparsers.add_parser("remove_repo", help="Remove a repository")
    remove_repo_parser.add_argument("id", help="Repository ID")

    # パース
    args = parser.parse_args()

    now = datetime.now()
    home = expanduser("~")
    reposfile = "$HOME/.dgc/repos.dgcaio".replace("$HOME", home)
    installedfile = "$HOME/.dgc/installed.dgcaio".replace("$HOME", home)

    print("DGC-All-In-One " + dgcaio_version)
    print("Built-in Pylo: " + pylo_version)
    print(f"Current Time(dgce64): {datetime_to_dgc_epoch64(now)}")
    print("Load Repository List: $HOME/.dgc/repos.dgcaio")

    # Available Packages
    os.makedirs(os.path.dirname(reposfile), exist_ok=True)

    if os.path.isfile(reposfile):
        with open(reposfile, "r") as f:
            aiofiles = json.load(f)

    else:
        file = open(reposfile, "w")
        file.write(
"""
[
    {
        "id": "main",
        "isremote": "true",
        "path": "https://versions.diamondgotcat.net/main.dgcaio"
    }
]
""".strip()
)
        file.close()
        with open(reposfile, "r") as f:
            aiofiles = json.load(f)

    # Installed Packages
    os.makedirs(os.path.dirname(installedfile), exist_ok=True)

    if os.path.isfile(installedfile):
        with open(installedfile, "r") as f:
            installed_packages = json.load(f)

    else:
        file = open(installedfile, "w")
        file.write("[]\n")
        file.close()

        with open(installedfile, "r") as f:
            installed_packages = json.load(f)

    for aiofile in aiofiles:
        if aiofile["isremote"] == "false":
            aio_list[aiofile["id"]] = json.load(aiofile["path"])
        else:
            r = requests.get(aiofile["path"])
            aio_list[aiofile["id"]] = r.json()
        for aiopackage in aio_list[aiofile["id"]]["packages"]:
            aiopackages_array.append(aiopackage)
            aiopackages_dict[aiopackage["id"]] = aiopackage
    
    if args.mode == "list":
        if args.content == "packages":
            print("----- Installed Packages -----")
            for package in installed_packages:
                print(f"{package["id"]} Version {package["version"]} by Repository {package["repo"]}")
        elif args.content == "repositorys":
            print("----- Installed Repositorys -----")
            for repository in aiofiles:
                if repository["isremote"] == "false":
                    isRemoteString = "Local"
                else:
                    isRemoteString = "Remote"
                print(f"[{repository["id"]}] {repository["path"]} ({isRemoteString})")

    elif args.mode == "run":
        action_id = args.id
        package_id = args.package
        package_version = args.version
        if package_id in aiopackages_dict.keys():
            package = aiopackages_dict[package_id]
            if package_version == "none":
                package_version = package["default_version"]
            if package_version in package["versions"].keys():
                if action_id in package["versions"][package_version]:
                    print(f"[INFO] Start Action[{package_id}@{package_version}/{action_id}]...")
                    pylo_script = package["versions"][package_version][action_id]
                    run_pylo(pylo_script)
                    print(f"[INFO] Action Finished.")

                    if action_id == "install":
                        repo_id = None
                        for rid, repo in aio_list.items():
                            if any(p["id"] == package_id for p in repo["packages"]):
                                repo_id = rid
                                break

                        if repo_id is None:
                            repo_id = "unknown"

                        already_installed = any(p["id"] == package_id and p["version"] == package_version for p in installed_packages)
                        if not already_installed:
                            installed_packages.append({
                                "id": package_id,
                                "repo": repo_id,
                                "version": package_version
                            })
                            with open(installedfile, "w") as f:
                                json.dump(installed_packages, f, indent=4)


                else:
                    print(f"[ERROR] Action Not Found: {action_id}")
            else:
                print(f"[ERROR] Version Not Found: {package_version}")

        else:
            print(f"[ERROR] Package Not Found: {package_id}")

    elif args.mode == "add_repo":
        aiofiles.append({"id": args.id, "isremote": args.isremote, "path": args.path})

        with open(reposfile, "w") as f:
            json.dump(aiofiles, f)
        
        print(f"[INFO] Repository '{args.id}' added.")

    elif args.mode == "remove_repo":
        # Remove the repository with matching ID
        aiofiles = [repo for repo in aiofiles if repo["id"] != args.id]

        with open(reposfile, "w") as f:
            json.dump(aiofiles, f)
        print(f"[INFO] Repository '{args.id}' removed.")

if __name__ == "__main__":
    main()
