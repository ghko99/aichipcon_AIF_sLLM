const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const { stringify } = require('csv-stringify/sync');

// 기존 CSV 파일 경로와 새로운 CSV 파일 경로
const csvFilePath = 'C:/Users/LG/Desktop/VS 공공데이터OpenAPI/collect_DATA/모든_변수_포함_일치하는_공고목록_세부매물.csv';
const outputCsvFilePath = 'C:/Users/LG/Desktop/VS 공공데이터OpenAPI/collect_DATA/중복제거_공고목록.csv';

// 중복 방지를 위한 Set 정의 (공고ID와 첨부파일명을 이용해 중복 제거)
const uniqueSet = new Set();
const filteredRows = [];

// CSV 파일을 읽고 중복 제거
fs.createReadStream(csvFilePath)
  .pipe(csv())
  .on('data', (row) => {
    // 공고ID와 첨부파일명을 조합해 고유한 키 생성
    const uniqueKey = `${row['공고ID']}_${row['첨부파일명']}`;

    // 중복되지 않은 경우에만 추가
    if (!uniqueSet.has(uniqueKey)) {
      uniqueSet.add(uniqueKey);
      filteredRows.push(row);
    }
  })
  .on('end', () => {
    console.log(`총 ${filteredRows.length}개의 고유 공고가 발견되었습니다.`);

    // CSV로 저장
    try {
      const outputCsv = stringify(filteredRows, { header: true });
      fs.writeFileSync(outputCsvFilePath, outputCsv, 'utf-8');
      console.log(`중복 제거된 공고 목록이 '${outputCsvFilePath}'에 저장되었습니다.`);
    } catch (error) {
      console.error('CSV 파일 저장 중 오류가 발생했습니다:', error);
    }
  })
  .on('error', (err) => {
    console.error('CSV 파일을 읽는 중 오류가 발생했습니다:', err);
  });
