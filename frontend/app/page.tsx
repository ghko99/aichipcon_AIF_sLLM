import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Search, MessageSquare } from 'lucide-react'

export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-[hsl(0,0%,100%)]">
      <Card className="w-full max-w-2xl border-[hsl(214.3,31.8%,91.4%)]">
        <CardHeader>
          <Link href="/intro">
            <CardTitle className="text-2xl font-bold text-center text-[hsl(222.2,84%,4.9%)]">LH 임대 주택 청약 챗봇 서비스</CardTitle>
          </Link>
          <Link href="/survey">
          <CardDescription className="text-center text-[hsl(215.4,16.3%,46.9%)]">Powerd by <span className="text-[hsl(222.2,84%,4.9%)] font-semibold">RBLN</span></CardDescription>
          </Link>

          <Link href="/dashboard">
          <CardDescription className="text-center text-[hsl(215.4,16.3%,46.9%)]">Sponserd by <span className="text-[hsl(222.2,84%,4.9%)] font-semibold">AI반도체기술인재선발대회</span></CardDescription>
          </Link>
{/*           
          <Link href="/chatbot">
          <CardDescription className="text-center text-[hsl(215.4,16.3%,46.9%)]">chatbot</CardDescription>
          </Link> */}



        </CardHeader>
        <CardContent className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-8">
          <Link href="/intro" className="w-48 h-48 relative group">
            <div className="absolute inset-0 bg-[hsl(221.2,83.2%,53.3%)] rounded-lg transition-all duration-300 group-hover:bg-[hsl(221.2,83.2%,53.3%)]">
              <div className="flex flex-col items-center justify-center h-full">
                <Search className="w-16 h-16 mb-2 text-[hsl(210,40%,98%)] group-hover:text-[hsl(210,40%,98%)]" />
                <span className="text-[hsl(210,40%,98%)] group-hover:text-[hsl(210,40%,98%)] text-lg font-semibold text-center">공고문 추천 & 검색</span>
              </div>
            </div>
          </Link>
          <Link href="/chatbot" className="w-48 h-48 relative group">
            <div className="absolute inset-0 bg-[hsl(210,40%,96.1%)] rounded-lg transition-all duration-300 group-hover:bg-[hsl(221.2,83.2%,53.3%)]">
              <div className="flex flex-col items-center justify-center h-full">
                <MessageSquare className="w-16 h-16 mb-2 text-[hsl(222.2,47.4%,11.2%)] group-hover:text-[hsl(210,40%,98%)]" />
                <span className="text-[hsl(222.2,47.4%,11.2%)] group-hover:text-[hsl(210,40%,98%)] text-lg font-semibold text-center">공고문 챗봇 서비스</span>
              </div>
            </div>
          </Link>
        </CardContent>
      </Card>
    </div>
  )
}

