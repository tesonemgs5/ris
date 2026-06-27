import { useState, useRef, useCallback } from 'react'

export function useVoice({ onResult, onError } = {}) {
  const [listening, setListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const recognitionRef = useRef(null)

  const start = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) {
      onError?.('Riconoscimento vocale non supportato su questo browser.')
      return
    }

    const recognition = new SpeechRecognition()
    recognition.lang = 'it-IT'
    recognition.continuous = true
    recognition.interimResults = true
    recognition.maxAlternatives = 1

    recognition.onstart = () => setListening(true)

    recognition.onresult = (e) => {
      let interim = ''
      let final = ''
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const t = e.results[i][0].transcript
        if (e.results[i].isFinal) final += t
        else interim += t
      }
      setTranscript(final || interim)
      if (final) onResult?.(final)
    }

    recognition.onerror = (e) => {
      setListening(false)
      onError?.(e.error)
    }

    recognition.onend = () => setListening(false)

    recognition.start()
    recognitionRef.current = recognition
  }, [onResult, onError])

  const stop = useCallback(() => {
    recognitionRef.current?.stop()
    setListening(false)
  }, [])

  const toggle = useCallback(() => {
    if (listening) stop()
    else start()
  }, [listening, start, stop])

  return { listening, transcript, start, stop, toggle }
}
