document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    const voiceBtn = document.getElementById('voice-btn');
    const voiceStatus = document.getElementById('voice-status');
    const userInput = document.getElementById('user-input');
    const chatForm = document.getElementById('chat-form');
    const chatMessages = document.getElementById('chat-messages');

    // Check if elements exist
    if (!voiceBtn || !voiceStatus || !userInput || !chatForm || !chatMessages) {
        console.error('Required DOM elements not found');
        return;
    }

    // Add voice controls
    const voiceControlsDiv = document.createElement('div');
    voiceControlsDiv.className = 'voice-controls';
    voiceControlsDiv.innerHTML = `
        <div class="voice-mode-toggle">
            <input type="checkbox" id="voice-mode-toggle" />
            <label for="voice-mode-toggle">Continuous Voice Mode</label>
        </div>
        <div class="voice-output-toggle">
            <input type="checkbox" id="voice-output-toggle" checked />
            <label for="voice-output-toggle">Female Voice Output</label>
        </div>
    `;
    document.querySelector('.chat-input-container').appendChild(voiceControlsDiv);

    const voiceModeToggle = document.getElementById('voice-mode-toggle');
    const voiceOutputToggle = document.getElementById('voice-output-toggle');

    // State variables
    let isRecording = false;
    let isSpeaking = false;
    let recognition = null;
    let continuousMode = false;
    let processingInput = false;
    let selectedFemaleVoice = null;
    let micAccessDenied = false;

    // Voice status colors
    const STATUS_COLORS = {
        idle: '#a0a0a0',
        listening: '#4CAF50',
        processing: '#2196F3',
        speaking: '#E91E63',
        error: '#FF5722'
    };

    // Check if browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const synth = window.speechSynthesis;
    
    if (!SpeechRecognition) {
        voiceBtn.disabled = true;
        voiceBtn.classList.add('disabled');
        voiceStatus.textContent = "Voice recognition not supported in this browser";
        voiceStatus.classList.add('error');
        return;
    }

    // Initialize speech synthesis and find a female voice
    function loadVoices() {
        const voices = synth.getVoices();
        console.log(`Found ${voices.length} voices`);
        
        // Try to find a female voice in this priority order:
        // 1. English voices with 'female' in the name
        // 2. English voices with common female names
        // 3. Any English voice as fallback
        
        // First priority: English voices with 'female' in the name
        let voice = voices.find(v => v.name.toLowerCase().includes('female') && v.lang.startsWith('en'));
        
        // Second priority: Common female voice names
        if (!voice) {
            const femaleNames = ['samantha', 'lisa', 'victoria', 'karen', 'moira', 'zira'];
            for (const name of femaleNames) {
                voice = voices.find(v => v.name.toLowerCase().includes(name) && v.lang.startsWith('en'));
                if (voice) break;
            }
        }
        
        // Third priority: Any English voice
        if (!voice) {
            voice = voices.find(v => v.lang.startsWith('en'));
        }
        
        // Last resort: Just use the first voice
        if (!voice && voices.length > 0) {
            voice = voices[0];
        }
        
        if (voice) {
            selectedFemaleVoice = voice;
            console.log(`Selected voice: ${voice.name} (${voice.lang})`);
            
            // Update UI with selected voice
            if (voiceStatus) {
                voiceStatus.textContent = `Voice ready: ${voice.name}`;
            }
        } else {
            console.error("No voices available");
        }
    }

    // Load voices
    if (synth) {
        if (synth.onvoiceschanged !== undefined) {
            synth.onvoiceschanged = loadVoices;
        }
        loadVoices();
    }

    // Initialize speech recognition
    function setupRecognition() {
        recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = true;
        recognition.continuous = false; // Set to false for better control
        
        recognition.onstart = () => {
            console.log('Recognition started');
            isRecording = true;
            voiceBtn.classList.add('recording');
            voiceBtn.innerHTML = '<i class="fas fa-stop"></i>';
            updateVoiceStatus('Listening...', STATUS_COLORS.listening);
        };
        
        recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript)
                .join(' ');
                
            userInput.value = transcript;
            
            if (event.results[0].isFinal) {
                updateVoiceStatus(`Recognized: "${transcript}"`, STATUS_COLORS.processing);
                processingInput = true;
                
                // Submit the form with the recognized text
                setTimeout(() => {
                    chatForm.dispatchEvent(new Event('submit'));
                }, 300);
            }
        };
        
        recognition.onerror = (event) => {
            console.error('Recognition error:', event.error);
            
            if (event.error === 'not-allowed') {
                micAccessDenied = true;
                updateVoiceStatus('Microphone access denied. Please allow microphone access.', STATUS_COLORS.error);
            } else {
                updateVoiceStatus(`Error: ${event.error}. Try again.`, STATUS_COLORS.error);
            }
            
            stopRecognition();
        };
        
        recognition.onend = () => {
            console.log('Recognition ended');
            isRecording = false;
            voiceBtn.classList.remove('recording');
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            
            // If in continuous mode and not processing a response, restart recognition
            if (continuousMode && !processingInput && !isSpeaking && !micAccessDenied) {
                setTimeout(startRecognition, 1000);
            } else if (!processingInput && !continuousMode && !isSpeaking) {
                updateVoiceStatus('Click microphone to speak', STATUS_COLORS.idle);
            }
        };
    }

    // Update voice status with color
    function updateVoiceStatus(message, color) {
        voiceStatus.textContent = message;
        voiceStatus.style.backgroundColor = color ? `${color}20` : ''; // 20 is hex for 12% opacity
        voiceStatus.style.borderColor = color || '';
        
        if (color === STATUS_COLORS.error) {
            voiceStatus.classList.add('error');
        } else {
            voiceStatus.classList.remove('error');
        }
        
        if (color === STATUS_COLORS.listening) {
            voiceStatus.classList.add('active');
        } else {
            voiceStatus.classList.remove('active');
        }
    }

    // Start recording
    function startRecognition() {
        if (isRecording) return;
        
        if (micAccessDenied) {
            updateVoiceStatus('Microphone access denied. Please allow microphone access and reload the page.', STATUS_COLORS.error);
            return;
        }
        
        setupRecognition();
        
        try {
            recognition.start();
        } catch (error) {
            console.error('Failed to start recognition:', error);
            updateVoiceStatus('Failed to start voice recognition. Please try again.', STATUS_COLORS.error);
        }
    }

    // Stop recording
    function stopRecognition() {
        if (!isRecording) return;
        
        try {
            recognition.stop();
        } catch (error) {
            console.error('Error stopping recognition:', error);
        }
        
        isRecording = false;
        voiceBtn.classList.remove('recording');
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    }

    // Stop any ongoing speech
    function stopSpeaking() {
        if (!synth || !isSpeaking) return;
        
        console.log('Stopping speech');
        synth.cancel();
        isSpeaking = false;
        voiceBtn.classList.remove('speaking');
    }

    // Speak text using selected female voice
    function speakMessage(message) {
        if (!synth || !voiceOutputToggle.checked) return;
        
        // Stop any ongoing speech
        stopSpeaking();
        
        // Clean the message if window.cleanThinkingContent is available
        if (window.cleanThinkingContent) {
            message = window.cleanThinkingContent(message);
        }
        
        // Create a new utterance
        const utterance = new SpeechSynthesisUtterance(message);
        
        // Set the female voice if available
        if (selectedFemaleVoice) {
            utterance.voice = selectedFemaleVoice;
        }
        
        // Configure voice parameters for more natural female voice
        utterance.pitch = 1.1;  // Slightly higher pitch for female voice
        utterance.rate = 1.0;   // Normal speed
        utterance.volume = 1.0;
        
        isSpeaking = true;
        voiceBtn.classList.add('speaking');
        updateVoiceStatus('Speaking...', STATUS_COLORS.speaking);
        
        // Listen for when speech ends
        utterance.onend = () => {
            console.log('Speech ended');
            isSpeaking = false;
            voiceBtn.classList.remove('speaking');
            processingInput = false;
            
            // If in continuous mode and not recording, restart recognition
            if (continuousMode && !isRecording) {
                setTimeout(startRecognition, 1000);
            } else {
                updateVoiceStatus('Click microphone to speak', STATUS_COLORS.idle);
            }
        };
        
        // Speech error handling
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            isSpeaking = false;
            voiceBtn.classList.remove('speaking');
            processingInput = false;
        };
        
        // Speak the message
        synth.speak(utterance);
    }

    // Toggle recording when microphone button is clicked
    voiceBtn.addEventListener('click', () => {
        if (voiceBtn.disabled) return;
        
        // If currently speaking, stop the speech
        if (isSpeaking) {
            stopSpeaking();
            updateVoiceStatus('Speech stopped', STATUS_COLORS.idle);
            
            // Start listening for new input after a brief delay
            setTimeout(() => {
                if (!isRecording && !isSpeaking) {
                    startRecognition();
                }
            }, 300);
            return;
        }
        
        // If recording, stop recording
        if (isRecording) {
            stopRecognition();
            
            // Also turn off continuous mode if it's enabled
            if (continuousMode) {
                continuousMode = false;
                voiceModeToggle.checked = false;
            }
        } else {
            // Otherwise, start recording
            startRecognition();
        }
    });

    // Toggle continuous mode
    voiceModeToggle.addEventListener('change', function() {
        continuousMode = this.checked;
        
        if (continuousMode) {
            updateVoiceStatus('Continuous voice mode enabled', STATUS_COLORS.listening);
            
            // Start recognition if not already recording and not synthesizing speech
            if (!isRecording && !isSpeaking) {
                startRecognition();
            }
        } else {
            updateVoiceStatus('Click microphone to speak', STATUS_COLORS.idle);
            
            // Stop recognition if recording
            if (isRecording) {
                stopRecognition();
            }
        }
    });

    // Handle form submission (when user sends a message)
    chatForm.addEventListener('submit', (e) => {
        // Stop recording if we're recording
        if (isRecording) {
            stopRecognition();
        }
        
        // Reset the input field after sending
        setTimeout(() => {
            userInput.value = '';
        }, 100);
    });
    
    // Create observer to watch for new AI responses
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(node => {
                    // Check if this is an assistant message
                    if (node.nodeType === Node.ELEMENT_NODE && 
                        node.classList.contains('message') && 
                        node.classList.contains('assistant')) {
                            
                        // Find the message content
                        const messageContent = node.querySelector('.message-content p');
                        if (messageContent) {
                            // Speak the message
                            speakMessage(messageContent.textContent);
                        }
                    }
                });
            }
        });
    });
    
    // Start observing the chat messages
    observer.observe(chatMessages, { childList: true });
    
    // Make functions available globally
    window.speakMessage = speakMessage;
    window.stopSpeaking = stopSpeaking;
    
    // Set initial status
    updateVoiceStatus('Click microphone to speak', STATUS_COLORS.idle);
    
    // Add visual indicator for speaking state
    const style = document.createElement('style');
    style.textContent = `
        .voice-btn.speaking {
            background-color: #E91E63;
            color: white;
            animation: pulse-speak 1.5s infinite;
        }
        
        @keyframes pulse-speak {
            0% {
                box-shadow: 0 0 0 0 rgba(233, 30, 99, 0.4);
            }
            70% {
                box-shadow: 0 0 0 10px rgba(233, 30, 99, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(233, 30, 99, 0);
            }
        }
    `;
    document.head.appendChild(style);
});