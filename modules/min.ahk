#Requires AutoHotkey v2.0
MinimizeApp(appExe) {
    pid := ProcessExist(appExe)
    if !pid
        return false
    hwnd := WinExist("ahk_pid " pid)
    if hwnd
        WinMinimize("ahk_id " hwnd)
    return true
}
