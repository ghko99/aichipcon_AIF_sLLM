const fs = require('fs');
const path = require('path');
const axios = require('axios');
const csv = require('csv-parser');

const csvFilePath = 'C:/Users/LG/Desktop/VS 공공데이터OpenAPI/collect_DATA/모든_변수_포함_일치하는_공고목록_세부매물.csv';
const downloadDir = 'C:/Users/LG/Desktop/VS 공공데이터OpenAPI/collect_DATA/공고중인PDFs';

// 다운로드 결과 기록용 변수들
let totalItems = 0;
let successfulDownloads = 0;
let failedDownloads = 0;

// 중복 방지를 위한 Set 정의 (공고ID와 첨부파일명을 이용해 중복 제거)
const uniqueDownloadSet = new Set();

// PDF 다운로드 함수 정의
const downloadPdf = async (fileName, link) => {
  const filePath = path.join(downloadDir, fileName);

  try {
    console.log(`다운로드 시작 - 파일명: ${fileName}, 링크: ${link}`);
    
    const response = await axios({
      url: link,
      method: 'GET',
      responseType: 'stream',
    });

    await new Promise((resolve, reject) => {
      const writer = fs.createWriteStream(filePath);
      response.data.pipe(writer);
      writer.on('finish', () => {
        successfulDownloads++;
        resolve();
      });
      writer.on('error', reject);
    });

    console.log(`다운로드 완료: ${fileName}`);
  } catch (error) {
    failedDownloads++;
    console.error(`다운로드 실패: ${fileName}, 오류: ${error.message}`);
  }
};

// 메인 함수 정의
const main = async () => {
  // 동적 import로 p-limit 모듈 가져오기
  const pLimit = (await import('p-limit')).default;

  // 병렬 다운로드 최대 개수 설정
  const limit = pLimit(5);

  const downloadPromises = [];
  
  fs.createReadStream(csvFilePath)
    .pipe(csv())
    .on('data', (row) => {
      // 공고 상태가 '공고중'인 경우에만 다운로드 진행
      if (row['공고상태'] === '공고중') {
        totalItems++;
        const fileName = row['첨부파일명'];
        const link = row['다운로드링크'];
        const uniqueKey = `${row['공고ID']}_${fileName}`; // 공고ID와 파일명을 조합해 고유한 키 생성

        // 다운로드 링크와 파일명이 존재할 때만 다운로드 진행하고, 중복 제거
        if (fileName && link && !uniqueDownloadSet.has(uniqueKey)) {
          uniqueDownloadSet.add(uniqueKey); // 중복 방지를 위해 Set에 추가
          downloadPromises.push(
            limit(() => downloadPdf(fileName, link))
          );
        }
      }
    })
    .on('end', async () => {
      console.log(`총 ${totalItems}개의 '공고중'인 공고가 발견되었습니다.`);
      console.log(`총 ${downloadPromises.length}개의 다운로드 작업이 준비되었습니다.`);
      
      try {
        await Promise.all(downloadPromises);
        console.log('모든 PDF 파일 다운로드 완료');
        console.log(`성공적으로 다운로드된 파일: ${successfulDownloads}개`);
        console.log(`다운로드에 실패한 파일: ${failedDownloads}개`);
      } catch (error) {
        console.error('일부 PDF 파일 다운로드에 실패했습니다.', error);
      }
    });
};

// 메인 함수 실행
main();
