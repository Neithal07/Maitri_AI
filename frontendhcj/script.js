/**
 * MAITRI Dashboard - Core Functionality
 * Mission Autonomous Intelligent Real-Time Interface
 * Version 1.0
 * 
 * Handles:
 * - Real-time clock synchronization
 * - Starfield parallax effects
 * - Chat interactions with AI response simulation
 * - Alert system with stress simulation
 * - Telemetry animations
 * - Edge processing indicators
 */

(function() {
    'use strict';

    // ===== DOM ELEMENTS =====
    const elements = {
        clock: document.getElementById('clock'),
        starLayers: [
            document.getElementById('layer1'),
            document.getElementById('layer2'),
            document.getElementById('layer3'),
            document.getElementById('layer4')
        ],
        chatInput: document.getElementById('chatInput'),
        sendBtn: document.getElementById('sendBtn'),
        chatHistory: document.getElementById('chatHistory'),
        typingIndicator: document.getElementById('typingIndicator'),
        alertPanel: document.getElementById('alertPanel'),
        dashboard: document.querySelector('.dashboard'),
        feedOverlay: document.querySelector('.feed-overlay'),
        confidenceTag: document.querySelector('.confidence-tag')
    };

    // ===== STATE MANAGEMENT =====
    const state = {
        isTyping: false,
        lastMessageTime: Date.now(),
        stressSimulationActive: false,
        telemetryInterval: null
    };

    // ===== INITIALIZATION =====
    function init() {
        initClock();
        initEventListeners();
        initTelemetrySimulation();
        initStressSimulation();
        
        // Start background animations
        console.log('MAITRI Dashboard initialized - Mission ready');
    }

    // ===== REAL-TIME CLOCK (UTC) =====
    function initClock() {
        updateClock();
        setInterval(updateClock, 500);
    }

    function updateClock() {
        if (!elements.clock) return;
        
        const now = new Date();
        const hours = String(now.getUTCHours()).padStart(2, '0');
        const minutes = String(now.getUTCMinutes()).padStart(2, '0');
        const seconds = String(now.getUTCSeconds()).padStart(2, '0');
        elements.clock.textContent = `${hours}:${minutes}:${seconds}`;
    }

    // ===== STARFIELD PARALLAX (3D Depth on Mouse Move) =====
    function initEventListeners() {
        // Mouse move parallax
        document.addEventListener('mousemove', handleMouseMove);
        
        // Chat input interactions
        if (elements.chatInput) {
            elements.chatInput.addEventListener('focus', handleChatFocus);
            elements.chatInput.addEventListener('blur', handleChatBlur);
            elements.chatInput.addEventListener('keypress', handleChatKeypress);
        }
        
        // Send button
        if (elements.sendBtn) {
            elements.sendBtn.addEventListener('click', handleSendMessage);
        }
        
        // Alert panel dismiss
        if (elements.alertPanel) {
            const dismissBtn = elements.alertPanel.querySelector('p:last-child');
            if (dismissBtn) {
                dismissBtn.addEventListener('click', dismissAlert);
            }
        }
    }

    function handleMouseMove(e) {
        if (!elements.starLayers.every(l => l)) return;
        
        // Calculate parallax offset based on mouse position
        const x = (e.clientX / window.innerWidth - 0.5) * 30;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;
        
        // Apply transforms to each layer with different intensities
        if (elements.starLayers[0]) {
            elements.starLayers[0].style.transform = 
                `translateX(${x * 0.2}px) translateY(${y * 0.1}px) translateZ(-200px) scale(1.5)`;
        }
        if (elements.starLayers[1]) {
            elements.starLayers[1].style.transform = 
                `translateX(${x * 0.5}px) translateY(${y * 0.3}px) translateZ(-100px) scale(1.3)`;
        }
        if (elements.starLayers[2]) {
            elements.starLayers[2].style.transform = 
                `translateX(${x * 0.8}px) translateY(${y * 0.5}px) translateZ(0px) scale(1)`;
        }
        if (elements.starLayers[3]) {
            elements.starLayers[3].style.transform = 
                `translateX(${x * 1.2}px) translateY(${y * 0.8}px) translateZ(80px) scale(0.9)`;
        }
    }

    // ===== CHAT INTERACTIONS =====
    function handleChatFocus() {
        // Dim starfield slightly when typing
        elements.starLayers.forEach(layer => {
            if (layer) {
                layer.style.transition = 'opacity 0.3s';
                layer.style.opacity = '0.3';
            }
        });
        
        // Trigger particle reaction (simulated via starfield dim)
        state.isTyping = true;
    }

    function handleChatBlur() {
        // Restore starfield
        elements.starLayers.forEach(layer => {
            if (layer) {
                layer.style.opacity = '';
            }
        });
        state.isTyping = false;
    }

    function handleChatKeypress(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    }

    function handleSendMessage() {
        const input = elements.chatInput;
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        // Clear input
        input.value = '';
        
        // Show typing indicator
        showTypingIndicator(true);
        
        // Simulate AI response after delay
        setTimeout(() => {
            simulateAIResponse(message);
            showTypingIndicator(false);
        }, 1300 + Math.random() * 700); // Variable delay for realism
    }

    function addMessageToChat(sender, text) {
        if (!elements.chatHistory) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'msg-user' : 'msg-maitri';
        
        // Add emotion badge based on content analysis (simulated)
        const badge = document.createElement('span');
        badge.className = 'emotion-badge';
        
        if (sender === 'user') {
            // Simple sentiment simulation
            const sentiment = analyzeSentiment(text);
            badge.textContent = sentiment.icon;
            messageDiv.textContent = text + '  ';
        } else {
            badge.textContent = '🛰️';
            messageDiv.textContent = text + '  ';
        }
        
        messageDiv.appendChild(badge);
        elements.chatHistory.appendChild(messageDiv);
        
        // Scroll to bottom
        elements.chatHistory.scrollTop = elements.chatHistory.scrollHeight;
    }

    function analyzeSentiment(text) {
        // Simple keyword-based sentiment for demo
        const lowerText = text.toLowerCase();
        if (lowerText.includes('stress') || lowerText.includes('anxious') || lowerText.includes('worried')) {
            return { icon: '😰', sentiment: 'stress' };
        } else if (lowerText.includes('good') || lowerText.includes('great') || lowerText.includes('fine')) {
            return { icon: '😊', sentiment: 'positive' };
        } else if (lowerText.includes('?') || lowerText.includes('help')) {
            return { icon: '🤔', sentiment: 'question' };
        }
        return { icon: '😐', sentiment: 'neutral' };
    }

    function showTypingIndicator(show) {
        if (!elements.typingIndicator) return;
        
        elements.typingIndicator.style.opacity = show ? '1' : '0.5';
        
        // Optional: trigger particle reaction
        if (show) {
            // Subtle background reaction
            elements.starLayers.forEach(layer => {
                if (layer) layer.style.filter = 'brightness(1.1)';
            });
        } else {
            elements.starLayers.forEach(layer => {
                if (layer) layer.style.filter = '';
            });
        }
    }

    function simulateAIResponse(userMessage) {
        // Generate contextual responses based on user input
        const lowerMsg = userMessage.toLowerCase();
        let response = '';
        
        if (lowerMsg.includes('stress') || lowerMsg.includes('anxious')) {
            response = 'Detecting elevated stress markers. Recommend deep breathing protocol. I\'m here to help.';
        } else if (lowerMsg.includes('hello') || lowerMsg.includes('hi')) {
            response = 'Hello, crew member. All vital signs nominal. How are you feeling today?';
        } else if (lowerMsg.includes('help') || lowerMsg.includes('support')) {
            response = 'Initiating cognitive support protocol. Edge-AI analysis suggests calm focus.';
        } else if (lowerMsg.includes('thank')) {
            response = 'You\'re welcome. MAITRI is here for your psychological safety.';
        } else if (lowerMsg.includes('status') || lowerMsg.includes('report')) {
            response = 'All systems stable. Stress index: 0.23. Cognitive load: moderate.';
        } else {
            // Default response
            const responses = [
                'Acknowledged. Edge inference suggests nominal cognitive state.',
                'Message received. Running multimodal analysis...',
                'Logging to mission telemetry. Continue.',
                'Processing through neural fusion layers. Please stand by.'
            ];
            response = responses[Math.floor(Math.random() * responses.length)];
        }
        
        addMessageToChat('maitri', response);
    }

    // ===== TELEMETRY SIMULATION =====
    function initTelemetrySimulation() {
        // Update ring percentages and confidence values periodically
        state.telemetryInterval = setInterval(updateTelemetry, 3000);
    }

    function updateTelemetry() {
        // Update confidence tag
        if (elements.confidenceTag) {
            const baseConfidence = 94;
            const variation = Math.floor(Math.random() * 6) - 2; // -2 to +3
            const newConfidence = Math.min(99, Math.max(85, baseConfidence + variation));
            
            // Update emotion based on simulated state
            const emotions = ['calm', 'focused', 'neutral', 'alert'];
            const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
            
            elements.confidenceTag.innerHTML = `CNN ${newConfidence}% · <span style="color:#8A2BE2;">${randomEmotion}</span>`;
        }
        
        // Update ring percentages
        const rings = document.querySelectorAll('.ring-inner');
        if (rings.length >= 4) {
            // Face emotion
            rings[0].textContent = Math.floor(70 + Math.random() * 20) + '%';
            // Voice emotion
            rings[1].textContent = Math.floor(60 + Math.random() * 25) + '%';
            // Text sentiment
            rings[2].textContent = Math.floor(75 + Math.random() * 15) + '%';
            // Unified state
            rings[3].textContent = Math.floor(80 + Math.random() * 10) + '%';
        }
    }

    // ===== STRESS SIMULATION & ALERT SYSTEM =====
    function initStressSimulation() {
        // Trigger first alert after 8 seconds (simulated stress)
        setTimeout(triggerStressAlert, 8000);
        
        // Then cycle every 45 seconds for demo
        setInterval(() => {
            if (!state.stressSimulationActive) {
                triggerStressAlert();
            }
        }, 45000);
    }

    function triggerStressAlert() {
        if (state.stressSimulationActive) return;
        
        state.stressSimulationActive = true;
        
        // Show alert panel
        if (elements.alertPanel) {
            elements.alertPanel.classList.add('active');
        }
        
        // Add ambient red glow to dashboard
        if (elements.dashboard) {
            elements.dashboard.style.boxShadow = 
                '0 40px 100px rgba(255,59,111,0.3), 0 0 0 1px #ff3b6f inset, 0 0 60px #ff3b6f';
        }
        
        // Add stress state to camera bounding box
        if (elements.feedOverlay) {
            elements.feedOverlay.classList.add('stress');
            elements.feedOverlay.style.borderColor = '#ff3b6f';
        }
        
        // Update confidence tag to show stress
        if (elements.confidenceTag) {
            elements.confidenceTag.innerHTML = 'CNN 88% · <span style="color:#ff6f91;">stress detected</span>';
        }
        
        // Auto-dismiss after 12 seconds (simulated intervention)
        setTimeout(dismissAlert, 12000);
    }

    function dismissAlert() {
        if (!state.stressSimulationActive) return;
        
        state.stressSimulationActive = false;
        
        // Hide alert panel
        if (elements.alertPanel) {
            elements.alertPanel.classList.remove('active');
        }
        
        // Restore normal dashboard glow
        if (elements.dashboard) {
            elements.dashboard.style.boxShadow = 
                '0 40px 100px rgba(0,0,0,0.7), 0 0 0 1px rgba(0,247,255,0.1) inset, 0 0 30px rgba(138,43,226,0.3)';
        }
        
        // Remove stress state from bounding box
        if (elements.feedOverlay) {
            elements.feedOverlay.classList.remove('stress');
            elements.feedOverlay.style.borderColor = '#00F7FF';
        }
        
        // Reset confidence tag
        if (elements.confidenceTag) {
            elements.confidenceTag.innerHTML = 'CNN 94% · <span style="color:#8A2BE2;">calm</span>';
        }
    }

    // ===== CLEANUP (for potential future use) =====
    function cleanup() {
        if (state.telemetryInterval) {
            clearInterval(state.telemetryInterval);
        }
    }

    // ===== START THE APPLICATION =====
    document.addEventListener('DOMContentLoaded', init);
    
    // Optional: expose for debugging
    window.maitri = {
        triggerStress: triggerStressAlert,
        dismissAlert: dismissAlert,
        state: state
    };
})();