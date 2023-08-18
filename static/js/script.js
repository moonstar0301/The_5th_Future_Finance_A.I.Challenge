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
    // 여기에 챗봇 응답 로직을 추가하세요
    return "챗봇 응답 예시: " + userMessage;
  }
  
  // 서버로 메시지 전송 함수 (가짜 챗봇 응답 사용)
  function sendToServer(userMessage) {
    const botResponse = getBotResponse(userMessage);
    appendMessage(botResponse, 'bot');
    scrollToBottom();
  }
  
  // 엔터 키 입력 이벤트 처리
  document.getElementById('userInput').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
      sendMessage();
    }
  });
  