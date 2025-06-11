; min.ahk – Uso: min.ahk <TítuloJanela>
if (%0% = 0) {
    MsgBox, Erro: especifique o título da janela.
    ExitApp
}
janela = %1%
WinMinimize, %janela%  ; Minimiza a janela especificada:contentReference[oaicite:21]{index=21}
ExitApp