# Audio Synthesis with TextToSpeech Class

A powerful text-to-speech system that integrates with Snowflake for generating synthetic audio data. Built on top of the Coqui TTS library, this class provides both simple single-speaker synthesis and complex multi-speaker dialogue generation.

## 🎯 Overview

The `TextToSpeech` class wraps the [Coqui TTS library](https://github.com/coqui-ai/TTS) and provides seamless integration with Snowflake Snowpark for saving audio files directly to stages. It supports both single-speaker and multi-speaker scenarios, making it ideal for creating realistic synthetic audio data for training, testing, and content generation.

## ✨ Key Features

- **Single & Multi-Speaker Support**: Generate speech with one or multiple distinct voices
- **Multilingual Capabilities**: Support for multiple languages depending on the model
- **Snowflake Integration**: Direct saving to Snowflake stages via Snowpark
- **Random Speaker Assignment**: Automatic voice assignment with gender alternation
- **Dialogue Generation**: Create realistic conversations between multiple speakers
- **Robust Error Handling**: Comprehensive validation and informative error messages
- **GPU Acceleration**: Automatic GPU detection and utilization when available

## 🚀 Quick Start

```python
from audio.text_to_speech import TextToSpeech

# Simple single-speaker TTS
tts = TextToSpeech(model="tts_models/en/ljspeech/tacotron2-DDC")
audio = tts.text_to_speech("Hello, this is a test of text to speech.")

# Multi-speaker dialogue
tts_dialogue = TextToSpeech(model="tts_models/multilingual/multi-dataset/xtts_v2")
dialogue = {
    "segments": [
        {"text": "Hello, how are you?", "speaker": "Claribel Dervla"},
        {"text": "I'm doing great!", "speaker": "Andrew Chipper"}
    ]
}
audio = tts_dialogue.create_dialogue(dialogue, language="en")
```

## 📋 Class Methods

### `__init__(model: str)`

Initialize the TextToSpeech model.

**Parameters:**
- `model` (str): The TTS model identifier to load (e.g., "tts_models/en/ljspeech/tacotron2-DDC")

**Features:**
- Automatic GPU/CPU detection
- Model validation and loading
- Sample rate configuration
- Multi-language and multi-speaker capability detection

### `text_to_speech(text, speaker=None, language=None, stage_location=None)`

Convert text to speech audio.

**Parameters:**
- `text` (str): The text to convert to speech
- `speaker` (str, optional): Speaker voice to use (if model supports multiple speakers)
- `language` (str, optional): Language to use (if model supports multiple languages)  
- `stage_location` (str, optional): Snowflake stage location to save the audio file

**Returns:**
- `numpy.ndarray`: Audio data as a numpy array

**Example:**
```python
# Simple usage
audio = tts.text_to_speech("Hello world!")

# With specific speaker and language
audio = tts.text_to_speech(
    text="Bonjour le monde!", 
    speaker="Claribel Dervla", 
    language="fr"
)

# Save directly to Snowflake stage
audio = tts.text_to_speech(
    text="Hello world!", 
    stage_location="@my_stage/audio.wav"
)
```

### `create_dialogue(dialogue, language=None, stage_location=None, random_speaker=False)`

Create a dialogue audio from multiple text segments with different speakers.

**Parameters:**
- `dialogue` (dict): Dictionary containing 'segments' key with list of {'text': str, 'speaker': str} dictionaries
- `language` (str, optional): Language to use for all segments
- `stage_location` (str, optional): Snowflake stage location to save the audio file
- `random_speaker` (bool, optional): Whether to randomly assign voices to speakers

**Returns:**
- `numpy.ndarray`: Combined audio data as a numpy array

**Example:**
```python
# Manual speaker assignment
dialogue_script = {
    "segments": [
        {"text": "Thank you for calling support.", "speaker": "Claribel Dervla"},
        {"text": "Hi, I need help with my order.", "speaker": "Andrew Chipper"},
        {"text": "I'd be happy to help you.", "speaker": "Claribel Dervla"}
    ]
}
audio = tts.create_dialogue(dialogue_script, language="en")

# Random speaker assignment (alternates gender automatically)
audio = tts.create_dialogue(
    dialogue_script, 
    language="en", 
    random_speaker=True
)
```

### `save_to_stage(session, stage_location, audio_bytes)`

Save audio data to a Snowflake stage as a WAV file.

**Parameters:**
- `session`: Active Snowpark session
- `stage_location` (str): Target stage location path
- `audio_bytes` (numpy.ndarray): Audio data to save

### `check_session()`

Verify that an active Snowpark session exists.

**Returns:**
- `snowflake.snowpark.Session`: The active Snowpark session

## 🎭 Available Voices

The system includes predefined voice configurations in `voices.py`. For the `tts_models/multilingual/multi-dataset/xtts_v2` model:

**Female Voices:** Claribel Dervla, Daisy Studious, Gracie Wise, Tammie Ema, Alison Dietlinde, and many more...

**Male Voices:** Ludvig Milivoj, Aaron Dreschner, Ferran Simen, Eugenio Mataracı, Andrew Chipper, and many more...

## 🌍 Supported Models

### Single-Speaker Models
- `tts_models/en/ljspeech/tacotron2-DDC` - Fast English synthesis
- `tts_models/en/ljspeech/glow-tts` - High-quality English synthesis

### Multi-Speaker Models  
- `tts_models/multilingual/multi-dataset/xtts_v2` - Multilingual, multi-speaker model
- `tts_models/en/vctk/vits` - English multi-speaker model

### Full list of Models

<details>
<summary>Click to expand the complete list of available TTS models</summary>

#### Text-to-Speech Models
These models convert written text into natural-sounding speech audio. They vary in quality, language support, and computational requirements. Single-speaker models generate consistent voice output, while multi-speaker models allow voice selection for different characters or scenarios.

| Model | Multispeaker | Multilanguage | Quality | Languages |
|-------|--------------|---------------|---------|-----------|
| `tts_models/multilingual/multi-dataset/xtts_v2` | ✅ | ✅ | High | 17+ languages |
| `tts_models/multilingual/multi-dataset/xtts_v1.1` | ✅ | ✅ | High | 17+ languages |
| `tts_models/multilingual/multi-dataset/your_tts` | ✅ | ✅ | Medium | 100+ languages |
| `tts_models/multilingual/multi-dataset/bark` | ✅ | ✅ | High | 13+ languages |
| `tts_models/bg/cv/vits` | ❌ | ❌ | Medium | Bulgarian |
| `tts_models/cs/cv/vits` | ❌ | ❌ | Medium | Czech |
| `tts_models/da/cv/vits` | ❌ | ❌ | Medium | Danish |
| `tts_models/et/cv/vits` | ❌ | ❌ | Medium | Estonian |
| `tts_models/ga/cv/vits` | ❌ | ❌ | Medium | Irish |
| `tts_models/en/ek1/tacotron2` | ❌ | ❌ | Medium | English |
| `tts_models/en/ljspeech/tacotron2-DDC` | ❌ | ❌ | High | English |
| `tts_models/en/ljspeech/tacotron2-DDC_ph` | ❌ | ❌ | High | English |
| `tts_models/en/ljspeech/glow-tts` | ❌ | ❌ | High | English |
| `tts_models/en/ljspeech/speedy-speech` | ❌ | ❌ | Medium | English |
| `tts_models/en/ljspeech/tacotron2-DCA` | ❌ | ❌ | High | English |
| `tts_models/en/ljspeech/vits` | ❌ | ❌ | High | English |
| `tts_models/en/ljspeech/vits--neon` | ❌ | ❌ | High | English |
| `tts_models/en/ljspeech/fast_pitch` | ❌ | ❌ | Medium | English |
| `tts_models/en/ljspeech/overflow` | ❌ | ❌ | Medium | English |
| `tts_models/en/ljspeech/neural_hmm` | ❌ | ❌ | Medium | English |
| `tts_models/en/vctk/vits` | ✅ | ❌ | High | English |
| `tts_models/en/vctk/fast_pitch` | ✅ | ❌ | Medium | English |
| `tts_models/en/sam/tacotron-DDC` | ❌ | ❌ | Medium | English |
| `tts_models/en/blizzard2013/capacitron-t2-c50` | ❌ | ❌ | Medium | English |
| `tts_models/en/blizzard2013/capacitron-t2-c150_v2` | ❌ | ❌ | Medium | English |
| `tts_models/en/multi-dataset/tortoise-v2` | ✅ | ❌ | High | English |
| `tts_models/en/jenny/jenny` | ❌ | ❌ | High | English |
| `tts_models/es/mai/tacotron2-DDC` | ❌ | ❌ | Medium | Spanish |
| `tts_models/es/css10/vits` | ❌ | ❌ | Medium | Spanish |
| `tts_models/fr/mai/tacotron2-DDC` | ❌ | ❌ | Medium | French |
| `tts_models/fr/css10/vits` | ❌ | ❌ | Medium | French |
| `tts_models/uk/mai/glow-tts` | ❌ | ❌ | Medium | Ukrainian |
| `tts_models/uk/mai/vits` | ❌ | ❌ | Medium | Ukrainian |
| `tts_models/zh-CN/baker/tacotron2-DDC-GST` | ❌ | ❌ | Medium | Chinese (Mandarin) |
| `tts_models/nl/mai/tacotron2-DDC` | ❌ | ❌ | Medium | Dutch |
| `tts_models/nl/css10/vits` | ❌ | ❌ | Medium | Dutch |
| `tts_models/de/thorsten/tacotron2-DCA` | ❌ | ❌ | Medium | German |
| `tts_models/de/thorsten/vits` | ❌ | ❌ | Medium | German |
| `tts_models/de/thorsten/tacotron2-DDC` | ❌ | ❌ | Medium | German |
| `tts_models/de/css10/vits-neon` | ❌ | ❌ | Medium | German |
| `tts_models/ja/kokoro/tacotron2-DDC` | ❌ | ❌ | Medium | Japanese |
| `tts_models/tr/common-voice/glow-tts` | ❌ | ❌ | Medium | Turkish |
| `tts_models/it/mai_female/glow-tts` | ❌ | ❌ | Medium | Italian |
| `tts_models/it/mai_female/vits` | ❌ | ❌ | Medium | Italian |
| `tts_models/it/mai_male/glow-tts` | ❌ | ❌ | Medium | Italian |
| `tts_models/it/mai_male/vits` | ❌ | ❌ | Medium | Italian |
| `tts_models/ewe/openbible/vits` | ❌ | ❌ | Medium | Ewe |
| `tts_models/hau/openbible/vits` | ❌ | ❌ | Medium | Hausa |
| `tts_models/lin/openbible/vits` | ❌ | ❌ | Medium | Lingala |
| `tts_models/tw_akuapem/openbible/vits` | ❌ | ❌ | Medium | Twi (Akuapem) |
| `tts_models/tw_asante/openbible/vits` | ❌ | ❌ | Medium | Twi (Asante) |
| `tts_models/yor/openbible/vits` | ❌ | ❌ | Medium | Yoruba |
| `tts_models/hu/css10/vits` | ❌ | ❌ | Medium | Hungarian |
| `tts_models/el/cv/vits` | ❌ | ❌ | Medium | Greek |
| `tts_models/fi/css10/vits` | ❌ | ❌ | Medium | Finnish |
| `tts_models/hr/cv/vits` | ❌ | ❌ | Medium | Croatian |
| `tts_models/lt/cv/vits` | ❌ | ❌ | Medium | Lithuanian |
| `tts_models/lv/cv/vits` | ❌ | ❌ | Medium | Latvian |
| `tts_models/mt/cv/vits` | ❌ | ❌ | Medium | Maltese |
| `tts_models/pl/mai_female/vits` | ❌ | ❌ | Medium | Polish |
| `tts_models/pt/cv/vits` | ❌ | ❌ | Medium | Portuguese |
| `tts_models/ro/cv/vits` | ❌ | ❌ | Medium | Romanian |
| `tts_models/sk/cv/vits` | ❌ | ❌ | Medium | Slovak |
| `tts_models/sl/cv/vits` | ❌ | ❌ | Medium | Slovenian |
| `tts_models/sv/cv/vits` | ❌ | ❌ | Medium | Swedish |
| `tts_models/ca/custom/vits` | ❌ | ❌ | Medium | Catalan |
| `tts_models/fa/custom/glow-tts` | ❌ | ❌ | Medium | Persian |
| `tts_models/fa/custom/vits-female` | ❌ | ❌ | Medium | Persian |
| `tts_models/bn/custom/vits-male` | ❌ | ❌ | Medium | Bengali |
| `tts_models/bn/custom/vits-female` | ❌ | ❌ | Medium | Bengali |
| `tts_models/be/common-voice/glow-tts` | ❌ | ❌ | Medium | Belarusian |

#### Vocoder Models
*Vocoders convert spectrograms into raw audio waveforms, improving the quality and naturalness of generated speech. These models work alongside TTS models to produce the final audio output.*

| Model | Language/Region | Architecture | Quality |
|-------|----------------|--------------|---------|
| `vocoder_models/universal/libri-tts/wavegrad` | Universal | WaveGrad | High |
| `vocoder_models/universal/libri-tts/fullband-melgan` | Universal | FullBand MelGAN | High |
| `vocoder_models/en/ek1/wavegrad` | English | WaveGrad | High |
| `vocoder_models/en/librispeech100/wavlm-hifigan` | English | WavLM HiFiGAN | High |
| `vocoder_models/en/librispeech100/wavlm-hifigan_prematched` | English | WavLM HiFiGAN (Pre-matched) | High |
| `vocoder_models/en/ljspeech/multiband-melgan` | English | Multiband MelGAN | High |
| `vocoder_models/en/ljspeech/hifigan_v2` | English | HiFiGAN v2 | High |
| `vocoder_models/en/ljspeech/univnet` | English | UnivNet | High |
| `vocoder_models/en/blizzard2013/hifigan_v2` | English | HiFiGAN v2 | High |
| `vocoder_models/en/vctk/hifigan_v2` | English | HiFiGAN v2 | High |
| `vocoder_models/en/sam/hifigan_v2` | English | HiFiGAN v2 | High |
| `vocoder_models/nl/mai/parallel-wavegan` | Dutch | Parallel WaveGAN | Medium |
| `vocoder_models/de/thorsten/wavegrad` | German | WaveGrad | Medium |
| `vocoder_models/de/thorsten/fullband-melgan` | German | FullBand MelGAN | Medium |
| `vocoder_models/de/thorsten/hifigan_v1` | German | HiFiGAN v1 | Medium |
| `vocoder_models/ja/kokoro/hifigan_v1` | Japanese | HiFiGAN v1 | Medium |
| `vocoder_models/uk/mai/multiband-melgan` | Ukrainian | Multiband MelGAN | Medium |
| `vocoder_models/tr/common-voice/hifigan` | Turkish | HiFiGAN | Medium |
| `vocoder_models/be/common-voice/hifigan` | Belarusian | HiFiGAN | Medium |

#### Voice Conversion Models
*Voice conversion models allow changing the speaker identity of existing audio while preserving the linguistic content. These models can transform one person's voice to sound like another person's voice.*

| Model | Language/Region | Architecture | Quality |
|-------|----------------|--------------|---------|
| `voice_conversion_models/multilingual/vctk/freevc24` | Multilingual | FreeVC | High |
| `voice_conversion_models/multilingual/multi-dataset/knnvc` | Multilingual | k-NN VC | High |
| `voice_conversion_models/multilingual/multi-dataset/openvoice_v1` | Multilingual | OpenVoice v1 | High |
| `voice_conversion_models/multilingual/multi-dataset/openvoice_v2` | Multilingual | OpenVoice v2 | High |
</details>

## 💡 Usage Examples

See the complete interactive examples in the **[SYNTHETIC_DATA_GENERATION_AUDIO.ipynb](../SYNTHETIC_DATA_GENERATION_AUDIO.ipynb)** notebook, which demonstrates:

### 1. Simple Text-to-Speech
```python
tts_simple = TextToSpeech(model="tts_models/en/ljspeech/tacotron2-DDC")
audio = tts_simple.text_to_speech("Welcome to our platform!")
```

### 2. Call Center Dialogue Simulation
```python
call_center_dialogue = {
    "segments": [
        {
            "text": "Thank you for calling TechCorp. This is Sarah speaking.",
            "speaker": "Representative"
        },
        {
            "text": "Hi Sarah, I'm having trouble with my order.",
            "speaker": "Customer"
        }
    ]
}

# Generate with random speaker assignment
audio = tts_dialogue.create_dialogue(
    call_center_dialogue, 
    language="en",
    random_speaker=True
)
```

### 3. Snowflake Integration
```python
# Generate and save directly to Snowflake stage
audio = tts.text_to_speech(
    text="This will be saved to Snowflake",
    speaker="Sofia Hellen",
    language="en",
    stage_location="@AUDIO/generated_file.wav"
)
```

## 🔧 Advanced Features

### Random Speaker Assignment
When `random_speaker=True` is used in `create_dialogue()`:
- Automatically assigns voices from the predefined voice pool
- Alternates between male and female voices for different speakers
- Ensures consistent voice mapping for the same character throughout the dialogue

### Error Handling
The class provides comprehensive error handling for:
- Invalid model names
- Unsupported speakers or languages
- Missing Snowflake sessions
- Invalid dialogue formats
- Audio generation failures

### GPU Acceleration
- Automatically detects and uses GPU when available
- Falls back gracefully to CPU processing
- Optimal performance for batch processing

## 📁 File Structure

```
audio/
├── __init__.py
├── text_to_speech.py    # Main TextToSpeech class
├── voices.py           # Voice configurations
└── Readme.md          # This documentation
```

## 🛠️ Dependencies

- `torch` - PyTorch for model execution
- `TTS` - Coqui TTS library
- `soundfile` - Audio file I/O
- `numpy` - Numerical operations
- `snowflake-snowpark-python` - Snowflake integration

## 📝 Requirements

- Python 3.8+
- Active Snowflake session (for stage operations)
- GPU recommended for optimal performance

## 🎯 Use Cases

- **Customer Service Training**: Generate realistic call center scenarios
- **Content Creation**: Automated narration and announcements
- **Data Augmentation**: Create diverse audio datasets for ML training
- **Accessibility**: Convert text content to audio
- **Synthetic Data Generation**: Create large-scale audio datasets

## 📚 Additional Resources

- [Complete Interactive Examples](../SYNTHETIC_DATA_GENERATION_AUDIO.ipynb) - Jupyter notebook with hands-on examples
- [Coqui TTS Documentation](https://tts.readthedocs.io/)
