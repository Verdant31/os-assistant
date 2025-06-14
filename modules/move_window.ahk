#Requires AutoHotkey v2.0

appExe := A_Args.Length >= 1 ? A_Args[1] : ""
position := A_Args.Length >= 2 ? A_Args[2] : ""
monitorIndex := A_Args.Length >= 3 ? A_Args[3] : 3
windowTitle := A_Args.Length >= 4 ? A_Args[4] : ""

if (appExe = "chrome.exe") {
    if (windowTitle != "") {
        windowPattern := "ahk_exe chrome.exe ahk_class Chrome_WidgetWin_1"
        windows := WinGetList(windowPattern)

        foundHwnd := 0
        loop windows.Length {
            hwnd := windows[A_Index]
            title := WinGetTitle("ahk_id " . hwnd)

            searchTitle := StrLower(windowTitle)
            windowTitleLower := StrLower(title)
            titleMatch := (windowTitle = "") || InStr(windowTitleLower, searchTitle)

            if (titleMatch) {
                foundHwnd := hwnd
                break
            }
        }

        if (!foundHwnd) {
            errorMsg := "Error: Could not find Chrome window"
            if (windowTitle != "") {
                errorMsg .= " containing title: " . windowTitle
            }
            MsgBox errorMsg
            ExitApp
        }
        hwnd := foundHwnd
    } else {
        hwnd := WinExist("ahk_exe chrome.exe ahk_class Chrome_WidgetWin_1")
        if (!hwnd) {
            MsgBox "Error: No Chrome window found. Please specify a profile name or window title if you have multiple Chrome windows."
            ExitApp
        }
    }
} else {
    hwnd := WinExist(appExe)
    if !hwnd {
        MsgBox "Error: Could not find the application window."
        ExitApp
    }
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