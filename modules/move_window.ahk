#Requires AutoHotkey v2.0

appExe := A_Args.Length >= 1 ? A_Args[1] : ""
position := A_Args.Length >= 2 ? A_Args[2] : ""
monitorIndex := A_Args.Length >= 3 ? A_Args[3] : 3

hwnd := WinExist(appExe)
if !hwnd {
    MsgBox "Erro: não foi possível encontrar a janela do aplicativo."
    ExitApp
}

MonitorGetWorkArea(monitorIndex, &left, &top, &right, &bottom)
WinActivate(hwnd)
WinRestore(hwnd)

width := right - left
height := bottom - top
isLandscape := (width >= height)

if (isLandscape) {
    if (position = "Maximized") {
        WinMove(left, top, width, height, "ahk_id " hwnd)
    } else if (position = "Top") {
        WinMove(left, top, width, (height) / 2, "ahk_id " hwnd)
    } else if (position = "Bottom") {
        WinMove(left, top + (height) / 2, width, (height) / 2, "ahk_id " hwnd)
    } else if (position = "Left") {
        WinMove(left, top, (width) / 2, height, "ahk_id " hwnd)
    } else if (position = "Right") {
        WinMove(left + (width) / 2, top, (width) / 2, height, "ahk_id " hwnd)
    }
} else {
    sizeA := height // 2
    sizeB := height - sizeA
    if (position = "Maximized") {
        WinMove(left, top, right - left, bottom - top, "ahk_id " hwnd)
    } else if (position = "Top") {
        WinMove(left, top, width, sizeA, "ahk_id " hwnd)
    } else if (position = "Bottom") {
        WinMove(left, top + (bottom - top) / 2, width, sizeB, "ahk_id " hwnd)
    } else if (position = "Left") {
        WinMove(left, top, (right - left) / 2, bottom - top, "ahk_id " hwnd)
    } else if (position = "Right") {
        WinMove(left + (right - left) / 2, top, (right - left) / 2, bottom - top, "ahk_id " hwnd)
    }
}
ExitApp