from dataclasses import dataclass
from src.smd.smd_structures import BonePositionData, BoneInitData, FrameData


@dataclass
class SMDDocument:
    doc_ver: int
    bones: dict[int, BoneInitData]
    frames: dict[int, FrameData]

    def to_string(self) -> str:
        yield f"version {self.doc_ver}\n"
        yield "nodes\n"

        for bone_id in sorted(self.bones.keys()):
            yield f"\t{bone_id} {self.bones[bone_id].bone_name} {self.bones[bone_id].bone_parent_id}\n"

        yield "end\n"
        yield "skeleton\n"

        for frame_id in sorted(self.frames.keys()):
            yield f"\ttime {frame_id}\n"

            for bone_data in self.frames[frame_id].to_string():
                yield f"\t\t{bone_data}"

        yield "end\n"

    @classmethod
    def from_string(cls, doc_string: str):
        bone_section = False
        frame_section = False
        last_frame_number: int = -1
        doc_version: int = 1
        bones_map: dict[int, BoneInitData] = dict()
        frames_map: dict[int, FrameData] = dict()
        bone_position_map: dict[int, BonePositionData] = dict()

        for line in doc_string.splitlines():
            if line.startswith("version"):
                doc_version = int(line.split()[1])

            elif line.startswith("nodes"):
                bone_section = True

            elif line.startswith("skeleton"):
                frame_section = True

            elif line.startswith("end"):
                bone_section = False
                frame_section = False

            elif bone_section:
                bone_data = BoneInitData.from_string(line)
                bones_map[bone_data.bone_id] = bone_data

            elif frame_section:
                if line.strip().startswith("time"):
                    if last_frame_number != -1:
                        frames_map[last_frame_number].frame_position_data = bone_position_map.copy()
                        bone_position_map = dict()

                    frame = FrameData.from_string(line)
                    last_frame_number = frame.frame_id
                    frames_map[last_frame_number] = frame

                else:
                    bone_position_data = BonePositionData.from_string(line)
                    bone_position_map[bone_position_data.bone_id] = bone_position_data

        if last_frame_number != -1:
            frames_map[last_frame_number].frame_position_data = bone_position_map.copy()

        return cls(doc_version, bones_map, frames_map)
