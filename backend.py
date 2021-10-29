import consts
import global_data
from audio import initialize_audio, initialize_midi_input, midi
from delay import DelayLine
from global_data import midi_state
from helpers import compose_oscillators, get_samples
from patches.patches import available_patches


def main_loop():
    audio_stream = initialize_audio()
    midi_input = initialize_midi_input()

    try:
        while True:
            if midi_state:
                osc = compose_oscillators([i["osc"] for _, i in midi_state.items()])
                b_samples = get_samples(osc)
                audio_stream.write(b_samples)

            if midi_input.poll():
                handle_midi_events(midi_input)

    except KeyboardInterrupt:
        audio_stream.close()


def handle_midi_events(midi_input):
    global current_patch
    for event in midi_input.read(num_events=8):
        (status, note, vel, data), _ = event

        if (
            status == consts.MIDI_NOTE_OFF
            and note in midi_state
            and midi_state[note] != "released"
        ):
            midi_state[note]["key_state"] = "released"

        elif (
            status == consts.MIDI_NOTE_ON
            and midi_state.get(note, {}).get("key_state") != "pressed"
        ):
            freq = midi.midi_to_frequency(note)
            osc = available_patches[global_data.global_sound_mods["current_patch"]](
                freq, (vel / 127)
            )

            if global_data.global_sound_mods["delay"]:
                osc = DelayLine(signal=osc)

            midi_state[note] = {"osc": osc, "key_state": "pressed"}

        elif (
            status == consts.MIDI_CONTROL_CHANGE
            and note == consts.MIDI_PREV_SCENE_CHANNEL
            and vel == 127
        ):
            patch = (global_data.global_sound_mods["current_patch"] - 1) % len(
                available_patches
            )
            global_data.global_sound_mods["current_patch"] = patch
            print(available_patches[patch].name)
        elif (
            status == consts.MIDI_CONTROL_CHANGE
            and note == consts.MIDI_NEXT_SCENE_CHANNEL
            and vel == 127
        ):
            patch = (global_data.global_sound_mods["current_patch"] + 1) % len(
                available_patches
            )
            global_data.global_sound_mods["current_patch"] = patch
            print(available_patches[patch].name)
        elif status == consts.MIDI_CONTROL_CHANGE and note == consts.MIDI_STOP_CHANNEL:
            exit()

        elif status == consts.MIDI_PITCH_WHEEL_CHANGE:
            normalized_val = (vel / 127) - 0.5
            global_data.global_sound_mods["pitch_mod"] = normalized_val

        elif (
            status == consts.MIDI_CONTROL_CHANGE
            and note == consts.MIDI_MOD_WHEEL_CHANGE_CHANNEL
        ):
            normalized_val = vel / 127
            global_data.global_sound_mods["mod_wheel"] = normalized_val

        elif (
            status == consts.MIDI_CONTROL_CHANGE
            and note == consts.MIDI_VOL_CHANGE_CHANNEL
        ):
            normalized_val = vel / 127
            global_data.global_sound_mods["vol"] = normalized_val

        elif (
            status == consts.MIDI_CONTROL_CHANGE
            and note == consts.MIDI_RECORD_CHANNEL
            and vel == 127
        ):
            global_data.global_sound_mods["delay"] = not global_data.global_sound_mods[
                "delay"
            ]


if __name__ == "__main__":

    # Initialize audio
    main_loop()
