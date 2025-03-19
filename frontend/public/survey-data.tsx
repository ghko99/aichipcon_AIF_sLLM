// survey-data.ts

import { ReactNode } from "react"
import { Check, X } from "lucide-react"

export type QuestionType = "multiple-choice" | "text" | "rating" | "income" | "birthdate" | "number" | "family-members" | "asset"

export interface Option {
  text: string
  icon: ReactNode
}

export interface Question {
  id: string
  type: QuestionType
  question: string[]
  options?: Option[]
  condition?: (answers: Record<string, any>) => boolean
}

export interface Announcement {
  id: string
  title: string
  description: string
}

export const questions: Question[] = [
  // 기존의 질문 데이터를 그대로 옮겨옵니다.
]

export const announcements: Announcement[] = [
  // 기존의 공고 데이터를 그대로 옮겨옵니다.
]
