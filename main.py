"""Mini NPU Simulator - 실행 파일

사용법: python3 main.py
  1. 사용자 입력 (3x3)
  2. data.json 분석
  0. 종료

data.json 위치: main.py와 같은 폴더 (환경 변수 NPU_DATA_PATH로 바꿀 수 있음)
"""

import os
import sys

from app import modes
from app.console import ask

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.environ.get("NPU_DATA_PATH", os.path.join(ROOT, "data.json"))

MENU = [
    ("1", "사용자 입력 (3x3)", lambda: modes.run_user_mode()),
    ("2", "data.json 분석", lambda: modes.run_json_mode(DATA_PATH)),
    ("0", "종료", None),
]


def main():
    print("=== Mini NPU Simulator ===")
    actions = {key: action for key, _, action in MENU}
    while True:
        print()
        print("[모드 선택]")
        for key, label, _ in MENU:
            print("{}. {}".format(key, label))
        choice = ask("선택: ").strip()
        if choice not in actions:
            print("⚠ 메뉴에 있는 번호({})를 입력하세요.".format(", ".join(k for k, _, _ in MENU)))
            continue
        if actions[choice] is None:
            print("프로그램을 종료합니다.")
            return 0
        actions[choice]()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 또는 입력이 끝남(Ctrl+D, 파이프 입력 끝) → 오류 화면 없이 종료
        print("\n입력이 중단되어 프로그램을 종료합니다.")
        sys.exit(0)
