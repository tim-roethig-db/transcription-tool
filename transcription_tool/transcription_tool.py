import pandas as pd

from transcription_tool.diarize_speakers import diarize_speakers
from transcription_tool.speech2text import speech2text


def transcribe(
        file_path: str, hf_token: str, language: str = "german", num_speakers: int = None,
        s2t_model: str = "openai/whisper-tiny"
):
    print("Diarizing speakers...")
    diarized_speakers = diarize_speakers(
        file_path,
        hf_token=hf_token,
        num_speakers=num_speakers,
    )

    print("Transcripting audio...")
    transcript = list()
    for i, speaker_section in enumerate(diarized_speakers):
        print(f"Transcripting part {i+1} of {len(diarized_speakers)}")
        text = speech2text(
            speaker_section["audio"],
            model=s2t_model,
            language=language,
        )

        transcript.append(
            [speaker_section["speaker"], speaker_section["time_stamp"], text]
        )

    # Store transcript in pandas Data Frame
    transcript = pd.DataFrame(data=transcript, columns=["speaker", "time_stamp", "text"])

    # save transcript
    print(transcript.to_markdown(index=False))