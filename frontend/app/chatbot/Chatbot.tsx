
'use client' 

import React, { useState, useRef, useEffect } from 'react'
import { Send } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import dynamic from 'next/dynamic'
import { motion, AnimatePresence } from 'framer-motion'
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw'

const ReactMarkdown = dynamic(() => import('react-markdown'), {
  ssr: false,
  loading: () => <p>Loading...</p>,
})

type Message = {
  text: string
  isUser: boolean
}

async function fetchStream(message: string,fileId : string |null, onChunk: (chunk: string) => void) {
  try {
    const response = await fetch(`http://localhost:5000/ex?file_id=${fileId}`, {
        method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    })

    if (!response.ok) {
      throw new Error('API 응답이 올바르지 않습니다.')
    }

    const reader = response.body?.getReader()
    const decoder = new TextDecoder('utf-8')
    let done = false
    let buffer = ''
    let accumulatedText = ''
    let v4Text = ''

    while (!done && reader) {
      const { value, done: streamDone } = await reader.read()
      done = streamDone
      
      if (value) {
        buffer += decoder.decode(value, { stream: true })
        const parts = buffer.split('\n\n')
        buffer = parts.pop() || ''

        for (const part of parts) {
          if (part.startsWith('data: ')) {
            const rawData = part.replace(/^data: /, '')
            if (rawData.trim() === '[DONE]') {
              done = true
              break
            } else {
              // 토큰 분석
              const data = rawData.replace(/^"/, '').replace(/"$/, '') // 따옴표 제거
              const tokenLength = data.length
              const leadingSpaces = data.length - data.trimLeft().length
              const trailingSpaces = data.length - data.trimRight().length
              const totalSpaces = (data.match(/\s/g) || []).length
              
              console.log(`
[토큰 상세 분석]
원본 토큰: "${rawData}"
처리된 토큰: "${data}"
토큰 길이: ${tokenLength}
앞쪽 공백: ${leadingSpaces}개
뒤쪽 공백: ${trailingSpaces}개
전체 공백: ${totalSpaces}개
------------------------`)
              
              // 토큰 처리
              if (data === '\\n' || data === '\n') {
                // 줄바꿈 처리 (이스케이프된 경우와 일반 줄바꿈 모두 처리)
                accumulatedText += '\n'
                v4Text += '\n'
                console.log('[처리] 줄바꿈 추가')
              } else if (data.includes('\\n')) {
                // 텍스트 중간에 줄바꿈이 있는 경우
                const processedData = data.replace(/\\n/g, '\n')
                const parts = processedData.split('\n')
                for (let i = 0; i < parts.length; i++) {
                  if (i > 0) {
                    accumulatedText += '\n'
                    v4Text += '\n'
                  }
                  if (parts[i]) {
                    const leadingSpaces = parts[i].length - parts[i].trimLeft().length
                    if (leadingSpaces === 2) {
                      accumulatedText += parts[i]
                      v4Text += ' ' + parts[i].trimLeft()
                    } else if (leadingSpaces === 1) {
                      accumulatedText += parts[i].trimLeft()
                      v4Text += parts[i].trimLeft()
                    } else {
                      accumulatedText += parts[i]
                      v4Text += parts[i]
                    }
                  }
                }
                console.log('[처리] 텍스트 내 줄바꿈 변환')
              } else {
                // v3 로직 (기존)
                const v3ProcessedData = leadingSpaces === 2 ? data : data.trimLeft()
                accumulatedText += v3ProcessedData
                console.log(`[v3] 처리된 데이터: "${v3ProcessedData}"`)
                
                // v4 로직 (새로운 방식)
                let v4ProcessedData = ''
                if (leadingSpaces === 1) {
                  v4ProcessedData = data.trimLeft()
                  console.log(`[v4] 공백(1개) 제거: "${data}" -> "${v4ProcessedData}"`)
                } else if (leadingSpaces === 2) {
                  v4ProcessedData = ' ' + data.trimLeft()
                  console.log(`[v4] 공백(2개) -> 공백(1개): "${data}" -> "${v4ProcessedData}"`)
                } else {
                  v4ProcessedData = data
                  console.log(`[v4] 공백 유지: "${data}"`)
                }
                
                v4Text += v4ProcessedData
              }
              
              console.log(`[v3] 누적 텍스트: "${accumulatedText}"`)
              console.log(`[v4] 누적 텍스트: "${v4Text}"`)
              console.log('------------------------')
              
              // 실제 출력은 v3 방식 사용
              onChunk(accumulatedText)
            }
          }
        }
      }
    }
  } catch (error) {
    console.error('스트리밍 중 오류 발생:', error)
    onChunk('오류가 발생했습니다.')
  }
}

const TypingIndicator = () => (
  <div className="typing-indicator flex items-center space-x-1">
    <span className="dot" />
    <span className="dot" />
    <span className="dot" />
    <style jsx>{`
      .dot {
        width: 8px;
        height: 8px;
        background-color: #bbb;
        border-radius: 50%;
        animation: blink 1.4s infinite both;
      }
      .dot:nth-child(2) {
        animation-delay: 0.2s;
      }
      .dot:nth-child(3) {
        animation-delay: 0.4s;
      }
      @keyframes blink {
        0% {
          opacity: 0.2;
        }
        20% {
          opacity: 1;
        }
        100% {
          opacity: 0.2;
        }
      }
    `}</style>
  </div>
)

const SkeletonMessage = () => (
  <div className="flex mb-4">
    <div className="animate-pulse flex space-x-4">
      <div className="rounded-full bg-gray-300 h-10 w-10" />
      <div className="flex-1 space-y-4 py-1">
        <div className="h-4 bg-gray-300 rounded w-3/4" />
        <div className="space-y-2">
          <div className="h-4 bg-gray-300 rounded" />
          <div className="h-4 bg-gray-300 rounded w-5/6" />
        </div>
      </div>
    </div>
  </div>
)
interface ChatbotProps {
    fileId: string | null;
  }
export default function Chatbot({ fileId }: ChatbotProps) {

  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const isRequesting = useRef(false)

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [messages])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() === '' || isLoading || isRequesting.current) return

    const userInput = input.trim()
    const userMessage: Message = { text: userInput, isUser: true }

    setMessages((prev) => [...prev, userMessage, { text: '', isUser: false }])
    setInput('')
    setIsLoading(true)
    setIsTyping(true)
    isRequesting.current = true

    try {
        
      await fetchStream(userInput, fileId,(chunk) => {
        setMessages((prev) => {
          const lastIndex = prev.length - 1
          if (lastIndex >= 0 && !prev[lastIndex].isUser) {
            const updatedMessage = { ...prev[lastIndex], text: chunk }
            const newMessages = [...prev]
            newMessages[lastIndex] = updatedMessage
            return newMessages
          } else {
            return [...prev, { text: chunk, isUser: false }]
          }
        })
      })
    } catch (error) {
      console.error('메시지 전송 중 오류 발생:', error)
      setMessages((prev) => [
        ...prev,
        { text: '죄송합니다. 오류가 발생했습니다.', isUser: false },
      ])
    } finally {
      setIsLoading(false)
      setIsTyping(false)
      isRequesting.current = false
    }
  }

  return (
    <div className="w-full h-[calc(100vh-2rem)] border rounded-lg overflow-hidden flex flex-col dark:bg-gray-800 dark:text-white">
      <div className="bg-blue-500 p-4">
        <h2 className="text-2xl font-bold text-primary-foreground">LH 임대 주택 챗봇</h2>
      </div>

      <ScrollArea className="flex-grow p-4 overflow-y-auto" ref={scrollAreaRef}>
        <AnimatePresence>
          {messages.map((message, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
              className={`mb-4 flex ${
                message.isUser ? 'justify-end' : 'justify-start'
              }`}
            >
              {!message.isUser && (
                <span className="mr-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-6 w-6 text-secondary-foreground"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M8 10h.01M12 10h.01M16 10h.01M21 12c0 4.418-4.03 8-9 8a9.013 9.013 0 01-4.546-1.172L3 20l1.172-4.454A8.96 8.96 0 013 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </span>
              )}
              <span
                className={`inline-block p-3 rounded-lg max-w-xs shadow ${
                  message.isUser
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeRaw]}
                  components={{
                    p: ({ children }) => (
                      <p className="whitespace-pre-line break-words m-0">
                        {children}
                      </p>
                    ),
                    br: () => <br />,
                  }}
                >
                  {message.text}
                </ReactMarkdown>
              </span>
            </motion.div>
          ))}
          {isLoading && <SkeletonMessage />}
          {isTyping && !isLoading && <TypingIndicator />}
        </AnimatePresence>
      </ScrollArea>

      <form onSubmit={handleSendMessage} className="p-4 border-t">
        <div className="flex space-x-2">
          <Input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="메시지를 입력하세요..."
            className="flex-grow"
            disabled={isLoading}
          />
          <Button type="submit" size="icon" disabled={isLoading} className="bg-blue-500 hover:bg-blue-600 text-white">
            <Send className="h-4 w-4" />
            <span className="sr-only">메시지 보내기</span>
          </Button>
        </div>
      </form>
    </div>
  )
}

