from pathlib import Path


def get_project_root() -> Path:
    """
    获取项目根目录（smartpick_bot）
    不依赖 cwd，最稳
    """
    p = Path(__file__).resolve()
    for parent in p.parents:
        if parent.name == "smartpick_bot":
            return parent
    raise RuntimeError("smartpick_bot 目录未找到")


def get_parent_dir(level: int = 1) -> Path:
    """
    获取当前文件的第 level 层父目录
    level=1 -> parents[1]
    """
    return Path(__file__).resolve().parents[level]

