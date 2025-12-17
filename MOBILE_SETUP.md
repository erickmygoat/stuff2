# My Son: Mobile Companion Setup

This guide explains how to install the **Sovereign AGI Mobile Interface** on your Samsung S21 Ultra (or any Android device).

## Prerequisites
1. Ensure the Agent is running on your "Mastermind" computer.
2. Ensure the Agent has successfully started **Ngrok** (look for "Global Access URL" in the console logs).

## Installation Steps

1. **Get the URL**
   - Check the console output of your agent for the `Global Access URL`.
   - It will look like: `https://<random-id>.ngrok-free.app`

2. **Open on S21 Ultra**
   - Open Chrome (or Samsung Internet) on your phone.
   - Navigate to: `https://<random-id>.ngrok-free.app/mobile`

3. **Install as App (PWA)**
   - Tap the **three dots** menu in Chrome.
   - Tap **"Add to Home Screen"** or **"Install App"**.
   - Confirm by tapping **"Install"**.

4. **Launch**
   - You will now see the "My Son" icon on your home screen.
   - Tap it to launch the interface in full-screen "App Mode".
   - You can now chat via text or voice directly with your Sovereign Agent.

## Features
- **OLED Dark Mode**: Optimized for battery life.
- **Voice Input**: Tap the microphone icon to speak commands.
- **Haptic Feedback**: Vibration confirmation on message send/receive.
- **Secure Connection**: Uses HTTPS tunneling via Ngrok.
