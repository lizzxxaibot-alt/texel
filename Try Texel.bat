@echo off
title Texel - demo
set BLENDER="C:\Users\opule\tools\blender-4.5.9-windows-x64\blender.exe"
if not exist %BLENDER% (
  echo Could not find Blender at %BLENDER%
  echo Edit this .bat and point BLENDER at your blender.exe
  pause
  exit /b 1
)
%BLENDER% --factory-startup --python "%~dp0demo_launch.py"
