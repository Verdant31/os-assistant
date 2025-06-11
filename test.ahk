#Requires AutoHotkey v2.0

SoundVolumeViewPath := "./SoundVolumeView.exe"

if (A_Args.Length < 1) {
    MsgBox("Uso: script.ahk aumentar|diminuir [action_value] [nome_do_programa]")
    ExitApp
}

Clamp(valor, minimo, maximo) {
    return (valor < minimo) ? minimo : (valor > maximo) ? maximo : valor
}

action := A_Args[1]
action_value := (A_Args.Length >= 2) ? A_Args[2] : 5
program_exe := (A_Args.Length >= 3) ? A_Args[3] : ""
pid := ProcessExist(program_exe)

if !(action = "aumentar" || action = "diminuir") {
    ExitApp
}

if !IsNumber(action_value) || action_value <= 0 || action_value > 100 {
    ExitApp
}

alteracao := (action = "aumentar") ? action_value : -action_value

AjustarVolumeSistema(alteracao) {
    volumeAtual := SoundGetVolume()
    novoVolume := volumeAtual + alteracao
    novoVolume := Clamp(novoVolume, 0, 100)
    SoundSetVolume(novoVolume)
}

AjustarVolumePrograma(alteracao, program_exe) {
    comando := Format('"{1}" /ChangeVolume "{2}" {3}', SoundVolumeViewPath, pid, alteracao)
    RunWait(comando, , "Hide")
}

if (program_exe = "") {
    AjustarVolumeSistema(alteracao)
} else {
    AjustarVolumePrograma(alteracao, program_exe)
}
