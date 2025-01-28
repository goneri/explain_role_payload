#!/usr/bin/env python3

import argparse
from enum import Enum
from pydantic import BaseModel
#from dataclasses import dataclass
from pathlib import Path
from typing import Union
import json

class RoleFileTypeEnum(str, Enum):
    Task = "task"
    Default = "default"
    Var = "var"
    Template = "template"

class AnsibleRoleFile(BaseModel):
    path: str
    type: RoleFileTypeEnum
    content: str


class Payload(BaseModel):
    files: list[AnsibleRoleFile] = []
    role_name: str
    model_id: str = ""
    focus_on_file: str = ""

files: list[AnsibleRoleFile] = []


parser = argparse.ArgumentParser(
        prog='Prepare payload',
        description='Generate a payload for the explanation/role end-point')
parser.add_argument("role_directory", type=Path, help="Path of the role directory")
args = parser.parse_args()

payload = Payload(role_name=args.role_directory.name)

for role_type in [RoleFileTypeEnum.Task, RoleFileTypeEnum.Default]:
    subdir = args.role_directory / f"{role_type.value}s"
    payload.files += [AnsibleRoleFile(path=str(p), type=role_type, content=p.read_text()) for p in subdir.glob("*.yml")]

payload.focus_on_file = "tasks/main.yml"

print(payload.model_dump_json())
