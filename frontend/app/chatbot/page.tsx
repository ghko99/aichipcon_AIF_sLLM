"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation"; // Next.js 13 이상
import PDFViewer from "@/components/PDFViewer";
import Chatbot from "./Chatbot";
console.log(Chatbot); // 함수나 클래스가 출력되어야 합니다.

export default function Home() {
  const searchParams = useSearchParams();
  const fileId = searchParams ? searchParams.get("file_id") : null;
  const [pdfUrl, setPdfUrl] = useState("sample2.pdf"); // 기본값 설정

  useEffect(() => {
    if (fileId) {
      // file_id가 존재하고 유효한지 추가 검증 가능
      setPdfUrl(`${fileId}.pdf`); // file_id를 기반으로 PDF URL 설정
    } else {
      // file_id가 없을 경우 기본 PDF 사용 또는 다른 처리를 할 수 있음
      setPdfUrl("sample2.pdf");
    }
  }, [fileId]);

  return (
    <main className="flex min-h-screen p-4">
      <div className="flex-1 mr-4">
        <PDFViewer pdfUrl={pdfUrl} />
      </div>
      <div className="w-1/3">
      <Chatbot fileId={fileId} />
      </div>
    </main>
  );
}
