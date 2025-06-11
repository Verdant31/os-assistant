; open.ahk – Uso: open.ahk <CaminhoOuExe>
#Requires AutoHotkey v2+

if (A_Args.Length = 0) {
    MsgBox("Erro: especifique o caminho ou nome do aplicativo.")
    ExitApp()
}

app := A_Args[1]
if !WinExist(app) {
    Run(app)
}
ExitApp