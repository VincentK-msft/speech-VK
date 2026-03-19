import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import os
import requests
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Azure Speech Synthesizer",
    page_icon="3a4",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #0078D4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .instruction-text {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border-radius: 0.5rem;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    </style>
    """, unsafe_allow_html=True)

# Application title
st.markdown('<div class="main-header">3a4 Azure Speech Synthesizer</div>', unsafe_allow_html=True)
st.markdown('<div class="instruction-text">Convert your text to speech using Azure AI Speech</div>', unsafe_allow_html=True)

# Initialize session state for audio data
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None

# Sidebar for Azure credentials
st.sidebar.header("99e0f Azure Configuration")
st.sidebar.info("Credentials are loaded from the .env file.")

speech_key = os.getenv("SPEECH_KEY", "")
speech_region = os.getenv("SPEECH_REGION", "eastus")

# Display loaded credentials status
if speech_key:
    st.sidebar.success("705 Speech Service credentials loaded")
else:
    st.sidebar.warning("6a0e0f Speech Service credentials not found. Add SPEECH_KEY to .env file")

# Translator credentials
st.sidebar.divider()
st.sidebar.header("310 Azure Translator Configuration")
st.sidebar.info("Credentials are loaded from the .env file.")

translator_key = os.getenv("TRANSLATOR_KEY", "")
translator_region = os.getenv("TRANSLATOR_REGION", "global")

# Display loaded credentials status
if translator_key:
    st.sidebar.success("705 Translator Service credentials loaded")
else:
    st.sidebar.warning("6a0e0f Translator Service credentials not found. Add TRANSLATOR_KEY to .env file")

# Translation function
def translate_text(text, translator_key, translator_region, target_language="en"):
    """Translate text using Azure Translator Service"""
    try:
        # Azure Translator always uses the global endpoint
        # The region parameter is passed in the header, not the URL
        endpoint = "https://api.cognitive.microsofttranslator.com"
        
        path = "/translate"
        # Don't specify source language - let the API auto-detect
        params = {
            "api-version": "3.0",
            "to": target_language
        }
        
        headers = {
            "Ocp-Apim-Subscription-Key": translator_key,
            "Ocp-Apim-Subscription-Region": translator_region,
            "Content-type": "application/json"
        }
        
        body = [{"text": text}]
        
        response = requests.post(
            endpoint + path,
            params=params,
            headers=headers,
            json=body,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result[0]["translations"][0]["text"]
        elif response.status_code == 400:
            error_detail = response.json() if response.text else "Bad request"
            raise Exception(f"Bad request - check text and credentials: {error_detail}")
        else:
            error_detail = response.text if response.text else f"HTTP {response.status_code}"
            raise Exception(f"Translation failed: {error_detail}")
    
    except requests.exceptions.Timeout:
        raise Exception("Translation request timed out. Please try again.")
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")

# Available voices for different languages
VOICES = {
    "English": {
        "en-US-AriaNeural": "Aria (Female, English - US)",
        "en-US-GuyNeural": "Guy (Male, English - US)",
        "en-US-JennyNeural": "Jenny (Female, English - US)",
        "en-US-AmberNeural": "Amber (Female, English - US)",
        "en-US-AshleyNeural": "Ashley (Female, English - US)",
        "en-US-CoraNeural": "Cora (Female, English - US)",
        "en-US-ElizabethNeural": "Elizabeth (Female, English - US)",
        "en-US-MichelleNeural": "Michelle (Female, English - US)",
        "en-GB-LibbyNeural": "Libby (Female, English - UK)",
        "en-GB-MaisieNeural": "Maisie (Female, English - UK)",
        "en-GB-RyanNeural": "Ryan (Male, English - UK)",
    },
    "Spanish": {
        "es-ES-AlvaroNeural": "Álvaro (Male, Spanish - Spain)",
        "es-ES-ElviraNeural": "Elvira (Female, Spanish - Spain)",
        "es-MX-JorgeNeural": "Jorge (Male, Spanish - Mexico)",
        "es-MX-LarissaNeural": "Larissa (Female, Spanish - Mexico)",
    },
    "French": {
        "fr-FR-BenedictNeural": "Bénédict (Male, French - France)",
        "fr-FR-CoralieNeural": "Coralie (Female, French - France)",
        "fr-FR-DeniseNeural": "Denise (Female, French - France)",
        "fr-FR-HenriNeural": "Henri (Male, French - France)",
        "fr-CA-AntoineNeural": "Antoine (Male, French - Canada)",
        "fr-CA-BrynneNeural": "Brynne (Female, French - Canada)",
    },
    "German": {
        "de-DE-BerndNeural": "Bernd (Male, German - Germany)",
        "de-DE-ConradNeural": "Conrad (Male, German - Germany)",
        "de-DE-KatjaNeural": "Katja (Female, German - Germany)",
        "de-AT-JonasNeural": "Jonas (Male, German - Austria)",
        "de-AT-IngridNeural": "Ingrid (Female, German - Austria)",
    },
    "Italian": {
        "it-IT-DiegoNeural": "Diego (Male, Italian)",
        "it-IT-ElsaNeural": "Elsa (Female, Italian)",
        "it-IT-IsabellaNeural": "Isabella (Female, Italian)",
    },
    "Japanese": {
        "ja-JP-KeitaNeural": "Keita (Male, Japanese)",
        "ja-JP-NanamiNeural": "Nanami (Female, Japanese)",
    },
    "Portuguese": {
        "pt-BR-AntonioNeural": "Antonio (Male, Portuguese - Brazil)",
        "pt-BR-FranciscaNeural": "Francisca (Female, Portuguese - Brazil)",
        "pt-PT-DuarteNeural": "Duarte (Male, Portuguese - Portugal)",
        "pt-PT-RaquelNeural": "Raquel (Female, Portuguese - Portugal)",
    },
    "Mandarin Chinese": {
        "zh-CN-XiaoxiaoNeural": "Xiaoxiao (Female, Mandarin)",
        "zh-CN-YunxiNeural": "Yunxi (Male, Mandarin)",
        "zh-CN-YunyeNeural": "Yunyé (Female, Mandarin)",
    },
    "Hindi": {
        "hi-IN-MadhurNeural": "Madhur (Male, Hindi)",
        "hi-IN-SwaraNeural": "Swara (Female, Hindi)",
    },
    "Thai": {
        "th-TH-AcharaNeural": "Achara (Female, Thai)",
        "th-TH-PremwadeeNeural": "Premwadee (Female, Thai)",
    },
}

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("4dd Text Input")
    text_input = st.text_area(
        "Enter text to convert to speech",
        placeholder="Type your message here...",
        height=150,
        help="Enter the text you want to convert to speech. Maximum 1000 characters."
    )

with col2:
    st.subheader("524 Settings")
    
    # Language selection
    selected_language = st.selectbox(
        "Select Language",
        list(VOICES.keys()),
        help="Choose the language for speech synthesis"
    )
    
    # Voice selection
    available_voices = VOICES[selected_language]
    selected_voice = st.selectbox(
        "Select Voice",
        list(available_voices.values()),
        help="Choose the voice for speech synthesis"
    )
    
    # Get the voice name from the selected option
    voice_name = [k for k, v in available_voices.items() if v == selected_voice][0]
    
    # Speech rate adjustment
    speech_rate = st.slider(
        "Speech Rate",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="1.0 is normal speed. Lower values slow down, higher values speed up."
    )

# Validation and synthesis
st.divider()

col_left, col_middle, col_right = st.columns([1, 1, 1])

with col_left:
    synthesize_button = st.button(
        "50a Synthesize Speech",
        type="primary",
        use_container_width=True,
        help="Click to convert text to speech"
    )

with col_middle:
    translate_button = st.button(
        "310 Translate to English",
        type="secondary",
        use_container_width=True,
        help="Translate the text to English"
    )

with col_right:
    if st.session_state.audio_data is not None:
        st.download_button(
            label="197e0f Download Audio",
            data=st.session_state.audio_data,
            file_name="speech_synthesis.wav",
            mime="audio/wav",
            use_container_width=True,
            help="Download the synthesized speech as a WAV file"
        )

# Process synthesis
if synthesize_button:
    # Validation
    if not speech_key or not speech_region:
        st.error("74c Please enter your Azure Speech Service credentials in the sidebar.")
    elif not text_input or text_input.strip() == "":
        st.error("74c Please enter some text to synthesize.")
    elif len(text_input) > 1000:
        st.error("74c Text exceeds 1000 characters. Please shorten your input.")
    else:
        try:
            with st.spinner("504 Synthesizing speech..."):
                # Initialize Speech Configuration
                speech_config = speechsdk.SpeechConfig(
                    subscription=speech_key,
                    region=speech_region
                )
                
                # Set voice
                speech_config.speech_synthesis_voice_name = voice_name
                
                # Set speech rate
                # Speech rate is expressed as a ratio relative to the normal rate
                # We need to send SSML with prosody rate
                
                # Create synthesizer with in-memory audio output
                # (no audio output device needed - we'll capture the bytes)
                synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=speech_config,
                    audio_config=None
                )
                
                # Create SSML with speech rate control
                ssml_text = f"""
                <speak version='1.0' xml:lang='en-US'>
                    <voice name='{voice_name}'>
                        <prosody rate='{speech_rate}'>
                            {text_input}
                        </prosody>
                    </voice>
                </speak>
                """
                
                # Synthesize speech
                speech_synthesis_result = synthesizer.speak_ssml_async(ssml_text).get()
                
                # Check result
                if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    # Get audio data
                    audio_data = speech_synthesis_result.audio_data
                    st.session_state.audio_data = audio_data
                    
                    # Display success message
                    st.markdown(
                        '<div class="success-message">705 Speech synthesis completed successfully!</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Display audio player
                    st.audio(audio_data, format="audio/wav")
                    
                    # Display synthesis info
                    st.info(f"""
                    **Synthesis Details:**
                    - Voice: {selected_voice}
                    - Language: {selected_language}
                    - Speech Rate: {speech_rate}x
                    - Audio Duration: {len(audio_data)} bytes
                    """)
                    
                elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = speech_synthesis_result.cancellation_details
                    error_msg = f"Speech synthesis canceled: {cancellation_details.reason}"
                    
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        error_msg += f"\nError details: {cancellation_details.error_details}"
                    
                    st.markdown(
                        f'<div class="error-message">74c {error_msg}</div>',
                        unsafe_allow_html=True
                    )
        
        except Exception as e:
            st.markdown(
                f'<div class="error-message">74c An error occurred: {str(e)}</div>',
                unsafe_allow_html=True
            )
            st.error(
                "Please check your credentials and try again. "
                "Make sure your API key and region are correct."
            )

# Process translation
if translate_button:
    # Validation
    if not translator_key or not translator_region:
        st.error("74c Please enter your Azure Translator credentials in the sidebar.")
    elif not text_input or text_input.strip() == "":
        st.error("74c Please enter some text to translate.")
    else:
        try:
            with st.spinner("310 Translating text to English..."):
                translated_text = translate_text(
                    text_input.strip(),
                    translator_key,
                    translator_region,
                    target_language="en"
                )
                
                st.markdown(
                    '<div class="success-message">705 Translation completed successfully!</div>',
                    unsafe_allow_html=True
                )
                
                st.subheader("4dd Translated Text")
                st.text_area(
                    "English Translation",
                    value=translated_text,
                    height=100,
                    disabled=True
                )
                
                st.info(f"""
                **Translation Details:**
                - Original Text Length: {len(text_input)} characters
                - Translated Text Length: {len(translated_text)} characters
                """)
        
        except Exception as e:
            st.markdown(
                f'<div class="error-message">74c Translation error: {str(e)}</div>',
                unsafe_allow_html=True
            )
            st.error(
                "Please check your Translator credentials and try again. "
                "Make sure your API key and region are correct."
            )

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
    <p>4a1 Tip: Use environment variables for automatic credential loading.</p>
    <p>510 Your credentials are never stored. They're only used for API calls.</p>
    </div>
    """,
    unsafe_allow_html=True
)