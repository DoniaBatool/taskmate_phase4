# 🎤🔊 Voice Features Documentation

## Overview

Todo Chatbot Phase 3 ab **Speech-to-Text (STT)** aur **Text-to-Speech (TTS)** features ke saath equipped hai! Aap apni tasks ko voice commands se manage kar sakte hain aur chatbot ke responses ko sun sakte hain.

## ✨ Features

### 1. 🎤 Speech-to-Text (STT)
- **Technology**: OpenAI Whisper API
- **Supported Formats**: MP3, MP4, WAV, WebM, OGG
- **Languages**: 100+ languages including English, Urdu, Arabic, etc.
- **Accuracy**: Industry-leading accuracy

### 2. 🔊 Text-to-Speech (TTS)
- **Technology**: OpenAI TTS API
- **Model**: TTS-1 (High quality, low latency)
- **Voices Available**: 6 voices (nova, alloy, echo, fable, onyx, shimmer)
- **Speed Control**: 0.25x to 4.0x speed
- **Default Voice**: Nova (female, energetic)

---

## 🚀 How to Use

### Voice Input (Speech-to-Text)

#### Method 1: Hold-to-Record (Recommended)
1. Chat page par **purple microphone button** (🎤) ko **hold** karein
2. Apna message bolein
3. Button **release** karein
4. Audio automatically transcribe ho jayega
5. Transcribed text input field mein aa jayega
6. Send button dabayein ya edit karein

#### Method 2: Touch (Mobile)
1. Microphone button ko **touch and hold** karein
2. Message bolein
3. Button release karein
4. Transcribed text aa jayega

**Visual Indicators:**
- 🟣 **Purple**: Ready to record
- 🔴 **Red (pulsing)**: Recording in progress
- 🔵 **Blue (spinning)**: Transcribing audio
- ⚪ **Red dot**: Recording indicator

**Example Commands:**
```
"Add task to buy groceries tomorrow"
"Show my tasks"
"Mark milk task as complete"
"Delete buy books task"
"Update shopping list to high priority"
```

---

### Voice Output (Text-to-Speech)

#### How to Listen to Responses:
1. Chatbot ka response aane ke baad
2. Message ke right side mein **speaker icon** (🔊) dikhega
3. Icon par click karein
4. Audio play hoga

**Visual Indicators:**
- 🔊 **Gray speaker**: Ready to play
- 🔵 **Blue (pulsing)**: Playing audio
- 🔄 **Spinning**: Loading audio

**Controls:**
- **Click once**: Play audio
- **Click again**: Stop playback
- **Automatic**: Audio ends naturally after playing

---

## 🎯 Technical Details

### Backend API Endpoints

#### 1. Speech-to-Text
```http
POST /api/voice/transcribe
Authorization: Bearer {token}
Content-Type: multipart/form-data

Body:
  audio: <audio file>

Response:
{
  "text": "Add task to buy groceries",
  "language": "en",
  "duration": 3.5
}
```

#### 2. Text-to-Speech
```http
POST /api/voice/text-to-speech
Authorization: Bearer {token}
Content-Type: application/json

Body:
{
  "text": "Task added successfully!",
  "voice": "nova",
  "speed": 1.0
}

Response: audio/mpeg (MP3 file)
```

#### 3. List Available Voices
```http
GET /api/voice/voices
Authorization: Bearer {token}

Response:
{
  "voices": [
    {
      "id": "nova",
      "name": "Nova",
      "description": "Female voice, energetic (default)"
    },
    ...
  ]
}
```

---

### Frontend Components

#### 1. VoiceRecorder Component
**Location**: `frontend/components/VoiceRecorder.tsx`

**Features:**
- MediaRecorder API for audio capture
- WebM format with Opus codec
- Real-time recording indicator
- Error handling and user feedback
- Touch and mouse support
- Automatic cleanup

**Props:**
```typescript
interface VoiceRecorderProps {
  onTranscription: (text: string) => void;
  disabled?: boolean;
}
```

#### 2. TextToSpeech Component
**Location**: `frontend/components/TextToSpeech.tsx`

**Features:**
- Audio playback control
- Loading and playing states
- Error handling
- Audio cleanup on unmount
- Pause/resume functionality

**Props:**
```typescript
interface TextToSpeechProps {
  text: string;
  voice?: string;        // Default: "nova"
  speed?: number;        // Default: 1.0 (range: 0.25 - 4.0)
}
```

---

## 🔧 Configuration

### Environment Variables

#### Backend
```bash
# .env
OPENAI_API_KEY=sk-...
```

#### Frontend
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Supported Audio Formats

**Input (STT):**
- MP3 (audio/mpeg)
- MP4 (audio/mp4)
- WAV (audio/wav)
- WebM (audio/webm)
- OGG (audio/ogg)

**Output (TTS):**
- MP3 (audio/mpeg)

---

## 🎨 Available TTS Voices

| Voice | Type | Description | Best For |
|-------|------|-------------|----------|
| **Nova** (Default) | Female | Energetic, clear | General use, friendly tone |
| **Alloy** | Neutral | Balanced, professional | Business, formal |
| **Echo** | Male | Warm, conversational | Friendly, casual |
| **Fable** | British | Expressive, accent | Storytelling, narration |
| **Onyx** | Male | Deep, authoritative | Serious, professional |
| **Shimmer** | Female | Soft, gentle | Calm, soothing |

---

## 📱 Browser Compatibility

### Speech-to-Text (Microphone Access):
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari (iOS 11+)
- ✅ Mobile browsers with HTTPS

### Text-to-Speech (Audio Playback):
- ✅ All modern browsers
- ✅ Mobile browsers
- ✅ Desktop browsers

**Requirements:**
- HTTPS connection (required for microphone access)
- Microphone permission granted
- Stable internet connection

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch" error

**Solutions:**
1. Ensure backend server is running on port 8000
2. Check that CORS is properly configured in backend/.env
3. Verify frontend proxy is working (/api/proxy)
4. Clear browser cache and reload page

### Issue: Microphone not working

**Solutions:**
1. Check browser permissions (Settings → Privacy → Microphone)
2. Ensure HTTPS is enabled
3. Try different browser (Chrome recommended)
4. Check if another app is using microphone

### Issue: Audio not playing

**Solutions:**
1. Check browser audio settings
2. Ensure volume is not muted
3. Try clicking speaker icon again
4. Check network connection

### Issue: Transcription inaccurate

**Solutions:**
1. Speak clearly and slowly
2. Reduce background noise
3. Use a better microphone
4. Speak closer to mic
5. Try shorter phrases

### Issue: "Permission denied" error

**Solutions:**
1. Grant microphone permission in browser
2. Reload the page
3. Check if HTTPS is enabled
4. Clear browser cache

---

## 🔒 Security & Privacy

### Data Handling:
- ✅ Audio sent to OpenAI via HTTPS
- ✅ No audio stored on server
- ✅ Transcriptions not logged
- ✅ JWT authentication required
- ✅ User isolation enforced

### OpenAI Privacy:
- Audio processed by OpenAI API
- Not used for model training (default)
- Deleted after processing
- See: [OpenAI Privacy Policy](https://openai.com/privacy)

---

## 💡 Usage Tips

### For Best Results:

**Speech-to-Text:**
1. 🎯 Speak clearly and at normal pace
2. 🔇 Minimize background noise
3. 📱 Hold device steady
4. 🗣️ Speak directly into mic
5. ⏱️ Keep messages under 30 seconds
6. 🌐 Use good internet connection

**Text-to-Speech:**
1. 🔊 Check audio before starting
2. 🎧 Use headphones for better quality
3. ⚡ Adjust speed if needed (future feature)
4. 🔄 Replay if needed
5. 📱 Ensure device volume is up

---

## 🎓 Examples

### Example 1: Add Task with Voice
```
1. Hold microphone button
2. Say: "Add task to call dentist tomorrow at 3pm with high priority"
3. Release button
4. Edit if needed
5. Send
6. Listen to confirmation by clicking speaker icon
```

### Example 2: Mark Task Complete
```
1. Hold mic
2. Say: "Mark dentist task as complete"
3. Release
4. Send
5. Listen to "Task marked as complete!" response
```

### Example 3: List Tasks
```
1. Hold mic
2. Say: "Show my tasks"
3. Release
4. Send
5. Listen to task list being read aloud
```

---

## 📊 Performance

### Speech-to-Text:
- **Latency**: 1-3 seconds (depends on audio length)
- **Accuracy**: 95%+ for clear audio
- **Max Duration**: 25MB file size limit
- **Supported Languages**: 100+

### Text-to-Speech:
- **Latency**: 500ms - 2 seconds
- **Quality**: 192 kbps MP3
- **Max Length**: 4096 characters
- **Voice Selection**: 6 voices

---

## 🚀 Future Enhancements

### Planned Features:
- [ ] Voice settings page (select preferred voice)
- [ ] Speed control for TTS (0.25x - 4.0x)
- [ ] Voice activity detection (auto-start/stop)
- [ ] Multi-language support in UI
- [ ] Offline voice recognition fallback
- [ ] Voice shortcuts/commands
- [ ] Conversation mode (continuous listening)
- [ ] Audio waveform visualization

---

## 📞 Support

### Issues?
- Check troubleshooting section above
- Verify browser compatibility
- Test with different browser
- Check microphone hardware

### Need Help?
- Open GitHub issue
- Check backend logs: `tail -f backend/logs/app.log`
- Check browser console for errors (F12)

---

## 🎉 Congratulations!

Aap ab apni tasks ko voice commands se manage kar sakte hain!

**Quick Start:**
1. 🎤 Hold mic button
2. 🗣️ Speak your command
3. ↗️ Release and send
4. 🔊 Listen to response

**Happy voice chatting! 🚀✨**
