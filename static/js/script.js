// script.js

// 메시지 추가 함수
function appendMessage(message, sender) {
  const chatbox = document.getElementById('chatbox');
  const messageElement = document.createElement('div');
  messageElement.className = `alert alert-${sender === 'user' ? 'primary' : 'secondary'} mb-2`;
  messageElement.textContent = message;
  chatbox.appendChild(messageElement);
}

// 메시지 전송 함수
function sendMessage() {
  const userInput = document.getElementById('userInput');
  let userMessage = userInput.value.trim();

  if (userMessage === "") {
    return;
  }

  userMessage = userMessage.replace(/\n/g, '');

  appendMessage(userMessage, 'user');
  scrollToBottom();

  getBotResponse(userMessage);
  
  userInput.value = '';
}

// 스크롤 맨 아래로 이동 함수
function scrollToBottom() {
  const chatbox = document.getElementById('chatbox');
  chatbox.scrollTop = chatbox.scrollHeight;
}

// 가짜 챗봇 응답 함수
function getBotResponse(userMessage) {
  $.ajax({
    url: '/chat',  // Flask 서버 경로
    method: 'POST',
    data: { message: userMessage },
    success: function(response) {
      appendMessage(response.bot_response, 'bot');
      scrollToBottom();
      anotherFunction(response.small_subject, response.contents);
    },
    error: function() {
      console.error('Error while fetching bot response.');
    }
  });
}

// 다른 함수에서 사용되는 샘플 함수
function anotherFunction(small_subject, contents) {
  // 이 함수에서 small_subject와 contents를 활용하여 원하는 작업을 수행할 수 있습니다.
  console.log('small_subject:', small_subject);
  console.log('contents:', contents);
  // 예: small_subject와 contents를 이용한 그래프 그리기, 목록 생성 등
}

// 엔터 키 입력 이벤트 처리
document.getElementById('userInput').addEventListener('keyup', function(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
});
