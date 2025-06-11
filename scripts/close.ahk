; close.ahk – Uso: close.ahk <TítuloJanela>
if (%0% = 0)  {
    MsgBox, Erro: especifique o título da janela a fechar.
    ExitApp
}
janela = %1%
if WinExist(janela) {
    WinClose, %janela%  ; Envia WM_CLOSE para a janela:contentReference[oaicite:26]{index=26}
}

ExitApp