; split_screen.ahk – Uso: split_screen.ahk <AppEsq> <AppDir>
if %0% < 2 {
    MsgBox, Erro: uso correto: %A_ScriptName% AppEsq AppDir
    ExitApp
}
appEsq = %1%
appDir = %2%

; Obtém coordenadas do monitor principal
SysGet, Mon, Monitor ; parâmetros: MonLeft, MonTop, MonRight, MonBottom
Width := MonRight - MonLeft
Height := MonBottom - MonTop
HalfWidth := Width // 2

; Abre e posiciona app esquerdo
if !WinExist(appEsq) {
    Run, %appEsq%
    WinWait, %appEsq%
}
WinRestore, %appEsq%
WinMove, %appEsq%, , %MonLeft%, %MonTop%, %HalfWidth%, %Height%

; Abre e posiciona app direito
if !WinExist(appDir) {
    Run, %appDir%
    WinWait, %appDir%
}
WinRestore, %appDir%
WinMove, %appDir%, , %MonLeft%+%HalfWidth%, %MonTop%, %HalfWidth%, %Height%
ExitApp