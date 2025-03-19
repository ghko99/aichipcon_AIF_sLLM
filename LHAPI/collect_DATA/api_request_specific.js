const axios = require('axios');
const fs = require('fs');
const path = require('path');
const csvWriter = require('csv-writer').createObjectCsvWriter;
require('dotenv').config();

// API 인증키 (Encoded)
const serviceKey = process.env.SERVICE_KEY;

// 첫 번째 API 호출: 공고 목록 조회
const firstApiUrl = 'http://apis.data.go.kr/B552555/lhLeaseNoticeInfo1/lhLeaseNoticeInfo1';

let firstQueryParams = '?' + encodeURIComponent('serviceKey') + '=' + serviceKey;
firstQueryParams += '&' + encodeURIComponent('PG_SZ') + '=' + encodeURIComponent('3000');
firstQueryParams += '&' + encodeURIComponent('PAGE') + '=' + encodeURIComponent('1');
firstQueryParams += '&' + encodeURIComponent('UPP_AIS_TP_CD') + '=' + encodeURIComponent('06');
firstQueryParams += '&' + encodeURIComponent('PAN_ST_DT') + '=' + encodeURIComponent('20231108');
firstQueryParams += '&' + encodeURIComponent('PAN_ED_DT') + '=' + encodeURIComponent('20241108');

let fileCount = 0;

// CSV 파일 작성기 정의 (헤더 정의 포함)
const writer = csvWriter({
  path: 'C:/Users/LG/Desktop/VS 공공데이터OpenAPI/collect_DATA/모든_변수_포함_일치하는_공고목록_세부표시.csv',
  header: [
    { id: 'PAN_NT_ST_DT', title: '공고게시일' },
    { id: 'PAN_ID', title: '공고ID' },
    { id: 'AIS_TP_CD_NM', title: '주택유형' },
    { id: 'CNP_CD_NM', title: '지역' },
    { id: 'ALL_CNT', title: '전체세대수' },
    { id: 'SPL_INF_TP_CD', title: '특별공급코드' },
    { id: 'AIS_TP_CD', title: '공급유형코드' },
    { id: 'PAN_DT', title: '공고일' },
    { id: 'RNUM', title: '번호' },
    { id: 'CCR_CNNT_SYS_DS_CD', title: '시스템구분' },
    { id: 'DTL_URL', title: '상세URL' },
    { id: 'CLSG_DT', title: '마감일' },
    { id: 'UPP_AIS_TP_CD', title: '상위공급코드' },
    { id: 'PAN_NM', title: '공고명' },
    { id: 'UPP_AIS_TP_NM', title: '상위주택유형' },
    { id: 'PAN_SS', title: '공고상태' },
    { id: 'DTL_URL_MOB', title: '모바일상세URL' },
    { id: 'HS_SBSC_ACP_TRG_CD_NM', title: '구분' },
    { id: 'ACP_DTTM', title: '신청일시' },
    { id: 'PZWR_PPR_SBM_ST_DT', title: '서류제출시작일' },
    { id: 'PZWR_PPR_SBM_ED_DT', title: '서류제출종료일' },
    { id: 'CTRT_ST_DT', title: '계약시작일' },
    { id: 'CTRT_ED_DT', title: '계약종료일' },
    { id: 'RSDN_DDO_AR', title: '전용면적' },
    { id: 'LS_GMY', title: '임대보증금' },
    { id: 'MM_RFE', title: '월임대료' },
    { id: 'SPL_AR', title: '공급면적' },
    { id: 'TOT_HSH_CNT', title: '총세대수' },
    { id: 'CMN_AHFL_NM', title: '첨부파일명' },
    { id: 'AHFL_URL', title: '다운로드링크' },
    { id: 'SL_PAN_AHFL_DS_CD_NM', title: '파일구분명' },
    { id: 'BZDT_NM', title: '단지명' },
    { id: 'LCT_ARA_ADR', title: '단지주소' },
    { id: 'LCT_ARA_DTL_ADR', title: '단지상세주소' },
    { id: 'EDC_FCL_CTS', title: '교육환경' },
    { id: 'TFFC_FCL_CTS', title: '교통여건' },
    { id: 'CVN_FCL_CTS', title: '편의시설' },
    { id: 'HTN_FMLA_DS_CD_NM', title: '난방방식' },
    { id: 'IDT_FCL_CTS', title: '부대시설' },
    { id: 'MVIN_XPC_YM', title: '입주예정월' }
  ]
});

axios.get(firstApiUrl + firstQueryParams)
  .then(async (firstResponse) => {
    console.log('첫 번째 API 응답 상태 코드:', firstResponse.status);
    console.log('첫 번째 API 호출 완료');
    const result = firstResponse.data;

    const dsList = result[1]?.dsList;
    
    if (dsList && dsList.length > 0) {
      console.log(`총 ${dsList.length}개의 매물 정보를 조회했습니다.`);
      const records = []; // 모든 공고의 정보를 저장할 배열

      for (let i = 0; i < dsList.length; i++) {
        const item = dsList[i];
        console.log(`매물 ${i + 1}/${dsList.length}에 대한 두 번째, 세 번째 API 호출 진행 중...`);

        // 두 번째 API 호출: 상세 정보 조회
        const secondApiUrl = 'http://apis.data.go.kr/B552555/lhLeaseNoticeDtlInfo1/getLeaseNoticeDtlInfo1';
        let secondQueryParams = '?' + encodeURIComponent('serviceKey') + '=' + serviceKey;
        secondQueryParams += '&' + encodeURIComponent('SPL_INF_TP_CD') + '=' + encodeURIComponent(item.SPL_INF_TP_CD);
        secondQueryParams += '&' + encodeURIComponent('CCR_CNNT_SYS_DS_CD') + '=' + encodeURIComponent(item.CCR_CNNT_SYS_DS_CD);
        secondQueryParams += '&' + encodeURIComponent('PAN_ID') + '=' + encodeURIComponent(item.PAN_ID);
        secondQueryParams += '&' + encodeURIComponent('UPP_AIS_TP_CD') + '=' + encodeURIComponent(item.UPP_AIS_TP_CD);
        secondQueryParams += '&' + encodeURIComponent('AIS_TP_CD') + '=' + encodeURIComponent(item.AIS_TP_CD);

        let secondApiData = null;
        try {
          const secondResponse = await axios.get(secondApiUrl + secondQueryParams);
          secondApiData = secondResponse.data[1] || {};
          console.log(`매물 ${i + 1}/${dsList.length}의 두 번째 API 호출 완료`);
        } catch (error) {
          console.log(`매물 ${i + 1}/${dsList.length}의 두 번째 API 요청 중 오류:`, error);
        }

        // 세 번째 API 호출: 공급 정보 조회
        const thirdApiUrl = 'http://apis.data.go.kr/B552555/lhLeaseNoticeSplInfo1/getLeaseNoticeSplInfo1';
        let thirdQueryParams = '?' + encodeURIComponent('serviceKey') + '=' + serviceKey;
        thirdQueryParams += '&' + encodeURIComponent('SPL_INF_TP_CD') + '=' + encodeURIComponent(item.SPL_INF_TP_CD);
        thirdQueryParams += '&' + encodeURIComponent('CCR_CNNT_SYS_DS_CD') + '=' + encodeURIComponent(item.CCR_CNNT_SYS_DS_CD);
        thirdQueryParams += '&' + encodeURIComponent('PAN_ID') + '=' + encodeURIComponent(item.PAN_ID);
        thirdQueryParams += '&' + encodeURIComponent('UPP_AIS_TP_CD') + '=' + encodeURIComponent(item.UPP_AIS_TP_CD);
        thirdQueryParams += '&' + encodeURIComponent('AIS_TP_CD') + '=' + encodeURIComponent(item.AIS_TP_CD);

        let thirdApiData = null;
        try {
          const thirdResponse = await axios.get(thirdApiUrl + thirdQueryParams);
          thirdApiData = thirdResponse.data[1] || {};
          console.log(`매물 ${i + 1}/${dsList.length}의 세 번째 API 호출 완료`);
        } catch (error) {
          console.log(`매물 ${i + 1}/${dsList.length}의 세 번째 API 요청 중 오류:`, error);
        }

        // 첨부파일 정보 필터링: '공고문(PDF)' 포함하고 파일명이 .pdf로 끝나는 항목만 필터링
        const ahflInfo = secondApiData?.dsAhflInfo?.filter(item => 
          item.SL_PAN_AHFL_DS_CD_NM.includes('공고문(PDF)') && item.CMN_AHFL_NM.endsWith('.pdf')
        ) || [];

        // 각각의 세부 항목들을 반복하면서 모든 조합을 생성
        const splScdl = secondApiData?.dsSplScdl || [{}];
        const sbd = secondApiData?.dsSbd || [{}];
        const list02 = thirdApiData?.dsList02 || [{}];

        splScdl.forEach(splScdlItem => {
            sbd.forEach(sbdItem => {
            list02.forEach(list02Item => {
                ahflInfo.forEach(ahflItem => {
                records.push({
                    PAN_NT_ST_DT: item.PAN_NT_ST_DT || 'NO_DATA',
                    PAN_ID: item.PAN_ID || 'NO_DATA',
                    AIS_TP_CD_NM: item.AIS_TP_CD_NM || 'NO_DATA',
                    CNP_CD_NM: item.CNP_CD_NM || 'NO_DATA',
                    ALL_CNT: item.ALL_CNT || 'NO_DATA',
                    SPL_INF_TP_CD: item.SPL_INF_TP_CD || 'NO_DATA',
                    AIS_TP_CD: item.AIS_TP_CD || 'NO_DATA',
                    PAN_DT: item.PAN_DT || 'NO_DATA',
                    RNUM: item.RNUM || 'NO_DATA',
                    CCR_CNNT_SYS_DS_CD: item.CCR_CNNT_SYS_DS_CD || 'NO_DATA',
                    DTL_URL: item.DTL_URL || 'NO_DATA',
                    CLSG_DT: item.CLSG_DT || 'NO_DATA',
                    UPP_AIS_TP_CD: item.UPP_AIS_TP_CD || 'NO_DATA',
                    PAN_NM: item.PAN_NM || 'NO_DATA',
                    UPP_AIS_TP_NM: item.UPP_AIS_TP_NM || 'NO_DATA',
                    PAN_SS: item.PAN_SS || 'NO_DATA',
                    DTL_URL_MOB: item.DTL_URL_MOB || 'NO_DATA',
                    HS_SBSC_ACP_TRG_CD_NM: splScdlItem.HS_SBSC_ACP_TRG_CD_NM || 'NO_DATA',
                    ACP_DTTM: splScdlItem.ACP_DTTM || 'NO_DATA',
                    PZWR_PPR_SBM_ST_DT: splScdlItem.PZWR_PPR_SBM_ST_DT || 'NO_DATA',
                    PZWR_PPR_SBM_ED_DT: splScdlItem.PZWR_PPR_SBM_ED_DT || 'NO_DATA',
                    CTRT_ST_DT: splScdlItem.CTRT_ST_DT || 'NO_DATA',
                    CTRT_ED_DT: splScdlItem.CTRT_ED_DT || 'NO_DATA',
                    RSDN_DDO_AR: sbdItem.MIN_MAX_RSDN_DDO_AR || 'NO_DATA',
                    LS_GMY: list02Item.LS_GMY || 'NO_DATA',
                    MM_RFE: list02Item.MM_RFE || 'NO_DATA',
                    SPL_AR: list02Item.SPL_AR || 'NO_DATA',
                    TOT_HSH_CNT: sbdItem.SUM_TOT_HSH_CNT || 'NO_DATA',
                    CMN_AHFL_NM: ahflItem.CMN_AHFL_NM || 'NO_DATA',
                    AHFL_URL: ahflItem.AHFL_URL || 'NO_DATA',
                    SL_PAN_AHFL_DS_CD_NM: ahflItem.SL_PAN_AHFL_DS_CD_NM || 'NO_DATA',
                    BZDT_NM: sbdItem.BZDT_NM || 'NO_DATA',
                    LCT_ARA_ADR: sbdItem.LCT_ARA_ADR || 'NO_DATA',
                    LCT_ARA_DTL_ADR: sbdItem.LCT_ARA_DTL_ADR || 'NO_DATA',
                    EDC_FCL_CTS: sbdItem.EDC_FCL_CTS || 'NO_DATA',
                    TFFC_FCL_CTS: sbdItem.TFFC_FCL_CTS || 'NO_DATA',
                    CVN_FCL_CTS: sbdItem.CVN_FCL_CTS || 'NO_DATA',
                    HTN_FMLA_DS_CD_NM: sbdItem.HTN_FMLA_DS_CD_NM || 'NO_DATA',
                    IDT_FCL_CTS: sbdItem.IDT_FCL_CTS || 'NO_DATA',
                    MVIN_XPC_YM: sbdItem.MVIN_XPC_YM || 'NO_DATA'
                });
                });
            });
            });
        });


        console.log(`매물 ${i + 1}/${dsList.length}의 모든 정보 저장 완료`);
        fileCount++;
      }

      // CSV 파일로 저장
      if (records.length > 0) {
        await writer.writeRecords(records);
        console.log(`총 ${fileCount}개의 공고가 CSV 파일에 저장되었습니다.`);
      } else {
        console.log('저장할 공고 데이터가 없습니다.');
      }
    } else {
      console.log('첫 번째 API에서 결과가 없습니다.');
    }
  })
  .catch((error) => {
    console.log('첫 번째 API 요청 중 오류:', error);
  });
