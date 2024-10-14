import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1000, // 가상 사용자 수
  duration: '30s', // 테스트 지속 시간
};

export default function () {
  let res = http.get('https://content-service:8000/contents/'); // 엔드포인트 주소
  check(res, {
    'status is 200': (r) => r.status === 200, // 상태 코드가 200인지 확인
  });
  sleep(1); // 1초 대기
}
