# 3a4 Azure Speech Synthesizer - Streamlit App

A modern, user-friendly Streamlit application that converts text to speech using Azure AI Speech Service with multiple language and voice options.

## Features

728 **Key Features:**
- 4dd Text-to-speech conversion using Azure AI Speech SDK
- 30d Support for 8+ languages (English, Spanish, French, German, Italian, Japanese, Portuguese, Mandarin Chinese)
- 524 Multiple voice options per language (Male/Female voices)
- 39ae0f Adjustable speech rate (0.5x to 2.0x speed)
- 50a Real-time audio playback
- 197e0f Download synthesized speech as WAV files
- 510 Secure credential handling
- 3a8 Beautiful, modern UI with Streamlit

## Prerequisites

Before you begin, make sure you have:
- Python 3.8 or higher
- An Azure account with an active subscription
- Azure Speech Service resource created

## Setup Instructions

### 1. Clone or Download the Project

```bash
cd /path/to/your/project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Azure Speech Service Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource"
3. Search for "Speech" and select "Speech service"
4. Fill in the required details:
   - **Resource Group**: Create new or select existing
   - **Region**: Choose a region (e.g., eastus, westus)
   - **Name**: Give your resource a name
   - **Pricing Tier**: Select F0 (free) or S0 (standard)
5. Click "Review + Create" and then "Create"

### 4. Get Your Credentials

1. Once your Speech Service is created, go to the resource
2. Click "Keys and Endpoint" in the left sidebar
3. Copy:
   - **Key 1** (or Key 2) - This is your `SPEECH_KEY`
   - **Location/Region** - This is your `SPEECH_REGION`

### 5. Configure Environment Variables

**Option A: Using .env file (Recommended)**

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   SPEECH_KEY=your-actual-api-key-here
   SPEECH_REGION=eastus
   ```

**Option B: Enter credentials in the app**

You can also enter your credentials directly in the Streamlit app's sidebar when you run it.

### 6. Run the Application

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Usage

1. **Configure Azure (Optional)**
   - Enter your Speech API Key and Region in the sidebar
   - If you've set up `.env`, these will auto-populate

2. **Select Language and Voice**
   - Choose your desired language from the "Select Language" dropdown
   - Choose a voice from the "Select Voice" dropdown
   - All voices are clearly labeled with gender and language variant

3. **Adjust Settings**
   - Use the "Speech Rate" slider to adjust speaking speed (0.5x = half speed, 2.0x = double speed)

4. **Enter Your Text**
   - Type or paste the text you want to convert to speech
   - Maximum 1000 characters

5. **Synthesize**
   - Click the "50a Synthesize Speech" button
   - Wait for the synthesis to complete
   - Listen to the audio in the player

6. **Download (Optional)**
   - Click "197e0f Download Audio" to save the audio as a WAV file

## Available Voices

### English
- **US Voices**: Aria, Guy, Jenny, Amber, Ashley, Cora, Elizabeth, Michelle (Female/Male)
- **UK Voices**: Libby, Maisie, Ryan (Female/Male)

### Spanish
- **Spain**: Álvaro, Elvira
- **Mexico**: Jorge, Larissa

### French
- **France**: Bénédict, Coralie, Denise, Henri
- **Canada**: Antoine, Brynne

### German
- **Germany**: Bernd, Conrad, Katja
- **Austria**: Jonas, Ingrid

### Italian
- Diego, Elsa, Isabella

### Japanese
- Keita, Nanami

### Portuguese
- **Brazil**: Antonio, Francisca
- **Portugal**: Duarte, Raquel

### Mandarin Chinese
- Xiaoxiao, Yunxi, Yunyé

## Troubleshooting

### "Please enter your Azure Speech Service credentials"
- Make sure you've entered both `SPEECH_KEY` and `SPEECH_REGION`
- Check that your credentials are correct
- Verify your resource exists in Azure Portal

### "Speech synthesis canceled: Error"
- Common causes:
  - Invalid API key
  - Wrong region
  - API quota exceeded
  - Rate limiting (too many requests)
- Solution: Verify your credentials and check your Azure resource status

### "Text exceeds 1000 characters"
- Shorten your text or split it into multiple requests

### Audio not playing in browser
- Try downloading the file instead
- Check your browser's audio permissions
- Try a different browser

## Security Best Practices

512 **Important Security Notes:**
- Never commit `.env` file with real credentials to version control
- Use `.gitignore` to exclude `.env` file
- Consider using Azure Managed Identity in production
- Rotate API keys regularly
- Monitor API usage in Azure Portal

## File Structure

```
.
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
└── README.md              # This file
```

## API Rate Limits

The free tier (F0) has the following limits:
- Requests: 20 requests per minute
- Duration: Unlimited

The standard tier (S0) has higher limits. For details, check [Azure Speech Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/)

## Advanced Configuration

### Custom Endpoints

If you have a custom endpoint, modify the `SpeechConfig` in `app.py`:

```python
speech_config = speechsdk.SpeechConfig(
    endpoint="https://your-custom-endpoint.api.cognitive.microsoft.com/",
    subscription=speech_key
)
```

### Changing Audio Output

To save to file instead of memory, modify the audio configuration:

```python
audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
```

## Supported Languages (SSML)

The app uses SSML (Speech Synthesis Markup Language) for advanced control. Supported languages include:
- Arabic, Chinese, Danish, Dutch, English, Finnish, French, German, Hindi, Hungarian, Indonesian, Italian, Japanese, Korean, Norwegian, Polish, Portuguese, Russian, Spanish, Swedish, Thai, Turkish, and more.

## Resources

- [Azure Speech Service Documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)
- [Speech Synthesis API Reference](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Speech SDK](https://github.com/Azure-Samples/cognitive-services-speech-sdk)

## Contributing

Feel free to fork and submit pull requests to improve this application!

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Support

For issues with:
- **Azure Speech Service**: Check [Azure Documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)
- **Streamlit**: Check [Streamlit Documentation](https://docs.streamlit.io/)
- **This App**: Review the troubleshooting section above

## Version History

### v1.0.0 (2024)
- Initial release
- Multiple language support
- Voice selection
- Speech rate adjustment
- Audio download functionality

---

**Made with 64e0f using Streamlit and Azure AI Speech Services**