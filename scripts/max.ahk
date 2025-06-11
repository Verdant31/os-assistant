; max.ahk – Uso: max.ahk <TítuloJanela>
if (%0% = 0)  {
    MsgBox, Erro: especifique o título da janela.
    ExitApp
}
janela = %1%
WinMaximize, %janela%  ; Maximiza a janela especificada:contentReference[oaicite:20]{index=20}
ExitApp