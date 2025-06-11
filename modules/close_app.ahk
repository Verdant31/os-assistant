#Requires AutoHotkey v2.0

if (A_Args.Length = 0) {
    MsgBox("Erro: especifique o caminho ou nome do aplicativo.")
    ExitApp
}

windowName := A_Args[1]

WinClose windowName

ExitApp