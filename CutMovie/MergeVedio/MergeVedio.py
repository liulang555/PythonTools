# > nul 2>&1 || cd "%~dp0" && python "%~0" && goto :eof
import ffmpegTool
import sys

if __name__ == "__main__":
    # path = r"D:\\媒体库\\输出目录\\#前田陽菜\\[2012]キャットウォーク-ポイズン-67-前田陽菜[CWP-67]"
    ffpeg = ffmpegTool.ffmpegTool()
    ffpeg.MergeMovie(sys.argv[1][:-1])