"""
Golden Dataset Runner

Chức năng:
- Đọc các test case trong thư mục inputs/
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
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, List, Protocol


logger = logging.getLogger(__name__)


# ==========================================================
# Directories
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

INPUTS_FOLDER = "inputs"
EXPECTED_FOLDER = "expected"
ACTUAL_FOLDER = "actual"
REPORTS_FOLDER = "reports"
SCHEMAS_FOLDER = "schemas"
SNAPSHOTS_FOLDER = "snapshots"

INPUT_DIR = BASE_DIR / INPUTS_FOLDER
ACTUAL_DIR = BASE_DIR / ACTUAL_FOLDER

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

def _ensure_input_dir_exists() -> None:
    """Đảm bảo thư mục inputs tồn tại trước khi liệt kê case."""

    INPUT_DIR.mkdir(parents=True, exist_ok=True)


def _clear_actual_json_outputs() -> None:
    """Xóa mọi file *.json trong actual/ để tránh output cũ."""

    for output_file in ACTUAL_DIR.glob("*.json"):
        output_file.unlink()


def list_cases() -> List[str]:
    """
    Lấy danh sách tên case.

    Returns
    -------
    list[str]
    """

    _ensure_input_dir_exists()

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

    logger.info("[%s] Running", case_name)

    chart = load_input(case_name)

    try:
        result = engine.interpret(chart)
    except Exception as exc:
        logger.exception("[%s] interpret failed", case_name)
        result = {
            "status": "error",
            "message": str(exc),
        }

    output_payload: Dict[str, Any]
    if is_dataclass(result):
        output_payload = asdict(result)
    else:
        output_payload = result

    output = save_output(
        case_name,
        output_payload,
    )

    logger.info("[%s] Finished", case_name)

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

    _ensure_input_dir_exists()
    _clear_actual_json_outputs()

    cases = list_cases()

    if not cases:
        logger.warning(
            "No golden dataset cases found in %s.",
            INPUT_DIR,
        )
        return []

    logger.info("Found %d cases.", len(cases))

    outputs: List[Path] = []

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
