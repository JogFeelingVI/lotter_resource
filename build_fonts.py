# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2026-02-05 20:19:39
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2026-02-06 08:20:46
import json
import pathlib
import time
from typing import Dict, Optional


def version():
    """
    version
    Args:
        grid (_type_, optional): _description_. Defaults to "%Y-%m-%d %H:%M:%S".
    """
    grid:str="%Y-%m-%d-%H-%M-%S"
    ts = time.time()
    spans_map = map(int, time.strftime(grid, time.localtime(ts)).split("-"))
    Y,m,d,h,M,s = spans_map
    def match_js(e):
        zgjs = ''
        match e:
            case 0|23:
                zgjs = 'z'
            case 1|2:
                zgjs = 'c'
            case 3|4:
                zgjs = 'y'
            case 5|6:
                zgjs = 'm'
            case 7|8:
                zgjs = 'C'
            case 9|10:
                zgjs = 's'
            case 11|12:
                zgjs = 'w'
            case 13|14:
                zgjs = 'W'
            case 15|16:
                zgjs = 'S'
            case 17|18:
                zgjs = 'Y'
            case 19|20:
                zgjs = 'x'
            case 21|22:
                zgjs = 'h'
            case _:
                zgjs = 'P'
        return zgjs
    
    return f'{m:02}{d:02}{Y}{match_js(h)}'

class FontManager:
    """管理并自动生成 Flet 可用的字体映射表"""
    
    SUPPORTED_EXTENSIONS = {".ttf", ".otf", ".woff", ".woff2"}

    def __init__(self, fonts_subdir: str = "fonts"):
        """
        :param fonts_subdir: 相对于 assets 目录的字体文件夹路径
        """
        self.assets_path = self.__find_assets_dir()
        self.fonts_path = self.assets_path / fonts_subdir
        self.relative_prefix = fonts_subdir
        self.font_map: Dict[str, str] = self._generate_font_map()
        
    def __find_assets_dir(self):
        """尝试自动获取 assets 目录路径"""
        # 在 Flet 安卓环境中，通常脚本运行在根目录，assets 就在同级
        assets_path = pathlib.Path(__file__).parent
        print(f'debug: {assets_path}')
        return assets_path

    def _generate_font_map(self) -> Dict[str, str]:
        fonts = {}
        if not self.fonts_path.exists() or not self.fonts_path.is_dir():
            print(f"Warning: Font directory not found at {self.fonts_path}")
            return fonts

        for file in self.fonts_path.iterdir():
            if file.is_file() and file.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                # 优化 Key 的生成逻辑：
                # 如果是 "Roboto-Bold.ttf"，Key 设为 "Roboto-Bold" 
                # 这样可以精确控制不同字重
                font_family_key = file.stem 
                
                # Flet 需要的是相对于 assets 目录的路径
                # 例如: "fonts/Roboto-Bold.ttf"
                fix_name_net = file.name.replace(" ","%20")
                fonts[font_family_key] = f"/{self.relative_prefix}/{fix_name_net}"
        
        fonts['--version'] = version()
        
        return fonts

    def get_fonts(self):
        return self.font_map

def main():
    print("Build Fonts to json")
    _fm = FontManager()
    print(f'fonts json {_fm.get_fonts()}')
    with open('fonts.json', 'w', encoding='utf-8') as w:
        json.dump(_fm.get_fonts(), w, indent=4, ensure_ascii=False)
    

if __name__ == "__main__":
    main()
