import ctypes
import sys

# 가능한 최신 DPI 인식 모드부터 시도하고 순차적으로 폴백
if sys.platform == 'win32':
    try:
        user32 = ctypes.windll.user32
        try:
            # Windows 10 이상 권장: PER_MONITOR_AWARE_V2
            user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
        except Exception:
            try:
                # Windows 8.1 이상: per-monitor DPI awareness
                shcore = ctypes.windll.shcore
                shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
            except Exception:
                try:
                    # 구버전 호환
                    user32.SetProcessDPIAware()
                except Exception:
                    pass
    except Exception:
        # ctypes 호출이 실패하면 무시
        pass

# 이제 pico2d를 import 하고 캔버스를 연다
from pico2d import *

import game_framework
import title_mode as start_mode
# import game_world
# from back_ground import BackGround
# from user_character import UserChar

open_canvas(1920, 1080)
game_framework.run(start_mode)
close_canvas()