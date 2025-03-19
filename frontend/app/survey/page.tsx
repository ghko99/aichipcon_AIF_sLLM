"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Slider } from "@/components/ui/slider"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ChevronLeft, ChevronRight, Check, X, Minus, Plus, Loader2, Info, CheckCircle } from 'lucide-react'
import { useRouter } from "next/navigation"
import { AgeSelector } from "@/components/AgeSelector"

type QuestionType = "multiple-choice" | "text" | "rating" | "income" | "age" | "number" | "asset" | "car-value" | "household-members" | "date" | "children-count"

interface Option {
  text: string
  icon: React.ReactNode
}

interface Question {
  id: string
  type: QuestionType
  question: string[]
  options?: Option[]
  condition?: (answers: Record<string, any>) => boolean
}

const questions: Question[] = [
  {
    id: "age",
    type: "age",
    question: ["귀하의 나이는 몇 세입니까?"],
  },
  {
    id: "enrolledUniversity",
    type: "multiple-choice",
    question: ["귀하는 대학생 계층에 속하십니까?"],
    options: [
      { text: "예", icon: <Check className="w-5 h-5" /> },
      { text: "아니오", icon: <X className="w-5 h-5" /> },
    ],
  },
  {
    id: "jobSeeking",
    type: "multiple-choice",
    question: ["귀하는 취업준비생이십니까?"],
    options: [
      { text: "예", icon: <Check className="w-5 h-5" /> },
      { text: "아니오", icon: <X className="w-5 h-5" /> },
    ],
  },
  {
    id: "familyMembersCount",
    type: "household-members",
    question: ["귀하의 가구원 수는 몇 명입니까?"],
  },
  {
    id: "married",
    type: "multiple-choice",
    question: ["혼인하셨나요?"],
    options: [
      { text: "예", icon: <Check className="w-5 h-5" /> },
      { text: "아니오", icon: <X className="w-5 h-5" /> },
    ],
  },
  {
    id: "marriageDate",
    type: "date",
    question: ["혼인한 날짜를 입력해주세요 (YYYY-MM-DD 형식)"],
    condition: (answers) => answers.married === "예",
  },
  {
    id: "dualIncome",
    type: "multiple-choice",
    question: ["가구가 맞벌이이신가요?"],
    options: [
      { text: "예", icon: <Check className="w-5 h-5" /> },
      { text: "아니오", icon: <X className="w-5 h-5" /> },
    ],
    condition: (answers) => answers.married === "예",
  },
  {
    id: "hasChildren",
    type: "multiple-choice",
    question: ["자녀가 있으신가요?"],
    options: [
      { text: "예", icon: <Check className="w-5 h-5" /> },
      { text: "아니오", icon: <X className="w-5 h-5" /> },
    ],
  },
  {
    id: "childrenCount",
    type: "children-count",
    question: ["자녀 수를 입력해주세요"],
    condition: (answers) => answers.hasChildren === "예",
  },
  {
    id: "youngestChildBirthDate",
    type: "date",
    question: ["가장 어린 자녀의 생년월일을 입력해주세요 (YYYY-MM-DD 형식)"],
    condition: (answers) => answers.hasChildren === "예",
  },
  {
    id: "singleParent",
    type: "multiple-choice",
    question: ["한부모 가정이신가요?"],
    options: [
      { text: "예", icon: <Check className="w-5 h-5" /> },
      { text: "아니오", icon: <X className="w-5 h-5" /> },
    ],
  },
  {
    id: "monthlyIncome",
    type: "income",
    question: ["본인의 월 평균 소득은 얼마입니까?"],
  },
  {
    id: "householdMonthlyIncome",
    type: "income",
    question: ["가구의 월 평균 소득은 얼마입니까?"],
  },
  {
    id: "ownHouse",
    type: "multiple-choice",
    question: ["귀하는 주택을 소유하고 계십니까?"],
    options: [
      { text: "예", icon: <Check className="w-5 h-5" /> },
      { text: "아니오", icon: <X className="w-5 h-5" /> },
    ],
  },
  {
    id: "assets",
    type: "asset",
    question: ["귀하의 총 자산은 얼마입니까?"],
  },
  {
    id: "ownCar",
    type: "multiple-choice",
    question: ["귀하는 자동차를 소유하고 계십니까?"],
    options: [
      { text: "예", icon: <Check className="w-5 h-5" /> },
      { text: "아니오", icon: <X className="w-5 h-5" /> },
    ],
  },
  {
    id: "carPrice",
    type: "car-value",
    question: ["소유하신 자동차의 가액은 얼마입니까?"],
    condition: (answers) => answers.ownCar === "예",
  },
  {
    id: "hasSubscriptionAccount",
    type: "multiple-choice",
    question: ["귀하는 주택청약종합저축에 가입하셨습니까?"],
    options: [
      { text: "예", icon: <Check className="w-5 h-5" /> },
      { text: "아니오", icon: <X className="w-5 h-5" /> },
    ],
  },
]

export default function SurveyPage() {
  const router = useRouter()
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, any>>({})
  const [income, setIncome] = useState<number>(3000)
  const [asset, setAsset] = useState<number>(10000)
  const [carValue, setCarValue] = useState<number>(0)
  const [age, setAge] = useState<string>("30")
  const [householdMembers, setHouseholdMembers] = useState<number>(1)
  const [isLoading, setIsLoading] = useState(false)
  const [submissionMessage, setSubmissionMessage] = useState<string>("")
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [error, setError] = useState<string | null>(null);
  const [loadingResults, setLoadingResults] = useState(false);
  const [savedResults, setSavedResults] = useState<Record<string, any> | null>(null);

  const currentQuestion = questions[currentQuestionIndex]

  const handleAnswer = (answer: any) => {
    setAnswers((prev) => {
      const newAnswers = { ...prev, [currentQuestion.id]: answer }
      console.log("Updated answers:", newAnswers)
      return newAnswers
    })
  }

  const handleNext = async () => {
    if (currentQuestionIndex < questions.length - 1) {
      let nextIndex = currentQuestionIndex + 1;
  
      // 다음 질문으로 이동하기 전에 조건 확인
      while (
        nextIndex < questions.length &&
        questions[nextIndex]?.condition && // Optional Chaining으로 condition 확인
        !questions[nextIndex].condition!(answers) // condition 함수 호출
      ) {
        nextIndex++;
      }
  
      // 유효한 다음 질문으로 이동하거나 설문 제출
      if (nextIndex < questions.length) {
        setCurrentQuestionIndex(nextIndex);
      } else {
        await handleSubmit();
      }
    } else {
      await handleSubmit();
    }
  };
  
  
  
  const handleSubmit = async () => {
    setIsLoading(true)
    setSubmissionMessage("설문 응답을 처리하고 있습니다...")
    try {
      const surveyResultJson = {
        age: parseInt(answers.age),
        enrolledUniversity: answers.enrolledUniversity === "예",
        jobSeeking: answers.jobSeeking === "예",
        familyMembersCount: answers.familyMembersCount,
        married: answers.married === "예",
        marriageDate: answers.married === "예" ? answers.marriageDate : null,
        dualIncome: answers.married === "예" ? answers.dualIncome === "예" : null,
        hasChildren: answers.hasChildren === "예",
        childrenCount: answers.hasChildren === "예" ? answers.childrenCount : null,
        youngestChildBirthDate: answers.hasChildren === "예" ? answers.youngestChildBirthDate : null,
        singleParent: answers.singleParent === "예",
        monthlyIncome: answers.monthlyIncome,
        householdMonthlyIncome: answers.householdMonthlyIncome,
        ownHouse: answers.ownHouse === "예",
        assets: answers.assets,
        ownCar: answers.ownCar === "예",
        carPrice: answers.ownCar === "예" ? answers.carPrice : null,
        hasSubscriptionAccount: answers.hasSubscriptionAccount === "예",
        region: "전국",
        status: "전체",
        startDate: "2024.01.01",
        endDate: "2024.11.08"
      };

      console.log("Sending survey result:", JSON.stringify(surveyResultJson, null, 2));
      
      const response = await fetch('http://127.0.0.1:5000/survey', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(surveyResultJson),
      });

      if (!response.ok) {
        throw new Error('Failed to submit survey');
      }

      // Construct query string from surveyResultJson
      const queryString = Object.entries(surveyResultJson)
        .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
        .join('&');

      // Redirect to dashboard with query parameters
      router.push(`/dashboard`);
    } catch (error) {
      console.error("Error submitting survey:", error)
      setSubmissionMessage("설문 제출 중 오류가 발생했습니다. 다시 시도해 주세요.")
      setError("네트워크 오류가 발생했습니다. 인터넷 연결을 확인해 주세요.");
    } finally {
      setIsLoading(false)
    }
  }

  const handlePrevious = () => {
    // let prevIndex = currentQuestionIndex - 1
    // while (
    //   prevIndex >= 0 &&
    //   questions[prevIndex].condition &&!questions[prevIndex].condition(answers)
    // ) {
    //   prevIndex--
    // }
    // if (prevIndex >= 0) {
    //   setCurrentQuestionIndex(prevIndex)
    // }
  }

  const handleIncomeChange = (value: number[]) => {
    setIncome(value[0])
    handleAnswer(value[0])
  }

  const handleIncomeInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value) || 0
    setIncome(value)
    handleAnswer(value)
  }

  const handleAssetChange = (value: number[]) => {
    setAsset(value[0])
    handleAnswer(value[0])
  }

  const handleAssetInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value) || 0
    setAsset(value)
    handleAnswer(value)
  }

  const handleCarValueChange = (value: number[]) => {
    setCarValue(value[0])
    handleAnswer(value[0])
  }

  const handleCarValueInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value) || 0
    setCarValue(value)
    handleAnswer(value)
  }

  const handleAgeChange = (value: string) => {
    setAge(value)
    handleAnswer(parseInt(value))
  }

  const handleHouseholdMembersChange = (value: string) => {
    const numValue = parseInt(value)
    setHouseholdMembers(numValue)
    handleAnswer(numValue)
  }

  const handleDateInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleAnswer(e.target.value)
  }

  const handleChildrenCountChange = (value: string) => {
    const numValue = parseInt(value)
    handleAnswer(numValue)
  }

  const isAnswerValid = () => {
    if (currentQuestion.type === "age") {
      return age !== ""
    }
    if (currentQuestion.type === "household-members") {
      return householdMembers > 0
    }
    if (currentQuestion.type === "date") {
      const dateRegex = /^\d{4}-\d{2}-\d{2}$/
      return dateRegex.test(answers[currentQuestion.id] || "")
    }
    if (currentQuestion.type === "children-count") {
      return answers[currentQuestion.id] > 0
    }
    return answers[currentQuestion.id] !== undefined
  }

  const progress = ((currentQuestionIndex + 1) / questions.length) * 100

  const formatCurrency = (value: number) => {
    if (value === 0) return "0원"
    if (value >= 10000) return `${(value / 10000).toFixed(1)}억 원`
    return `${value}만 원`
  }

  const surveyContent = (
    <div className="flex flex-col justify-center items-center min-h-screen bg-gray-100 p-4">
      <div className="w-full max-w-md mb-4 bg-gray-200 rounded-full h-2.5">
        <div
          className="bg-blue-500 h-2.5 rounded-full transition-all duration-300 ease-in-out"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <Card className="w-full max-w-md bg-white text-gray-900 border-gray-200">
        <CardHeader>
          <CardTitle className="text-xl font-bold">
            {currentQuestion.question.map((line, index) => (
              <div key={index}>{line}</div>
            ))}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {currentQuestion.type === "multiple-choice" && (
            <div className="space-y-2">
              {currentQuestion.options?.map((option, index) => (
                <Button
                  key={index}
                  className={`w-full justify-start text-left font-normal border-none ${
                    answers[currentQuestion.id] === option.text
                      ? "bg-blue-500 hover:bg-blue-600 text-white"
                      : "bg-gray-100 hover:bg-gray-200 text-gray-900"
                  }`}
                  onClick={() => handleAnswer(option.text)}
                >
                  <span className="mr-3">{option.icon}</span>
                  {option.text}
                </Button>
              ))}
            </div>
          )}
          {currentQuestion.type === "income" && (
            <div className="space-y-4">
              <Input
                type="number"
                value={income}
                onChange={handleIncomeInput}
                className="w-full bg-white text-gray-900 border-gray-300"
                placeholder="직접 입력"
              />
              <p className="text-center text-lg">{formatCurrency(income)}</p>
              <Slider
                min={0}
                max={1000}
                step={10}
                value={[income]}
                onValueChange={handleIncomeChange}
                className="w-full"
              />
            </div>
          )}
          {currentQuestion.type === "asset" && (
            <div className="space-y-4">
              <Input
                type="number"
                value={asset}
                onChange={handleAssetInput}
                className="w-full bg-white text-gray-900 border-gray-300"
                placeholder="직접 입력"
              />
              <p className="text-center text-lg">{formatCurrency(asset)}</p>
              <Slider
                min={0}
                max={50000}
                step={100}
                value={[asset]}
                onValueChange={handleAssetChange}
                className="w-full"
              />
            </div>
          )}
          {currentQuestion.type === "car-value" && (
            <div className="space-y-4">
              <Input
                type="number"
                value={carValue}
                onChange={handleCarValueInput}
                className="w-full bg-white text-gray-900 border-gray-300"
                placeholder="직접 입력"
              />
              <p className="text-center text-lg">{formatCurrency(carValue)}</p>
              <Slider
                min={0}
                max={10000}
                step={100}
                value={[carValue]}
                onValueChange={handleCarValueChange}
                className="w-full"
              />
            </div>
          )}
          {currentQuestion.type === "age" && (
            <div className="flex justify-center">
              <AgeSelector value={age} onChange={handleAgeChange} />
            </div>
          )}
          {currentQuestion.type === "household-members" && (
            <div className="space-y-4">
              <Select value={householdMembers.toString()} onValueChange={handleHouseholdMembersChange}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="가구원 수 선택" />
                </SelectTrigger>
                <SelectContent>
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                    <SelectItem key={num} value={num.toString()}>{num}명</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
          {currentQuestion.type === "date" && (
            <div className="space-y-4">
              <Input
                type="date"
                value={answers[currentQuestion.id] || ""}
                onChange={handleDateInput}
                className="w-full bg-white text-gray-900 border-gray-300"
              />
            </div>
          )}
          {currentQuestion.type === "children-count" && (
            <div className="space-y-4">
              <Select value={answers[currentQuestion.id]?.toString() || ""} onValueChange={handleChildrenCountChange}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="자녀 수 선택" />
                </SelectTrigger>
                <SelectContent>
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                    <SelectItem key={num} value={num.toString()}>{num}명</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
            className="bg-gray-200 hover:bg-gray-300 text-gray-900 border-none"
          >
            <ChevronLeft className="mr-2 h-4 w-4" /> 이전
          </Button>
          <Button
            className="bg-blue-500 hover:bg-blue-600 text-white border-none"
            onClick={handleNext}
            disabled={!isAnswerValid()}
          >
            {currentQuestionIndex === questions.length - 1 ? "제출" : "다음"}
            {currentQuestionIndex !== questions.length - 1 && (
              <ChevronRight className="ml-2 h-4 w-4" />
            )}
          </Button>
        </CardFooter>
      </Card>
      <div className="mt-4 text-xs text-gray-500">
        현재 답변 상태: {JSON.stringify(answers[currentQuestion.id])}
      </div>
    </div>
  )

  return (
    <div className="flex h-screen bg-gray-100">
      <main className="flex-1 overflow-auto">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong className="font-bold">오류 발생!</strong>
            <span className="block sm:inline"> {error}</span>
          </div>
        )}
        {isLoading ? (
          <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <Loader2 className="w-16 h-16 text-blue-500 animate-spin" />
            <p className="mt-4 text-xl text-gray-900">설문 제출 중...</p>
            <p className="mt-2 text-lg text-gray-700">{submissionMessage}</p>
          </div>
        ) : isSubmitted ? (
          <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <CheckCircle className="w-16 h-16 text-green-500 animate-bounce" />
            <p className="mt-4 text-xl text-gray-900">설문이 성공적으로 제출되었습니다!</p>
            <p className="mt-2 text-lg text-gray-700">곧 대시보드로 이동합니다...</p>
          </div>
        ) : loadingResults ? (
          <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <Loader2 className="w-16 h-16 text-blue-500 animate-spin" />
            <p className="mt-4 text-xl text-gray-900">이전 설문 결과를 불러오는 중...</p>
          </div>
        ) : savedResults ? (
          <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <h2 className="text-2xl font-bold mb-4">이전 설문 결과</h2>
            <pre className="bg-white p-4 rounded shadow-md overflow-auto max-w-lg">
              {JSON.stringify(savedResults, null, 2)}
            </pre>
            <Button
              className="mt-4 bg-blue-500 hover:bg-blue-600 text-white"
              onClick={() => {
                setCurrentQuestionIndex(0);
                setAnswers({});
                setSavedResults(null);
              }}
            >
              새 설문 시작하기
            </Button>
          </div>
        ) : (
          surveyContent
        )}
      </main>
    </div>
  );
}

