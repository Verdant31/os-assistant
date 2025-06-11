#Requires AutoHotkey v2.0

MaximizeApp(appExe) {
    pid := ProcessExist(appExe)
    if !pid
        return false
    hwnd := WinExist("ahk_pid " pid)
    if hwnd
        WinMaximize("ahk_id " hwnd)
    return true
}
