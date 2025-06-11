; open.ahk – Uso: open.ahk <CaminhoOuExe>
if (%0% = 0) {
    MsgBox, Erro: especifique o caminho ou nome do aplicativo.
    ExitApp
}

app = %1%               ; Exemplo: "chrome.exe" ou título da janela
if !WinExist(app) {
    Run, %app%          ; Executa o aplicativo
}
ExitApp