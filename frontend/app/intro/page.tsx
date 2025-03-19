'use client'

import { useState, useEffect, useMemo, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useRouter } from 'next/navigation'

const containerVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 }
}

const emojiVariants = {
  initial: { scale: 0 },
  animate: { scale: 1 }
}

const textVariants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 }
}

export default function IntroPage() {
  const [step, setStep] = useState(0)
  const router = useRouter()

  const messages = useMemo(() => [
    { text: "안녕하세요 AIF LAB입니다.", emoji: "👋" },
    { text: "설문에 응답해주세요. 맞춤형 공고를 추천해드릴게요", emoji: "📝" },
    { text: "AIF LAB", emoji: "🚀" }
  ], [])

  const navigateToSurvey = useCallback(() => {
    router.push('/survey')
  }, [router])

  useEffect(() => {
    const timer = setTimeout(() => {
      if (step < 2) {
        setStep(step + 1)
      } else {
        navigateToSurvey()
      }
    }, 2500)

    return () => clearTimeout(timer)
  }, [step, navigateToSurvey])

  return (
    <div className="flex items-center justify-center h-screen bg-background text-foreground scrollbar-themed">
      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          variants={containerVariants}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={{ duration: 0.5 }}
          className="text-center"
        >
          <motion.div
            className="text-7xl mb-4"
            variants={emojiVariants}
            transition={{ type: "spring", stiffness: 260, damping: 20 }}
          >
            {messages[step].emoji}
          </motion.div>
          <motion.h1 
            className="text-4xl font-bold"
            variants={textVariants}
            transition={{ delay: 0.3 }}
          >
            {messages[step].text}
          </motion.h1>
        </motion.div>
      </AnimatePresence>
    </div>
  )
}

