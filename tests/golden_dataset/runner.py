"""
Golden Dataset Runner

Chức năng:
- Đọc các test case trong thư mục input/
- Chạy Interpretation Engine
- Ghi kết quả vào thư mục actual/

Runner KHÔNG:
- So sánh kết quả
- Validate dữ liệu
- Sinh báo cáo
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Protocol


logger = logging.getLogger(__name__)


# ==========================================================
# Directories
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "input"
ACTUAL_DIR = BASE_DIR / "actual"

INPUT_DIR.mkdir(parents=True, exist_ok=True)
ACTUAL_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Engine Protocol
# ==========================================================

class InterpretationEngineProtocol(Protocol):
    """Protocol cho Interpretation Engine."""

    def interpret(self, chart: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sinh kết quả luận giải.

        Parameters
        ----------
        chart : dict
            Dữ liệu đầu vào.

        Returns
        -------
        dict
            Kết quả luận giải.
        """
        ...


# ==========================================================
# Helpers
# ==========================================================

def list_cases() -> List[str]:
    """
    Lấy danh sách tên case.

    Returns
    -------
    list[str]
    """

    return sorted(file.stem for file in INPUT_DIR.glob("*.json"))


def load_input(case_name: str) -> Dict[str, Any]:
    """
    Đọc dữ liệu input.

    Parameters
    ----------
    case_name : str

    Returns
    -------
    dict
    """

    file_path = INPUT_DIR / f"{case_name}.json"

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_output(
    case_name: str,
    result: Dict[str, Any]
) -> Path:
    """
    Lưu output.

    Parameters
    ----------
    case_name : str

    result : dict

    Returns
    -------
    Path
    """

    output_path = ACTUAL_DIR / f"{case_name}.json"

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=4,
            sort_keys=True,
        )

    return output_path


# ==========================================================
# Runner
# ==========================================================

def run_case(
    case_name: str,
    engine: InterpretationEngineProtocol,
) -> Path:
    """
    Chạy một test case.

    Parameters
    ----------
    case_name : str

    engine :
        Interpretation Engine

    Returns
    -------
    Path
        File output.
    """

    logger.info("Running case: %s", case_name)

    chart = load_input(case_name)

    result = engine.interpret(chart)

    output = save_output(
        case_name,
        result,
    )

    logger.info("Finished: %s", case_name)

    return output


def run_all_cases(
    engine: InterpretationEngineProtocol,
) -> List[Path]:
    """
    Chạy toàn bộ Golden Dataset.

    Parameters
    ----------
    engine

    Returns
    -------
    list[Path]
    """

    outputs: List[Path] = []

    cases = list_cases()

    logger.info("Found %d cases.", len(cases))

    for case_name in cases:

        output = run_case(
            case_name,
            engine,
        )

        outputs.append(output)

    logger.info(
        "Finished %d cases.",
        len(outputs),
    )

    return outputs


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
    )

    print(
        "Golden Dataset Runner\n"
        "Import runner và truyền Interpretation Engine vào run_all_cases()."
    )
