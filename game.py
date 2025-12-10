import ctypes
import sys

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

from pico2d import *

import game_framework
import title_mode as start_mode

open_canvas(1920, 1080)
game_framework.run(start_mode)
close_canvas()