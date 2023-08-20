// 메시지 추가 함수 --- 채팅 박스 출력
function appendMessage(message, sender) {
  const chatbox = document.getElementById('chatbox');
  const messageElement = document.createElement('div');
  messageElement.className = `alert alert-${sender === 'user' ? 'primary' : 'secondary'} mb-2`;
  messageElement.textContent = message;
  chatbox.appendChild(messageElement);
}

// 메시지 전송 함수 --- 사용자 입력 string (서버), (출력 함수)로 전송
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

// 챗봇 응답 함수
function getBotResponse(userMessage) {
  $.ajax({
    url: '/chat',  // Flask 서버 경로
    method: 'POST',
    data: { message: userMessage },
    success: function(response) {
      if (response.mind_map_flag) { // 마인드맵 활성화
        appendMindMapMessage(response.bot_response, response.subject, response.contents);
        scrollToBottom();
      }
      else {
        appendMessage(response.bot_response, 'bot');
        scrollToBottom();
      }
    },
    error: function() {
      console.error('Error while fetching bot response.');
    }
  });
}


/// *** 마인드맵 활성화된 메시지 추가 함수 *** ///

// 메시지 추가 함수 --- 채팅 박스 출력
function appendMindMapMessage(message, subject, contents) {
  const chatbox = document.getElementById('chatbox');
  const messageElement = document.createElement('div');
  messageElement.className = `alert alert-secondary mb-2`;
  messageElement.textContent = message;

  const brElement = document.createElement('br'); // 줄바꿈
  messageElement.appendChild(brElement);
  const hrElement = document.createElement('hr'); // 선 긋기
  messageElement.appendChild(hrElement);

  var MindMapButtonContainer = document.createElement("div"); // 마인드맵 버튼 컨테이너 생성
  MindMapButtonContainer.className = "text-center"; // 가운데 정렬 스타일 클래스 추가

  const mindMapButton = document.createElement('button');
  mindMapButton.innerHTML = "Mind Map";
  mindMapButton.className = "btn btn-success";
  mindMapButton.style.width = "260px";

  MindMapButtonContainer.appendChild(mindMapButton);

  mindMapButton.onclick = function() {
    var subButtons = messageElement.querySelector('.sub-buttons');
    
    if (subButtons) {
      subButtons.remove();
    } else {
      subButtons = document.createElement("div");
      subButtons.className = "sub-buttons";
  
      subject.forEach(function(subjectItem, subjectIndex) {
        var subjectButton = document.createElement("button");
        subjectButton.innerHTML = subjectItem;
        subjectButton.className = "btn btn-warning";
  
        subjectButton.onclick = function() {
          var contentButtons = subjectButton.querySelector('.content-buttons'); // 수정된 부분
  
          if (contentButtons) {
            contentButtons.remove()
          } else {
            contentButtons = document.createElement("div");
            contentButtons.className = "content-buttons";
  
            contents[subjectIndex].forEach(function(content) {
              var contentButton = document.createElement("button");
              contentButton.innerHTML = content;
              contentButton.className = "btn btn-info text-left";
              contentButtons.appendChild(contentButton);
            });
  
            subjectButton.appendChild(contentButtons); // 수정된 부분
          }
        };
        subjectButton.style.display = "block";
        subButtons.appendChild(subjectButton);
      });
  
      messageElement.appendChild(subButtons);
    }
  };

  messageElement.appendChild(MindMapButtonContainer);
  chatbox.appendChild(messageElement);
}


/// *** 건들지 말기 *** ///

// 스크롤 맨 아래로 이동 함수
function scrollToBottom() {
  const chatbox = document.getElementById('chatbox');
  chatbox.scrollTop = chatbox.scrollHeight;
}

// 엔터 키 입력 이벤트 처리
document.getElementById('userInput').addEventListener('keyup', function(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
});


/// *** 질문 추천 버튼 *** ///

// 초기화 및 첫 번째 메시지 전송
document.addEventListener("DOMContentLoaded", function() {
  getBotRecommend();
});

// 추천 질문을 통신으로 받아오기
function getBotRecommend() {
  $.ajax({
    url: '/qgenerator',  // Flask 서버 경로
    method: 'POST',
    success: function(recommend) {
      makeQButton(recommend);  // 추천 질문을 버튼으로 만들기
      scrollToBottom();
    },
    error: function() {
      console.error('Error while fetching bot response.');
    }
  });
}

// 추천 버튼을 생성하는 함수
function makeQButton(recommend) {
  var chatbox = document.getElementById('chatbox');

  // 버튼을 감싸는 div 요소 생성
  var buttonContainer = document.createElement("div");
  buttonContainer.className = "text-center"; // 가운데 정렬 스타일 클래스 추가

  recommend.forEach(function(item) {
    var recommendButton = document.createElement("button");
    recommendButton.innerHTML = item;
    recommendButton.className = "btn btn-secondary mr-2 mb-2 border-solid";
    recommendButton.onclick = function() {
      sendQMessage(item); // 해당 추천 질문을 사용자 메시지로 전송
    };

    buttonContainer.appendChild(recommendButton);
  });

  chatbox.appendChild(buttonContainer); // 감싸는 div 요소를 채팅 박스에 추가

  const hrElement = document.createElement('hr'); // 선 긋기
  chatbox.appendChild(hrElement);
}

// 질문 버튼을 누르면 질문을 userMessage 취급해 통신하도록
function sendQMessage(recommendQuestion) {
  appendMessage(recommendQuestion, 'user');
  scrollToBottom();

  getBotResponse(recommendQuestion);

  userInput.value = '';
}
