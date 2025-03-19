'use client'

import { useState } from 'react'
import { Viewer, Worker, SpecialZoomLevel } from '@react-pdf-viewer/core'
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { FileWarning } from 'lucide-react'
// import { useTheme } from 'next-themes'
// import { ThemeProvider } from '@react-pdf-viewer/theme'

// Import the styles
import '@react-pdf-viewer/core/lib/styles/index.css'
import '@react-pdf-viewer/default-layout/lib/styles/index.css'

export default function PDFViewer({ pdfUrl }: { pdfUrl: string }) {
  const [numPages, setNumPages] = useState<number>(0)
  const [error, setError] = useState<string | null>(null)

  // Create new plugin instance
  const defaultLayoutPluginInstance = defaultLayoutPlugin()

  // Handle relative URLs
  const fullPdfUrl = pdfUrl.startsWith('http') ? pdfUrl : `/${pdfUrl}`

  // const { theme: nextTheme } = useTheme()

  // const theme = {
  //   theme: nextTheme === 'dark' ? 'dark' : 'light',
  //   customColors: {
  //     primary: '#3b82f6', // blue-500
  //     secondary: '#60a5fa', // blue-400
  //   },
  // }

  if (!pdfUrl) {
    return (
      <Card className="w-full h-full flex items-center justify-center">
        <CardContent className="pt-6">
          <Alert variant="destructive">
            <FileWarning className="h-4 w-4" />
            <AlertTitle>오류</AlertTitle>
            <AlertDescription>
              PDF 파일 URL이 제공되지 않았습니다.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full h-[calc(100vh-2rem)] flex flex-col">
      <CardContent className="flex-grow p-0 overflow-hidden">
        <div className="w-full h-full">
          <Worker workerUrl={`https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`}>
            {/* <ThemeProvider theme={theme}> */}
              <Viewer
                fileUrl={fullPdfUrl}
                plugins={[defaultLayoutPluginInstance]}
                defaultScale={SpecialZoomLevel.PageFit}
                theme="auto"
                onDocumentLoad={(e) => setNumPages(e.doc.numPages)}
                renderError={(error) => (
                  <Alert variant="destructive" className="m-4">
                    <FileWarning className="h-4 w-4" />
                    <AlertTitle>PDF 로드 오류</AlertTitle>
                    <AlertDescription>
                      PDF 파일을 불러오는 중 오류가 발생했습니다: {(error as Error).message}.
                    </AlertDescription>
                  </Alert>
                )}
              />
            {/* </ThemeProvider> */}
          </Worker>
        </div>
      </CardContent>
      {numPages > 0 && (
        <div className="text-sm text-gray-500 p-2 text-center border-t border-gray-200">
          총 {numPages}페이지
        </div>
      )}
    </Card>
  )
}

