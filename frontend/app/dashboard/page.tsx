'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link' // Link 컴포넌트 임포트
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbList,
  BreadcrumbPage,
} from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Star, CalendarIcon, Search } from 'lucide-react'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { format } from "date-fns"
import { cn } from "@/lib/utils"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

interface TableData {
  번호: number
  주택유형: string
  공고명: string
  지역: string
  공고게시일: string
  마감일: string
  공고상태: string
  age?: number,
  enrolledUniversity?: boolean,
  jobSeeking?: boolean,
  familyMembersCount?: number,
  married?: boolean,
  marriageDate?: Date | null,
  dualIncome?: boolean,
  hasChildren?: boolean,
  childrenCount?: number,
  youngestChildBirthDate?: Date | null,
  singleParent?: boolean,
  monthlyIncome?: number,
  householdMonthlyIncome?: number,
  ownHouse?: boolean,
  assets?: number,
  ownCar?: boolean,
  carPrice?: number,
  hasSubscriptionAccount?: boolean,
}

export default function Page() {
  return <DashboardContent />
}

function DashboardContent() {
  const [tableData, setTableData] = useState<TableData[]>([])
  const [filteredData, setFilteredData] = useState<TableData[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const [itemsPerPage, setItemsPerPage] = useState(50)
  const [currentPage, setCurrentPage] = useState(1)
  const [searchParams, setSearchParams] = useState({
    유형: '전체',
    지역: '전국',
    상태: '공고중',
    공고명: '',
    시작일: new Date('2024-10-01'),
    종료일: new Date('2024-12-01'),
  })
  const [showDetailedFilters, setShowDetailedFilters] = useState(false)
  const [detailedFilters, setDetailedFilters] = useState({
    age: null,
    enrolledUniversity: false,
    jobSeeking: false,
    familyMembersCount: null,
    married: false,
    marriageDate: null,
    dualIncome: false,
    hasChildren: false,
    childrenCount: null,
    youngestChildBirthDate: null,
    singleParent: false,
    monthlyIncome: null,
    householdMonthlyIncome: null,
    ownHouse: false,
    assets: null,
    ownCar: false,
    carPrice: null,
    hasSubscriptionAccount: false,
  })

  // Fetch data from the API when the component mounts
  useEffect(() => {
    fetch('http://127.0.0.1:5000/dashboard')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        return response.json();
      })
      .then((data: TableData[]) => {
        setTableData(data);
        setFilteredData(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
        setError('데이터를 불러오는데 실패했습니다.');
        setLoading(false);
      });
  }, []);

  const handleSearch = () => {
    let filtered = tableData

    if (searchParams.유형 !== '전체') {
      filtered = filtered.filter(item => item.주택유형 === searchParams.유형)
    }

    if (searchParams.지역 !== '전국') {
      filtered = filtered.filter(item => item.지역 === searchParams.지역)
    }

    if (searchParams.상태) {
      filtered = filtered.filter(item => item.공고상태 === searchParams.상태)
    }

    if (searchParams.공고명) {
      filtered = filtered.filter(item => 
        item.공고명.toLowerCase().includes(searchParams.공고명.toLowerCase())
      )
    }

    if (searchParams.시작일 && searchParams.종료일) {
      filtered = filtered.filter(item => {
        const itemDate = new Date(item.공고게시일.replace(/\./g, '-'))
        return itemDate >= searchParams.시작일! && itemDate <= searchParams.종료일!
      })
    }

    // Apply detailed filters
    if (detailedFilters.age) {
      filtered = filtered.filter(item => item.age === detailedFilters.age)
    }
    if (detailedFilters.enrolledUniversity) {
      filtered = filtered.filter(item => item.enrolledUniversity)
    }
    if (detailedFilters.jobSeeking) {
      filtered = filtered.filter(item => item.jobSeeking)
    }
    if (detailedFilters.familyMembersCount) {
      filtered = filtered.filter(item => item.familyMembersCount === detailedFilters.familyMembersCount)
    }
    if (detailedFilters.married) {
      filtered = filtered.filter(item => item.married)
    }
    if (detailedFilters.marriageDate) {
      // filtered = filtered.filter(item => item.marriageDate?.getTime() === detailedFilters.marriageDate?.getTime())
    }
    if (detailedFilters.dualIncome) {
      filtered = filtered.filter(item => item.dualIncome)
    }
    if (detailedFilters.hasChildren) {
      filtered = filtered.filter(item => item.hasChildren)
    }
    if (detailedFilters.childrenCount) {
      filtered = filtered.filter(item => item.childrenCount === detailedFilters.childrenCount)
    }
    if (detailedFilters.youngestChildBirthDate) {
      // filtered = filtered.filter(item => item.youngestChildBirthDate?.getTime() === detailedFilters.youngestChildBirthDate?.getTime())
    }
    if (detailedFilters.singleParent) {
      filtered = filtered.filter(item => item.singleParent)
    }
    if (detailedFilters.monthlyIncome) {
      filtered = filtered.filter(item => item.monthlyIncome === detailedFilters.monthlyIncome)
    }
    if (detailedFilters.householdMonthlyIncome) {
      filtered = filtered.filter(item => item.householdMonthlyIncome === detailedFilters.householdMonthlyIncome)
    }
    if (detailedFilters.ownHouse) {
      filtered = filtered.filter(item => item.ownHouse)
    }
    if (detailedFilters.assets) {
      filtered = filtered.filter(item => item.assets === detailedFilters.assets)
    }
    if (detailedFilters.ownCar) {
      filtered = filtered.filter(item => item.ownCar)
    }
    if (detailedFilters.carPrice) {
      filtered = filtered.filter(item => item.carPrice === detailedFilters.carPrice)
    }
    if (detailedFilters.hasSubscriptionAccount) {
      filtered = filtered.filter(item => item.hasSubscriptionAccount)
    }

    setFilteredData(filtered)
    setCurrentPage(1)
  }

  const paginatedData = filteredData.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  )

  if (loading) return <div>로딩 중...</div>
  if (error) return <div>{error}</div>

  return (
    <>
      <div className="p-6 space-y-4">
        <Card className="bg-white shadow-sm">
          <CardContent className="p-6">
            <div className="space-y-4">
              <div className="grid grid-cols-4 gap-6">
                {/* 유형 */}
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center">
                    <span className="text-red-500 mr-1">•</span>
                    유형
                  </label>
                  <Select 
                    value={searchParams.유형}
                    onValueChange={(value) => setSearchParams(prev => ({...prev, 유형: value}))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="전체">전체</SelectItem>
                      <SelectItem value="국민임대">국민임대</SelectItem>
                      <SelectItem value="공공임대">공공임대</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                {/* 지역 */}
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center">
                    <span className="text-red-500 mr-1">•</span>
                    지역
                  </label>
                  <Select
                    value={searchParams.지역}
                    onValueChange={(value) => setSearchParams(prev => ({...prev, 지역: value}))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="전국">전국</SelectItem>
                      <SelectItem value="경기도">경기도</SelectItem>
                      <SelectItem value="강원특별자치도">강원특별자치도</SelectItem>
                      <SelectItem value="충청남도">충청남도</SelectItem>
                      <SelectItem value="경상남도">경상남도</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* 상태 */}
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center">
                    <span className="text-red-500 mr-1">•</span>
                    상태
                  </label>
                  <Select
                    value={searchParams.상태}
                    onValueChange={(value) => setSearchParams(prev => ({...prev, 상태: value}))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="공고중">공고중</SelectItem>
                      <SelectItem value="마감">마감</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* 기간 */}
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center">
                    <span className="text-red-500 mr-1">•</span>
                    기간
                  </label>
                  <div className="flex items-center gap-2">
                    <Popover>
                      <PopoverTrigger asChild>
                        <Button
                          variant={"outline"}
                          className={cn(
                            "justify-start text-left font-normal",
                            !searchParams.시작일 && "text-muted-foreground"
                          )}
                        >
                          {searchParams.시작일 ? format(searchParams.시작일, "yyyy-MM-dd") : "시작일"}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0" align="start">
                        <Calendar
                          mode="single"
                          selected={searchParams.시작일}
                          // onSelect={(date) => setSearchParams(prev => ({...prev, 시작일: date}))}
                          initialFocus
                        />
                      </PopoverContent>
                    </Popover>
                    <span>~</span>
                    <Popover>
                      <PopoverTrigger asChild>
                        <Button
                          variant={"outline"}
                          className={cn(
                            "justify-start text-left font-normal",
                            !searchParams.종료일 && "text-muted-foreground"
                          )}
                        >
                          {searchParams.종료일 ? format(searchParams.종료일, "yyyy-MM-dd") : "종료일"}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0" align="start">
                        <Calendar
                          mode="single"
                          selected={searchParams.종료일}
                          // onSelect={(date) => setSearchParams(prev => ({...prev, 종료일: date}))}
                          initialFocus
                        />
                      </PopoverContent>
                    </Popover>
                  </div>
                </div>
              </div>

              {/* 공고명 */}
              <div className="space-y-2">
                <label className="text-sm font-medium flex items-center">
                  <span className="text-red-500 mr-1">•</span>
                  공고명
                </label>
                <div className="flex gap-2">
                  <Input
                    placeholder="공고명을 입력하여 검색해 보세요."
                    value={searchParams.공고명}
                    onChange={(e) => setSearchParams(prev => ({...prev, 공고명: e.target.value}))}
                    className="flex-1"
                  />
                  <div className="flex gap-2">
                    <Button 
                      onClick={handleSearch}
                      className="bg-[#2B3674] text-white hover:bg-[#2B3674]/90 px-6"
                    >
                      <Search className="h-4 w-4 mr-2" />
                      검색
                    </Button>
                    <Dialog open={showDetailedFilters} onOpenChange={setShowDetailedFilters}>
                      <DialogTrigger asChild>
                        <Button variant="outline" className="bg-black text-white hover:bg-black/90">
                        <Search className="h-4 w-4 mr-2" />
                        상세 검색
          
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="max-w-[800px] w-full">
                        <DialogHeader>
                          <DialogTitle>상세 조건 필터링</DialogTitle>
                        </DialogHeader>
                        {/* DetailedFilters component would go here */}
                      </DialogContent>
                    </Dialog>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="bg-white rounded-lg shadow-sm">
          <div className="p-6">
            <div className="flex justify-between items-center mb-4">
              <div className="text-sm">
                전체 <span className="text-[#2B3674] font-bold">{filteredData.length}건</span>{' '}
                {Math.ceil(filteredData.length / itemsPerPage)}페이지 중 {currentPage}페이지
              </div>
              <Select
                value={itemsPerPage.toString()}
                onValueChange={(value) => setItemsPerPage(Number(value))}
              >
                <SelectTrigger className="w-[100px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="10">10건</SelectItem>
                  <SelectItem value="25">25건</SelectItem>
                  <SelectItem value="50">50건</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="relative overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="bg-gray-50">
                    <TableHead className="font-medium">번호</TableHead>
                    <TableHead className="font-medium">유형</TableHead>
                    <TableHead className="font-medium">공고명</TableHead>
                    <TableHead className="font-medium">지역</TableHead>
                    <TableHead className="font-medium">게시일</TableHead>
                    <TableHead className="font-medium">마감일</TableHead>
                    <TableHead className="font-medium">상태</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {paginatedData.map((item) => (
                    <TableRow key={item.번호} className="hover:bg-gray-50">
                      <TableCell>{item.번호}</TableCell>
                      <TableCell>{item.주택유형}</TableCell>
                      <TableCell>
                        <Link href={`/chatbot?file_id=${item.번호}`} className="text-[#2B3674] hover:underline cursor-pointer">
                          {item.공고명}
                        </Link>
                      </TableCell>
                      <TableCell>{item.지역}</TableCell>
                      <TableCell>{item.공고게시일}</TableCell>
                      <TableCell>{item.마감일}</TableCell>
                      <TableCell>
                        <span className={cn(
                          "text-sm",
                          item.공고상태 === "공고중" ? "text-green-600" : "text-red-600"
                        )}>
                          {item.공고상태}
                        </span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
