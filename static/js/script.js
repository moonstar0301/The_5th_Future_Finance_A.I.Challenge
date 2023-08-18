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

  sendToServer(userMessage);

  userInput.value = '';
}

// 스크롤 맨 아래로 이동 함수
function scrollToBottom() {
  const chatbox = document.getElementById('chatbox');
  chatbox.scrollTop = chatbox.scrollHeight;
}

// 가짜 챗봇 응답 함수 (가상의 응답 로직 사용)
function getBotResponse(userMessage) {
  $.ajax({
    url: '/chat',  // Flask 서버 경로
    method: 'POST',
    data: { message: userMessage },  // 데이터 필드명 수정
    success: function(response) {
      appendMessage(response, 'bot');      // 챗봇 응답을 화면에 표시
      scrollToBottom();
    },
    error: function() {
      console.error('Error while fetching bot response.');
    }
  });
}


// 서버로 메시지 전송 함수 (가짜 챗봇 응답 사용)
function sendToServer(userMessage) {
  const botResponse = getBotResponse(userMessage);
  scrollToBottom();
}

// 엔터 키 입력 이벤트 처리
document.getElementById('userInput').addEventListener('keyup', function(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
});